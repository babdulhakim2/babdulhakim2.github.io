---
layout: default
permalink: /final_project/
title: MSc Computing Project October 2025 A
---

# MSc Computing Project October 2025 A

This page presents the final dissertation artefacts for **Encoder-Based Policy Guardrails for Autonomous Web Agents**, including the dissertation, defense deck, benchmark-grounded PCM pipeline, trained model, and focused SuiteCRM pilot.

<div class="welcome-banner">
  <h2>Project Overview</h2>
  <p>
    The project investigates whether a lightweight encoder can act as a practical
    policy-compliance guardrail for autonomous web agents. The final artefact is
    a DeBERTa-v3-based Policy Compliance Module (PCM) trained on a benchmark-grounded
    synthetic corpus derived from ST-WebAgentBench and evaluated both offline and
    in a small live SuiteCRM pilot.
  </p>
</div>

## Key Artefacts

<div class="module-grid">
  <div class="module-card has-content">
    <h2><a href="./Encoder_Based_Policy_Guardrails_for_Web_Agents.pdf">Dissertation PDF</a></h2>
    <p>The final submitted dissertation, including methodology, results, figures, limitations, and future work.</p>
  </div>

  <div class="module-card has-content">
    <h2><a href="./PCM_Dissertation_Defense.pptx">Defense Deck</a></h2>
    <p>The presentation used to communicate the research problem, artefact design, empirical evidence, and live pilot findings.</p>
  </div>

  <div class="module-card has-content">
    <h2><a href="./README.md">Project README</a></h2>
    <p>A practical guide to the final repository contents, reproduction steps, benchmark-grounded dataset, and retained comparison artefacts.</p>
  </div>

  <div class="module-card has-content">
    <h2><a href="https://huggingface.co/superfunguy/pcm-benchmark-grounded-deberta">Hugging Face Model</a></h2>
    <p>The final benchmark-grounded PCM checkpoint released as a reusable text-classification artefact.</p>
  </div>

  <div class="module-card has-content">
    <h2><a href="https://github.com/babdulhakim2/babdulhakim2.github.io/tree/main/final_project">GitHub Repository</a></h2>
    <p>The full repository subtree for the dissertation artefacts, scripts, dataset, notebook, and evaluation harness.</p>
  </div>

  <div class="module-card has-content">
    <h2><a href="./pcm_benchmark_grounded.ipynb">Training Notebook</a></h2>
    <p>The notebook used to train and evaluate the benchmark-grounded PCM on cloud GPU infrastructure.</p>
  </div>
</div>

## Final Results

| Evaluation | Precision | Recall | F1 | FPR | ROC-AUC |
|:--|--:|--:|--:|--:|--:|
| Standard test | 0.9972 | 1.0000 | 0.9986 | 0.0028 | 1.0000 |
| Challenge split | 1.0000 | 0.8424 | 0.9145 | 0.0000 | 0.9792 |

Focused live SuiteCRM pilot:

- Baseline agent completed the task with `8` observed violations.
- PCM reduced observed violations to `6`, but introduced a live false positive on `click Create Account (link)`.

## What Can Be Browsed Here

- [Dissertation source (LaTeX)](./final_dissertation.tex)
- [Offline evaluation script](./evaluate_pcm.py)
- [Training script](./train_pcm.py)
- [Dataset builder](./build_benchmark_grounded_pcm_dataset.py)
- [Policy-compliant wrapper](./policy_compliant_agent.py)
- [Live SuiteCRM evaluation harness](./run_stwebagentbench_eval.py)
- [Benchmark-grounded dataset manifest](./data/benchmark_grounded/manifest.json)
- [Focused SuiteCRM pilot summary](./results/cup_eval_suitecrm_pilot_hf_small/cup_summary.json)

## Research Contribution

The main contribution is a benchmark-grounded, encoder-based compliance layer that
can be placed in front of a BrowserGym-compatible web agent without modifying the
base agent itself. The results show strong challenge-split precision and zero
challenge false positives, while the live pilot highlights the remaining calibration
problem that must be solved before broader deployment.

## Notes

- The final dissertation checkpoint is stored locally in `models/pcm_benchmark_grounded_hf/`.
- The repository also retains older model and evaluation folders for comparison.
- `ST-WebAgentBench/` is included locally because it is used both for dataset grounding and the SuiteCRM pilot environment.

<div class="back-to-home">
  <a href="{{ '/' | relative_url }}" class="back-link">← Back to Home</a>
</div>
