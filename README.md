# HR Policy Assistant — Small Language Model (SLM)

A beginner-friendly Python/FastAPI demonstration using a **local** SmolLM2-360M-Instruct model. No hosted LLM API. Example HR policies are **fictional**.

## Windows 10 / VS Code setup

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.data.prepare
pytest -q
uvicorn src.api.main:app --reload
```

Open http://127.0.0.1:8000/docs and test POST /ask. First model download requires internet and may take time. CPU generation can be slow.

Example JSON: `{"question":"How many sick leave days are available?"}`

## Experiments

```powershell
python -m src.optimization.compare
python -m src.evaluation.benchmark
```

The benchmark saves `experiments/benchmark.csv` and prints baseline versus adapted token recall and latency. Results are **not precomputed**.

## Assignment stages

1. Model research: `reports/model_comparison.md` (complete license/context/hardware verification needed)
2. Dataset: `data/raw/hr_faq.jsonl` and `src/data/prepare.py`
3. Baseline: `src/model/inference.py` with `optimized=False` and evaluation script
4. Adaptation: policy context + system prompt; no fine-tuning performed
5. Optimization: deterministic decoding, token limit experiment
6. Evaluation: `src/evaluation/benchmark.py` (small proxy metric)
7. Deployment: `src/api/main.py` FastAPI and validation tests

## Submission caveats

A true independent held-out evaluation and actual measured results are required for a strong submission. This sample is intentionally small and must be expanded. Record local CPU, RAM, package versions, model revision and model-card license. Never publish employer-private HR data.
