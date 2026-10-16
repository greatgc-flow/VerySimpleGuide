"""Read-only optional reference selector. This tool is not a conformance requirement."""
import argparse, json, sys
from pathlib import Path

sys.dont_write_bytecode = True
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from validate_package import resolve_safe_evidence_path

BASE = Path(__file__).resolve().parents[1]


def select(stage=None, concern=None):
    matrix = json.loads((BASE / '03_LIFECYCLE/lifecycle-matrix.json').read_text(encoding='utf-8'))
    known_stages = {x['id'] for x in matrix['stages']}
    known_concerns = {x['id'] for x in matrix['concerns']}
    if stage is not None and stage not in known_stages:
        raise ValueError('Unknown stage: ' + str(stage))
    if concern is not None and concern not in known_concerns:
        raise ValueError('Unknown concern: ' + str(concern))
    catalog = json.loads((BASE / '08_KNOWLEDGE/guidance-catalog.json').read_text(encoding='utf-8'))
    references = json.loads((BASE / '08_KNOWLEDGE/references/catalog.json').read_text(encoding='utf-8'))
    refs = {x['id']: x for x in references['sources']}
    rows = []
    for item in catalog['guidance']:
        if stage and stage not in item['stage_ids']:
            continue
        if concern and concern not in item['concern_ids']:
            continue
        rows.append((item, [refs[i] for i in item['reference_ids'] if i in refs], catalog))
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(description='Optional VerySimple lifecycle guidance selector')
    p.add_argument('--stage')
    p.add_argument('--concern')
    p.add_argument('--evidence-file')
    a = p.parse_args(argv)
    try:
        target = resolve_safe_evidence_path(a.evidence_file, root=BASE) if a.evidence_file else None
        matches = select(a.stage, a.concern)
    except ValueError as exc:
        print('ERROR=' + str(exc), file=sys.stderr)
        return 2
    out = ['mode=OPTIONAL_REFERENCE', 'not_normative=true', 'matches=' + str(len(matches))]
    for x, refs, catalog in matches:
        alts = x.get('alternatives') or catalog.get('default_alternatives', [])
        out.extend([
            x['id'] + ' ' + x['title'],
            '  use_when: ' + x['use_when'],
            '  avoid_when: ' + x['avoid_when'],
            '  alternatives: ' + '; '.join(alts),
        ])
        for ref in refs:
            out.append('  reference: ' + ref['url'] + ' [' + ref['source_status'] + ']')
    text = '\n'.join(out) + '\n'
    print(text, end='')
    if target is not None:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())

