import json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    records=[]; seen=set()
    for line in (ROOT/'data/raw/hr_faq.jsonl').read_text(encoding='utf-8').splitlines():
        try: r=json.loads(line)
        except json.JSONDecodeError: continue
        if not all(isinstance(r.get(k),str) and r[k].strip() for k in ('question','answer','topic')): continue
        key=r['question'].strip().lower()
        if key in seen: continue
        seen.add(key);records.append(r)
    random.Random(42).shuffle(records)
    n=len(records); a=int(n*.67);b=int(n*.83)
    for name,items in [('train',records[:a]),('validation',records[a:b]),('test',records[b:])]:
        (ROOT/f'data/processed/{name}.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in items),encoding='utf-8')
        print(name,len(items))
if __name__=='__main__':main()
