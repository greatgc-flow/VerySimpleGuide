"""Read-only optional reference selector. This tool is not a conformance requirement."""
import argparse, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]

def select(stage=None, concern=None):
    catalog=json.loads((BASE/'08_KNOWLEDGE/guidance-catalog.json').read_text(encoding='utf-8'))
    references=json.loads((BASE/'08_KNOWLEDGE/references/catalog.json').read_text(encoding='utf-8'))
    refs={x['id']:x for x in references['sources']}
    rows=[]
    for item in catalog['guidance']:
        if stage and stage not in item['stage_ids']: continue
        if concern and concern not in item['concern_ids']: continue
        rows.append((item,[refs[i] for i in item['reference_ids'] if i in refs]))
    return rows

def main():
    p=argparse.ArgumentParser(description='Optional VerySimple lifecycle guidance selector')
    p.add_argument('--stage')
    p.add_argument('--concern')
    p.add_argument('--evidence-file')
    a=p.parse_args()
    out=['mode=OPTIONAL_REFERENCE','not_normative=true']
    matches=select(a.stage,a.concern)
    out.append('matches='+str(len(matches)))
    for x,refs in matches:
        out.extend([x['id']+' '+x['title'],'  use_when: '+x['use_when'],'  avoid_when: '+x['avoid_when'],'  alternatives: '+'; '.join(x['alternatives'])])
        for ref in refs: out.append('  reference: '+ref['url']+' ['+ref['source_status']+']')
    text='\n'.join(out)+'\n'
    print(text,end='')
    if a.evidence_file:
        target=Path(a.evidence_file)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text,encoding='utf-8')
if __name__=='__main__':main()
