import os
import time
from functools import lru_cache

MODEL_ID = os.getenv(
    "SLM_MODEL",
    "HuggingFaceTB/SmolLM2-360M-Instruct"
)

FALLBACK = "I do not have that policy information."


@lru_cache(maxsize=1)
def load_model():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=torch.float32
    )

    model.eval()
    return tokenizer, model


def generate(question, context="", optimized=False):
    import torch

    tok, model = load_model()

    question = question.strip()
    context = context.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if optimized and not context:
        return {
            "answer": FALLBACK,
            "latency_seconds": 0.0,
            "model": MODEL_ID
        }

    if optimized:
        system_prompt = (
            "You are an HR policy assistant. "
            "Answer the employee's question using only "
            "the supplied HR policy. "
            "If the policy contains the answer, provide it. "
            "If the answer is not available, say exactly: "
            f"{FALLBACK}"
        )

        user_prompt = (
            f"HR Policy:\n{context}\n\n"
            f"Employee Question:\n{question}\n\n"
            "Answer:"
        )
    else:
        system_prompt = "You are a helpful assistant."
        user_prompt = question

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    prompt = tok.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tok(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    start = time.perf_counter()

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=96,
            do_sample=False,
            pad_token_id=tok.eos_token_id
        )

    generated_tokens = output[0][
        inputs["input_ids"].shape[-1]:
    ]

    answer = tok.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    if not answer:
        answer = FALLBACK

    return {
        "answer": answer,
        "latency_seconds": round(
            time.perf_counter() - start, 3
        ),
        "model": MODEL_ID
    }