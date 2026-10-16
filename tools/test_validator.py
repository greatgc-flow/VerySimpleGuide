"""Deterministic negative controls; a validator that accepts these must not issue PASS."""
from pathlib import Path
import copy, json, sys

sys.dont_write_bytecode = True
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)


def run_negative_suite(root):
    # Imported only after main validator loads successfully; no mutation to product files.
    from validate_package import (check_trace, check_controls, valid_schema_instance,
                                  valid_relative_path, check_manifest, load_schemas, check_invariants, check_lifecycle_models, check_project_lifecycle, check_artifact_ownership, check_project_registry)
    from jsonschema import ValidationError
    errors = []
    count = 0
    schemas = load_schemas(root, errors)
    trace = json.loads((root / '07_CONTRACTS/examples/project-trace.example.json').read_text(encoding='utf-8'))

    def negative_json(name, schema_name, instance):
        nonlocal count
        count += 1
        try:
            valid_schema_instance(schemas, schema_name, instance)
        except ValidationError:
            return
        except Exception as exc:
            errors.append('negative-test-error:' + name + ':' + str(exc))
            return
        errors.append('negative-test-accepted-invalid:' + name)

    def negative_trace(name, instance):
        nonlocal count
        count += 1
        flaws = []
        check_trace(instance, flaws)
        if not flaws:
            errors.append('negative-test-accepted-invalid:' + name)

    maturity_valid = {'items':[{'id':'feature-1','status':'VERIFIED','candidate_identity':'commit:abc','verified_at':'2026-10-16T00:00:00Z','evidence':['run:verified']}]}
    valid_schema_instance(schemas, 'maturity.schema.json', maturity_valid)
    negative_json('VERIFIED-without-proof', 'maturity.schema.json', {'items':[{'id':'feature-1','status':'VERIFIED','evidence':[]}]})
    bad = copy.deepcopy(maturity_valid); bad['items'][0]['verified_at']='not-a-date'
    negative_json('VERIFIED-invalid-datetime', 'maturity.schema.json', bad)
    gate_valid = trace['gates'][0]
    negative_json('PASS-stale', 'gate-evidence.schema.json', {**gate_valid, 'freshness':'STALE'})
    negative_json('PASS-empty-evidence', 'gate-evidence.schema.json', {**gate_valid,'evidence_refs':[]})
    negative_json('PASS-no-digest', 'gate-evidence.schema.json', {k:v for k,v in gate_valid.items() if k!='artifact_digest'})
    registry=json.loads((root/'07_CONTRACTS/examples/component-registry.example.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(registry);bad['components'][1]['required_scopes']=['BASE']
    negative_json('optional-extension-cannot-be-required-for-base','component-registry.schema.json',bad)
    bad=copy.deepcopy(registry);bad['components'][1]['boundary_roles']=['NONE','PROVIDER']
    negative_json('NONE-exclusive-boundary-role','component-registry.schema.json',bad)
    bad=copy.deepcopy(trace);bad['feedback'][0]['test_ids']=['NONEXISTENT'];negative_trace('orphan-feedback-test',bad)
    bad=copy.deepcopy(trace);bad['tests'][0].pop('red_evidence_ref');negative_trace('closed-without-red-or-exception',bad)
    bad=copy.deepcopy(trace);bad['feedback'][0].pop('release_evidence_ref');negative_trace('closed-without-release-evidence',bad)
    bad=copy.deepcopy(trace);bad['observations'][1]['observed_at']='2026-10-15T00:00:00Z';negative_trace('post-outcome-precedes-gate',bad)
    bad=copy.deepcopy(trace);bad['feedback'][0]['closure_candidate_identity']='source:other';negative_trace('gate-candidate-mismatch',bad)
    bad=copy.deepcopy(trace);bad['observations'][1]['evaluation']='MISSES_TARGET';negative_trace('outcome-not-accepted',bad)
    bad=copy.deepcopy(trace);bad['feedback'][0]['outcome_observation_id']='OBS-1';negative_trace('no-post-release-outcome',bad)
    bad=copy.deepcopy(trace);bad['observations'].append(copy.deepcopy(bad['observations'][0]));negative_trace('duplicate-observation-ids',bad)
    bad=copy.deepcopy(trace);bad['observations'][0]['metric_id']='NO-METRIC';negative_trace('orphan-measure',bad)
    bad=copy.deepcopy(trace);bad['feedback']=[];negative_trace('orphan-source-observation',bad)
    bad=copy.deepcopy(trace);bad['feedback'][0]['disposition']='DEFER';bad['feedback'][0].pop('revisit_trigger',None);negative_trace('defer-without-revisit',bad)
    coverage=json.loads((root / '06_GOVERNANCE/control-coverage.json').read_text(encoding='utf-8'))
    std=json.loads((root / '06_GOVERNANCE/unified-package-standard.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(coverage);bad['controls'].pop();flaws=[];check_controls(root,std,bad,flaws);count+=1
    if not flaws:errors.append('negative-test-accepted-invalid:missing-control')
    invariant_index=json.loads((root/'06_GOVERNANCE/invariant-coverage.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(invariant_index);bad['invariants'].pop();flaws=[];check_invariants(root,std,bad,flaws);count+=1
    if not flaws:errors.append('negative-test-accepted-invalid:missing-invariant')
    bad=copy.deepcopy(invariant_index);bad['invariants'][0]['primary_control']='BAD';flaws=[];check_invariants(root,std,bad,flaws);count+=1
    if not flaws:errors.append('negative-test-accepted-invalid:invariant-bad-owner')
    for path in ('../secret.txt','/tmp/other.txt','A\\B','C:/absolute.txt'):
        count+=1
        if valid_relative_path(path):errors.append('negative-test-accepted-invalid:unsafe-path:'+path)
    # R10: openness and namespace regression. Strict common fields, permissive namespaced extensions.
    example_choice=json.loads((root/'07_CONTRACTS/examples/implementation-choice.example.json').read_text(encoding='utf-8'))
    invalid=copy.deepcopy(example_choice);invalid['decision']='INSTANT_ADOPT'
    negative_json('invalid-innovation-decision','implementation-choice.schema.json',invalid)
    invalid=copy.deepcopy(example_choice);invalid['evidence_plan']=''
    negative_json('unfalsifiable-technology-choice','implementation-choice.schema.json',invalid)
    invalid=copy.deepcopy(example_choice);invalid['alternatives']=[]
    negative_json('no-alternative-evaluated','implementation-choice.schema.json',invalid)
    registry=json.loads((root/'07_CONTRACTS/examples/component-registry.example.json').read_text(encoding='utf-8'))
    invalid=copy.deepcopy(registry);invalid['components'][1]['extensions']={'no_namespace':True}
    negative_json('non-namespaced-metadata','component-registry.schema.json',invalid)
    valid_schema_instance(schemas,'component-registry.schema.json',registry)
    valid_schema_instance(schemas,'implementation-choice.schema.json',example_choice)
    evolution=json.loads((root/'07_CONTRACTS/examples/standard-evolution.example.json').read_text(encoding='utf-8'))
    invalid=copy.deepcopy(evolution);invalid['coverage_gap']=''
    negative_json('no-coverage-gap','standard-evolution.schema.json',invalid)
    valid_schema_instance(schemas,'standard-evolution.schema.json',evolution)
    # Positive non-lock-in proof: governed future control counts can expand beyond 15.
    future_std=copy.deepcopy(std)
    future_coverage=copy.deepcopy(coverage)
    future_std['controls'].append({'id':'UPS-FUTURE','name':'Versioned optional future control'})
    new_coverage=copy.deepcopy(future_coverage['controls'][0]);new_coverage['control_id']='UPS-FUTURE'
    future_coverage['controls'].append(new_coverage)
    flaws=[];check_controls(root,future_std,future_coverage,flaws);count+=1
    if flaws:errors.append('positive-control-evolution-rejected:'+repr(flaws))
    # Positive reference proof, not just negative tests.
    flaws=[];check_trace(trace,flaws);count+=1
    if flaws:errors.append('positive-trace-rejected:'+repr(flaws))
    # R11: full lifecycle / optional knowledge negative controls.
    matrix=json.loads((root/'03_LIFECYCLE/lifecycle-matrix.json').read_text(encoding='utf-8'))
    guidance=json.loads((root/'08_KNOWLEDGE/guidance-catalog.json').read_text(encoding='utf-8'))
    sources=json.loads((root/'08_KNOWLEDGE/references/catalog.json').read_text(encoding='utf-8'))
    project=json.loads((root/'07_CONTRACTS/examples/project-lifecycle.example.json').read_text(encoding='utf-8'))
    def negative_lifecycle(name,ma=matrix,gu=guidance,rs=sources,pr=project):
        nonlocal count
        count+=1
        flaws=[]
        check_lifecycle_models(ma,gu,rs,pr,std['controls'],flaws)
        if not flaws: errors.append('negative-test-accepted-invalid:'+name)
    bad=copy.deepcopy(matrix);bad['stages'].pop();negative_lifecycle('missing-lifecycle-phase',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][1]['id']=bad['stages'][0]['id'];negative_lifecycle('duplicate-lifecycle-phase',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['coverage'].pop('OUTCOME_VALUE');negative_lifecycle('missing-crosscut-concern',ma=bad)
    bad=copy.deepcopy(matrix);bad['concerns'][0]['primary_control']='UPS-BAD';negative_lifecycle('unowned-crosscut-concern',ma=bad)
    bad=copy.deepcopy(matrix);bad['concerns'][0]['reference_ids']=['BAD-REF'];negative_lifecycle('crosscut-reference-invalid',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['primary_control']='UPS-INVALID';negative_lifecycle('unowned-lifecycle-stage',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['next_stages']=['NONEXISTENT'];negative_lifecycle('broken-transition',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['reference_ids']=['BAD-REF'];negative_lifecycle('orphan-reference',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['revisit_stages']=[];negative_lifecycle('missing-revisit',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][-1]['next_stages']=['ASSESS'];negative_lifecycle('retirement-learning-lost',ma=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['applicability']='REQUIRED';negative_lifecycle('mandatory-advisory-guide',gu=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['avoid_when']='';negative_lifecycle('pattern-without-avoid-when',gu=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['reference_ids']=['NO-REF'];negative_lifecycle('guidance-missing-source',gu=bad)
    bad=copy.deepcopy(project);bad['stages'][0]['evidence_refs']=[];negative_lifecycle('lifecycle-pass-without-evidence',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][-1]['revisit_trigger']='';negative_lifecycle('lifecycle-NA-without-trigger',pr=bad)
    bad=copy.deepcopy(project);bad['stages'].pop();negative_lifecycle('project-stage-unclassified',pr=bad)
    bad=copy.deepcopy(sources);bad['sources'][0]['stages']=['UNKNOWN'];negative_lifecycle('reference-to-bad-stage',rs=bad)
    bad=copy.deepcopy(sources);bad['sources'][0]['reviewed_at']='2099-01-01';negative_lifecycle('reference-review-after-snapshot',rs=bad)
    # Positive future evolution: new lifecycle concern is not rejected solely due to count.
    future=copy.deepcopy(matrix)
    future['concerns'].append({'id':'FUTURE_CONCERN','label':'Future governed dimension','primary_control':'UPS-DOC','reference_ids':['ADR']})
    for st in future['stages']: st['coverage']['FUTURE_CONCERN']='CONSIDER'
    future_guidance=copy.deepcopy(guidance)
    future_guidance['guidance'][0]['concern_ids'].append('FUTURE_CONCERN')
    future_project=copy.deepcopy(project)
    future_project['concerns'].append({'concern_id':'FUTURE_CONCERN','status':'OPTIONAL','owner':'future-reviewer','reason':'governed growth','revisit_trigger':'risk update','evidence_refs':[]})
    flaws=[];check_lifecycle_models(future,future_guidance,sources,future_project,std['controls'],flaws);count+=1
    if flaws:errors.append('positive-future-concern-rejected:'+repr(flaws))
    valid_schema_instance(schemas,'lifecycle-matrix.schema.json',matrix)
    valid_schema_instance(schemas,'guidance-catalog.schema.json',guidance)
    valid_schema_instance(schemas,'reference-catalog.schema.json',sources)
    valid_schema_instance(schemas,'project-lifecycle.schema.json',project)
    count+=1
    good=[]
    check_lifecycle_models(matrix,guidance,sources,project,std['controls'],good)
    if good:errors.append('positive-lifecycle-rejected:'+repr(good))
    # R12 cross-recursive coverage and false-positive prevention.
    bad=copy.deepcopy(project);bad['concerns'].pop();negative_lifecycle('project-concern-unclassified',pr=bad)
    bad=copy.deepcopy(project);bad['concerns'][1]['concern_id']=bad['concerns'][0]['concern_id'];negative_lifecycle('project-concern-duplicate',pr=bad)
    bad=copy.deepcopy(project);bad['concerns'][0]['status']='PASS';bad['concerns'][0]['evidence_refs']=[];negative_lifecycle('project-concern-pass-no-evidence',pr=bad)
    bad=copy.deepcopy(project);bad['cell_overrides']=[{'stage_id':'BAD','concern_id':'OUTCOME_VALUE','status':'N_A','owner':'review','reason':'x','revisit_trigger':'x','evidence_refs':[]}]
    negative_lifecycle('cell-override-bad-coordinate',pr=bad)
    bad=copy.deepcopy(project);record={'stage_id':'DISCOVER','concern_id':'OUTCOME_VALUE','status':'N_A','owner':'review','reason':'x','revisit_trigger':'x','evidence_refs':[]};bad['cell_overrides']=[record,copy.deepcopy(record)]
    negative_lifecycle('cell-override-duplicate',pr=bad)
    bad=copy.deepcopy(project);bad['cell_overrides']=[{'stage_id':'DISCOVER','concern_id':'OUTCOME_VALUE','status':'PASS','owner':'review','reason':'','revisit_trigger':'','evidence_refs':[]}]
    negative_lifecycle('cell-override-false-pass',pr=bad)
    bad=copy.deepcopy(trace)
    bad['requirements'].append({'id':'REQ-2','scope':'BASE','owner':'engineering','acceptance':'a second independent acceptance'})
    bad['feedback'][0]['requirement_ids'].append('REQ-2')
    negative_trace('feedback-partially-covered-requirement',bad)
    bad=copy.deepcopy(trace)
    second=copy.deepcopy(bad['gates'][0]);second['gate_id']='GATE-2';second['artifact_digest']='sha256:'+'b'*64
    bad['gates'].append(second);bad['feedback'][0]['closure_gate_ids'].append('GATE-2')
    negative_trace('feedback-mixed-gate-artifact',bad)
    ledger=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(ledger);bad['files'][0]['rogue_ownership']='not allowed'
    negative_json('manifest-reject-unknown-field','manifest.schema.json',bad)
    bad=copy.deepcopy(ledger);bad['files'].pop();flaws=[];check_artifact_ownership(root,std,flaws,bad);count+=1
    if not any('artifact-ownership-inventory-diff' in x for x in flaws):errors.append('negative-test-accepted-invalid:missing-artifact-owner')
    bad=copy.deepcopy(ledger);bad['files'][0]['primary_control']='UPS-NOBODY';flaws=[];check_artifact_ownership(root,std,flaws,bad);count+=1
    if not any('artifact-invalid-primary-owner' in x for x in flaws):errors.append('negative-test-accepted-invalid:invalid-artifact-owner')
    bad=copy.deepcopy(ledger)
    for item in bad['files']:
        if item['path']=='02_STANDARD/CLI_STANDARD.md':
            item['primary_control']='UPS-COMP'
            break
    flaws=[];check_artifact_ownership(root,std,flaws,bad);count+=1
    if not any('artifact-primary-standard-control-mismatch' in x for x in flaws):
        errors.append('negative-test-accepted-invalid:cross-control-normative-owner')
    bad=copy.deepcopy(ledger);bad['files'].append(copy.deepcopy(bad['files'][0]));flaws=[];check_artifact_ownership(root,std,flaws,bad);count+=1
    if not any('artifact-ownership-duplicate' in x for x in flaws):errors.append('negative-test-accepted-invalid:duplicate-artifact')
    reg=json.loads((root/'07_CONTRACTS/examples/component-registry.example.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(reg);bad['components'][0]['id']=bad['components'][1]['id'];flaws=[];check_project_registry(bad,flaws);count+=1
    if not any('duplicate-component-id' in x for x in flaws):errors.append('negative-test-accepted-invalid:duplicate-component')
    # Positive project 12+10+cell override.
    good=copy.deepcopy(project)
    good['cell_overrides']=[{'stage_id':'DISCOVER','concern_id':'RISK_SECURITY','status':'DEFERRED','owner':'review','reason':'requires evidence','revisit_trigger':'next risk review','evidence_refs':[]}]
    flaws=[];check_project_lifecycle(good,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws);count+=1
    if flaws: errors.append('positive-project-cell-override-rejected:'+repr(flaws))
    return count,errors
