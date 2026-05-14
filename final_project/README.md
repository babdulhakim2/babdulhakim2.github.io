# PCM Final Project

Final project artefacts for the dissertation **Encoder-Based Policy Guardrails for Autonomous Web Agents**.

This repository contains the final benchmark-grounded PCM pipeline, the dissertation source, the defense deck, and the supporting scripts used to build, train, evaluate, and pilot the policy-compliance module.

## Final Artefacts

### Dissertation

- `final_dissertation.tex` — final LaTeX source
- `final_dissertation.pdf` — compiled dissertation
- `PCM_Dissertation_Defense.pptx` — final defense presentation

### Core PCM pipeline

- `build_benchmark_grounded_pcm_dataset.py` — builds the benchmark-grounded synthetic corpus from the local ST-WebAgentBench catalogue
- `train_pcm.py` — fine-tunes the DeBERTa-v3 PCM classifier
- `evaluate_pcm.py` — evaluates the PCM on held-out test and challenge splits
- `policy_compliant_agent.py` — BrowserGym wrapper and PCM inference logic
- `run_stwebagentbench_eval.py` — focused live evaluation harness for SuiteCRM / ST-WebAgentBench
- `pcm_benchmark_grounded.ipynb` — notebook used for cloud training and evaluation

### Data and models

- `data/benchmark_grounded/` — benchmark-grounded dataset
  - `train.jsonl`
  - `val.jsonl`
  - `test.jsonl`
  - `challenge.jsonl`
  - `sanity_probes.jsonl`
  - `manifest.json`
- `models/pcm_benchmark_grounded_hf/` — final benchmark-grounded checkpoint mirrored from Hugging Face

### Benchmark dependency

- `ST-WebAgentBench/` — local benchmark subtree used for dataset grounding and SuiteCRM evaluation

## Final Headline Results

Offline benchmark-grounded evaluation:

- Standard test: `Precision 0.9972`, `Recall 1.0000`, `F1 0.9986`, `FPR 0.0028`, `ROC-AUC 1.0000`
- Challenge split: `Precision 1.0000`, `Recall 0.8424`, `F1 0.9145`, `FPR 0.0000`, `ROC-AUC 0.9792`

Focused live SuiteCRM pilot:

- Baseline: task completed with `8` observed violations
- PCM: task did not complete and reduced observed violations to `6`, but exposed a live false positive on `click Create Account (link)`

## External Artefacts

- GitHub repository: [babdulhakim2/final_project](https://github.com/babdulhakim2/babdulhakim2.github.io/tree/main/final_project)
- Hugging Face model: [superfunguy/pcm-benchmark-grounded-deberta](https://huggingface.co/superfunguy/pcm-benchmark-grounded-deberta)

## Reproducing the Final Pipeline

### 1. Install the base Python dependencies

```bash
pip install -r requirements.txt
pip install "transformers==4.51.1" sentencepiece protobuf
```

### 2. Build the benchmark-grounded dataset

```bash
python build_benchmark_grounded_pcm_dataset.py \
  --catalog ST-WebAgentBench/stwebagentbench/test.raw.json \
  --output_dir data/benchmark_grounded \
  --seed 42
```

### 3. Train the PCM

```bash
python train_pcm.py \
  --train data/benchmark_grounded/train.jsonl \
  --val data/benchmark_grounded/val.jsonl \
  --output_dir models/pcm_benchmark_grounded \
  --model_name microsoft/deberta-v3-base \
  --epochs 5 \
  --batch_size 16 \
  --max_len 512 \
  --patience 2
```

### 4. Evaluate offline

```bash
python evaluate_pcm.py \
  --model models/pcm_benchmark_grounded/best \
  --test data/benchmark_grounded/test.jsonl \
  --challenge data/benchmark_grounded/challenge.jsonl \
  --output results/benchmark_grounded_test_metrics.json \
  --threshold 0.5
```

### 5. Run the focused SuiteCRM pilot

Install the browser stack first:

```bash
pip install "browsergym[stwebagentbench]" playwright openai
playwright install chromium
```

Set the required environment variables and run:

```bash
export SUITECRM_URL=http://localhost:8080
export OPENAI_API_KEY=YOUR_KEY_HERE

python run_stwebagentbench_eval.py \
  --site suitecrm \
  --pcm_model models/pcm_benchmark_grounded_hf \
  --base_agent gpt-5-mini \
  --output_dir results/cup_eval_suitecrm_pilot_hf_small \
  --max_tasks 1 \
  --max_steps 6 \
  --configs baseline pcm
```

## Repository Notes

- `models/pcm_hf/`, `models/pcm/`, and `models/pcm_v2/` are retained as older or comparison checkpoints. The final dissertation checkpoint is `models/pcm_benchmark_grounded_hf/`.
- `results/` contains multiple smoke-test and pilot runs collected during development. The final small live pilot discussed in the dissertation is `results/cup_eval_suitecrm_pilot_hf_small/`.
- `final_dissertation.aux`, `final_dissertation.log`, `final_dissertation.out`, and `final_dissertation.toc` are LaTeX build artefacts.
- `pptx_inspect_tmp/`, `pptx_edit_tmp/`, and `pptx_update_tmp/` are local slide-edit scratch workspaces and are not required to understand or rerun the PCM pipeline.

## Suggested Minimal Layout

```text
final_project/
├── final_dissertation.tex
├── final_dissertation.pdf
├── PCM_Dissertation_Defense.pptx
├── pcm_benchmark_grounded.ipynb
├── build_benchmark_grounded_pcm_dataset.py
├── train_pcm.py
├── evaluate_pcm.py
├── policy_compliant_agent.py
├── run_stwebagentbench_eval.py
├── data/
│   └── benchmark_grounded/
├── models/
│   └── pcm_benchmark_grounded_hf/
├── results/
│   └── cup_eval_suitecrm_pilot_hf_small/
└── ST-WebAgentBench/
```
