# Limitations and experiment integrity

- This is a runnable starter implementation, not a measured finished benchmark.
- The example HR rules are synthetic and not authoritative.
- Adaptation uses policy-conditioned prompting, NOT LoRA fine-tuning.
- The keyword context lookup is narrow and may miss paraphrases; it is an elementary retrieval component.
- The benchmark is a token-overlap proxy, not factual accuracy; manually review every prediction.
- The small dataset and context retrieval from the full FAQ file can cause test-information leakage. For a rigorous benchmark, isolate test facts from the adaptation corpus, or evaluate novel paraphrases against a fixed permitted policy document and disclose this setup.
- No inference or training has been executed here; benchmark CSV is generated only after running the benchmark.
