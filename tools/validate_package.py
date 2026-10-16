"""General validation: integrity, JSON-schema, traceability, negative-test harness.

Python 3.8+ and jsonschema >= 4.18. All visible output is mirrored verbatim to evidence.
Pure validation: no writes to canonical package files; evidence written to ignored .validation area.
"""
from pathlib import Path, PurePosixPath
import argparse, copy, hashlib, json, os, re, sys
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
    FormatChecker = None
    _IMPORT_ERROR = str(exc)

ROOT = Path(__file__).resolve().parents[1]
VERSION = json.loads((ROOT / '06_GOVERNANCE/unified-package-standard.json').read_text(encoding='utf-8'))['version']
PACK_NAME = 'VerySimpleGuide'
# MANIFEST.json is explicitly self-excluded from its own file inventory;
# manifest digests detect accidental changes, not cryptographic provenance.
EXCLUDED = {'MANIFEST.json'}


def _is_link_or_reparse(path_obj):
    try:
        st = os.lstat(path_obj)
    except OSError:
        return False
    return path_obj.is_symlink() or getattr(st, 'st_reparse_tag', 0) != 0


def resolve_safe_evidence_path(raw_path, root=ROOT, input_paths=()):
    if raw_path is None:
        return None
    raw_str = str(raw_path).strip()
    if not raw_str:
        raise ValueError('Evidence path cannot be empty')
    norm_segs = raw_str.replace('\\', '/').split('/')
    if '..' in norm_segs:
        raise ValueError('Evidence path cannot contain parent traversal: ' + raw_str)
    p = Path(raw_str)
    root_real = root.resolve(strict=False)
    val_dir = root_real / '.validation'
    if _is_link_or_reparse(val_dir):
        raise ValueError('Evidence directory .validation cannot be a symlink or junction')
    val_real = val_dir.resolve(strict=False)
    candidate = p if p.is_absolute() else (root_real / p)
    # Check candidate and its ancestors up to root_real for symlinks/junctions
    cur = candidate
    while True:
        if _is_link_or_reparse(cur):
            raise ValueError('Evidence path cannot traverse symlink or junction: ' + raw_str)
        if cur == val_real or cur == root_real or cur.parent == cur:
            break
        cur = cur.parent
    target = candidate.resolve(strict=False)
    if val_real not in target.parents:
        raise ValueError('Evidence output must reside strictly inside .validation/: ' + raw_str)
    if target.exists():
        if target.is_dir():
            raise ValueError('Evidence path cannot be a directory: ' + raw_str)
        for canon_rel in file_inventory(root_real) | set(EXCLUDED):
            canon_path = root_real / canon_rel
            if canon_path.exists():
                try:
                    if os.path.samefile(target, canon_path):
                        raise ValueError('Evidence output cannot alias canonical file: ' + canon_rel)
                except OSError:
                    pass
    for inp in input_paths:
        if not inp:
            continue
        inp_p = Path(str(inp))
        inp_abs = (inp_p if inp_p.is_absolute() else (root_real / inp_p)).resolve(strict=False)
        inp_cwd = inp_p.resolve(strict=False)
        if target in (inp_abs, inp_cwd):
            raise ValueError('Evidence output cannot alias input file: ' + str(inp))
        if target.exists():
            for cand_inp in (inp_abs, inp_cwd, inp_p):
                if cand_inp.exists():
                    try:
                        if os.path.samefile(target, cand_inp):
                            raise ValueError('Evidence output cannot alias input file identity: ' + str(inp))
                    except OSError:
                        pass
    if target.exists():
        try:
            st = os.lstat(target)
        except OSError as exc:
            raise ValueError('Cannot stat evidence path: ' + str(exc))
        if getattr(st, 'st_nlink', 1) > 1:
            raise ValueError('Evidence output cannot be a hard-linked file (st_nlink > 1): ' + raw_str)
    return target


class EvidenceSink:
    """stdout single source, persisted byte-for-byte as UTF-8 evidence."""
    def __init__(self, path=None, root=ROOT, input_paths=()):
        self.root = root
        self.input_paths = tuple(input_paths)
        self.path = Path(path) if path else None
        self.target = resolve_safe_evidence_path(self.path, root=self.root, input_paths=self.input_paths) if self.path else None
        self.lines = []
    def say(self, msg):
        line = str(msg)
        print(line)
        self.lines.append(line)
    def close(self):
        if self.path is None:
            return
        target = resolve_safe_evidence_path(self.path, root=self.root, input_paths=self.input_paths)
        target.parent.mkdir(parents=True, exist_ok=True)
        target = resolve_safe_evidence_path(self.path, root=self.root, input_paths=self.input_paths)
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
    if rel.startswith('/') or rel.endswith('/'):
        return False
    raw_parts = rel.split('/')
    if any(seg in ('', '.', '..') for seg in raw_parts):
        return False
    pure = PurePosixPath(rel)
    return not pure.is_absolute() and pure.as_posix() == rel


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


def _collect_schema_formats(obj, out=None):
    if out is None:
        out = set()
    if isinstance(obj, dict):
        fmt = obj.get('format')
        if isinstance(fmt, str):
            out.add(fmt)
        for val in obj.values():
            _collect_schema_formats(val, out)
    elif isinstance(obj, list):
        for item in obj:
            _collect_schema_formats(item, out)
    return out


REQUIRED_FORMAT_CHECKERS = ('date-time', 'date')


def check_format_checkers(errors, checker=None, schemas=None):
    if Draft202012Validator is None or FormatChecker is None:
        errors.append('missing-dependency:jsonschema>=4.18:' + str(_IMPORT_ERROR))
        return False
    fc = checker if checker is not None else FormatChecker()
    required = set(REQUIRED_FORMAT_CHECKERS)
    if schemas:
        for schema_doc in schemas.values():
            required.update(_collect_schema_formats(schema_doc))
    missing = sorted(fmt for fmt in required if fmt not in fc.checkers)
    if missing:
        errors.append(
            'missing-format-checker:' + ','.join(missing)
            + ':install rfc3339-validator (python -m pip install -r tools/requirements-validation.txt)'
        )
        return False
    return True


def load_schemas(root, errors):
    parsed = {}
    if Draft202012Validator is None:
        errors.append('missing-dependency:jsonschema>=4.18:' + str(_IMPORT_ERROR))
        return parsed
    for path in sorted((root / '07_CONTRACTS/schemas').glob('*.schema.json')):
        try:
            schema = read_json(path)
            Draft202012Validator.check_schema(schema)
            expected_id = f"https://example.invalid/verysimple/{path.name[:-len('.schema.json')]}/{VERSION[:3]}"
            if schema.get('$id') != expected_id:
                errors.append('schema-id-mismatch:' + path.name)
            if schema.get('additionalProperties') is not False:
                errors.append('schema-missing-additional-properties-false:' + path.name)
            parsed[path.name] = schema
        except (SchemaError, json.JSONDecodeError, OSError) as exc:
            errors.append('invalid-json-schema:' + path.name + ':' + str(exc)[:200])
    if not parsed:
        errors.append('missing-schemas')
    if not check_format_checkers(errors, schemas=parsed):
        return {}
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
            else:
                target.pop('$schema', None)
                target.pop('$id', None)
            return walk(target)
        return {k: walk(value) for k,value in obj.items()}
    return walk(v)


def valid_schema_instance(schemas, schema_name, instance, checker=None):
    fc = checker if checker is not None else FormatChecker()
    fmt_errors = []
    if not check_format_checkers(fmt_errors, checker=fc, schemas={schema_name: schemas[schema_name]}):
        raise RuntimeError(fmt_errors[0])
    schema = local_refs(schemas[schema_name], schemas)
    for key in ('standard_version', 'version'):
        if key in schema.get('properties', {}): schema['properties'][key] = {'const': VERSION}
    Draft202012Validator(schema, format_checker=fc).validate(instance)


def check_vocabularies(std, schemas, errors):
    """Canonical lists own vocabulary; check every duplicate enum, including schema lists."""
    canonical = schemas['unified-package-standard.schema.json']['properties']
    vocab = {k: v for k, v in std.items() if isinstance(v, list) and v and all(isinstance(x, str) for x in v) and k != 'invariants'}
    vocab.update(std['outcome_contract'])
    vocab['normative_levels'] = std['openness_contract']['normative_levels']
    aliases = {'plane':'planes', 'component_class':'component_classes', 'kind':'state_kinds',
               'recovery_class':'recovery_classes', 'status':'maturity', 'result':'assessment_results',
               'disposition':'feedback_dispositions', 'event':'feedback_events', 'from':'distribution', 'to':'distribution'}
    for key, values in vocab.items():
        if not isinstance(values, list): continue
        props = canonical
        if key.startswith('claim_'): props = canonical['outcome_contract']['properties']
        if key == 'normative_levels': props = canonical['openness_contract']['properties']
        if set(props.get(key, {}).get('items', {}).get('enum', [])) != set(values):
            errors.append('vocabulary-drift:canonical:' + key)
    def walk(obj, name, path=()):
        if not isinstance(obj, dict): return
        for key, value in obj.get('properties', {}).items():
            target = aliases.get(key, key)
            if name == 'project-trace.schema.json' and key == 'status' and 'feedback' in path:
                target = 'feedback_statuses'
            enum = value.get('enum', value.get('items', {}).get('enum'))
            if name == 'project-trace.schema.json' and key in ('status', 'kind') and 'feedback' not in path: continue
            if name == 'standard-evolution.schema.json' and key in ('status', 'kind'): continue
            # Conditional subsets express guards, not vocabulary definitions.
            if enum is not None and target in vocab and 'allOf' not in path and 'if' not in path and 'then' not in path:
                if set(enum) != set(vocab[target]):
                    errors.append('vocabulary-drift:' + name + ':' + '/'.join(path + (key,)))
        for key, value in obj.items():
            if isinstance(value, dict): walk(value, name, path + (key,))
            elif isinstance(value, list):
                for item in value: walk(item, name, path + (key,))
    for name, schema in schemas.items():
        # Gate/test statuses and observation kinds are distinct contracts.
        if name in ('gate-evidence.schema.json',): continue
        walk(schema, name)


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
    roles = {x['path']: x.get('role') for x in read_json(root / 'MANIFEST.json')['files']}
    for row in rows:
        if roles.get(row.get('standard_ref')) not in ('NORMATIVE_SOURCE', 'MACHINE_SSOT'):
            errors.append('invariant-nonauthoritative-home:' + str(row.get('invariant_id')))
        if row.get('primary_control') not in controls:
            errors.append('invariant-orphan-control:' + str(row.get('invariant_id')))
        gate_ob = row.get('product_gate_obligation')
        if not isinstance(gate_ob, str) or not gate_ob or ' ' in gate_ob or gate_ob != gate_ob.lower():
            errors.append('invariant-without-gate-obligation:' + str(row.get('invariant_id')))
        try:
            if not safe_target(root,row.get('standard_ref','')).is_file():
                errors.append('invariant-standard-missing:' + str(row.get('invariant_id')))
        except ValueError:
            errors.append('invariant-unsafe-standard-ref:' + str(row.get('invariant_id')))
        if row.get('assurance_level') != 'DESIGN_COVERED':
            errors.append('invariant-false-product-proof:' + str(row.get('invariant_id')))


def check_maturity(item, errors):
    if item.get('status') != 'VERIFIED': return
    gates = {g.get('gate_id'): g for g in item.get('gates', [])}
    required = item.get('required_gate_ids', [])
    if not required or not item.get('candidate_identity') or not item.get('artifact_digest') or not item.get('verified_at') or not item.get('evidence'):
        errors.append('maturity-without-proof:' + item.get('id', ''))
    for gid in required:
        gate = gates.get(gid, {})
        if (gate.get('status') != 'PASS' or gate.get('freshness') != 'FRESH' or not gate.get('evidence_refs')
            or gate.get('candidate_identity') != item.get('candidate_identity')
            or gate.get('artifact_digest') != item.get('artifact_digest')):
            errors.append('maturity-invalid-gate:' + gid)
        elif datetime_utc(gate['observed_at']) > datetime_utc(item['verified_at']):
            errors.append('maturity-verified-before-gate:' + gid)
    if len(gates) != len(item.get('gates', [])): errors.append('maturity-duplicate-gate')


def check_choice(choice, trace, errors):
    if choice.get('decision') != 'ADOPT': return
    fb = next((x for x in (trace or {}).get('feedback', []) if x['id'] == choice.get('feedback_id')), None)
    if (not trace or choice.get('project_id') != trace.get('project_id') or not fb
        or fb.get('decision_ref') != choice.get('decision_id') or fb.get('disposition') != 'ACCEPT'
        or not fb.get('requirement_ids') or (fb.get('status') != 'CLOSED' and not fb.get('next_action'))):
        errors.append('adoption-without-owned-feedback')


def check_project_registry(registry, errors):
    """Semantic crosschecks beyond the component-registry JSON Schema."""
    rows=registry.get('components',[])
    ids=[row.get('id') for row in rows]
    if len(ids)!=len(set(ids)): errors.append('project-registry-duplicate-component-id')
    for row in rows:
        ident=str(row.get('id','unknown'))
        if row.get('component_class')=='EXTENSION' and 'BASE' in row.get('required_scopes',[]):
            errors.append('project-registry-optional-extension-required-base:'+ident)
        verification = row.get('verification', {})
        if row.get('maturity') == 'VERIFIED':
            if verification.get('id') != row.get('id') or verification.get('status') != 'VERIFIED':
                errors.append('project-registry-unverified-component:' + ident)
            check_maturity(verification, errors)
        ownership=row.get('state_ownership',[])
        names=[x.get('name') for x in ownership]
        if len(names)!=len(set(names)):
            errors.append('project-registry-duplicate-state-owner:'+ident)
        for st in ownership:
            if st.get('recovery_class') == 'AUTHORITATIVE' and st.get('backup_policy') == 'EXCLUDE':
                alt = st.get('recovery_alternative', {})
                if not all(alt.get(k) for k in ('decision_ref', 'approved_by', 'mechanism', 'evidence_refs')):
                    errors.append('project-registry-unapproved-recovery-alternative:' + ident)
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
        if name.startswith('02_STANDARD/'):
            claimed = standard_claims.get(name, set())
            if row.get('primary_control') not in claimed:
                errors.append('artifact-primary-standard-control-mismatch:'+name)
            expected_related = sorted(claimed - {row.get('primary_control')})
            if sorted(row.get('related_controls', [])) != expected_related:
                errors.append('artifact-related-standard-control-mismatch:'+name)
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


def check_candidate_records(trace, errors):
    changes = duplicate_check(trace.get('changes', []), 'change', errors)
    releases = duplicate_check(trace.get('releases', []), 'release', errors)
    gates = {g['gate_id']: g for g in trace.get('gates', [])}
    tests = {t['id']: t for t in trace.get('tests', [])}
    observations = {o['id']: o for o in trace.get('observations', [])}
    allowed = {('NOT_PUBLISHED','CANDIDATE'), ('CANDIDATE','PUBLISHED'), ('PUBLISHED','PROMOTED'),
               ('CANDIDATE','WITHDRAWN'), ('PUBLISHED','WITHDRAWN'), ('PROMOTED','WITHDRAWN'), ('WITHDRAWN','CANDIDATE')}
    state, times, identities, reinstated, scopes = {}, {}, {}, {}, {}
    for release in trace.get('releases', []):
        rid = release['id']
        candidate, digest = release.get('candidate_identity'), release.get('artifact_digest')
        identity = (candidate, digest)
        if not str(release.get('scope', '')).strip() or (identity in scopes and scopes[identity] != release.get('scope')):
            errors.append('distribution-scope-changed:' + rid)
        scopes[identity] = release.get('scope')
        at = datetime_utc(release['released_at'])
        prior = state.get(identity, 'NOT_PUBLISHED')
        if ((release.get('from'), release.get('to')) not in allowed or release.get('from') != prior
            or (identity in times and at < times[identity])):
            errors.append('distribution-invalid-transition:' + rid)
        if candidate in identities and identities[candidate] != digest:
            errors.append('distribution-candidate-artifact-changed:' + rid)
        identities[candidate] = digest
        if not release.get('owner') or not release.get('decision_ref') or not release.get('evidence_refs'):
            errors.append('distribution-missing-authorization:' + rid)
        if release.get('from') == 'WITHDRAWN': reinstated[identity] = at
        if release.get('to') == 'WITHDRAWN' and not all(release.get(k) for k in ('reason','notice_ref','recovery_obligations')):
            errors.append('distribution-withdrawal-without-obligations:' + rid)
        if release.get('to') == 'PROMOTED' and not any(r.get('scope') == release.get('scope') for r in trace.get('requirements', [])):
            errors.append('distribution-promotion-unowned-scope:' + rid)
        if release.get('to') in ('PUBLISHED', 'PROMOTED'):
            if release['to'] == 'PUBLISHED' and not release.get('limitations'):
                errors.append('distribution-publication-without-limitations:' + rid)
            if not release.get('change_ids'):
                errors.append('release-without-change:' + rid)
            for cid in release.get('change_ids', []):
                change = changes.get(cid, {})
                if ((change.get('candidate_identity'), change.get('artifact_digest')) != identity
                    or not change.get('artifact_refs') or not change.get('owner') or not change.get('evidence_refs')):
                    errors.append('release-invalid-change:' + rid + ':' + cid)
            deployment = release.get('deployment', {})
            if ((deployment.get('candidate_identity'), deployment.get('artifact_digest')) != identity
                or not deployment.get('deployed_at') or not deployment.get('evidence_refs')):
                errors.append('release-invalid-deployment:' + rid)
            elif datetime_utc(deployment['deployed_at']) > at:
                errors.append('release-before-deployment:' + rid)
            required = release.get('gate_ids', [])
            if (release['to'] == 'PROMOTED' or identity in reinstated) and not required:
                errors.append('distribution-promotion-without-gates:' + rid)
            for gid in required:
                gate = gates.get(gid, {})
                if (gate.get('status') != 'PASS' or gate.get('freshness') != 'FRESH'
                    or (gate.get('candidate_identity'), gate.get('artifact_digest')) != identity or not gate.get('evidence_refs')):
                    errors.append('release-invalid-gate:' + rid + ':' + gid)
                elif (datetime_utc(gate['observed_at']) > at
                      or (deployment.get('deployed_at') and datetime_utc(gate['observed_at']) > datetime_utc(deployment['deployed_at']))
                      or (identity in reinstated and datetime_utc(gate['observed_at']) < reinstated[identity])):
                    errors.append('release-gate-order:' + rid)
        state[identity], times[identity] = release.get('to'), at
    for fb in trace.get('feedback', []):
        if fb.get('status') != 'CLOSED' or fb.get('disposition') != 'ACCEPT': continue
        release = releases.get(fb.get('release_evidence_ref'), {})
        candidate = fb.get('closure_candidate_identity')
        proof_gates = [gates[g] for g in fb.get('closure_gate_ids', []) if g in gates]
        identity = (candidate, proof_gates[0].get('artifact_digest') if proof_gates else None)
        if ((release.get('candidate_identity'), release.get('artifact_digest')) != identity
            or release.get('to') not in ('PUBLISHED', 'PROMOTED')):
            errors.append('feedback-unresolved-release:' + fb['id'])
        for tid in fb.get('test_ids', []):
            test = tests.get(tid, {})
            if (test.get('candidate_identity'), test.get('artifact_digest')) != identity:
                errors.append('feedback-test-candidate-mismatch:' + tid)
            elif not test.get('observed_at') or any(datetime_utc(test['observed_at']) > datetime_utc(g['observed_at']) for g in proof_gates):
                errors.append('feedback-test-after-gate:' + tid)
        if not set(fb.get('closure_gate_ids', [])).issubset(set(release.get('gate_ids', []))):
            errors.append('feedback-release-missing-closure-gate:' + fb['id'])
        outcome = observations.get(fb.get('outcome_observation_id'))
        if outcome and release.get('deployment'):
            if datetime_utc(outcome['observed_at']) < max(datetime_utc(release['deployment']['deployed_at']), datetime_utc(release['released_at'])):
                errors.append('feedback-outcome-before-deployment:' + fb['id'])


def check_trace(trace, errors):
    check_candidate_records(trace, errors)
    req = duplicate_check(trace.get('requirements',[]),'requirement',errors)
    tests = duplicate_check(trace.get('tests',[]),'test',errors)
    gates = duplicate_check([{**x, 'id':x.get('gate_id')} for x in trace.get('gates',[])],'gate',errors)
    obs = duplicate_check(trace.get('observations',[]),'observation',errors)
    fbs = duplicate_check(trace.get('feedback',[]),'feedback',errors)
    metrics = duplicate_check(trace['objective']['success_measures'],'metric',errors)
    for metric in metrics.values():
        if metric.get('baseline_status') == 'MEASURED' and not metric.get('baseline_evidence_refs'):
            errors.append('measured-baseline-without-evidence:' + metric['id'])
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
        history = fb.get('history', [])
        for ev in history:
            if ev.get('event') == 'REOPEN':
                if not ev.get('decision_ref') or not ev.get('prior_closure_evidence_ref'):
                    errors.append('feedback-reopen-missing-decision-or-prior-evidence:' + fb['id'])
        if history and history[-1].get('event') == 'REOPEN':
            if fb.get('status') != 'OPEN':
                errors.append('feedback-reopen-not-open:' + fb['id'])
            if not fb.get('next_action') or not fb.get('decision_ref'):
                errors.append('feedback-reopen-missing-next-action-or-decision:' + fb['id'])
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


def _validate_disposition_record(row, prefix, ident, errors):
    if not row.get('owner'):
        errors.append(f'{prefix}-no-owner:{ident}')
    app = row.get('applicability')
    approach = row.get('approach')
    res = row.get('result')
    deferred = row.get('deferred')
    if app not in ('REQUIRED', 'OPTIONAL', 'N_A'):
        errors.append(f'{prefix}-invalid-applicability:{ident}')
    if approach not in ('COMPLY', 'ADAPT', 'PRODUCT_SPECIFIC'):
        errors.append(f'{prefix}-invalid-approach:{ident}')
    if res not in ('NOT_EVALUATED', 'PASS', 'FAIL'):
        errors.append(f'{prefix}-invalid-result:{ident}')
    if not isinstance(deferred, bool):
        errors.append(f'{prefix}-invalid-deferred:{ident}')
    if app == 'N_A':
        if not row.get('reason') or not row.get('revisit_trigger'):
            errors.append(f'{prefix}-unjustified-N_A:{ident}')
        if res == 'PASS':
            errors.append(f'{prefix}-na-cannot-pass:{ident}')
    if deferred is True:
        if not row.get('reason') or not row.get('revisit_trigger'):
            errors.append(f'{prefix}-unjustified-DEFERRED:{ident}')
        if res == 'PASS':
            errors.append(f'{prefix}-deferred-cannot-pass:{ident}')
    if approach == 'ADAPT' and (not row.get('reason') or not row.get('acceptance_criteria')):
        errors.append(f'{prefix}-adapt-without-equivalent-contract:{ident}')
    if res == 'PASS':
        if not row.get('acceptance_criteria') or not row.get('candidate_identity') or not row.get('evidence_refs'):
            errors.append(f'{prefix}-pass-no-evidence:{ident}')


def check_project_lifecycle(project, stage_ids, concern_ids, errors, matrix=None):
    """Project profile (COMPACT or FULL) classification derived from flags plus sparse cell_overrides."""
    if matrix is None:
        matrix = read_json(ROOT / '03_LIFECYCLE/lifecycle-matrix.json')
    rules = matrix.get('profile_rules', {})
    profile = project.get('profile')
    if profile not in ('COMPACT', 'FULL'):
        errors.append('project-invalid-profile:' + str(profile))
        return
    esc = project.get('escalation_flags', {})
    act = project.get('activity_flags', {})
    exp = project.get('exposure_flags', {})
    if not isinstance(esc, dict) or set(esc.keys()) != set(rules.get('escalation_flags', [])) or not all(isinstance(v, bool) for v in esc.values()):
        errors.append('project-invalid-escalation-flags')
    if not isinstance(act, dict) or set(act.keys()) != set(rules.get('activity_flag_stages', {}).keys()) or not all(isinstance(v, bool) for v in act.values()):
        errors.append('project-invalid-activity-flags')
    if not isinstance(exp, dict) or set(exp.keys()) != set(rules.get('exposure_flag_concerns', {}).keys()) or not all(isinstance(v, bool) for v in exp.values()):
        errors.append('project-invalid-exposure-flags')
    if profile == 'COMPACT' and any(esc.values()):
        errors.append('project-compact-forbidden-by-escalation-flag')

    flag_stages = set(rules.get('compact_mandatory_stages', []))
    for k, v in (act.items() if isinstance(act, dict) else []):
        if v:
            flag_stages.update(rules.get('activity_flag_stages', {}).get(k, []))
    flag_concerns = set(rules.get('compact_mandatory_concerns', []))
    for k, v in (exp.items() if isinstance(exp, dict) else []):
        if v:
            flag_concerns.update(rules.get('exposure_flag_concerns', {}).get(k, []))

    req_stages = set(stage_ids) if profile == 'FULL' else flag_stages
    req_concerns = set(concern_ids) if profile == 'FULL' else flag_concerns

    for section, key, all_known, required_ids, active_ids in [
        ('stages', 'stage_id', set(stage_ids), req_stages, flag_stages),
        ('concerns', 'concern_id', set(concern_ids), req_concerns, flag_concerns),
    ]:
        rows = project.get(section, [])
        actual = [x.get(key) for x in rows]
        if len(actual) != len(set(actual)) or not set(actual).issubset(all_known) or not required_ids.issubset(set(actual)):
            errors.append('project-' + section + '-coverage-missing-or-duplicate')
        if profile == 'FULL' and set(actual) != all_known:
            errors.append('project-' + section + '-coverage-missing-or-duplicate')
        for row in rows:
            ident = str(row.get(key, 'unknown'))
            _validate_disposition_record(row, 'project-' + section, ident, errors)
            if ident in active_ids and row.get('applicability') == 'N_A':
                errors.append('project-' + section + '-flag-na-conflict:' + ident)

    overrides = project.get('cell_overrides', [])
    seen = set()
    for row in overrides:
        stage, concern = row.get('stage_id'), row.get('concern_id')
        key = (stage, concern)
        if key in seen:
            errors.append('project-cell-duplicate:' + str(key))
        seen.add(key)
        if stage not in stage_ids or concern not in concern_ids:
            errors.append('project-cell-unknown-coordinate:' + str(key))
        _validate_disposition_record(row, 'project-cell', str(key), errors)


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
    source_map={x.get('id'):x for x in reference_list}
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
            elif sid not in source_map[ref].get('stages',[]):
                errors.append('lifecycle-stage-not-in-reference-stages:'+sid+':'+str(ref))
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
    default_alts = guidance.get('default_alternatives',[])
    default_ev = guidance.get('default_evidence_strategy','')
    default_rev = guidance.get('default_review_trigger','')
    for entry in guidance.get('guidance',[]):
        ident=entry.get('id','unknown')
        source_stages = {s for rid in entry.get('reference_ids', []) for s in source_map.get(rid, {}).get('stages', [])}
        if not set(entry.get('stage_ids', [])).issubset(source_stages):
            errors.append('guidance-stage-not-in-sources:' + ident)
        if entry.get('applicability')!='OPTIONAL':
            errors.append('guidance-illegal-mandate:'+ident)
        alts = entry.get('alternatives') if 'alternatives' in entry else default_alts
        ev_strat = entry.get('evidence_strategy') if 'evidence_strategy' in entry else default_ev
        rev_trig = entry.get('review_trigger') if 'review_trigger' in entry else default_rev
        if not entry.get('avoid_when') or not alts or not entry.get('tradeoffs') or not ev_strat or not rev_trig:
            errors.append('guidance-missing-tradeoff:'+ident)
        if entry.get('problem','').strip() == entry.get('use_when','').strip():
            errors.append('guidance-identical-problem-and-use-when:'+ident)
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
    check_project_lifecycle(project,set(stages),set(concerns),errors,matrix=matrix)

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
        rel_md = fp.relative_to(root).as_posix()
        if rel_md.startswith('07_AUDIT/') or rel_md == 'CHANGELOG.md':
            continue
        text = fp.read_text(encoding='utf-8')
        for m in re.findall(r'VS-UNIFIED-PACKAGE-STANDARD\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?)', text):
            if m not in (VERSION, VERSION[:3]):
                errors.append('stale-standard-label:'+fp.name)
        if '26+ documented invariants' in text:
            errors.append('stale-invariant-count:'+fp.name)
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
            check_vocabularies(std, schemas, errors)
            try:
                valid_schema_instance(schemas,'manifest.schema.json',read_json(root/'MANIFEST.json'))
            except (ValueError,KeyError,ValidationError,OSError,json.JSONDecodeError) as exc:
                errors.append('invalid-manifest-schema:'+str(exc)[:180])
            try:
                valid_schema_instance(schemas,'unified-package-standard.schema.json',std)
            except (ValueError,KeyError,ValidationError,OSError,json.JSONDecodeError) as exc:
                errors.append('invalid-unified-package-standard-schema:'+str(exc)[:180])
            check_examples(root, schemas, errors)
            check_choice(read_json(root / '07_CONTRACTS/examples/implementation-choice.example.json'), trace, errors)
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
    parser = argparse.ArgumentParser(description='VerySimple static package validator')
    parser.add_argument('--evidence-file',default='.validation/validation_evidence.txt')
    parser.add_argument('--implementation-choice', help='Adoption record; ADOPT requires --project-trace')
    parser.add_argument('--project-trace',help='Validate a real project trace JSON (structural/semantic only)')
    parser.add_argument('--project-registry',help='Validate a real project component registry JSON (structural only)')
    parser.add_argument('--project-lifecycle',help='Validate the project-specific 12-stage lifecycle applicability JSON')
    parser.add_argument('--skip-negative-tests',action='store_true',help='Local development only; not a release gate')
    args = parser.parse_args(argv)
    try:
        sink = EvidenceSink(
            args.evidence_file,
            root=ROOT,
            input_paths=(args.project_trace, args.project_registry, args.project_lifecycle, args.implementation_choice),
        )
    except ValueError as exc:
        print('ERROR=unsafe-evidence-file:' + str(exc))
        print('RESULT=FAIL')
        return 1
    startup_errors = []
    if not check_format_checkers(startup_errors):
        for e in startup_errors:
            sink.say('ERROR=' + e)
        sink.say('RESULT=FAIL')
        sink.close()
        return 1
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
                    check_project_lifecycle(data,{x['id'] for x in mat['stages']},{x['id'] for x in mat['concerns']},local_errors,matrix=mat)
            except (OSError, ValueError, KeyError, ValidationError, json.JSONDecodeError) as exc:
                local_errors.append(typ + '-invalid:' + str(exc)[:200])
            user_checks.append(typ+'='+('PASS' if not local_errors else 'FAIL'))
            errors.extend(local_errors)
    if args.implementation_choice:
        try:
            choice = read_json(Path(args.implementation_choice))
            valid_schema_instance(load_schemas(ROOT, errors), 'implementation-choice.schema.json', choice)
            check_choice(choice, read_json(Path(args.project_trace)) if args.project_trace else None, errors)
        except (OSError, ValueError, KeyError, ValidationError) as exc:
            errors.append('invalid-implementation-choice:' + str(exc)[:200])
    static_errors = list(errors)
    neg_checks = None
    neg_result = 'NOT_EVALUATED'
    if not args.skip_negative_tests:
        try:
            from test_validator import run_negative_suite
            neg_checks, test_errors = run_negative_suite(ROOT)
            errors.extend(test_errors)
            neg_result = 'PASS' if not test_errors else 'FAIL'
        except Exception as exc:
            errors.append('negative-suite-error:' + repr(exc))
            neg_result = 'FAIL'
    else:
        errors.append('negative-tests-mandatory-for-release')
    std_doc = read_json(ROOT / '06_GOVERNANCE/unified-package-standard.json')
    sink.say('PACKAGE=' + PACK_NAME)
    sink.say('standard_version=' + VERSION)
    sink.say('controls=' + str(len(std_doc['controls'])))
    sink.say('invariants=' + str(len(std_doc['invariants'])))
    sink.say('claim_DESIGN_COVERED=' + ('PASS' if not static_errors else 'FAIL'))
    sink.say('claim_SCHEMA_CHECKED=' + ('PASS' if not static_errors else 'FAIL'))
    sink.say('claim_NEGATIVE_TESTED=' + neg_result)
    sink.say('claim_PRODUCT_VERIFIED=NOT_EVALUATED')
    sink.say('external_project_trace=' + ('CHECKED' if args.project_trace else 'NOT_SUPPLIED'))
    sink.say('external_project_lifecycle=' + ('CHECKED' if args.project_lifecycle else 'NOT_SUPPLIED'))
    sink.say('lifecycle_matrix=12x10')
    sink.say('project_classification=12_stages+10_concerns+optional_overrides')
    if not errors:
        sink.say('artifact_ownership=CHECKED')
        sink.say('package_assurance=PASS')
    for result in user_checks: sink.say(result)
    sink.say('static_checks=' + ('PASS' if not static_errors else 'FAIL'))
    if neg_checks is not None:
        sink.say('contract_fixture_checks=' + str(neg_checks))
    elif args.skip_negative_tests:
        sink.say('contract_fixture_checks=SKIPPED')
    for e in errors:
        sink.say('ERROR=' + e)
    sink.say('RESULT=' + ('PASS' if not errors else 'FAIL'))
    sink.close()
    return 0 if not errors else 1

if __name__ == '__main__':
    sys.exit(main())
