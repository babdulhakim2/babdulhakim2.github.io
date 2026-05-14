"""
train_pcm.py
============
Fine-tunes DeBERTa-v3-base on synthetic PCM training data.
Binary classifier: label=1 (policy violation) / label=0 (compliant).

FIX 2 — Class weighting (Section 4.2.3):
    Inverse frequency class weights w_c = N / (K * n_c) are applied to the
    cross-entropy loss so the minority class (violations) contributes
    proportionally to the gradient signal.

FIX 5 — AdamW implementation (Section 4.2.2):
    Uses transformers.AdamW (Loshchilov & Hutter 2019 decoupled weight decay)
    rather than torch.optim.AdamW, consistent with the dissertation citation.

Usage (GPU, full run):
    python train_pcm.py --train data/train.jsonl --val data/val.jsonl \\
        --output_dir models/pcm --epochs 5 --batch_size 16 --max_len 512
"""

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm.auto import tqdm
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup,
)
from torch.optim import AdamW  # HF removed AdamW in v4.44+; torch.optim.AdamW
                                # applies decoupled weight decay identically
from sklearn.metrics import (
    precision_recall_fscore_support,
    confusion_matrix,
)


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

class PCMDataset(Dataset):
    def __init__(self, path: str, tokenizer, max_len: int = 512):
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.samples = []
        with open(path) as f:
            for line in f:
                self.samples.append(json.loads(line.strip()))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        enc = self.tokenizer(
            item["text"],
            max_length=self.max_len,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        return {
            "input_ids":      enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "token_type_ids": enc.get(
                "token_type_ids",
                torch.zeros(self.max_len, dtype=torch.long)
            ).squeeze(0),
            "labels":    torch.tensor(item["label"], dtype=torch.long),
            "dimension": item["dimension"],
        }


def collate_fn(batch):
    return {
        "input_ids":      torch.stack([b["input_ids"]      for b in batch]),
        "attention_mask": torch.stack([b["attention_mask"] for b in batch]),
        "token_type_ids": torch.stack([b["token_type_ids"] for b in batch]),
        "labels":         torch.stack([b["labels"]         for b in batch]),
        "dimensions":     [b["dimension"] for b in batch],
    }


def validate_binary_labels(labels, split_name: str, num_classes: int = 2) -> Counter:
    counts = Counter(labels)
    missing = [c for c in range(num_classes) if counts.get(c, 0) == 0]
    if missing:
        raise ValueError(
            f"{split_name} split is missing class(es) {missing}. "
            f"Label counts: {dict(sorted(counts.items()))}. "
            "Regenerate the dataset before training."
        )
    return counts


# ---------------------------------------------------------------------------
# Class weight computation — FIX 2
# ---------------------------------------------------------------------------

def compute_class_weights(dataset: PCMDataset, num_classes: int = 2) -> torch.Tensor:
    """
    Inverse frequency weighting: w_c = N / (K * n_c)
    where N = total samples, K = num_classes, n_c = count of class c.
    Consistent with Section 4.2.3 of the dissertation.
    """
    labels = [item["label"] for item in dataset.samples]
    counts = validate_binary_labels(labels, "train", num_classes=num_classes)
    N = len(labels)
    weights = []
    for c in range(num_classes):
        n_c = counts[c]
        weights.append(N / (num_classes * n_c))
    print(f"\nClass weights (N={N}): " +
          " | ".join(f"class {c}: {w:.3f}" for c, w in enumerate(weights)),
          flush=True)
    return torch.tensor(weights, dtype=torch.float)


# ---------------------------------------------------------------------------
# Training and evaluation
# ---------------------------------------------------------------------------

def train_epoch(model, loader, optimizer, scheduler, criterion, device, epoch=None, epochs=None):
    model.train()
    total_loss = 0.0
    desc = f"Epoch {epoch}/{epochs} Train" if epoch is not None and epochs is not None else "Train"
    progress = tqdm(loader, desc=desc, leave=False, dynamic_ncols=True)
    for step, batch in enumerate(progress, start=1):
        optimizer.zero_grad()
        logits = model(
            input_ids=      batch["input_ids"].to(device),
            attention_mask= batch["attention_mask"].to(device),
            token_type_ids= batch["token_type_ids"].to(device),
        ).logits                                             # FIX 2: use custom loss
        loss = criterion(logits, batch["labels"].to(device))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        total_loss += loss.item()
        progress.set_postfix(loss=f"{total_loss / step:.4f}")
    return total_loss / len(loader)


def evaluate(model, loader, device, label="Eval"):
    model.eval()
    all_preds, all_labels, all_dims = [], [], []
    with torch.no_grad():
        for batch in tqdm(loader, desc=label, leave=False, dynamic_ncols=True):
            logits = model(
                input_ids=      batch["input_ids"].to(device),
                attention_mask= batch["attention_mask"].to(device),
                token_type_ids= batch["token_type_ids"].to(device),
            ).logits
            preds = logits.argmax(dim=-1).cpu().tolist()
            all_preds.extend(preds)
            all_labels.extend(batch["labels"].tolist())
            all_dims.extend(batch["dimensions"])

    p, r, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average="binary", pos_label=1, zero_division=0
    )
    acc = sum(p == l for p, l in zip(all_preds, all_labels)) / len(all_labels)

    print(f"\n{'='*60}", flush=True)
    print(f"{label} — Overall", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"  Accuracy : {acc:.4f}", flush=True)
    print(f"  Precision: {p:.4f}  (target ≥ 0.85)", flush=True)
    print(f"  Recall   : {r:.4f}  (target ≥ 0.80)", flush=True)
    print(f"  F1       : {f1:.4f}  (target ≥ 0.82)", flush=True)

    dims = sorted(set(all_dims))
    print(f"\n{label} — Per-Dimension", flush=True)
    print(f"  {'Dimension':<28} {'Prec':>6} {'Rec':>6} {'F1':>6} {'FPR':>6} {'N':>5}", flush=True)
    print("  " + "-" * 60, flush=True)
    per_dim = {}
    for dim in dims:
        idx = [i for i, d in enumerate(all_dims) if d == dim]
        y_true = [all_labels[i] for i in idx]
        y_pred = [all_preds[i]  for i in idx]
        dp, dr, df, _ = precision_recall_fscore_support(
            y_true, y_pred, average="binary", pos_label=1, zero_division=0
        )
        if len(set(y_true)) > 1:
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        else:
            tn, fp, fn, tp = 0, 0, 0, 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        per_dim[dim] = {"precision": dp, "recall": dr, "f1": df, "fpr": fpr, "n": len(idx)}
        print(f"  {dim:<28} {dp:6.3f} {dr:6.3f} {df:6.3f} {fpr:6.3f} {len(idx):5d}", flush=True)

    return {"precision": p, "recall": r, "f1": f1, "accuracy": acc, "per_dim": per_dim}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train",       default="data/train.jsonl")
    parser.add_argument("--val",         default="data/val.jsonl")
    parser.add_argument("--output_dir",  default="models/pcm")
    parser.add_argument("--challenge_val", default="",
                        help="Optional held-out challenge validation split used for checkpoint selection.")
    parser.add_argument("--model_name",  default="microsoft/deberta-v3-base")
    parser.add_argument("--max_len",     type=int,   default=512)
    parser.add_argument("--epochs",      type=int,   default=5)
    parser.add_argument("--batch_size",  type=int,   default=16)
    parser.add_argument("--lr",          type=float, default=2e-5)
    parser.add_argument("--weight_decay",type=float, default=0.01)
    parser.add_argument("--warmup_ratio",type=float, default=0.1)
    parser.add_argument("--patience",    type=int,   default=2,
                        help="Early stopping patience (epochs without val F1 improvement)")
    parser.add_argument("--seed",        type=int,   default=42)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f"Device : {device}", flush=True)
    print(f"Model  : {args.model_name}", flush=True)

    # DeBERTa-v3 uses SentencePiece; forcing the slow tokenizer avoids
    # fragile fast-tokenizer conversion paths in fresh cloud runtimes.
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name, num_labels=2
    ).to(device)

    train_ds = PCMDataset(args.train, tokenizer, args.max_len)
    val_ds   = PCMDataset(args.val,   tokenizer, args.max_len)
    challenge_ds = None
    if args.challenge_val:
        challenge_ds = PCMDataset(args.challenge_val, tokenizer, args.max_len)

    validate_binary_labels([item["label"] for item in train_ds.samples], "train")
    validate_binary_labels([item["label"] for item in val_ds.samples], "val")
    if challenge_ds is not None:
        validate_binary_labels([item["label"] for item in challenge_ds.samples], "challenge_val")

    # FIX 2: compute and apply inverse-frequency class weights to loss
    class_weights = compute_class_weights(train_ds, num_classes=2).to(device)
    # Cast to match model dtype (avoids FP16/FP32 mismatch on GPU; FP32 on CPU)
    class_weights = class_weights.to(next(model.parameters()).dtype)
    criterion = nn.CrossEntropyLoss(weight=class_weights)

    train_loader = DataLoader(
        train_ds, batch_size=args.batch_size, shuffle=True,  collate_fn=collate_fn
    )
    val_loader = DataLoader(
        val_ds,   batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn
    )
    challenge_loader = None
    if challenge_ds is not None:
        challenge_loader = DataLoader(
            challenge_ds, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn
        )

    total_steps  = len(train_loader) * args.epochs
    warmup_steps = int(total_steps * args.warmup_ratio)

    # torch.optim.AdamW with decoupled weight decay (Loshchilov & Hutter, 2019)
    optimizer = AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    best_f1       = 0.0
    patience_cnt  = 0
    history = []

    print(f"\nTraining {args.epochs} epochs on {len(train_ds):,} samples "
          f"(warmup={warmup_steps} steps, patience={args.patience})", flush=True)
    if challenge_loader is not None:
        print(f"Checkpoint selection split: challenge_val ({len(challenge_ds):,} samples)", flush=True)
    else:
        print(f"Checkpoint selection split: val ({len(val_ds):,} samples)", flush=True)

    for epoch in range(1, args.epochs + 1):
        loss = train_epoch(
            model, train_loader, optimizer, scheduler, criterion, device,
            epoch=epoch, epochs=args.epochs,
        )
        print(f"\nEpoch {epoch}/{args.epochs}  train_loss={loss:.4f}", flush=True)
        val_metrics = evaluate(model, val_loader, device, label=f"Epoch {epoch} Val")
        selected_metrics = val_metrics
        challenge_metrics = None
        if challenge_loader is not None:
            challenge_metrics = evaluate(
                model, challenge_loader, device, label=f"Epoch {epoch} Challenge Val"
            )
            selected_metrics = challenge_metrics

        history_entry = {
            "epoch": epoch,
            "train_loss": loss,
            "val": {
                "accuracy": val_metrics["accuracy"],
                "precision": val_metrics["precision"],
                "recall": val_metrics["recall"],
                "f1": val_metrics["f1"],
            },
        }
        if challenge_metrics is not None:
            history_entry["challenge_val"] = {
                "accuracy": challenge_metrics["accuracy"],
                "precision": challenge_metrics["precision"],
                "recall": challenge_metrics["recall"],
                "f1": challenge_metrics["f1"],
            }
        history.append(history_entry)

        if selected_metrics["f1"] > best_f1:
            best_f1 = selected_metrics["f1"]
            patience_cnt = 0
            model.save_pretrained(output_dir / "best")
            tokenizer.save_pretrained(output_dir / "best")
            split_name = "challenge val" if challenge_loader is not None else "val"
            print(f"  *** New best {split_name} F1={best_f1:.4f} — checkpoint saved ***", flush=True)
        else:
            patience_cnt += 1
            print(f"  No improvement ({patience_cnt}/{args.patience})", flush=True)
            if patience_cnt >= args.patience:
                print(f"  Early stopping triggered at epoch {epoch}.", flush=True)
                break

    history_path = output_dir / "training_history.json"
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    metric_name = "challenge val" if challenge_loader is not None else "val"
    print(f"\nTraining complete.  Best {metric_name} F1 = {best_f1:.4f}", flush=True)
    print(f"Best checkpoint: {output_dir / 'best'}", flush=True)
    print(f"Training history: {history_path}", flush=True)


if __name__ == "__main__":
    main()
