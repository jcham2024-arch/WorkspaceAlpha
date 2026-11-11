# Local Training Macos

Scope: local_training_macos (hugging-face-model-trainer).
Load when: you need the local_training_macos (hugging-face-model-trainer) detail described in SKILL.md.

## Contents

- Local Training Macos

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
# Local training on macOS

Use an environment with reviewed compatible PyTorch, Transformers, TRL and PEFT
versions. Confirm `torch.backends.mps.is_available()` and actual supported dtypes
for the installed macOS/PyTorch/device; chip names alone do not guarantee bf16
support. The CUDA-oriented Unsloth example is not a general MPS implementation.

Start with a small model and bounded subset/steps; measure memory at actual
sequence length and precision. Unified memory is also used by macOS and other
applications. Reduce context, per-device batch, model size or use supported
checkpointing when out of memory. Do not disable the MPS high-watermark guard as
a generic workaround: that can exhaust system memory and destabilize the host.

Use the model's reviewed chat template. Reject missing/invalid message data;
never stringify an entire row as a fallback, which can leak unrelated metadata
into training. Keep evaluation separate. Save full durable checkpoints for resume
and local adapter/tokenizer exports for inference. Remote publication and tracking
require separate approval. Do not infer speed from CUDA benchmarks.
