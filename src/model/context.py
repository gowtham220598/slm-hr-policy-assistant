import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def find_policy(question):
    rows=[json.loads(x) for x in (ROOT/'data/raw/hr_faq.jsonl').read_text(encoding='utf-8').splitlines()]
    q=question.lower(); matches=[]
    for row in rows:
        topic=row['topic'].lower()
        words=[w for w in topic.split() if len(w)>3]
        if topic in q or (words and all(w in q for w in words)):
            matches.append(row['answer'])
    return ' '.join(matches)
