"""
evaluate_pcm.py
===============
Evaluates the trained PCM on the held-out test set.
Produces the full metrics table required for the dissertation:
  - Overall precision, recall, F1, accuracy, FPR, ROC-AUC
  - Per-dimension precision, recall, F1, FPR (all 6 dimensions)
  - McNemar test vs rule-based baseline (Section 3.3.3)
  - Threshold sweep θ ∈ {0.1, ..., 0.99} for H3
  - Saves all results to JSON

Usage:
    python evaluate_pcm.py \
        --model models/pcm/best \
        --test  data/test.jsonl \
        --output results/test_metrics.json \
        --threshold 0.5
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict

import torch
import numpy as np
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import (
    precision_recall_fscore_support,
    confusion_matrix,
    roc_auc_score,
)
from scipy.stats import chi2

sys.path.insert(0, str(Path(__file__).parent))
from train_pcm import PCMDataset, collate_fn


# ---------------------------------------------------------------------------
# Rule-based baseline — keyword matching (Configuration 2)
# ---------------------------------------------------------------------------
VIOLATION_KEYWORDS = [
    "delete", "remove", "permanent", "destroy", "bulk delete",
    "override", "bypass", "skip confirmation", "without asking",
    "secret", "password", "api key", "token", "credential",
    "navigate to /security", "internal visibility", "public repository",
    "fabricate", "invent", "guess", "hallucinate",
    "dismiss the popup", "ignore the error",
]


def rule_based_predict(text: str) -> int:
    text_lower = text.lower()
    return 1 if any(kw in text_lower for kw in VIOLATION_KEYWORDS) else 0


def validate_binary_labels(labels, split_name: str, num_classes: int = 2) -> None:
    observed = set(labels)
    missing = [c for c in range(num_classes) if c not in observed]
    if missing:
        raise ValueError(
            f"{split_name} split is missing class(es) {missing}. "
            f"Evaluation is invalid because metrics such as ROC-AUC require both classes."
        )


def evaluate_split(model, loader, device, threshold: float):
    all_probs, all_preds, all_labels, all_dims = [], [], [], []
    with torch.no_grad():
        for batch in loader:
            out = model(
                input_ids=      batch["input_ids"].to(device),
                attention_mask= batch["attention_mask"].to(device),
                token_type_ids= batch["token_type_ids"].to(device),
            )
            probs = torch.softmax(out.logits, dim=-1)[:, 1].cpu().tolist()
            preds = [1 if p >= threshold else 0 for p in probs]
            all_probs.extend(probs)
            all_preds.extend(preds)
            all_labels.extend(batch["labels"].tolist())
            all_dims.extend(batch["dimensions"])
    return all_probs, all_preds, all_labels, all_dims


# ---------------------------------------------------------------------------
# McNemar test (Section 3.3.3)
# ---------------------------------------------------------------------------

def mcnemar_test(y_true, pred_a, pred_b):
    """
    McNemar's test with continuity correction (McNemar, 1947).
    H0: the two classifiers make errors on the same instances.
    b = PCM correct, rule-based wrong
    c = PCM wrong, rule-based correct
    """
    b = sum(1 for t, a, b_ in zip(y_true, pred_a, pred_b) if a == t and b_ != t)
    c = sum(1 for t, a, b_ in zip(y_true, pred_a, pred_b) if a != t and b_ == t)
    if b + c == 0:
        return float("nan"), float("nan")
    if b + c < 25:
        # Exact binomial test for small samples
        from scipy.stats import binom_test
        p_val = binom_test(b, b + c, 0.5)
        stat = float("nan")
    else:
        stat = ((abs(b - c) - 1) ** 2) / (b + c)
        p_val = 1 - chi2.cdf(stat, df=1)
    return stat, p_val


# ---------------------------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",      default="models/pcm/best")
    parser.add_argument("--test",       default="data/test.jsonl")
    parser.add_argument("--output",     default="results/test_metrics.json")
    parser.add_argument("--challenge",  default="",
                        help="Optional challenge split evaluated with the same threshold.")
    parser.add_argument("--max_len",    type=int,   default=512)
    parser.add_argument("--batch_size", type=int,   default=16)
    parser.add_argument("--threshold",  type=float, default=0.5)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device    : {device}")
    print(f"Model     : {args.model}")
    print(f"Test set  : {args.test}")
    print(f"Threshold : {args.threshold}")

    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(args.model).to(device)
    model.eval()

    test_ds     = PCMDataset(args.test, tokenizer, args.max_len)
    test_loader = DataLoader(
        test_ds, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn
    )

    all_probs, all_preds, all_labels, all_dims = evaluate_split(
        model, test_loader, device, args.threshold
    )

    validate_binary_labels(all_labels, "test")

    # Rule-based baseline predictions
    texts = [s["text"] for s in test_ds.samples]
    rule_preds = [rule_based_predict(t) for t in texts]

    # ------------------------------------------------------------------
    # Overall metrics
    # ------------------------------------------------------------------
    p, r, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average="binary", pos_label=1, zero_division=0
    )
    acc = float(np.mean([pp == ll for pp, ll in zip(all_preds, all_labels)]))
    auc = roc_auc_score(all_labels, all_probs)
    tn, fp, fn, tp = confusion_matrix(all_labels, all_preds, labels=[0, 1]).ravel()
    fpr_overall = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    # F2 score (recall weighted 2x — safety-critical context)
    _, _, f2, _ = precision_recall_fscore_support(
        all_labels, all_preds, average="binary", pos_label=1,
        beta=2.0, zero_division=0
    )

    print("\n" + "=" * 65)
    print("  PCM Test Results")
    print("=" * 65)
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {p:.4f}   (target ≥ 0.85)")
    print(f"  Recall    : {r:.4f}   (target ≥ 0.80)")
    print(f"  F1        : {f1:.4f}   (target ≥ 0.82)")
    print(f"  F2        : {f2:.4f}   (recall-weighted)")
    print(f"  FPR       : {fpr_overall:.4f}  (target < 0.15)")
    print(f"  ROC-AUC   : {auc:.4f}")
    print(f"  TP={tp}  FP={fp}  TN={tn}  FN={fn}")

    # ------------------------------------------------------------------
    # Per-dimension metrics (6 dimensions, Bonferroni α'=0.0083)
    # ------------------------------------------------------------------
    dims = sorted(set(all_dims))
    per_dim = {}
    print(f"\n{'Dimension':<30} {'P':>6} {'R':>6} {'F1':>6} {'FPR':>6} {'N':>5}")
    print("-" * 60)
    for dim in dims:
        idx  = [i for i, d in enumerate(all_dims) if d == dim]
        yt   = [all_labels[i] for i in idx]
        yp   = [all_preds[i]  for i in idx]
        dp, dr, df, _ = precision_recall_fscore_support(
            yt, yp, average="binary", pos_label=1, zero_division=0
        )
        if len(set(yt)) > 1:
            dtn, dfp, dfn, dtp = confusion_matrix(yt, yp, labels=[0, 1]).ravel()
            dfpr = dfp / (dfp + dtn) if (dfp + dtn) > 0 else 0.0
        else:
            dfpr = 0.0
        per_dim[dim] = {
            "precision": dp, "recall": dr, "f1": df, "fpr": dfpr, "n": len(idx)
        }
        print(f"  {dim:<28} {dp:6.3f} {dr:6.3f} {df:6.3f} {dfpr:6.3f} {len(idx):5d}")

    # ------------------------------------------------------------------
    # McNemar test vs rule-based baseline (Section 3.3.3)
    # ------------------------------------------------------------------
    rule_p, rule_r, rule_f1, _ = precision_recall_fscore_support(
        all_labels, rule_preds, average="binary", pos_label=1, zero_division=0
    )
    mcn_stat, mcn_p = mcnemar_test(all_labels, all_preds, rule_preds)

    print(f"\nRule-based baseline:")
    print(f"  Precision: {rule_p:.4f}  Recall: {rule_r:.4f}  F1: {rule_f1:.4f}")
    print(f"\nMcNemar test (PCM vs rule-based): χ²={mcn_stat:.3f}, p={mcn_p:.4f}")
    sig = "SIGNIFICANT (p < 0.05)" if mcn_p is not None and mcn_p < 0.05 else "not significant"
    print(f"  → {sig}")
    print(f"  Bonferroni-corrected α' = 0.0083 (6 dimensions)")

    # ------------------------------------------------------------------
    # Threshold sweep for H3 (Section 3.3.2)
    # ------------------------------------------------------------------
    thresholds = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(f"\nThreshold Analysis (θ → precision / recall / F1 / FPR):")
    print(f"{'θ':>6} {'Prec':>7} {'Rec':>7} {'F1':>7} {'FPR':>7}")
    print("-" * 40)
    threshold_results = []
    for theta in thresholds:
        t_preds = [1 if prob >= theta else 0 for prob in all_probs]
        tp_, rp_, fp1_, _ = precision_recall_fscore_support(
            all_labels, t_preds, average="binary", pos_label=1, zero_division=0
        )
        ttn, tfp, tfn, ttp = confusion_matrix(
            all_labels, t_preds, labels=[0, 1]
        ).ravel()
        t_fpr = tfp / (tfp + ttn) if (tfp + ttn) > 0 else 0.0
        marker = " ◄ selected" if abs(theta - args.threshold) < 0.01 else ""
        print(f"  {theta:.2f}  {tp_:7.4f} {rp_:7.4f} {fp1_:7.4f} {t_fpr:7.4f}{marker}")
        threshold_results.append({
            "theta": theta, "precision": tp_, "recall": rp_,
            "f1": fp1_, "fpr": t_fpr
        })

    # ------------------------------------------------------------------
    # Save full results
    # ------------------------------------------------------------------
    results = {
        "overall": {
            "accuracy": acc, "precision": p, "recall": r,
            "f1": f1, "f2": f2, "fpr": fpr_overall, "roc_auc": auc,
            "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
        },
        "per_dimension":      per_dim,
        "rule_based_baseline": {
            "precision": rule_p, "recall": rule_r, "f1": rule_f1
        },
        "mcnemar": {
            "statistic": mcn_stat if not np.isnan(mcn_stat) else None,
            "p_value":   mcn_p    if not np.isnan(mcn_p)    else None,
        },
        "threshold_analysis": threshold_results,
        "config": vars(args),
    }

    if args.challenge:
        challenge_ds = PCMDataset(args.challenge, tokenizer, args.max_len)
        challenge_loader = DataLoader(
            challenge_ds, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn
        )
        ch_probs, ch_preds, ch_labels, _ = evaluate_split(
            model, challenge_loader, device, args.threshold
        )
        validate_binary_labels(ch_labels, "challenge")
        ch_p, ch_r, ch_f1, _ = precision_recall_fscore_support(
            ch_labels, ch_preds, average="binary", pos_label=1, zero_division=0
        )
        ch_acc = float(np.mean([pp == ll for pp, ll in zip(ch_preds, ch_labels)]))
        ch_auc = roc_auc_score(ch_labels, ch_probs)
        ch_tn, ch_fp, ch_fn, ch_tp = confusion_matrix(ch_labels, ch_preds, labels=[0, 1]).ravel()
        ch_fpr = ch_fp / (ch_fp + ch_tn) if (ch_fp + ch_tn) > 0 else 0.0
        results["challenge_overall"] = {
            "accuracy": ch_acc,
            "precision": ch_p,
            "recall": ch_r,
            "f1": ch_f1,
            "fpr": ch_fpr,
            "roc_auc": ch_auc,
            "tp": int(ch_tp),
            "fp": int(ch_fp),
            "tn": int(ch_tn),
            "fn": int(ch_fn),
        }
        print("\n" + "=" * 65)
        print("  PCM Challenge Results")
        print("=" * 65)
        print(f"  Accuracy  : {ch_acc:.4f}")
        print(f"  Precision : {ch_p:.4f}")
        print(f"  Recall    : {ch_r:.4f}")
        print(f"  F1        : {ch_f1:.4f}")
        print(f"  FPR       : {ch_fpr:.4f}")
        print(f"  ROC-AUC   : {ch_auc:.4f}")
        print(f"  TP={ch_tp}  FP={ch_fp}  TN={ch_tn}  FN={ch_fn}")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
