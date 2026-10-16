"""Deterministic negative controls; a validator that accepts these must not issue PASS."""
from pathlib import Path
import copy, json, os, subprocess, sys, tempfile

sys.dont_write_bytecode = True
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)


def run_negative_suite(root, include_fs=True, require_fs_tests=False, fs_report=None):
    # Imported only after main validator loads successfully; no mutation to product files.
    from validate_package import (check_trace, check_controls, valid_schema_instance, check_format_checkers,
                                  valid_relative_path, resolve_safe_evidence_path, check_manifest, load_schemas, check_invariants, check_lifecycle_models, check_project_lifecycle, check_artifact_ownership, check_project_registry)
    from suggest_guidance import select as select_guidance
    from jsonschema import FormatChecker, ValidationError
    errors = []
    count = 0
    schemas = load_schemas(root, errors)
    trace = json.loads((root / '07_CONTRACTS/examples/project-trace.example.json').read_text(encoding='utf-8'))
    registry=json.loads((root/'07_CONTRACTS/examples/component-registry.example.json').read_text(encoding='utf-8'))

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

    def negative_trace(name, instance, expected_error):
        nonlocal count
        count += 1
        flaws = []
        check_trace(instance, flaws)
        if not any(expected_error in f for f in flaws):
            errors.append('negative-test-accepted-invalid:' + name + ':expected=' + expected_error + ':got=' + repr(flaws))

    def positive_trace(name, instance, prior=None):
        nonlocal count
        count += 1
        valid_schema_instance(schemas, 'project-trace.schema.json', instance)
        flaws = []
        check_trace(instance, flaws, prior)
        if flaws: errors.append('positive-' + name + '-rejected:' + repr(flaws))

    maturity_valid = {'items':[registry['components'][0]['verification']]}
    valid_schema_instance(schemas, 'maturity.schema.json', maturity_valid)
    negative_json('VERIFIED-without-proof', 'maturity.schema.json', {'items':[{'id':'feature-1','status':'VERIFIED','evidence':[]}]})
    bad = copy.deepcopy(maturity_valid); bad['items'][0]['verified_at']='not-a-date'
    negative_json('VERIFIED-invalid-datetime', 'maturity.schema.json', bad)
    # Fail-closed guard when date-time format checker is absent or schema uses an unbacked format.
    stripped_fc = FormatChecker()
    stripped_fc.checkers = {k: v for k, v in stripped_fc.checkers.items() if k != 'date-time'}
    fmt_flaws = []
    count += 1
    if check_format_checkers(fmt_flaws, checker=stripped_fc) or not any('missing-format-checker:date-time' in x for x in fmt_flaws):
        errors.append('negative-test-accepted-invalid:missing-datetime-format-checker-guard')
    count += 1
    try:
        valid_schema_instance(schemas, 'maturity.schema.json', maturity_valid, checker=stripped_fc)
        errors.append('negative-test-accepted-invalid:valid-schema-instance-without-datetime-checker')
    except RuntimeError as exc:
        if 'missing-format-checker:date-time' not in str(exc):
            errors.append('negative-test-wrong-error:valid-schema-instance-without-datetime-checker:' + str(exc))
    unbacked_flaws = []
    count += 1
    if check_format_checkers(unbacked_flaws, schemas={'unbacked.schema.json': {'type': 'string', 'format': 'unbacked-custom-format'}}) or not any('missing-format-checker:unbacked-custom-format' in x for x in unbacked_flaws):
        errors.append('negative-test-accepted-invalid:unbacked-schema-format-guard')
    gate_valid = trace['gates'][0]
    negative_json('PASS-stale', 'gate-evidence.schema.json', {**gate_valid, 'freshness':'STALE'})
    negative_json('PASS-empty-evidence', 'gate-evidence.schema.json', {**gate_valid,'evidence_refs':[]})
    negative_json('PASS-no-digest', 'gate-evidence.schema.json', {k:v for k,v in gate_valid.items() if k!='artifact_digest'})
    bad=copy.deepcopy(registry);bad['components'][1]['required_scopes']=['BASE']
    negative_json('optional-extension-cannot-be-required-for-base','component-registry.schema.json',bad)
    bad=copy.deepcopy(registry);bad['components'][1]['boundary_roles']=['NONE','PROVIDER']
    negative_json('NONE-exclusive-boundary-role','component-registry.schema.json',bad)
    bad=copy.deepcopy(trace);bad['feedback'][0]['test_ids'].append('NONEXISTENT');negative_trace('orphan-feedback-test',bad,'feedback-missing-pass-test')
    bad=copy.deepcopy(trace);bad['tests'][0].pop('red_evidence_ref');negative_trace('closed-without-red-or-exception',bad,'feedback-missing-red-evidence-or-exception')
    bad=copy.deepcopy(trace);bad['feedback'][0].pop('release_evidence_ref');negative_trace('closed-without-release-evidence',bad,'feedback-closed-without-release-evidence')
    bad=copy.deepcopy(trace);bad['observations'][1]['observed_at']='2026-10-15T00:00:00Z';negative_trace('post-outcome-precedes-gate',bad,'feedback-outcome-before-gate')
    bad=copy.deepcopy(trace);bad['gates'][0]['candidate_identity']='source:other';negative_trace('gate-candidate-mismatch',bad,'feedback-invalid-gate-candidate')
    bad=copy.deepcopy(trace);bad['observations'][1]['candidate_identity']='source:other';negative_trace('outcome-candidate-mismatch',bad,'feedback-missing-post-release-outcome')
    bad=copy.deepcopy(trace);bad['observations'][1]['evaluation']='MISSES_TARGET';negative_trace('outcome-not-accepted',bad,'feedback-missing-post-release-outcome')
    bad=copy.deepcopy(trace);bad['feedback'][0]['outcome_observation_id']='OBS-1';negative_trace('no-post-release-outcome',bad,'feedback-missing-post-release-outcome')
    bad=copy.deepcopy(trace);bad['observations'].append(copy.deepcopy(bad['observations'][0]));negative_trace('duplicate-observation-ids',bad,'duplicate-observation')
    bad=copy.deepcopy(trace);bad['observations'][0]['metric_id']='NO-METRIC';negative_trace('orphan-measure',bad,'observation-without-fitness-measure')
    bad=copy.deepcopy(trace);bad['feedback']=[];negative_trace('orphan-source-observation',bad,'orphan-source-observation')
    bad=copy.deepcopy(trace);bad['feedback'][0]['disposition']='DEFER';bad['feedback'][0]['status']='OPEN';bad['feedback'][0].pop('revisit_trigger',None);negative_trace('defer-without-revisit',bad,'feedback-defer-without-revisit')
    bad=copy.deepcopy(trace);bad['feedback'][0]['disposition']='DEFER';bad['feedback'][0]['revisit_trigger']='next-quarter';negative_trace('closed-while-deferred',bad,'feedback-closed-deferred')
    coverage=json.loads((root / '06_GOVERNANCE/control-coverage.json').read_text(encoding='utf-8'))
    std=json.loads((root / '06_GOVERNANCE/unified-package-standard.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(coverage);bad['controls'].pop();flaws=[];check_controls(root,std,bad,flaws);count+=1
    if not any('control-coverage-incomplete' in x for x in flaws):errors.append('negative-test-accepted-invalid:missing-control')
    invariant_index=json.loads((root/'06_GOVERNANCE/invariant-coverage.json').read_text(encoding='utf-8'))
    bad=copy.deepcopy(invariant_index);bad['invariants'].pop();flaws=[];check_invariants(root,std,bad,flaws);count+=1
    if not any('invariant-coverage-incomplete' in x for x in flaws):errors.append('negative-test-accepted-invalid:missing-invariant')
    bad=copy.deepcopy(invariant_index);bad['invariants'][0]['primary_control']='BAD';flaws=[];check_invariants(root,std,bad,flaws);count+=1
    if not any('invariant-orphan-control' in x for x in flaws):errors.append('negative-test-accepted-invalid:invariant-bad-owner')
    for path in ('../secret.txt','/tmp/other.txt','A\\B','C:/absolute.txt','a//b','./a','a/.','a/'):
        count+=1
        if valid_relative_path(path):errors.append('negative-test-accepted-invalid:unsafe-path:'+path)
    for bad_ev,inps in (('MANIFEST.json',()),('06_GOVERNANCE/unified-package-standard.json',()),('.validation/../MANIFEST.json',()),('../outside.txt',()),('.validation',()),('.validation/input_alias.json',('.validation/input_alias.json',))):
        count+=1
        try:
            resolve_safe_evidence_path(bad_ev,root=root,input_paths=inps)
            errors.append('negative-test-accepted-invalid:unsafe-evidence-path:'+bad_ev)
        except ValueError:
            pass
    count+=1
    try:
        select_guidance(stage='UNKNOWN_STAGE')
        errors.append('negative-test-accepted-invalid:unknown-guidance-stage')
    except ValueError:
        pass
    count+=1
    try:
        select_guidance(concern='UNKNOWN_CONCERN')
        errors.append('negative-test-accepted-invalid:unknown-guidance-concern')
    except ValueError:
        pass
    # R10: openness and namespace regression. Strict common fields, permissive namespaced extensions.
    example_choice=json.loads((root/'07_CONTRACTS/examples/implementation-choice.example.json').read_text(encoding='utf-8'))
    invalid=copy.deepcopy(example_choice);invalid['decision']='INSTANT_ADOPT'
    negative_json('invalid-innovation-decision','implementation-choice.schema.json',invalid)
    invalid=copy.deepcopy(example_choice);invalid['evidence_plan']=''
    negative_json('unfalsifiable-technology-choice','implementation-choice.schema.json',invalid)
    invalid=copy.deepcopy(example_choice);invalid['alternatives']=[]
    negative_json('no-alternative-evaluated','implementation-choice.schema.json',invalid)
    invalid=copy.deepcopy(registry);invalid['components'][1]['extensions']={'no_namespace':True}
    negative_json('non-namespaced-metadata','component-registry.schema.json',invalid)
    invalid=copy.deepcopy(registry);invalid['components'][0]['state_ownership'][0].pop('name',None)
    negative_json('state-without-name','component-registry.schema.json',invalid)
    invalid=copy.deepcopy(registry);invalid['components'][0]['state_ownership'][0]['kind']='SECRET';invalid['components'][0]['state_ownership'][0]['secret']=False
    negative_json('secret-kind-with-false-flag','component-registry.schema.json',invalid)
    invalid_std=copy.deepcopy(std);invalid_std['rogue_root_key']=True
    negative_json('unified-standard-reject-unknown-field','unified-package-standard.schema.json',invalid_std)
    valid_schema_instance(schemas,'unified-package-standard.schema.json',std)
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
    positive_trace('trace',trace)
    # R11: full lifecycle / optional knowledge negative controls.
    matrix=json.loads((root/'03_LIFECYCLE/lifecycle-matrix.json').read_text(encoding='utf-8'))
    guidance=json.loads((root/'08_KNOWLEDGE/guidance-catalog.json').read_text(encoding='utf-8'))
    sources=json.loads((root/'08_KNOWLEDGE/references/catalog.json').read_text(encoding='utf-8'))
    project=json.loads((root/'07_CONTRACTS/examples/project-lifecycle.example.json').read_text(encoding='utf-8'))
    def negative_lifecycle(name,expected_error,ma=matrix,gu=guidance,rs=sources,pr=project):
        nonlocal count
        count+=1
        flaws=[]
        check_lifecycle_models(ma,gu,rs,pr,std['controls'],flaws)
        if not any(expected_error in f for f in flaws):
            errors.append('negative-test-accepted-invalid:'+name+':expected='+expected_error+':got='+repr(flaws))
    bad=copy.deepcopy(matrix);bad['stages'].pop();negative_lifecycle('missing-lifecycle-phase','lifecycle-stages-not-complete',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][1]['id']=bad['stages'][0]['id'];negative_lifecycle('duplicate-lifecycle-phase','lifecycle-stages-not-complete',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['coverage'].pop('OUTCOME_VALUE');negative_lifecycle('missing-crosscut-concern','lifecycle-horizontal-gap',ma=bad)
    bad=copy.deepcopy(matrix);bad['concerns'][0]['primary_control']='UPS-BAD';negative_lifecycle('unowned-crosscut-concern','lifecycle-unowned-concern',ma=bad)
    bad=copy.deepcopy(matrix);bad['concerns'][0]['reference_ids']=['BAD-REF'];negative_lifecycle('crosscut-reference-invalid','lifecycle-concern-unknown-ref',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['primary_control']='UPS-INVALID';negative_lifecycle('unowned-lifecycle-stage','lifecycle-unowned-stage',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['next_stages']=['NONEXISTENT'];negative_lifecycle('broken-transition','lifecycle-broken-next_stages',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['reference_ids']=['BAD-REF'];negative_lifecycle('orphan-reference','lifecycle-unresolved-reference',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][0]['revisit_stages']=[];negative_lifecycle('missing-revisit','lifecycle-no-feedback-return',ma=bad)
    bad=copy.deepcopy(matrix);bad['stages'][-1]['next_stages']=['ASSESS'];negative_lifecycle('retirement-learning-lost','lifecycle-retirement-not-learned',ma=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['applicability']='REQUIRED';negative_lifecycle('mandatory-advisory-guide','guidance-illegal-mandate',gu=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['avoid_when']='';negative_lifecycle('pattern-without-avoid-when','guidance-missing-tradeoff',gu=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['problem']=bad['guidance'][0]['use_when'];negative_lifecycle('guidance-identical-problem-and-use-when','guidance-identical-problem-and-use-when',gu=bad)
    bad=copy.deepcopy(guidance);bad['guidance'][0]['reference_ids']=['NO-REF'];negative_lifecycle('guidance-missing-source','guidance-unknown-reference',gu=bad)
    bad=copy.deepcopy(project);bad['stages'][0]['evidence_refs']=[];negative_lifecycle('lifecycle-pass-without-evidence','project-stages-pass-no-evidence',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][0]['candidate_identity']='';negative_lifecycle('lifecycle-pass-without-candidate-identity','project-stages-pass-no-evidence',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][0]['acceptance_criteria']='';negative_lifecycle('lifecycle-pass-without-criteria','project-stages-pass-no-evidence',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][-1]['revisit_trigger']='';negative_lifecycle('lifecycle-NA-without-trigger','project-stages-unjustified-N_A',pr=bad)
    bad=copy.deepcopy(project);bad['stages'].pop();negative_lifecycle('project-stage-unclassified','project-stages-coverage-missing-or-duplicate',pr=bad)
    bad=copy.deepcopy(sources);bad['sources'][0]['stages']=['UNKNOWN'];negative_lifecycle('reference-to-bad-stage','reference-unrecognized-stage',rs=bad)
    bad=copy.deepcopy(sources);bad['sources'][0]['reviewed_at']='2099-01-01';negative_lifecycle('reference-review-after-snapshot','reference-reviewed-in-future',rs=bad)
    bad=copy.deepcopy(sources)
    for s in bad['sources']:
        if s['id']=='RADAR': s['stages']=['ASSESS']
    negative_lifecycle('stage-reference-not-in-source-stages','lifecycle-stage-not-in-reference-stages',rs=bad)
    # Positive future evolution: new lifecycle concern is not rejected solely due to count.
    future=copy.deepcopy(matrix)
    future['concerns'].append({'id':'FUTURE_CONCERN','label':'Future governed dimension','primary_control':'UPS-DOC','reference_ids':['ADR']})
    for st in future['stages']: st['coverage']['FUTURE_CONCERN']='CONSIDER'
    future_guidance=copy.deepcopy(guidance)
    future_guidance['guidance'][0]['concern_ids'].append('FUTURE_CONCERN')
    future_project=copy.deepcopy(project)
    future_project['concerns'].append({'concern_id':'FUTURE_CONCERN','applicability':'OPTIONAL','approach':'COMPLY','result':'NOT_EVALUATED','deferred':False,'owner':'future-reviewer','reason':'governed growth','revisit_trigger':'risk update','acceptance_criteria':'','candidate_identity':'','evidence_refs':[]})
    flaws=[];check_lifecycle_models(future,future_guidance,sources,future_project,std['controls'],flaws);count+=1
    if flaws:errors.append('positive-future-concern-rejected:'+repr(flaws))
    valid_schema_instance(schemas,'lifecycle-matrix.schema.json',matrix)
    valid_schema_instance(schemas,'guidance-catalog.schema.json',guidance)
    valid_schema_instance(schemas,'reference-catalog.schema.json',sources)
    bad_ref_date=copy.deepcopy(sources);bad_ref_date['as_of']='not-a-date'
    negative_json('reference-catalog-invalid-date','reference-catalog.schema.json',bad_ref_date)
    bad_ref_url=copy.deepcopy(sources);bad_ref_url['sources'][0]['url']='https://bad url with spaces'
    negative_json('reference-catalog-invalid-url','reference-catalog.schema.json',bad_ref_url)
    valid_schema_instance(schemas,'project-lifecycle.schema.json',project)
    count+=1
    good=[]
    check_lifecycle_models(matrix,guidance,sources,project,std['controls'],good)
    if good:errors.append('positive-lifecycle-rejected:'+repr(good))
    # R12 & R13 cross-recursive coverage and false-positive prevention.
    bad=copy.deepcopy(project);bad['concerns'].pop();negative_lifecycle('project-concern-unclassified','project-concerns-coverage-missing-or-duplicate',pr=bad)
    bad=copy.deepcopy(project);bad['concerns'][1]['concern_id']=bad['concerns'][0]['concern_id'];negative_lifecycle('project-concern-duplicate','project-concerns-coverage-missing-or-duplicate',pr=bad)
    bad=copy.deepcopy(project);bad['concerns'][0]['result']='PASS';bad['concerns'][0]['evidence_refs']=[];negative_lifecycle('project-concern-pass-no-evidence','project-concerns-pass-no-evidence',pr=bad)
    bad=copy.deepcopy(project);bad['concerns'][0]['deferred']=True;bad['concerns'][0]['result']='PASS';negative_lifecycle('project-concern-deferred-cannot-pass','project-concerns-deferred-cannot-pass',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][8]['approach']='ADAPT';bad['stages'][8]['acceptance_criteria']='';negative_lifecycle('project-stage-adapt-without-criteria','project-stages-adapt-without-equivalent-contract',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][5]['applicability']='N_A';bad['stages'][5]['result']='NOT_EVALUATED';bad['stages'][5]['reason']='no code';bad['stages'][5]['revisit_trigger']='later'
    negative_lifecycle('project-active-flag-marked-na','project-stages-flag-na-conflict',pr=bad)
    # COMPACT profile negative and positive tests.
    compact_valid={
        'project_id':'compact-internal-tool',
        'scope':'INTERNAL_MODULE',
        'profile':'COMPACT',
        'escalation_flags':{'public_contract_change':False,'authoritative_data':False,'security_boundary':False,'external_dependency':False},
        'activity_flags':{'code':True,'distribution':False,'supported_operation':False,'compat_or_data_transition':False,'withdrawal':False},
        'exposure_flags':{'human_interaction':False,'personal_or_sensitive_data':False,'dependencies':False,'distribution':False,'operation':False,'material_resource_commitments':False},
        'stages':[
            {'stage_id':sid,'applicability':'REQUIRED','approach':'COMPLY','result':'NOT_EVALUATED','deferred':False,'owner':'dev','reason':'compact baseline','revisit_trigger':'scope change','acceptance_criteria':'pass checks','candidate_identity':'','evidence_refs':[]}
            for sid in ('SPECIFY','DESIGN','IMPLEMENT','VERIFY')
        ],
        'concerns':[
            {'concern_id':cid,'applicability':'REQUIRED','approach':'COMPLY','result':'NOT_EVALUATED','deferred':False,'owner':'dev','reason':'compact baseline','revisit_trigger':'scope change','acceptance_criteria':'pass checks','candidate_identity':'','evidence_refs':[]}
            for cid in ('OUTCOME_VALUE','RISK_SECURITY','QUALITY_ASSURANCE','GOVERNANCE_EVIDENCE')
        ],
        'cell_overrides':[]
    }
    valid_schema_instance(schemas,'project-lifecycle.schema.json',compact_valid)
    flaws=[];check_project_lifecycle(compact_valid,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix);count+=1
    if flaws:errors.append('positive-compact-lifecycle-rejected:'+repr(flaws))
    compact_explicit_na=copy.deepcopy(compact_valid)
    compact_explicit_na['stages'].append({'stage_id':'RETIRE','applicability':'N_A','approach':'COMPLY','result':'NOT_EVALUATED','deferred':False,'owner':'dev','reason':'not retiring internal module','revisit_trigger':'when module is scheduled for sunset','acceptance_criteria':'','candidate_identity':'','evidence_refs':[]})
    valid_schema_instance(schemas,'project-lifecycle.schema.json',compact_explicit_na)
    flaws=[];check_project_lifecycle(compact_explicit_na,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix);count+=1
    if flaws:errors.append('positive-compact-explicit-na-rejected:'+repr(flaws))
    bad_compact_na_flag=copy.deepcopy(compact_explicit_na)
    bad_compact_na_flag['activity_flags']['withdrawal']=True
    negative_lifecycle('compact-active-withdrawal-flag-marked-na','project-stages-flag-na-conflict',pr=bad_compact_na_flag)
    bad_compact=copy.deepcopy(compact_valid);bad_compact['escalation_flags']['security_boundary']=True
    negative_lifecycle('compact-with-escalation-flag','project-compact-forbidden-by-escalation-flag',pr=bad_compact)
    bad_compact2=copy.deepcopy(compact_valid);bad_compact2['stages']=[x for x in bad_compact2['stages'] if x['stage_id']!='IMPLEMENT']
    negative_lifecycle('compact-missing-activity-flag-stage','project-stages-coverage-missing-or-duplicate',pr=bad_compact2)
    bad_compact3=copy.deepcopy(compact_valid);bad_compact3['exposure_flags']['human_interaction']=True
    negative_lifecycle('compact-missing-exposure-flag-concern','project-concerns-coverage-missing-or-duplicate',pr=bad_compact3)
    bad=copy.deepcopy(project);bad['cell_overrides']=[{'stage_id':'BAD','concern_id':'OUTCOME_VALUE','applicability':'N_A','approach':'COMPLY','result':'NOT_EVALUATED','deferred':False,'owner':'review','reason':'x','revisit_trigger':'x','acceptance_criteria':'','candidate_identity':'','evidence_refs':[]}]
    negative_lifecycle('cell-override-bad-coordinate','project-cell-unknown-coordinate',pr=bad)
    bad=copy.deepcopy(project);record={'stage_id':'DISCOVER','concern_id':'OUTCOME_VALUE','applicability':'N_A','approach':'COMPLY','result':'NOT_EVALUATED','deferred':False,'owner':'review','reason':'x','revisit_trigger':'x','acceptance_criteria':'','candidate_identity':'','evidence_refs':[]};bad['cell_overrides']=[record,copy.deepcopy(record)]
    negative_lifecycle('cell-override-duplicate','project-cell-duplicate',pr=bad)
    bad=copy.deepcopy(project);bad['cell_overrides']=[{'stage_id':'DISCOVER','concern_id':'OUTCOME_VALUE','applicability':'REQUIRED','approach':'COMPLY','result':'PASS','deferred':False,'owner':'review','reason':'','revisit_trigger':'','acceptance_criteria':'','candidate_identity':'','evidence_refs':[]}]
    negative_lifecycle('cell-override-false-pass','project-cell-pass-no-evidence',pr=bad)
    bad=copy.deepcopy(trace)
    bad['requirements'].append({'id':'REQ-2','scope':'BASE','owner':'engineering','acceptance':'a second independent acceptance'})
    bad['feedback'][0]['requirement_ids'].append('REQ-2')
    negative_trace('feedback-partially-covered-requirement',bad,'feedback-accepted-requirement-untested')
    bad=copy.deepcopy(trace)
    second=copy.deepcopy(bad['gates'][0]);second['gate_id']='GATE-2';second['artifact_digest']='sha256:'+'b'*64
    bad['gates'].append(second);bad['feedback'][0]['closure_gate_ids'].append('GATE-2')
    negative_trace('feedback-mixed-gate-artifact',bad,'feedback-mixed-gate-artifact-digests')
    bad=copy.deepcopy(trace)
    bad['feedback'][0]['history'].append({'event':'REOPEN','at':'2026-10-16T02:00:00Z','actor':'lead','reason':'regression','decision_ref':'decision:reopen-1','prior_closure_evidence_ref':'REL-3'})
    negative_trace('feedback-reopen-still-closed',bad,'feedback-history-state-mismatch')
    bad=copy.deepcopy(trace)
    bad['feedback'][0]['status']='OPEN';bad['feedback'][0]['next_action']='fix regression'
    bad['feedback'][0]['history'].append({'event':'REOPEN','at':'2026-10-16T02:00:00Z','actor':'lead','reason':'regression'})
    negative_json('feedback-reopen-without-prior-evidence','project-trace.schema.json',bad)
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
    bad=copy.deepcopy(registry);bad['components'][0]['id']=bad['components'][1]['id'];flaws=[];check_project_registry(bad,flaws);count+=1
    if not any('duplicate-component-id' in x for x in flaws):errors.append('negative-test-accepted-invalid:duplicate-component')
    # Positive project 12+10+cell override.
    good=copy.deepcopy(project)
    good['cell_overrides']=[{'stage_id':'DISCOVER','concern_id':'RISK_SECURITY','applicability':'REQUIRED','approach':'COMPLY','result':'NOT_EVALUATED','deferred':True,'owner':'review','reason':'requires threat model','revisit_trigger':'before DESIGN exit','acceptance_criteria':'threat model ratified','candidate_identity':'','evidence_refs':[]}]
    flaws=[];check_project_lifecycle(good,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix);count+=1
    if flaws: errors.append('positive-project-cell-override-rejected:'+repr(flaws))
    from validate_package import check_vocabularies
    for key in ('planes','component_classes','boundary_roles','state_kinds','recovery_classes','maturity','distribution','applicability','approach','assessment_results','feedback_dispositions','feedback_statuses','feedback_events','legacy_feature_strategies','exit_semantics','value_semantics'):
        bad=copy.deepcopy(std);bad[key]=['BOGUS'];flaws=[];count+=1
        check_vocabularies(bad,schemas,flaws)
        if not any('vocabulary-drift' in x for x in flaws): errors.append('negative-test-accepted-invalid:vocabulary:'+key)
    for key in ('claim_kinds','claim_results'):
        bad=copy.deepcopy(std);bad['outcome_contract'][key]=['BOGUS'];flaws=[];count+=1
        check_vocabularies(bad,schemas,flaws)
        if not flaws: errors.append('negative-test-accepted-invalid:vocabulary:'+key)
    bad=copy.deepcopy(schemas);bad['component-registry.schema.json']['properties']['components']['items']['properties']['component_class']['enum']=['BOGUS']
    flaws=[];check_vocabularies(std,bad,flaws);count+=1
    if not flaws: errors.append('negative-test-accepted-invalid:schema-vocabulary-drift')
    bad=copy.deepcopy(guidance);bad['guidance'][0]['stage_ids'].append('IMPLEMENT')
    negative_lifecycle('guidance-stage-unsupported-by-sources','guidance-stage-not-in-sources',gu=bad)
    bad=copy.deepcopy(invariant_index);bad['invariants'][0]['standard_ref']='04_ASSURANCE/TDD_TRACEABILITY.md'
    flaws=[];check_invariants(root,std,bad,flaws);count+=1
    if not any('invariant-nonauthoritative-home' in x for x in flaws): errors.append('negative-test-accepted-invalid:invariant-guide-home')
    from validate_package import check_maturity, check_choice
    proof=registry['components'][0]['verification']
    for field in ('candidate_identity','artifact_digest','verified_at','required_gate_ids','gates'):
        bad=copy.deepcopy(registry);bad['components'][0]['verification'].pop(field)
        negative_json('verified-component-missing-'+field,'component-registry.schema.json',bad)
    for field,value in (('candidate_identity','wrong'),('artifact_digest','wrong'),('status','FAIL'),('freshness','STALE'),('evidence_refs',[])):
        bad=copy.deepcopy(proof);bad['gates'][0][field]=value;flaws=[];check_maturity(bad,flaws);count+=1
        if not any('maturity-invalid-gate' in x for x in flaws): errors.append('negative-test-accepted-invalid:verified-gate-'+field)
    bad=copy.deepcopy(proof);bad['verified_at']='2026-10-15T00:00:00Z';flaws=[];check_maturity(bad,flaws);count+=1
    if not any('maturity-verified-before-gate' in x for x in flaws): errors.append('negative-test-accepted-invalid:verified-before-gate')
    for field in ('decision_ref','approved_by','mechanism','evidence_refs'):
        bad=copy.deepcopy(registry);bad['components'][0]['state_ownership'][0]['recovery_alternative'].pop(field)
        negative_json('recovery-alternative-without-'+field,'component-registry.schema.json',bad)
    for field in ('decision_owner','rollback_plan','project_id','feedback_id','reason'):
        bad=copy.deepcopy(example_choice);bad.pop(field,None)
        negative_json('adopt-without-'+field,'implementation-choice.schema.json',bad)
    bad=copy.deepcopy(example_choice);bad['decision_owner']='   ';negative_json('adopt-blank-owner','implementation-choice.schema.json',bad)
    bad=copy.deepcopy(example_choice);bad['feedback_id']='unknown';flaws=[];check_choice(bad,trace,flaws);count+=1
    if not flaws: errors.append('negative-test-accepted-invalid:adopt-unresolved-feedback')
    bad=copy.deepcopy(trace);bad['objective']['success_measures'][0]['baseline_evidence_refs']=[]
    negative_json('measured-empty-baseline','project-trace.schema.json',bad)
    negative_trace('measured-empty-baseline-semantic',bad,'measured-baseline-without-evidence')
    for name,field,value in (('mutation-contract','retry','BLIND_RETRY'),('mutation-contract','uncertain_execution','RETRY'),('protocol-adapter','identity_mapping','TRANSPORT_IS_DOMAIN'),('protocol-adapter','storage_access','PRIVATE_STORAGE')):
        bad=json.loads((root/('07_CONTRACTS/examples/'+name+'.example.json')).read_text(encoding='utf-8'));bad[field]=value
        negative_json(name+'-'+field,name+'.schema.json',bad)
    bad=copy.deepcopy(trace);bad['standard_version']='1.8.0';negative_json('stale-contract-version','project-trace.schema.json',bad)
    for section,field,value,expected in (
        ('tests','candidate_identity','wrong','feedback-test-candidate-mismatch'),
        ('tests','artifact_digest','wrong','feedback-test-candidate-mismatch'),
        ('tests','observed_at','2026-10-16T02:00:00Z','feedback-test-after-gate'),
        ('changes','candidate_identity','wrong','release-invalid-change'),
        ('changes','artifact_digest','wrong','release-invalid-change'),
        ('changes','artifact_refs',[],'release-invalid-change')):
        bad=copy.deepcopy(trace);bad[section][0][field]=value;negative_trace(section+'-'+field,bad,expected)
    for field in ('candidate_identity','artifact_digest'):
        bad=copy.deepcopy(trace);bad['releases'][-1]['deployment'][field]='wrong'
        negative_trace('deployment-'+field,bad,'release-invalid-deployment')
    bad=copy.deepcopy(trace);bad['feedback'][0]['release_evidence_ref']='unresolved'
    negative_trace('unresolved-release',bad,'feedback-unresolved-release')
    bad=copy.deepcopy(trace);bad['releases'][-1]['deployment']['deployed_at']='2026-10-16T00:05:00Z'
    negative_trace('deployment-before-gate',bad,'release-gate-order')
    bad=copy.deepcopy(trace);bad['observations'][1]['observed_at']='2026-10-16T00:20:00Z'
    negative_trace('outcome-before-deployment',bad,'feedback-outcome-before-deployment')
    for target in ('NOT_PUBLISHED','CANDIDATE','PUBLISHED'):
        bad=copy.deepcopy(trace);bad['releases'][-1]['to']=target
        negative_trace('forbidden-distribution-'+target,bad,'distribution-invalid-transition')
    bad=copy.deepcopy(trace);bad['releases'][-1]['from']='CANDIDATE'
    negative_trace('distribution-history-gap',bad,'distribution-invalid-transition')
    bad=copy.deepcopy(trace);bad['releases'][-1]['gate_ids']=[]
    negative_trace('promotion-no-gates',bad,'distribution-promotion-without-gates')
    bad=copy.deepcopy(trace);bad['releases'][-1]['to']='WITHDRAWN'
    negative_trace('withdrawal-without-obligations',bad,'distribution-withdrawal-without-obligations')
    bad=copy.deepcopy(trace);bad['releases'][-1]['artifact_digest']='wrong'
    negative_trace('replacement-bytes-same-candidate',bad,'distribution-candidate-artifact-changed')
    bad=copy.deepcopy(trace);bad['tests'][0].pop('candidate_identity')
    negative_json('passed-proof-without-candidate','project-trace.schema.json',bad)
    from validate_package import check_history
    bad=copy.deepcopy(trace);bad['feedback'][0]['history']=[]
    negative_trace('closed-history-deleted',bad,'feedback-history-state-mismatch')
    bad=copy.deepcopy(trace);bad['feedback'][0]['status']='OPEN';bad['feedback'][0]['next_action']='repair'
    negative_trace('open-trailing-close',bad,'feedback-history-state-mismatch')
    bad=copy.deepcopy(trace);bad['feedback'][0]['history'][0]['at']='2026-10-15T00:00:00Z'
    negative_trace('close-before-measurement',bad,'feedback-close-before-outcome')
    bad=copy.deepcopy(trace);bad['feedback'][0]['history'].append({'event':'REOPEN','at':'2026-10-15T00:00:00Z','actor':'owner','reason':'regression','decision_ref':'reopen','prior_closure_evidence_ref':'REL-3'})
    negative_trace('history-not-chronological',bad,'feedback-history-out-of-order')
    bad=copy.deepcopy(trace);later=copy.deepcopy(bad['observations'][1]);later.update(id='OBS-LATER',observed_at='2026-10-16T02:00:00Z',evaluation='MISSES_TARGET');bad['observations'].append(later)
    negative_trace('regression-closed',bad,'feedback-contradictory-outcome-not-reopened')
    bad['feedback'][0]['decision_ref']='generic-risk-acceptance'
    negative_trace('generic-decision-cannot-waive-regression',bad,'feedback-contradictory-outcome-not-reopened')
    reopened=copy.deepcopy(bad);fb=reopened['feedback'][0];fb.update(status='OPEN',next_action='Investigate OBS-LATER',decision_ref='decision:regression');fb['history'].append({'event':'REOPEN','at':'2026-10-16T02:10:00Z','actor':'owner','reason':'new target miss','decision_ref':'decision:regression','prior_closure_evidence_ref':'REL-3','observation_ids':['OBS-LATER']})
    positive_trace('reopen',reopened,trace)
    accepted=copy.deepcopy(reopened);fb=accepted['feedback'][0];fb.update(status='CLOSED',outcome_decision='EXCEPTION_ACCEPTED',outcome_observation_id='OBS-EXCEPTION')
    accepted['observations'].append({**accepted['observations'][1], 'id':'OBS-EXCEPTION', 'evaluation':'EXCEPTION_ACCEPTED', 'observed_at':'2026-10-16T02:15:00Z'})
    fb['history'].append({'event':'CLOSE','at':'2026-10-16T02:20:00Z','actor':'owner','reason':'Explicitly accept measured regression risk','decision_ref':'decision:accept-regression','closure_evidence_ref':'REL-3','observation_ids':['OBS-LATER']})
    positive_trace('specific-regression-decision',accepted,reopened)
    bad=copy.deepcopy(trace);bad['feedback'][0]['history'][0]['reason']='rewritten';flaws=[];check_trace(bad,flaws,trace);count+=1
    if not any('feedback-history-rewritten' in x for x in flaws): errors.append('negative-test-accepted-invalid:history-prefix')
    bad=copy.deepcopy(trace);bad['releases'].pop();flaws=[];check_trace(bad,flaws,trace);count+=1
    if not any('trace-prior-evidence-rewritten' in x for x in flaws): errors.append('negative-test-accepted-invalid:prior-release-deleted')
    for section in ('stages','concerns'):
        bad=copy.deepcopy(project);bad[section][0]['result']='PASS';bad[section][0]['revisit_trigger']=''
        negative_lifecycle(section+'-pass-no-revisit','project-'+section+'-pass-without-revisit',pr=bad)
    bad=copy.deepcopy(project);bad['cell_overrides']=[{**bad['stages'][0],'concern_id':'OUTCOME_VALUE'}];bad['cell_overrides'][0]['revisit_trigger']=''
    negative_lifecycle('cell-pass-no-revisit','project-cell-pass-without-revisit',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][0]['result']='FAIL'
    negative_lifecycle('failed-stage-no-open-action','project-trigger-without-open-feedback',pr=bad)
    bad=copy.deepcopy(project);bad['stages'][0]['trigger_observation_ids']=['OBS-LATER']
    negative_lifecycle('recorded-trigger-no-action','project-trigger-without-open-feedback',pr=bad)
    for field,value,expected in (
        ('product_gate_obligations',['missing-gate'],'scoped-unresolved-obligation'),
        ('control_ids',['UPS-MISSING'],'scoped-unknown-control'),
        ('owner','   ','scoped-requirement-no-owner'),
        ('invariant_ids',['missing-invariant'],'scoped-unknown-invariant'),
        ('stage_id','MISSING','scoped-unknown-coordinate')):
        bad=copy.deepcopy(trace);bad['requirements'][0][field]=value
        negative_trace('scope-'+field,bad,expected)
    bad=copy.deepcopy(trace);r=copy.deepcopy(bad['requirements'][0]);r['id']='REQ-UNCOVERED';bad['requirements'].append(r)
    negative_trace('accepted-scoped-requirement-untested',bad,'scoped-accepted-requirement-untested')
    pending=copy.deepcopy(trace);pending['feedback']=[];pending['observations']=[];pending['releases']=[];pending['requirements'][0].update(result='NOT_EVALUATED',pending_decision_ref='decision:pending-proof');pending['tests'][0]['status']='NOT_RUN';pending['gates'][0]['status']='PENDING'
    positive_trace('pending-scoped-requirement',pending)
    bad=copy.deepcopy(pending);bad['requirements'][0].pop('pending_decision_ref');negative_trace('pending-requirement-without-decision',bad,'scoped-pending-without-decision')
    bad=copy.deepcopy(trace);bad['requirements'][0]['invariant_ids']=['core_must_not_depend_on_optional_extensions']
    negative_trace('catalog-obligation-unresolved',bad,'scoped-unresolved-obligation')
    bad=copy.deepcopy(trace);bad['tests'][0]['status']='FAIL';negative_trace('scoped-proof-fails',bad,'scoped-obligation-not-passing')
    bad=copy.deepcopy(registry);bad['project_id']='other';flaws=[];check_project_registry(bad,flaws,trace);count+=1
    if not any('owner-association-invalid' in x for x in flaws): errors.append('negative-test-accepted-invalid:registry-project-association')
    bad=copy.deepcopy(trace);bad['objective']['owner']='   ';flaws=[];check_project_registry(registry,flaws,bad);count+=1
    if not any('owner-association-invalid' in x for x in flaws): errors.append('negative-test-accepted-invalid:registry-inherited-owner')
    bad=copy.deepcopy(trace);bad['tests'][0]['candidate_identity']='wrong';flaws=[];check_project_registry(registry,flaws,bad);count+=1
    if not any('scoped-accepted-requirement-untested' in x for x in flaws): errors.append('negative-test-accepted-invalid:registry-scoped-verification')
    interaction=copy.deepcopy(trace);interaction['requirements'][0].update(stage_id='VERIFY',concern_id='QUALITY_ASSURANCE')
    positive_trace('selected-interaction',interaction)
    bad=copy.deepcopy(interaction);bad['requirements'][0]['product_gate_obligations']=[]
    negative_trace('selected-interaction-no-proof',bad,'scoped-without-proof-obligation')
    bad=copy.deepcopy(trace);bad['gates'][0]['artifact_digest']='other'
    negative_trace('scoped-mixed-proof-artifact',bad,'scoped-mixed-proof-artifacts')
    bad=copy.deepcopy(project);bad['stages'][0]['result']='FAIL'
    negative_lifecycle('lifecycle-failure-without-observation','project-failure-without-observation',pr=bad)
    bad=copy.deepcopy(registry);bad['components'][0].pop('verification')
    negative_json('VERIFIED-without-verification','component-registry.schema.json',bad)
    flaws=[];check_project_registry(bad,flaws);count+=1
    if not any('project-registry-unverified-component' in x for x in flaws): errors.append('negative-test-accepted-invalid:verified-component-no-proof')
    bad=copy.deepcopy(registry);bad['components'][0]['state_ownership'][0].pop('recovery_alternative')
    negative_json('excluded-authority-without-alternative','component-registry.schema.json',bad)
    bad=copy.deepcopy(trace);bad['objective']['success_measures'][0].pop('baseline_evidence_refs')
    negative_json('measured-missing-baseline','project-trace.schema.json',bad)
    bad=copy.deepcopy(example_choice);bad['rollback_plan']='   '
    negative_json('adopt-blank-rollback','implementation-choice.schema.json',bad)
    triggered=copy.deepcopy(project);triggered['project_id']=reopened['project_id']
    triggered['stages'][0].update(result='FAIL',feedback_ids=['FB-1'],trigger_observation_ids=['OBS-LATER'])
    flaws=[];check_project_lifecycle(triggered,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix,trace=reopened);count+=1
    if flaws: errors.append('positive-triggered-reentry-rejected:'+repr(flaws))
    bad=copy.deepcopy(triggered);bad['stages'][0]['trigger_observation_ids']=['UNADDRESSED']
    flaws=[];check_project_lifecycle(bad,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix,trace=reopened);count+=1
    if not any('project-trigger-observation-unaddressed' in x for x in flaws): errors.append('negative-test-accepted-invalid:unaddressed-lifecycle-trigger')
    bad=copy.deepcopy(trace);collision=copy.deepcopy(bad['tests'][0]);collision['id']='GATE-1';bad['tests'].append(collision)
    negative_trace('ambiguous-proof-obligation',bad,'scoped-ambiguous-obligation')
    bad=copy.deepcopy(trace);bad['releases'][0].pop('scope')
    negative_json('candidate-without-intended-scope','project-trace.schema.json',bad)
    bad=copy.deepcopy(trace);bad['releases'][-1]['scope']='OTHER'
    negative_trace('distribution-scope-changed',bad,'distribution-scope-changed')
    bad=copy.deepcopy(trace);bad['feedback']=[];bad['observations']=[];bad['requirements'][0]['result']='NOT_EVALUATED';bad['tests'][0]['status']='NOT_RUN'
    negative_trace('promoted-scope-without-proof',bad,'scoped-accepted-requirement-untested')
    bad=copy.deepcopy(trace);second=copy.deepcopy(bad['gates'][0]);second['gate_id']='REQUIRED-2';bad['gates'].append(second);bad['requirements'][0]['product_gate_obligations'].append('REQUIRED-2')
    negative_trace('promotion-omits-required-gate',bad,'scoped-release-missing-obligation')
    selected=copy.deepcopy(project);selected['project_id']=interaction['project_id'];selected['cell_overrides']=[{**selected['stages'][0],'stage_id':'VERIFY','concern_id':'QUALITY_ASSURANCE','candidate_identity':trace['gates'][0]['candidate_identity']}]
    flaws=[];check_project_lifecycle(selected,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix,trace=interaction);count+=1
    if flaws: errors.append('positive-selected-cell-proof-rejected:'+repr(flaws))
    flaws=[];check_project_lifecycle(selected,{x['id'] for x in matrix['stages']},{x['id'] for x in matrix['concerns']},flaws,matrix=matrix,trace=trace);count+=1
    if not any('project-cell-pass-without-scoped-proof' in x for x in flaws): errors.append('negative-test-accepted-invalid:selected-cell-unbound')
    bad=copy.deepcopy(trace)
    for release in bad['releases']: release['scope']='UNOWNED'
    negative_trace('promotion-unowned-scope',bad,'distribution-promotion-unowned-scope')
    # R14 review: isolate candidate obligations and bind every executed proof at acceptance.
    multiple=copy.deepcopy(trace)
    replacements={'source:candidate-B':'source:candidate-C','REQ-1':'REQ-C','TEST-1':'TEST-C','GATE-1':'GATE-C',
                  'CHANGE-1':'CHANGE-C','REL-1':'REL-C1','REL-2':'REL-C2','REL-3':'REL-C3'}
    def renamed(value):
        if isinstance(value, dict): return {k:renamed(v) for k,v in value.items()}
        if isinstance(value, list): return [renamed(v) for v in value]
        return replacements.get(value,value) if isinstance(value,str) else value
    for section in ('requirements','tests','gates','changes','releases'):
        multiple[section].extend(renamed(trace[section]))
    positive_trace('two-candidates-same-scope',multiple,trace)
    bad=copy.deepcopy(multiple);bad['requirements'][-1]['product_gate_obligations']=['TEST-1','GATE-1']
    negative_trace('candidate-borrows-older-proof',bad,'scoped-obligation-not-passing')
    scoped=copy.deepcopy(trace);scoped['feedback']=[];scoped['observations']=[]
    scoped['requirements'][0]['product_gate_obligations']=['TEST-1']
    positive_trace('test-only-scoped-proof',scoped)
    for field,value in (('artifact_digest','sha256:'+'b'*64),('observed_at','2026-10-16T01:00:00Z')):
        bad=copy.deepcopy(scoped);bad['tests'][0][field]=value
        negative_trace('scoped-executed-proof-'+field,bad,'scoped-proof-artifact-or-order')
    for template,name in ((trace,'scoped-test-after-gate'),(scoped,'scoped-test-only-after-release-gate')):
        bad=copy.deepcopy(template);bad['feedback']=[];bad['observations']=[];bad['tests'][0]['observed_at']='2026-10-16T00:11:00Z'
        negative_trace(name,bad,'scoped-proof-artifact-or-order')
    flaws=[];check_project_registry(registry,flaws,multiple);count+=1
    if flaws: errors.append('positive-registry-two-candidates-rejected:'+repr(flaws))
    for field,value,expected in (('status','PENDING','scoped-obligation-not-passing'),
                                 ('artifact_digest','sha256:'+'b'*64,'maturity-invalid-gate'),
                                 ('observed_at','2026-10-16T00:11:00Z','maturity-verified-before-gate')):
        bad=copy.deepcopy(trace);bad['gates'][0][field]=value;flaws=[];check_project_registry(registry,flaws,bad);count+=1
        if not any(expected in x for x in flaws): errors.append('negative-test-accepted-invalid:registry-trace-gate-'+field)
    bad=copy.deepcopy(trace);bad['requirements'][0].update(result='NOT_EVALUATED',pending_decision_ref='decision:pending');flaws=[];check_project_registry(registry,flaws,bad);count+=1
    if not any('verified-scope-not-passing' in x for x in flaws): errors.append('negative-test-accepted-invalid:registry-pending-requirement')
    bad=copy.deepcopy(trace);bad['feedback'][0]['requirement_ids']=['MISSING-REQ'];flaws=[];check_choice(example_choice,bad,flaws);count+=1
    if not any('adoption-unresolved-requirement' in x for x in flaws): errors.append('negative-test-accepted-invalid:adopt-unresolved-requirement')
    adoption=copy.deepcopy(pending);adoption['observations']=[copy.deepcopy(trace['observations'][0])]
    adoption['feedback']=[copy.deepcopy(trace['feedback'][0])];adoption['feedback'][0].update(status='IN_PROGRESS',history=[],next_action='Implement and measure')
    positive_trace('pending-adoption',adoption)
    flaws=[];check_choice(example_choice,adoption,flaws);count+=1
    if flaws: errors.append('positive-adopt-pending-requirement-rejected:'+repr(flaws))
    withdrawn=copy.deepcopy(trace);withdrawn['releases'].append({**trace['releases'][-1], 'id':'REL-W', 'from':'PROMOTED', 'to':'WITHDRAWN',
        'released_at':'2026-10-16T02:00:00Z','decision_ref':'decision:withdrawal', 'reason':'Invalid artifact', 'notice_ref':'notice:withdrawal','recovery_obligations':'Restore prior artifact'})
    negative_trace('withdrawal-leaves-closed-feedback',withdrawn,'feedback-withdrawal-not-addressed')
    decision=copy.deepcopy(withdrawn);decision['feedback'][0]['history'][0].update(at='2026-10-16T02:10:00Z',decision_ref='unrelated')
    negative_trace('unrelated-decision-after-withdrawal',decision,'feedback-withdrawal-not-addressed')
    reopened_withdrawal=copy.deepcopy(withdrawn);fb=reopened_withdrawal['feedback'][0];fb.update(status='IN_PROGRESS',next_action='Restore prior artifact',decision_ref='decision:withdrawal')
    fb['history'].append({'event':'REOPEN','at':'2026-10-16T02:10:00Z','actor':'owner','reason':'Withdrawal REL-W', 'decision_ref':'decision:withdrawal','prior_closure_evidence_ref':'REL-3'})
    positive_trace('withdrawal-reopen-in-progress',reopened_withdrawal,trace)
    decision=copy.deepcopy(reopened_withdrawal);fb=decision['feedback'][0];fb['status']='CLOSED'
    fb['history'].append({'event':'CLOSE','at':'2026-10-16T02:20:00Z','actor':'owner','reason':'Withdrawal decision explicitly accepts this feedback outcome despite REL-W', 'decision_ref':'decision:withdrawal','closure_evidence_ref':'REL-3'})
    positive_trace('withdrawal-specific-decision',decision,reopened_withdrawal)
    retained=copy.deepcopy(decision);history=retained['feedback'][0]['history']
    history.extend([{**history[-2], 'at':'2026-10-16T02:30:00Z', 'decision_ref':'decision:followup'},
                    {**history[-1], 'at':'2026-10-16T02:40:00Z', 'decision_ref':'decision:followup'}])
    positive_trace('withdrawal-decision-retained',retained,decision)
    for section in ('tests','gates'):
        for mutation in ('rewrite','delete'):
            bad=copy.deepcopy(trace)
            if mutation=='rewrite': bad[section][0]['evidence_refs']=['replacement:proof']
            else: bad[section]=[]
            flaws=[];check_trace(bad,flaws,trace);count+=1
            if not any('trace-prior-evidence-rewritten:'+section in x for x in flaws): errors.append('negative-test-accepted-invalid:prior-'+section+'-'+mutation)
    positive_trace('pending-proof-can-complete',trace,pending)
    bad=copy.deepcopy(trace);bad['changes'][0]['owner']='   '
    negative_json('trace-shared-nonblank','project-trace.schema.json',bad)
    bad=copy.deepcopy(trace);bad['changes'][0]['evidence_refs']=['proof','proof']
    negative_json('trace-shared-unique-references','project-trace.schema.json',bad)
    stats = {'executed': 0, 'skipped': 0, 'n_a': 0}
    if include_fs:
        stats, fs_errors = run_filesystem_fixtures()
        errors.extend(fs_errors)
        count += stats['executed']
    else:
        stats.update(skipped=5 if os.name == 'nt' else 4, n_a=0 if os.name == 'nt' else 1)
    if fs_report is not None: fs_report.update(stats)
    errors.extend(filesystem_gate_errors(stats, require_fs_tests))
    for skipped,required,expected in ((1,True,True),(0,True,False),(1,False,False)):
        count+=1
        if bool(filesystem_gate_errors({'skipped':skipped},required)) != expected:
            errors.append('negative-test-accepted-invalid:filesystem-required-accounting')
    from validate_package import check_package_trace, PACKAGE_TRACE
    actual=json.loads((root/PACKAGE_TRACE).read_text(encoding='utf-8'))
    valid_schema_instance(schemas,'project-trace.schema.json',actual)
    flaws=[];check_package_trace(root,actual,flaws);count+=1
    if flaws: errors.append('positive-package-trace-rejected:'+repr(flaws))
    for mutation,expected in (('example','package-trace-not-actual-work'),('missing-artifact','package-change-artifact-missing'),('unsafe-artifact','package-change-artifact-unsafe'),('empty-feedback','package-trace-not-actual-work')):
        bad=copy.deepcopy(actual)
        if mutation=='example': bad['project_id']='example-project'
        if mutation=='missing-artifact': bad['changes'][0]['artifact_refs']=['nonexistent-package-file']
        if mutation=='unsafe-artifact': bad['changes'][0]['artifact_refs']=['../outside']
        if mutation=='empty-feedback': bad['feedback']=[]
        flaws=[];check_package_trace(root,bad,flaws);count+=1
        if not any(expected in x for x in flaws): errors.append('negative-test-accepted-invalid:actual-package-'+mutation)
    bad=copy.deepcopy(actual);bad['feedback'][0]['status']='CLOSED'
    negative_json('package-closure-without-deployment-and-outcome','project-trace.schema.json',bad)
    return count,errors


def filesystem_gate_errors(stats, required):
    return ['required-filesystem-fixtures-skipped:' + str(stats['skipped'])] if required and stats['skipped'] else []


def run_filesystem_fixtures():
    """Five defenses; unavailable execution never increments the executed count."""
    from validate_package import resolve_safe_evidence_path
    stats = {'executed': 0, 'skipped': 0, 'n_a': 0}
    errors = []
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            val = root / '.validation'
            val.mkdir()
            canon = root / 'MANIFEST.json'; canon.write_text('{}', encoding='utf-8')
            inp = val / 'input.json'; inp.write_text('{}', encoding='utf-8')
            other = val / 'other.txt'; other.write_text('x', encoding='utf-8')
            fixtures = [
                ('canonical-alias', canon, 'alias canonical file', ()),
                ('input-alias', inp, 'alias input file identity', (str(inp),)),
                ('hardlink-count', other, 'st_nlink > 1', ()),
                ('symlink', canon, 'symlink or junction', ()),
                ('junction', root, 'symlink or junction', ()),
            ]
            for name, source, expected, inputs in fixtures:
                target = val / name
                if name == 'junction' and os.name != 'nt':
                    stats['n_a'] += 1
                    continue
                try:
                    if name == 'symlink': target.symlink_to(source)
                    elif name == 'junction':
                        result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(target), str(source)], capture_output=True)
                        if result.returncode: raise OSError('junction creation failed')
                    else: os.link(source, target)
                except OSError as exc:
                    # Windows without symlink privilege uses the separately required junction defense.
                    if name == 'symlink' and os.name == 'nt' and getattr(exc, 'winerror', None) == 1314:
                        stats['n_a'] += 1
                    else: stats['skipped'] += 1
                    continue
                stats['executed'] += 1
                rel = '.validation/' + name + ('/MANIFEST.json' if name == 'junction' else '')
                try:
                    resolve_safe_evidence_path(rel, root=root, input_paths=inputs)
                    errors.append('negative-test-accepted-invalid:' + name)
                except ValueError as exc:
                    if expected not in str(exc): errors.append('negative-test-wrong-error:' + name + ':' + str(exc))
                finally:
                    if name == 'junction': os.rmdir(target)
    except OSError as exc:
        remaining = 5 - sum(stats.values())
        stats['skipped'] += remaining
        errors.append('filesystem-fixture-setup-error:' + str(exc))
    return stats, errors


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--no-fs-tests', action='store_true', help='Local only: report filesystem fixtures as skipped')
    mode.add_argument('--require-fs-tests', action='store_true', help='Fail on skipped applicable filesystem fixtures')
    args = parser.parse_args()
    _root = Path(__file__).resolve().parents[1]
    stats = {}
    _count, _errs = run_negative_suite(_root, include_fs=not args.no_fs_tests, require_fs_tests=args.require_fs_tests, fs_report=stats)
    print(f'contract_fixture_checks={_count}')
    for key, value in stats.items(): print('filesystem_' + key + '=' + str(value))
    for _e in _errs: print(f'ERROR={_e}')
    print('NEGATIVE_TESTED=' + ('FAIL' if _errs else 'NOT_EVALUATED' if stats['skipped'] else 'PASS'))
    print('RESULT=' + ('PASS' if not _errs else 'FAIL'))
    sys.exit(0 if not _errs else 1)
