# HR Policy Assistant using Small Language Model (SLM)

## Project Overview

The HR Policy Assistant is a domain-specific Generative AI prototype developed using a Small Language Model (SLM).

The application is designed to answer employee questions related to HR policies, including leave eligibility, working hours, and workplace guidelines.

The project demonstrates dataset preparation, SLM inference, policy retrieval, baseline evaluation, inference optimization experiments, and FastAPI deployment.

**Current Status:** Prototype – Work in Progress

## Technologies Used

- Python 3.11
- Hugging Face Transformers
- HuggingFaceTB/SmolLM2-360M-Instruct
- PyTorch
- FastAPI
- Pydantic
- JSONL datasets
- pytest
- Git and GitHub
- Visual Studio Code

## Project Objectives

1. Implement a domain-specific HR policy assistant using an SLM.
2. Prepare a structured HR FAQ dataset.
3. Implement baseline model inference.
4. Integrate HR policy retrieval and context-aware prompting.
5. Compare model responses and inference latency.
6. Expose the application through REST API endpoints.
7. Document limitations and opportunities for improvement.

## System Architecture

User Question → FastAPI Input Validation → HR Policy Retrieval → Prompt Preparation → SLM Inference → API Response

The application also includes separate evaluation and optimization scripts.

## Dataset Preparation

The project uses a sample HR FAQ dataset stored in JSONL format.

The dataset preparation process creates three splits:

| Dataset | Records |
|---|---:|
| Training | 8 |
| Validation | 1 |
| Testing | 3 |

The dataset contains sample HR policies for demonstration purposes and does not represent the official policies of a real organization.

## Model Implementation

**Selected Model:** HuggingFaceTB/SmolLM2-360M-Instruct

The application loads the instruction-tuned model locally using Hugging Face Transformers.

Two inference configurations have been evaluated:

- Baseline: General model prompting without retrieved policy context.
- Policy Context: HR policy retrieval with domain-specific prompting.

The policy-context approach is a prompt/retrieval adaptation, not a fine-tuned model.

## Benchmark Results

The following results were recorded during local testing:

| Metric | Baseline | Policy Context |
|---|---:|---:|
| Average Token Recall | 0.333 | 0.000 |
| Average Latency | 8.794 seconds | 2.589 seconds |

The benchmark results demonstrate that policy-context inference was faster in the recorded experiment, but answer quality requires improvement.

The current benchmark is illustrative because policy retrieval may access examples from the test dataset. A leakage-free evaluation remains pending.

## Optimization Experiment

A separate local optimization comparison produced the following results:

| Configuration | Latency |
|---|---:|
| Unoptimized | 11.451 seconds |
| Optimized | 2.853 seconds |

These results represent individual measurements, not a statistically validated performance benchmark.

## Expected vs Actual Output

**Question:** How many casual leave days do employees receive?

**Expected Answer:**

Employees receive 12 casual leave days per calendar year.

**Observed Model Answer:**

I do not have that policy information.

**Observation:** The policy retrieval component returned the expected policy information, but the SLM did not consistently generate the correct answer. Improving context utilization and response accuracy remains an open task.

## FastAPI Implementation

The application exposes two endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Application health check |
| `/ask` | POST | Submit an HR policy question |

**Swagger UI:** http://127.0.0.1:8000/docs

During local testing, both endpoints returned HTTP 200 responses.

The `/ask` endpoint successfully returned a structured fallback response when a policy answer was unavailable or not identified.

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/USERNAME/slm-hr-policy-assistant.git
cd slm-hr-policy-assistant
```

Create a virtual environment:

```bash
py -3.11 -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Prepare the dataset:

```bash
python -m src.data.prepare
```

Run the API:

```bash
uvicorn src.api.main:app --reload
```

Open Swagger UI:

http://127.0.0.1:8000/docs

## Evaluation

Run the benchmark:

```bash
python -m src.evaluation.benchmark
```

Run the optimization comparison:

```bash
python -m src.optimization.compare
```

The benchmark generates an output file under `experiments/`.

## Current Limitations

- The model does not consistently produce correct policy-grounded answers.
- Fine-tuning has not been completed.
- The benchmark requires leakage-free held-out evaluation.
- Inference speed measurements need repeated runs.
- Local memory constraints have limited additional experiments.
- Further model optimization and deployment validation are required.

## Future Improvements

- Improve policy retrieval and prompt construction.
- Implement stronger answer validation.
- Evaluate smaller or quantized models.
- Investigate LoRA/QLoRA fine-tuning on suitable hardware.
- Expand the domain-specific dataset.
- Perform leakage-free evaluation.
- Improve model accuracy and resource efficiency.

## Project Status

This repository contains the implementation and experiments completed so far. It is submitted as a working prototype with documented limitations, rather than a fully optimized production-ready application.

## Author

Gowtham M

Generative AI / Python Project
