
from src.model.inference import load_model
import torch

tokenizer, model = load_model()

messages = [
    {
        "role": "system",
        "content": (
            "You are an HR assistant. "
            "Answer using the supplied policy."
        )
    },
    {
        "role": "user",
        "content": (
            "Policy: Employees receive 12 casual leave "
            "days per calendar year.\n"
            "Question: How many casual leave days "
            "do employees receive?"
        )
    }
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

print("\n===== MODEL PROMPT =====")
print(prompt)

inputs = tokenizer(prompt, return_tensors="pt")

with torch.inference_mode():
    output = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

answer = tokenizer.decode(
    output[0][inputs["input_ids"].shape[-1]:],
    skip_special_tokens=True
)

print("\n===== RAW MODEL ANSWER =====")
print(repr(answer))
