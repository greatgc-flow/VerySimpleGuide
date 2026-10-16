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

from validate_package import ROOT, file_inventory, sha256  # noqa: E402

MANIFEST_PATH = ROOT / 'MANIFEST.json'
SELF_EXCLUDED = {'MANIFEST.json'}


def reseal(root=ROOT):
    manifest_file = root / 'MANIFEST.json'
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    existing = {row['path']: row for row in manifest.get('files', []) if 'path' in row}
    inventory = sorted(file_inventory(root) - SELF_EXCLUDED)
    updated_files = []
    for rel in inventory:
        target = root / rel
        prev = existing.get(rel, {})
        entry = {
            'path': rel,
            'sha256': sha256(target),
            'size_bytes': target.stat().st_size,
            'role': prev.get('role', 'HUMAN_GUIDE'),
            'primary_control': prev.get('primary_control', 'UPS-DOC'),
            'related_controls': prev.get('related_controls', []),
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
