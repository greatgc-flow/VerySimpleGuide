"""Reseal MANIFEST.json sha256 and size_bytes from the working tree.

MANIFEST.json is explicitly self-excluded from its own file inventory:
it records accidental-change detection digests for all other tracked package
files, not cryptographic provenance of the manifest itself.
"""
from pathlib import Path
import json, sys

sys.dont_write_bytecode = True

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from validate_package import ROOT, expected_role_for_path, file_inventory, sha256  # noqa: E402

MANIFEST_PATH = ROOT / 'MANIFEST.json'
SELF_EXCLUDED = {'MANIFEST.json'}


def default_primary_control(rel):
    if rel.startswith('07_CONTRACTS/'):
        return 'UPS-SCHEMA'
    if rel.startswith(('tools/', '.github/')):
        return 'UPS-TEST'
    return 'UPS-DOC'


def reseal(root=ROOT):
    manifest_file = root / 'MANIFEST.json'
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    existing = {row['path']: row for row in manifest.get('files', []) if 'path' in row}
    cov_file = root / '06_GOVERNANCE/control-coverage.json'
    standard_claims = {}
    if cov_file.is_file():
        cov = json.loads(cov_file.read_text(encoding='utf-8'))
        for owner in cov.get('controls', []):
            for referenced_path in owner.get('standard_refs', []):
                standard_claims.setdefault(referenced_path, set()).add(owner.get('control_id'))

    inventory = sorted(file_inventory(root) - SELF_EXCLUDED)
    updated_files = []
    for rel in inventory:
        target = root / rel
        prev = existing.get(rel, {})
        role = expected_role_for_path(rel) or prev.get('role', 'HUMAN_GUIDE')
        primary = prev.get('primary_control') or default_primary_control(rel)
        if rel in standard_claims:
            related = sorted(standard_claims[rel] - {primary})
        else:
            related = prev.get('related_controls', [])
        entry = {
            'path': rel,
            'sha256': sha256(target),
            'size_bytes': target.stat().st_size,
            'role': role,
            'primary_control': primary,
            'related_controls': related,
        }
        updated_files.append(entry)
    manifest['files'] = updated_files
    manifest_file.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    return len(updated_files)


def main():
    count = reseal(ROOT)
    print(f'resealed_files={count}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
