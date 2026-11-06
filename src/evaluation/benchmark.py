import csv
import json
import re
import sys
from pathlib import Path
from src.model.inference import generate
from src.model.context import find_policy

ROOT = Path(__file__).resolve().parents[2]

def tokens(text):
    return set(re.findall(r"\b\w+\b", text.lower()))

def token_recall(prediction, reference):
    expected = tokens(reference)
    return len(expected & tokens(prediction)) / len(expected) if expected else 0.0

def main():
    path = ROOT / 'data' / 'processed' / 'test.jsonl'
    if not path.exists():
        sys.exit('Run python -m src.data.prepare first')
    items = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not items:
        sys.exit('Test dataset is empty')
    rows = []
    # Hold generation settings fixed to isolate the effect of policy context/prompting.
    for item in items:
        for mode in ('baseline', 'policy_context'):
            context = find_policy(item['question']) if mode == 'policy_context' else ''
            result = generate(item['question'], context, optimized=(mode == 'policy_context'))
            rows.append({
                'id': item['id'], 'mode': mode,
                'question': item['question'], 'reference': item['answer'],
                'prediction': result['answer'],
                'token_recall': round(token_recall(result['answer'], item['answer']), 3),
                'latency_seconds': result['latency_seconds'],
                'context_found': bool(context)
            })
    output = ROOT / 'experiments' / 'benchmark.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for mode in ('baseline', 'policy_context'):
        subset = [row for row in rows if row['mode'] == mode]
        print(mode,
              'avg_token_recall', round(sum(row['token_recall'] for row in subset) / len(subset), 3),
              'avg_latency', round(sum(row['latency_seconds'] for row in subset) / len(subset), 3))
    print('Saved:', output)
    print('WARNING: find_policy currently reads data/raw/hr_faq.jsonl, which may include test examples. '
          'This benchmark is illustrative, not a leakage-free held-out evaluation.')

if __name__ == '__main__':
    main()
