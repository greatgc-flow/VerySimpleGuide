"""General 1.7 validation: integrity, JSON-schema, traceability, negative-test harness.

Python 3.8+ and jsonschema >= 4.18. All visible output is mirrored verbatim to evidence.
Pure validation: no writes to canonical package files; evidence written to ignored .validation area.
"""
from pathlib import Path, PurePosixPath
import argparse, copy, hashlib, json, sys
from datetime import datetime

sys.dont_write_bytecode = True
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError, ValidationError
    _IMPORT_ERROR = None
except ImportError as exc:
    Draft202012Validator = None
    _IMPORT_ERROR = str(exc)

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.7.0'
PACK_NAME = 'VerySimpleGuide'
# MANIFEST.json is explicitly self-excluded from its own file inventory;
# manifest digests detect accidental changes, not cryptographic provenance.
EXCLUDED = {'MANIFEST.json'}


class EvidenceSink:
    """stdout single source, persisted byte-for-byte as UTF-8 evidence."""
    def __init__(self, path=None):
        self.path = Path(path) if path else None
        self.lines = []
    def say(self, msg):
        line = str(msg)
        print(line)
        self.lines.append(line)
    def close(self):
        if self.path is None:
            return
        target = self.path.resolve(strict=False)
        if target == (ROOT / '07_AUDIT/BASELINE_VALIDATION_EVIDENCE.txt').resolve():
            raise ValueError('Evidence output cannot overwrite frozen baseline evidence')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('\n'.join(self.lines) + '\n', encoding='utf-8')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def valid_relative_path(rel):
    if not isinstance(rel, str) or not rel or '\\' in rel or ':' in rel:
        return False
    pure = PurePosixPath(rel)
    return (not pure.is_absolute() and all(x not in ('', '.', '..') for x in pure.parts))


def safe_target(root, rel):
    if not valid_relative_path(rel):
        raise ValueError('unsafe path: ' + str(rel))
    root_real = root.resolve()
    target = (root / rel).resolve(strict=False)
    try:
        target.relative_to(root_real)
    except ValueError:
        raise ValueError('path escape: ' + rel)
    return target


def file_inventory(root):
    out = set()
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith('.validation/') or rel in EXCLUDED or any(part in {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.idea', '.vscode', 'dist', 'build'} for part in path.relative_to(root).parts) or path.name.endswith(('.pyc', '.pyo')):
            continue
        out.add(rel)
    return out


def check_manifest(root, errors):
    try:
        manifest = read_json(root / 'MANIFEST.json')
        assert manifest.get('package') == PACK_NAME
        assert manifest.get('standard_version') == VERSION
        records = manifest['files']
        assert isinstance(records, list)
    except (OSError, json.JSONDecodeError, AssertionError, KeyError, TypeError) as exc:
        errors.append('bad-manifest:' + str(exc))
        return set()
    declared = set()
    for item in records:
        rel = item.get('path')
        if rel in declared:
            errors.append('manifest-duplicate:' + str(rel))
        declared.add(rel)
        try:
            target = safe_target(root, rel)
            if not target.is_file():
                errors.append('manifest-missing:' + rel)
                continue
            if sha256(target) != item.get('sha256'):
                errors.append('manifest-sha:' + rel)
            if target.stat().st_size != item.get('size_bytes'):
                errors.append('manifest-size:' + rel)
        except (OSError, TypeError, ValueError) as exc:
            errors.append('manifest-unsafe:' + str(exc))
    expected = file_inventory(root)
    if declared != expected:
        errors.append('manifest-inventory-diff:missing=' + repr(sorted(expected-declared)) + ';extra=' + repr(sorted(declared-expected)))
    return declared


def load_schemas(root, errors):
    parsed = {}
    if Draft202012Validator is None:
        errors.append('missing-dependency:jsonschema>=4.18:' + str(_IMPORT_ERROR))
        return parsed
    for path in sorted((root / '07_CONTRACTS/schemas').glob('*.schema.json')):
        try:
            schema = read_json(path)
            Draft202012Validator.check_schema(schema)
            parsed[path.name] = schema
        except (SchemaError, json.JSONDecodeError, OSError) as exc:
            errors.append('invalid-json-schema:' + path.name + ':' + str(exc)[:200])
    if not parsed:
        errors.append('missing-schemas')
    return parsed


def local_refs(schema, schemas):
    """Replace local relative schema refs with same-file defs for offline validation."""
    v = copy.deepcopy(schema)
    def walk(obj):
        if isinstance(obj, list):
            return [walk(x) for x in obj]
        if not isinstance(obj, dict):
            return obj
        if '$ref' in obj and not obj['$ref'].startswith('#'):
            pointer = obj['$ref']
            file_name, _, fragment = pointer.partition('#')
            if file_name not in schemas:
                raise ValueError('unknown local schema: ' + file_name)
            target = copy.deepcopy(schemas[file_name])
            if fragment:
                for part in fragment.strip('/').split('/'):
                    target = target[part]
            return walk(target)
        return {k: walk(value) for k,value in obj.items()}
    return walk(v)


def valid_schema_instance(schemas, schema_name, instance):
    schema = local_refs(schemas[schema_name], schemas)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(instance)


def check_examples(root, schemas, errors):
    examples = {
        'component-registry.example.json': 'component-registry.schema.json',
        'gate-evidence.example.json': 'gate-evidence.schema.json',
        'mutation-contract.example.json': 'mutation-contract.schema.json',
        'protocol-adapter.example.json': 'protocol-adapter.schema.json',
        'project-trace.example.json': 'project-trace.schema.json',
        'implementation-choice.example.json': 'implementation-choice.schema.json',
        'standard-evolution.example.json': 'standard-evolution.schema.json'
    }
    for name, schema_name in examples.items():
        try:
            valid_schema_instance(schemas, schema_name, read_json(root / '07_CONTRACTS/examples'/name))
        except (ValueError, KeyError, ValidationError, OSError, json.JSONDecodeError) as exc:
            errors.append('invalid-example:' + name + ':' + str(exc)[:180])


def check_controls(root, std, coverage, errors):
    controls = std.get('controls', [])
    expected = {x['id'] for x in controls}
    rows = coverage.get('controls', [])
    actual = [x.get('control_id') for x in rows]
    if len(controls) < 15 or len(expected) != len(controls) or len(actual) != len(controls) or set(actual) != expected or len(actual) != len(set(actual)):
        errors.append('control-coverage-incomplete')
    mapped_standards = {ref for row in rows for ref in row.get('standard_refs', [])}
    actual_standards = {x.relative_to(root).as_posix() for x in (root / '02_STANDARD').glob('*.md')}
    if not actual_standards.issubset(mapped_standards):
        errors.append('standard-owner-unmapped:' + repr(sorted(actual_standards - mapped_standards)))
    for row in rows:
        refs = row.get('standard_refs')
        if not isinstance(refs, list) or not refs:
            errors.append('control-without-standard:' + str(row.get('control_id')))
        else:
            for ref in refs:
                try:
                    if not safe_target(root, ref).is_file(): errors.append('control-standard-missing:' + ref)
                except ValueError as exc: errors.append(str(exc))
        if not row.get('verification_obligation'):
            errors.append('control-without-verification-obligation:' + str(row.get('control_id')))
        if row.get('assurance_level') != 'DESIGN_COVERED':
            errors.append('general-controls-not-runtime-verified:' + str(row.get('control_id')))


def check_invariants(root, std, index, errors):
    expected = std.get('invariants', [])
    rows = index.get('invariants', [])
    actual = [x.get('invariant_id') for x in rows]
    controls = {x['id'] for x in std.get('controls', [])}
    if index.get('standard_version') != VERSION or len(expected) != len(actual) or set(actual)!=set(expected) or len(actual)!=len(set(actual)):
        errors.append('invariant-coverage-incomplete')
    for row in rows:
        if row.get('primary_control') not in controls:
            errors.append('invariant-orphan-control:' + str(row.get('invariant_id')))
        if not row.get('product_gate_obligation'):
            errors.append('invariant-without-gate-obligation:' + str(row.get('invariant_id')))
        try:
            if not safe_target(root,row.get('standard_ref','')).is_file():
                errors.append('invariant-standard-missing:' + str(row.get('invariant_id')))
        except ValueError:
            errors.append('invariant-unsafe-standard-ref:' + str(row.get('invariant_id')))
        if row.get('assurance_level') != 'DESIGN_COVERED':
            errors.append('invariant-false-product-proof:' + str(row.get('invariant_id')))


def check_project_registry(registry, errors):
    """Semantic crosschecks beyond the component-registry JSON Schema."""
    rows=registry.get('components',[])
    ids=[row.get('id') for row in rows]
    if len(ids)!=len(set(ids)): errors.append('project-registry-duplicate-component-id')
    for row in rows:
        ident=str(row.get('id','unknown'))
        if row.get('component_class')=='EXTENSION' and 'BASE' in row.get('required_scopes',[]):
            errors.append('project-registry-optional-extension-required-base:'+ident)
        ownership=row.get('state_ownership',[])
        names=[x.get('name') for x in ownership]
        if len(names)!=len(set(names)):
            errors.append('project-registry-duplicate-state-owner:'+ident)
        for st in ownership:
            if st.get('recovery_class')=='EPHEMERAL' and st.get('backup_policy')=='REQUIRED':
                errors.append('project-registry-ephemeral-mandatory-backup:'+ident)


def expected_role_for_path(rpath):
    if rpath.startswith('07_CONTRACTS/schemas/'):
        return 'MACHINE_SSOT'
    if rpath.startswith('07_CONTRACTS/examples/'):
        return 'EXAMPLE'
    if rpath in ('03_LIFECYCLE/12x10_OVERVIEW.md', '06_GOVERNANCE/CONTROL_CATALOG.md'):
        return 'GENERATED_VIEW'
    if (rpath.startswith('06_GOVERNANCE/') and rpath.endswith('.json')) or rpath == '03_LIFECYCLE/lifecycle-matrix.json':
        return 'MACHINE_SSOT'
    if rpath in ('08_KNOWLEDGE/guidance-catalog.json', '08_KNOWLEDGE/references/catalog.json'):
        return 'REFERENCE_CATALOG'
    if rpath.startswith('02_STANDARD/') or rpath in ('LICENSE', 'NOTICE'):
        return 'NORMATIVE_SOURCE'
    if rpath.startswith(('tools/', '.github/')):
        return 'VALIDATION_TOOL'
    return None


def check_artifact_ownership(root, std, errors, ledger_override=None):
    """All tracked semantic artifacts in MANIFEST.json must have a valid Control owner and authority role."""
    ledger = ledger_override if ledger_override is not None else read_json(root / 'MANIFEST.json')
    control_ids = {c['id'] for c in std.get('controls',[])}
    roles = {'NORMATIVE_SOURCE','MACHINE_SSOT','HUMAN_GUIDE','GENERATED_VIEW',
             'EXAMPLE','REFERENCE_CATALOG','ASSURANCE_EVIDENCE','VALIDATION_TOOL'}
    records = ledger.get('files', ledger.get('artifacts', []))
    paths = [x.get('path') for x in records]
    if len(paths)!=len(set(paths)):
        errors.append('artifact-ownership-duplicate')
    actual = file_inventory(root)
    cov = read_json(root/'06_GOVERNANCE/control-coverage.json')
    standard_claims = {}
    for owner in cov.get('controls',[]):
        for referenced_path in owner.get('standard_refs',[]):
            standard_claims.setdefault(referenced_path,set()).add(owner.get('control_id'))
    for row in records:
        name=row.get('path','')
        if name.startswith('02_STANDARD/') and row.get('primary_control') not in standard_claims.get(name,set()):
            errors.append('artifact-primary-standard-control-mismatch:'+name)
    if set(paths)!=actual:
        errors.append('artifact-ownership-inventory-diff:missing='+repr(sorted(actual-set(paths)))+';extra='+repr(sorted(set(paths)-actual)))
    for row in records:
        rpath = row.get('path','')
        if row.get('primary_control') not in control_ids:
            errors.append('artifact-invalid-primary-owner:'+str(rpath))
        if row.get('role') not in roles:
            errors.append('artifact-invalid-role:'+str(rpath))
        expected_role = expected_role_for_path(rpath)
        if expected_role and row.get('role') != expected_role:
            errors.append('artifact-authority-role-mismatch:'+str(rpath))
        others = row.get('related_controls',[])
        if not isinstance(others,list) or any(x not in control_ids or x==row.get('primary_control') for x in others) or len(set(others))!=len(others):
            errors.append('artifact-invalid-secondary-owners:'+str(rpath))
        if rpath not in actual:
            errors.append('artifact-unknown-path:'+str(rpath))


def duplicate_check(items, label, errors):
    ids = [x.get('id') for x in items]
    if len(ids) != len(set(ids)):
        errors.append('duplicate-' + label)
    return {x.get('id'):x for x in items}


def check_trace(trace, errors):
    req = duplicate_check(trace.get('requirements',[]),'requirement',errors)
    tests = duplicate_check(trace.get('tests',[]),'test',errors)
    gates = duplicate_check([{**x, 'id':x.get('gate_id')} for x in trace.get('gates',[])],'gate',errors)
    obs = duplicate_check(trace.get('observations',[]),'observation',errors)
    fbs = duplicate_check(trace.get('feedback',[]),'feedback',errors)
    metrics = duplicate_check(trace['objective']['success_measures'],'metric',errors)
    for t in tests.values():
        if t['status']=='PASS' and not t.get('evidence_refs'):
            errors.append('passed-test-without-evidence:' + t['id'])
        for rid in t['requirement_ids']:
            if rid not in req: errors.append('orphan-test-requirement:' + rid)
    for o in obs.values():
        if o['metric_id'] not in metrics:
            errors.append('observation-without-fitness-measure:' + o['id'])
    for fb in fbs.values():
        obs_id = fb['observation_id']
        if obs_id not in obs or obs[obs_id]['kind'] != 'SOURCE':
            errors.append('feedback-invalid-source:' + fb['id'])
        if fb['status'] == 'CLOSED' and fb['disposition'] == 'PENDING':
            errors.append('feedback-closed-pending:' + fb['id'])
        if fb['status'] == 'CLOSED' and fb['disposition'] == 'DEFER':
            errors.append('feedback-closed-deferred:' + fb['id'])
        if fb['disposition'] == 'ACCEPT' and fb['status'] == 'CLOSED':
            # Each accepted requirement must have an explicit PASS test in this feedback's test set.
            for required_id in fb['requirement_ids']:
                if not any(tid in tests and tests[tid]['status']=='PASS'
                           and required_id in tests[tid]['requirement_ids']
                           for tid in fb['test_ids']):
                    errors.append('feedback-accepted-requirement-untested:'+fb['id']+':'+required_id)
            # Multiple gates for a promoted candidate must not silently prove different artifacts.
            digests = {gates[gid].get('artifact_digest') for gid in fb['closure_gate_ids'] if gid in gates and gates[gid]['status']=='PASS'}
            if len(digests)>1:
                errors.append('feedback-mixed-gate-artifact-digests:'+fb['id'])
            for rid in fb['requirement_ids']:
                if rid not in req: errors.append('feedback-orphan-requirement:' + rid)
            for tid in fb['test_ids']:
                if tid not in tests or tests[tid]['status']!='PASS' or not set(tests[tid]['requirement_ids']).intersection(fb['requirement_ids']):
                    errors.append('feedback-missing-pass-test:' + tid)
                elif not tests[tid].get('red_evidence_ref') and not tests[tid].get('accepted_red_exception_ref'):
                    errors.append('feedback-missing-red-evidence-or-exception:' + tid)
            for gid in fb['closure_gate_ids']:
                if gid not in gates or gates[gid]['status']!='PASS' or gates[gid]['freshness']!='FRESH' or gates[gid]['candidate_identity']!=fb['closure_candidate_identity']:
                    errors.append('feedback-invalid-gate-candidate:' + gid)
            outcome = obs.get(fb['outcome_observation_id'])
            if (not outcome or outcome['kind']!='POST_RELEASE_OUTCOME' or outcome['candidate_identity']!=fb['closure_candidate_identity']
                or outcome['evaluation'] != fb['outcome_decision']
                or fb['outcome_decision'] not in ('MEETS_TARGET','EXCEPTION_ACCEPTED')):
                errors.append('feedback-missing-post-release-outcome:' + fb['id'])
            elif obs_id in obs and obs[obs_id]['metric_id']!=outcome['metric_id']:
                errors.append('feedback-outcome-metric-mismatch:' + fb['id'])
            if outcome and fb['closure_gate_ids']:
                for gid in fb['closure_gate_ids']:
                    if gid in gates and datetime_utc(outcome['observed_at']) < datetime_utc(gates[gid]['observed_at']):
                        errors.append('feedback-outcome-before-gate:' + fb['id'])
            if fb['outcome_decision']=='EXCEPTION_ACCEPTED' and not fb.get('decision_ref'):
                errors.append('feedback-exception-without-decision:' + fb['id'])
        if fb['disposition']=='ACCEPT' and fb['status']=='CLOSED' and not fb.get('release_evidence_ref'):
            errors.append('feedback-closed-without-release-evidence:' + fb['id'])
        if fb['disposition']=='DEFER' and (not fb.get('revisit_trigger') or not fb.get('decision_ref')):
            errors.append('feedback-defer-without-revisit:' + fb['id'])
    for obs_id, ob in obs.items():
        if ob['kind']=='SOURCE' and not any(fb['observation_id']==obs_id for fb in fbs.values()):
            errors.append('orphan-source-observation:' + obs_id)




def generated_lifecycle_overview(matrix):
    """Human view generated deterministically from the machine lifecycle SSOT."""
    concerns=[x['id'] for x in matrix['concerns']]
    head='# Lifecycle 12×10 overview (GENERATED FROM MACHINE SSOT)\n\n'
    head+='FOCUS = a review priority in this stage; CONSIDER = assess applicability for the product. Neither requires installing a technology or producing an artifact.\n\n'
    head+='| Stage | Objective | Output | Exit decision | Primary control | Next / Revisit | '+' | '.join(concerns)+' |\n'
    head+='|---|---|---|---|---|---|'+('---|'*len(concerns))+'\n'
    for x in matrix['stages']:
        cells=['**F**' if x['coverage'][c]=='FOCUS' else '·' for c in concerns]
        fields=[x['id'],x['objective'],x['minimum_output'],x['exit_decision'],x['primary_control'],', '.join(x['next_stages'])+' / '+', '.join(x['revisit_stages'])]
        head+='| '+' | '.join(fields+cells)+' |\n'
    head+='\nFor owner/ref details use `lifecycle-matrix.json` (not this generated view).\n'
    return head

def check_project_lifecycle(project, stage_ids, concern_ids, errors):
    """Project 12+10 classification plus optional cell-specific overrides (not a 120-row form)."""
    for section,key,expected in [('stages','stage_id',stage_ids),('concerns','concern_id',concern_ids)]:
        rows=project.get(section,[])
        actual=[x.get(key) for x in rows]
        if len(rows)!=len(expected) or set(actual)!=set(expected) or len(set(actual))!=len(actual):
            errors.append('project-'+section+'-coverage-missing-or-duplicate')
        for row in rows:
            ident=row.get(key,'unknown')
            if not row.get('owner'):
                errors.append('project-'+section+'-no-owner:'+str(ident))
            status=row.get('status')
            if status in ('N_A','DEFERRED') and (not row.get('reason') or not row.get('revisit_trigger')):
                errors.append('project-'+section+'-unjustified-'+str(status)+':'+str(ident))
            if status=='PASS' and not row.get('evidence_refs'):
                errors.append('project-'+section+'-pass-no-evidence:'+str(ident))
    overrides=project.get('cell_overrides',[])
    seen=set()
    for row in overrides:
        stage,concern=row.get('stage_id'),row.get('concern_id')
        key=(stage,concern)
        if key in seen: errors.append('project-cell-duplicate:'+str(key))
        seen.add(key)
        if stage not in stage_ids or concern not in concern_ids:
            errors.append('project-cell-unknown-coordinate:'+str(key))
        if not row.get('owner'):
            errors.append('project-cell-owner-missing:'+str(key))
        status=row.get('status')
        if status in ('N_A','DEFERRED') and (not row.get('reason') or not row.get('revisit_trigger')):
            errors.append('project-cell-unjustified:'+str(key))
        if status=='PASS' and not row.get('evidence_refs'):
            errors.append('project-cell-pass-no-evidence:'+str(key))


def check_lifecycle_models(matrix, guidance, references, project, controls, errors):
    """Semantic crosswalk; JSON Schema shape alone cannot check graph/foreign keys."""
    concerns=[x.get('id') for x in matrix.get('concerns',[])]
    stages=[x.get('id') for x in matrix.get('stages',[])]
    if len(concerns)<10 or len(set(concerns))!=len(concerns):
        errors.append('lifecycle-concerns-not-mece')
    if len(stages)<12 or len(set(stages))!=len(stages) or not {'DISCOVER','RETIRE'}.issubset(set(stages)):
        errors.append('lifecycle-stages-not-complete')
    control_ids={x.get('id') for x in controls}
    reference_list=references.get('sources',[])
    reference_ids=[x.get('id') for x in reference_list]
    if len(reference_ids)!=len(set(reference_ids)):
        errors.append('reference-ids-duplicate')
    refs=set(reference_ids)
    for r in reference_list:
        if r.get('reviewed_at','')>references.get('as_of',''):
            errors.append('reference-reviewed-in-future:'+str(r.get('id')))
        for st in r.get('stages',[]):
            if st not in stages: errors.append('reference-unrecognized-stage:'+str(r.get('id'))+':'+str(st))
    stage_index={x.get('id'):x for x in matrix.get('stages',[])}
    for concern in matrix.get('concerns',[]):
        cid=concern.get('id','unknown')
        if concern.get('primary_control') not in control_ids:
            errors.append('lifecycle-unowned-concern:'+cid)
        for rid in concern.get('reference_ids',[]):
            if rid not in refs:
                errors.append('lifecycle-concern-unknown-ref:'+cid+':'+str(rid))
    for st in matrix.get('stages',[]):
        sid=st.get('id','unknown')
        if set(st.get('coverage',{})) != set(concerns):
            errors.append('lifecycle-horizontal-gap:'+sid)
        if st.get('primary_control') not in control_ids:
            errors.append('lifecycle-unowned-stage:'+sid)
        if not st.get('objective') or not st.get('minimum_output') or not st.get('exit_decision'):
            errors.append('lifecycle-stage-no-outcome-exit:'+sid)
        for edge_group in ('next_stages','revisit_stages'):
            for target in st.get(edge_group,[]):
                if target not in stages:
                    errors.append('lifecycle-broken-'+edge_group+':'+sid+':'+str(target))
        if not st.get('revisit_stages'):
            errors.append('lifecycle-no-feedback-return:'+sid)
        for ref in st.get('reference_ids',[]):
            if ref not in refs:
                errors.append('lifecycle-unresolved-reference:'+sid+':'+str(ref))
    # Graph connectivity is a generic guidance sanity test (not a mandated waterfall).
    reachable=set(); todo=['DISCOVER']
    while todo:
        node=todo.pop()
        if node in reachable or node not in stage_index: continue
        reachable.add(node)
        todo.extend(stage_index[node].get('next_stages',[]))
    if set(stages)-reachable:
        errors.append('lifecycle-unreachable-stages:'+repr(sorted(set(stages)-reachable)))
    if 'DISCOVER' not in stage_index.get('RETIRE',{}).get('next_stages',[]):
        errors.append('lifecycle-retirement-not-learned')
    gids=[x.get('id') for x in guidance.get('guidance',[])]
    if len(gids)!=len(set(gids)):
        errors.append('guidance-duplicate-ids')
    for entry in guidance.get('guidance',[]):
        ident=entry.get('id','unknown')
        if entry.get('applicability')!='OPTIONAL':
            errors.append('guidance-illegal-mandate:'+ident)
        if not entry.get('avoid_when') or not entry.get('alternatives') or not entry.get('tradeoffs'):
            errors.append('guidance-missing-tradeoff:'+ident)
        for name,values,known in [('stage',entry.get('stage_ids',[]),stages),('concern',entry.get('concern_ids',[]),concerns),('reference',entry.get('reference_ids',[]),reference_ids)]:
            for value in values:
                if value not in known:
                    errors.append('guidance-unknown-'+name+':'+ident+':'+str(value))
    if set(stages)-{st for x in guidance.get('guidance',[]) for st in x.get('stage_ids',[])}:
        errors.append('guidance-stages-without-any-reference')
    if set(concerns)-{c for x in guidance.get('guidance',[]) for c in x.get('concern_ids',[])}:
        errors.append('guidance-concerns-without-any-reference')
    used_refs={rid for x in matrix.get('stages',[])+matrix.get('concerns',[])+guidance.get('guidance',[]) for rid in x.get('reference_ids',[])}
    if refs-used_refs:
        errors.append('knowledge-unreferenced-sources:'+repr(sorted(refs-used_refs)))
    check_project_lifecycle(project,set(stages),set(concerns),errors)

def generated_control_catalog(std):
    return '# Control Catalog (machine SSOT generated)\n\n' + ''.join(
        '- **' + c['id'] + '** — ' + c['name'] + '\n' for c in std['controls']
    )


def datetime_utc(value):
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def semantic_lint(root, std, errors):
    if std.get('version') != VERSION: errors.append('standard-version-mismatch')
    if len(std.get('controls',[])) < 15: errors.append('control-count-regression')
    if not all(std.get('openness_contract',{}).get(k) for k in ('language_agnostic','platform_agnostic','reference_tool_non_normative','baseline_controls_not_immutable','innovation_proposals_supported')):
        errors.append('missing-openness-contract')
    if len(std.get('invariants',[])) < 37: errors.append('invariant-count-regression')
    if 'RELEASED' in std.get('maturity',[]):errors.append('maturity-distribution-conflation')
    if len(set(std.get('invariants',[])))!=len(std.get('invariants',[])):errors.append('duplicate-invariants')
    for fp in root.rglob('*.md'):
        text = fp.read_text(encoding='utf-8')
        if 'VS-UNIFIED-PACKAGE-STANDARD 1.2' in text:errors.append('stale-standard-label:'+fp.name)
    if (root / '06_GOVERNANCE/CONTROL_CATALOG.md').read_text(encoding='utf-8') != generated_control_catalog(std):
        errors.append('human-control-catalog-drift')
    if (not std.get('lifecycle_contract',{}).get('not_a_waterfall') or not std.get('guidance_contract',{}).get('not_normative_by_default')): errors.append('lifecycle-or-reference-improperly-normative')
    if not std.get('outcome_contract',{}).get('feedback_post_release_evaluation_required'):
        errors.append('missing-operational-closure-contract')


def check_all(root):
    errors = []
    check_manifest(root, errors)
    try:
        std = read_json(root / '06_GOVERNANCE/unified-package-standard.json')
        coverage = read_json(root / '06_GOVERNANCE/control-coverage.json')
        invariants = read_json(root / '06_GOVERNANCE/invariant-coverage.json')
        trace = read_json(root / '07_CONTRACTS/examples/project-trace.example.json')
        semantic_lint(root, std, errors)
        check_controls(root, std, coverage, errors)
        check_invariants(root, std, invariants, errors)
        check_artifact_ownership(root, std, errors)
        schemas = load_schemas(root, errors)
        if schemas:
            try:
                valid_schema_instance(schemas,'manifest.schema.json',read_json(root/'MANIFEST.json'))
            except (ValueError,KeyError,ValidationError,OSError,json.JSONDecodeError) as exc:
                errors.append('invalid-manifest-schema:'+str(exc)[:180])
            check_examples(root, schemas, errors)
            check_project_registry(read_json(root / '07_CONTRACTS/examples/component-registry.example.json'),errors)
            if not errors or all(not x.startswith('invalid-example') for x in errors):
                check_trace(trace, errors)
            models=[('03_LIFECYCLE/lifecycle-matrix.json','lifecycle-matrix.schema.json'),
                    ('08_KNOWLEDGE/guidance-catalog.json','guidance-catalog.schema.json'),
                    ('08_KNOWLEDGE/references/catalog.json','reference-catalog.schema.json'),
                    ('07_CONTRACTS/examples/project-lifecycle.example.json','project-lifecycle.schema.json')]
            instances=[]
            for rel, schema in models:
                data=read_json(root / rel)
                try: valid_schema_instance(schemas,schema,data)
                except (ValueError,KeyError,ValidationError) as exc: errors.append('invalid-lifecycle-model:'+rel+':'+str(exc)[:180])
                instances.append(data)
            check_lifecycle_models(*instances,std.get('controls',[]),errors)
            if (root/'03_LIFECYCLE/12x10_OVERVIEW.md').read_text(encoding='utf-8') != generated_lifecycle_overview(instances[0]): errors.append('lifecycle-human-view-drift')
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        errors.append('validation-runtime:'+str(exc)[:250])
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description='VerySimple 1.7 static package validator')
    parser.add_argument('--evidence-file',default='.validation/validation_evidence.txt')
    parser.add_argument('--project-trace',help='Validate a real project trace JSON (structural/semantic only)')
    parser.add_argument('--project-registry',help='Validate a real project component registry JSON (structural only)')
    parser.add_argument('--project-lifecycle',help='Validate the project-specific 12-stage lifecycle applicability JSON')
    parser.add_argument('--skip-negative-tests',action='store_true',help='Local development only; not a release gate')
    args = parser.parse_args(argv)
    sink = EvidenceSink(args.evidence_file)
    errors = check_all(ROOT)
    user_checks = []
    if args.project_trace or args.project_registry or args.project_lifecycle:
        schema_errors = []
        schemas = load_schemas(ROOT,schema_errors)
        errors.extend(schema_errors)
        for typ,filename,schema_name in [('project_trace',args.project_trace,'project-trace.schema.json'),('project_registry',args.project_registry,'component-registry.schema.json'),('project_lifecycle',args.project_lifecycle,'project-lifecycle.schema.json')]:
            if not filename: continue
            local_errors = []
            try:
                data = read_json(Path(filename))
                valid_schema_instance(schemas,schema_name,data)
                if typ == 'project_trace': check_trace(data,local_errors)
                if typ == 'project_registry': check_project_registry(data,local_errors)
                if typ == 'project_lifecycle':
                    mat=read_json(ROOT/'03_LIFECYCLE/lifecycle-matrix.json')
                    check_project_lifecycle(data,{x['id'] for x in mat['stages']},{x['id'] for x in mat['concerns']},local_errors)
            except (OSError, ValueError, KeyError, ValidationError, json.JSONDecodeError) as exc:
                local_errors.append(typ + '-invalid:' + str(exc)[:200])
            user_checks.append(typ+'='+('PASS' if not local_errors else 'FAIL'))
            errors.extend(local_errors)
    sink.say('PACKAGE=' + PACK_NAME)
    sink.say('standard_version=' + VERSION)
    sink.say('controls=' + str(len(read_json(ROOT / '06_GOVERNANCE/unified-package-standard.json')['controls'])))
    sink.say('invariants=' + str(len(read_json(ROOT / '06_GOVERNANCE/unified-package-standard.json')['invariants'])))
    sink.say('assurance_level=SCHEMA_AND_STATIC_VALIDATED')
    sink.say('product_runtime_assurance=NOT_EVALUATED')
    sink.say('external_project_trace=' + ('CHECKED' if args.project_trace else 'NOT_SUPPLIED'))
    sink.say('external_project_lifecycle=' + ('CHECKED' if args.project_lifecycle else 'NOT_SUPPLIED'))
    sink.say('lifecycle_matrix=12x10')
    sink.say('project_classification=12_stages+10_concerns+optional_overrides')
    sink.say('artifact_ownership=CHECKED')
    for result in user_checks: sink.say(result)
    sink.say('static_checks=' + ('PASS' if not errors else 'FAIL'))
    if not args.skip_negative_tests:
        try:
            from test_validator import run_negative_suite
            checks, test_errors = run_negative_suite(ROOT)
            sink.say('contract_fixture_checks=' + str(checks))
            errors.extend(test_errors)
        except Exception as exc:
            errors.append('negative-suite-error:' + repr(exc))
    else:
        sink.say('contract_fixture_checks=SKIPPED')
        errors.append('negative-tests-mandatory-for-release')
    for e in errors:
        sink.say('ERROR=' + e)
    sink.say('RESULT=' + ('PASS' if not errors else 'FAIL'))
    sink.close()
    return 0 if not errors else 1

if __name__ == '__main__':
    sys.exit(main())
