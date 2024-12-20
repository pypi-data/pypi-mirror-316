# vllmlp

`vllmlp` is a collection of Logits Processors for VLLM. Currently, it contains the following processors:

- `vllmlp/qwen/NoCJKLogitsProcessor`: A Logits Processor that prevents CJK characters from being generated in the output. ONLY works with QWen2.5 models.

## Installation

```bash
pip install vllmlp
```