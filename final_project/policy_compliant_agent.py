"""
policy_compliant_agent.py
=========================
PolicyCompliantAgent — a modular BrowserGym-compatible wrapper that intercepts
proposed actions, classifies them against active enterprise policies using the
trained PCM, and blocks violations before browser execution.

FIX 4 — Action naturalisation (Section 4.1.2):
    _naturalise_action() implements the three-stage procedure described in the
    dissertation:
        Stage 1: map BrowserGym function names to natural-language verbs
        Stage 2: resolve bid arguments against the AXTree to retrieve element
                 labels, roles, and accessible names
        Stage 3: concatenate verb + resolved element label into a readable
                 action description

    Previously this method just called str() on the action — this caused
    out-of-distribution inputs to the classifier trained on natural-language
    synthetic data.

Per-action audit log satisfies EU AI Act Article 12 (logging) and
Article 13 (interpretable per-action indicators).
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# ---------------------------------------------------------------------------
# Stage 1 — verb mapping table
# Maps BrowserGym function names to natural-language verb phrases.
# ---------------------------------------------------------------------------
VERB_MAP = {
    "click":           "click",
    "press":           "press",
    "fill":            "type into",
    "type":            "type into",
    "goto":            "navigate to",
    "navigate":        "navigate to",
    "select_option":   "select from",
    "select":          "select from",
    "check":           "check",
    "uncheck":         "uncheck",
    "hover":           "hover over",
    "focus":           "focus on",
    "scroll":          "scroll",
    "drag":            "drag",
    "drop":            "drop onto",
    "upload":          "upload file to",
    "download":        "download from",
    "send_msg_to_user":"send message to user",
    "report_infeasible":"report task as infeasible",
}

GENERIC_POLICY_DESCRIPTIONS = {
    "Check if certain content appears on the page and verify action type",
    "Do not navigate or visit a URL pattern",
    "Verify specific content on the page using a locator and ensure it matches required criteria.",
}

DIMENSION_MAP = {
    "boundary_and_scope_limitation": "boundary_and_scope",
}


def _parse_action_call(action: str):
    """
    Parse a BrowserGym action string of the form:
        func_name(arg1, arg2, ...)
    Returns (func_name: str, args: list[str]).
    Returns (action, []) if the string does not match this pattern.
    """
    action = action.strip()
    paren_open = action.find("(")
    if paren_open == -1:
        return action, []
    func_name = action[:paren_open].strip()
    args_str = action[paren_open + 1:].rstrip(")")
    # Split on first comma only — second arg is typically a fill value
    args = [a.strip().strip("'\"") for a in args_str.split(",", 1)]
    return func_name, args


def _split_or_values(value: Optional[str]) -> list[str]:
    if not value or not isinstance(value, str):
        return []
    return [part.strip() for part in value.split("|OR|") if part.strip()]


def _format_terms(terms: list[str]) -> str:
    if not terms:
        return ""
    if len(terms) == 1:
        return f"'{terms[0]}'"
    if len(terms) == 2:
        return f"'{terms[0]}' or '{terms[1]}'"
    return ", ".join(f"'{term}'" for term in terms[:-1]) + f", or '{terms[-1]}'"


def _normalise_policy_text(policy_obj: Dict) -> Optional[str]:
    """
    Convert ST-WebAgentBench policy metadata into concrete natural-language
    guardrails. Returns None for evaluator-only scaffolding that lacks enough
    information to form a meaningful policy text.
    """
    description = (policy_obj.get("description") or "").strip()
    template = (
        policy_obj.get("policy_template")
        or policy_obj.get("policy_template_id")
        or ""
    ).strip()
    eval_meta = policy_obj.get("eval") if isinstance(policy_obj.get("eval"), dict) else {}

    if template == "irreversible_actions":
        terms = _split_or_values(eval_meta.get("must_include"))
        action = eval_meta.get("must_include_action")
        if action == "click" and terms:
            return (
                f"Do not click elements containing {_format_terms(terms)} "
                "unless explicitly authorised."
            )
        return "Do not perform irreversible or destructive actions unless explicitly authorised."

    if template == "navigation_limitation":
        if description and description not in GENERIC_POLICY_DESCRIPTIONS:
            return description
        terms = _split_or_values(eval_meta.get("reference_url"))
        if terms:
            return f"Do not navigate to URLs or modules matching {_format_terms(terms)}."
        return None

    if template == "ask_the_user":
        must_include = eval_meta.get("must_include")
        if must_include:
            return (
                f"Ask the user for permission before performing this action, "
                f"especially before interacting with '{must_include}'."
            )
        return description or "Ask the user for permission before performing this action."

    if template in {"policy_contradiction", "jailbreaking", "sensitive_information"}:
        return description or None

    if description and description not in GENERIC_POLICY_DESCRIPTIONS:
        return description

    return None


def _resolve_bid(bid: str, axtree: Optional[Dict]) -> Optional[Dict]:
    """
    Stage 2: resolve a bid (browser element identifier) against the AXTree
    observation to retrieve the element's accessible name, role, and label.

    The AXTree is expected as a dict mapping bid strings to element objects
    with fields: name, role, label (all optional).

    Returns a dict with keys 'name', 'role', 'label', or None if resolution
    fails (element not found or AXTree unavailable).
    """
    if axtree is None or not isinstance(axtree, dict):
        return None

    # BrowserGym observations expose the accessibility tree as
    # {"nodes": [...]} with bids stored in each node's "browsergym_id".
    nodes = axtree.get("nodes")
    if isinstance(nodes, list):
        bid = str(bid)
        for node in nodes:
            if str(node.get("browsergym_id", "")) != bid:
                continue
            name = ""
            if isinstance(node.get("name"), dict):
                name = node["name"].get("value", "") or ""
            role = ""
            if isinstance(node.get("role"), dict):
                role = node["role"].get("value", "") or ""
            return {
                "name": name,
                "role": role,
                "label": name,
            }
        return None

    # Backward-compatible fallback for dict-like bid maps.
    element = axtree.get(bid)
    if element is None:
        return None
    return {
        "name":  element.get("name", ""),
        "role":  element.get("role", ""),
        "label": element.get("label", element.get("name", "")),
    }


def _naturalise_action(action: str, axtree: Optional[Dict] = None) -> tuple:
    """
    Three-stage action naturalisation (Section 4.1.2).

    Stage 1 — extract function name and map to verb.
    Stage 2 — resolve bid argument against AXTree.
    Stage 3 — concatenate verb + element label to produce readable description.

    Special cases:
    - send_msg_to_user: message content is already natural language; pass through.
    - report_infeasible: pass through.
    - goto/navigate: URL is meaningful directly.
    - fill: include fill value in description.

    Returns (naturalised_text: str, resolution_failed: bool).
    resolution_failed=True is logged in the audit entry for transparency.
    """
    func_name, args = _parse_action_call(action)

    # Pass-through actions — content is already natural language
    if func_name in ("send_msg_to_user", "report_infeasible"):
        content = args[0] if args else action
        verb = VERB_MAP.get(func_name, func_name)
        return f"{verb}: '{content}'", False

    # Navigate actions — URL is the meaningful element
    if func_name in ("goto", "navigate"):
        url = args[0] if args else ""
        return f"navigate to {url}", False

    # Stage 1: map function to verb
    verb = VERB_MAP.get(func_name, func_name)

    if not args:
        return f"{verb}", False

    bid = args[0]
    fill_value = args[1] if len(args) > 1 else None

    # Stage 2: resolve bid against AXTree
    resolution_failed = False
    element = _resolve_bid(bid, axtree)

    if element and element.get("label"):
        # Stage 3: verb + element label
        element_desc = element["label"]
        if element.get("role") and element["role"] not in ("generic", "none", ""):
            element_desc = f"{element['label']} ({element['role']})"
    elif element and element.get("name"):
        element_desc = element["name"]
    else:
        # Fallback: use raw bid — flag resolution failure for audit log
        element_desc = bid
        resolution_failed = True

    if fill_value:
        return f"{verb} {element_desc} with '{fill_value}'", resolution_failed
    else:
        return f"{verb} {element_desc}", resolution_failed


# ---------------------------------------------------------------------------
# PCM Classifier
# ---------------------------------------------------------------------------

class PCMClassifier:
    """Wraps the fine-tuned DeBERTa-v3-base checkpoint for inference."""

    def __init__(self, model_path: str, device: str = "auto", max_len: int = 512):
        self.max_len = max_len
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        print(f"[PCM] Loading model from {model_path} on {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, num_labels=2
        ).to(self.device)
        self.model.eval()

    def predict(self, policy: str, context: str, action: str) -> float:
        """
        Returns P(violation) for a single [POLICY]+[CONTEXT]+[ACTION] triple.
        Uses priority-preserving truncation (Section 4.1.3):
            policy + action retained in full; context truncated from the end.
        """
        text = f"[POLICY] {policy} [SEP] [CONTEXT] {context} [SEP] [ACTION] {action}"
        enc = self.tokenizer(
            text,
            max_length=self.max_len,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        with torch.no_grad():
            logits = self.model(
                input_ids=      enc["input_ids"].to(self.device),
                attention_mask= enc["attention_mask"].to(self.device),
            ).logits
        probs = torch.softmax(logits, dim=-1)
        return probs[0, 1].item()  # P(violation)


# ---------------------------------------------------------------------------
# Policy extraction helpers
# ---------------------------------------------------------------------------

def _extract_policies(obs: Dict) -> List[Dict]:
    """
    Extract active policy objects from the BrowserGym observation.
    The custom_env.py stores policies under the ``policies`` key.
    Falls back to ``POLICY_CONTEXT`` / ``policy_context`` for compatibility.
    Each policy object has fields: description, policy_category, source.
    Returns [] if no policies are present.
    """
    return obs.get("policies", obs.get("POLICY_CONTEXT", obs.get("policy_context", [])))


def _extract_context(obs: Dict) -> str:
    """
    Build a compact page context string from the BrowserGym observation.
    Extracts: application name, URL, page type, and key AXTree elements.
    """
    parts = []
    if "app" in obs:
        parts.append(f"app: {obs['app']}")
    if "url" in obs:
        url = obs["url"]
        # Keep only path component to save tokens
        from urllib.parse import urlparse
        parts.append(f"url: {urlparse(url).path}")
    if "page_type" in obs:
        parts.append(f"page: {obs['page_type']}")
    if "focused_element" in obs:
        parts.append(f"focused: {obs['focused_element']}")
    if not parts:
        parts.append("page: enterprise_app")
    return "; ".join(parts)


# ---------------------------------------------------------------------------
# PolicyCompliantAgent
# ---------------------------------------------------------------------------

class PolicyCompliantAgent:
    """
    Modular BrowserGym-compatible wrapper implementing pre-execution PCM
    compliance gating. Requires no modification to the base agent.

    Args:
        base_agent:         Any BrowserGym-compatible agent with an act(obs) method.
        pcm:                Loaded PCMClassifier instance.
        theta:              Violation probability threshold (default 0.5).
        replan_on_block:    If True, attempt one re-plan on blocked actions (Config 4).
        audit_log_path:     Path for JSONL audit log (EU AI Act Article 12).
    """

    PRIORITY_ORDER = {"org": 0, "user": 1, "task": 2}

    def __init__(
        self,
        base_agent,
        pcm: PCMClassifier,
        theta: float = 0.5,
        replan_on_block: bool = False,
        audit_log_path: str = "audit_log.jsonl",
    ):
        self.base_agent      = base_agent
        self.pcm             = pcm
        self.theta           = theta
        self.replan_on_block = replan_on_block
        self.audit_log_path  = Path(audit_log_path)
        self._step           = 0
        self._task_id        = "unknown"

    def set_task(self, task_id: str):
        self._task_id = task_id
        self._step    = 0

    def reset(self, task_id: str = "unknown"):
        self.set_task(task_id)
        if hasattr(self.base_agent, "reset"):
            self.base_agent.reset(task_id=task_id)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def act(self, obs: Dict) -> Any:
        """
        Six-step PCM execution (Section 4.3.1):
        1. Extract active policies from POLICY_CONTEXT.
        2. Extract page context from observation.
        3. Call base agent to obtain proposed action.
        4. Naturalise action text (FIX 4).
        5. Run PCM classification for each active policy.
        6. Permit, block, or re-plan.
        """
        self._step += 1
        policies = _extract_policies(obs)
        context  = _extract_context(obs)
        axtree   = obs.get("axtree_object", obs.get("axtree", None))

        # Step 3: get proposed action from base agent
        proposed_action = self.base_agent.act(obs)

        # Step 4: naturalise action (FIX 4)
        nat_text, resolution_failed = _naturalise_action(
            str(proposed_action), axtree
        )

        # Step 5 & 6: classify against each active policy
        if not policies:
            self._log(obs, nat_text, policy=None, dimension=None,
                      violation_prob=0.0, decision="PERMIT",
                      resolution_failed=resolution_failed)
            return proposed_action

        # Sort by priority: org > user > task (Section 4.3.2)
        # Actual field is "source"; normalize "organization" -> "org"
        def _get_priority(p):
            raw = p.get("source", p.get("priority", "task"))
            if raw == "organization":
                raw = "org"
            return self.PRIORITY_ORDER.get(raw, 2)

        policies_sorted = sorted(policies, key=_get_priority)

        max_prob      = 0.0
        blocking_policy = None
        for policy_obj in policies_sorted:
            policy_text = _normalise_policy_text(policy_obj)
            if not policy_text:
                continue

            raw_dimension = policy_obj.get("policy_category", policy_obj.get("dimension", "unknown"))
            dimension   = DIMENSION_MAP.get(raw_dimension, raw_dimension)
            raw_priority = policy_obj.get("source", policy_obj.get("priority", "task"))
            priority    = "org" if raw_priority == "organization" else raw_priority

            t0   = time.perf_counter()
            prob = self.pcm.predict(policy_text, context, nat_text)
            latency_ms = (time.perf_counter() - t0) * 1000

            self._log(obs, nat_text,
                      policy=policy_text, dimension=dimension,
                      violation_prob=prob,
                      decision="BLOCK" if prob >= self.theta else "PERMIT",
                      latency_ms=latency_ms,
                      resolution_failed=resolution_failed)

            if prob > max_prob:
                max_prob = prob

            # Org-level violation: immediate block regardless of other policies
            if prob >= self.theta:
                blocking_policy = policy_obj
                if priority == "org":
                    break

        if max_prob < self.theta:
            return proposed_action

        # Action blocked
        return self._handle_block(obs, blocking_policy, nat_text, resolution_failed)

    # ------------------------------------------------------------------
    # Blocking and re-planning (Section 4.3.3)
    # ------------------------------------------------------------------

    def _handle_block(self, obs, blocking_policy, nat_text, resolution_failed):
        policy_text = _normalise_policy_text(blocking_policy) or blocking_policy.get(
            "description", blocking_policy.get("policy_template", str(blocking_policy))
        )
        raw_dimension = blocking_policy.get("policy_category", blocking_policy.get("dimension", "unknown"))
        dimension   = DIMENSION_MAP.get(raw_dimension, raw_dimension)

        if not self.replan_on_block:
            return "send_msg_to_user('Action blocked by Policy Compliance Module.')"

        # Config 4: inject structured feedback and re-plan once
        feedback_obs = dict(obs)
        feedback_obs["last_action_error"] = (
            f"Action blocked by Policy Compliance Module "
            f"(P(violation)={self.theta:.2f}). "
            f"The following policy was violated: '{policy_text}'. "
            f"Please propose a compliant alternative."
        )

        revised_action = self.base_agent.act(feedback_obs)
        revised_nat, rev_resolution_failed = _naturalise_action(
            str(revised_action), obs.get("axtree_object", obs.get("axtree"))
        )

        # Re-classify revised action
        context  = _extract_context(obs)
        t0       = time.perf_counter()
        rev_prob = self.pcm.predict(policy_text, context, revised_nat)
        latency_ms = (time.perf_counter() - t0) * 1000

        if rev_prob < self.theta:
            self._log(obs, revised_nat, policy=policy_text, dimension=dimension,
                      violation_prob=rev_prob, decision="PERMIT_AFTER_REPLAN",
                      latency_ms=latency_ms, resolution_failed=rev_resolution_failed)
            return revised_action

        # Revised action also blocked — safe fallback (Section 4.3.3)
        self._log(obs, revised_nat, policy=policy_text, dimension=dimension,
                  violation_prob=rev_prob, decision="DOUBLE_BLOCK",
                  latency_ms=latency_ms, resolution_failed=rev_resolution_failed)

        fallback_msg = (
            f"I cannot complete this action under the active policy: '{policy_text}'. "
            f"Please advise how you would like to proceed."
        )
        # Return a send_msg_to_user action as safe fallback
        return f"send_msg_to_user('{fallback_msg}')"

    # ------------------------------------------------------------------
    # Audit log (EU AI Act Article 12) — Section 4.3.4
    # ------------------------------------------------------------------

    def _log(
        self,
        obs: Dict,
        action: str,
        policy: Optional[str],
        dimension: Optional[str],
        violation_prob: float,
        decision: str,
        latency_ms: float = 0.0,
        resolution_failed: bool = False,
    ):
        entry = {
            "timestamp":          datetime.now(timezone.utc).isoformat(),
            "task_id":            self._task_id,
            "step":               self._step,
            "dimension":          dimension,
            "policy":             policy,
            "context_summary":    _extract_context(obs),
            "action":             action,
            "violation_prob":     round(violation_prob, 4),
            "decision":           decision,
            "threshold":          self.theta,
            "latency_ms":         round(latency_ms, 2),
            "resolution_failed":  resolution_failed,
        }
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
