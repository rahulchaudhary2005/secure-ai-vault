import re
from pathlib import Path

root = Path('backend')
if not root.exists():
    raise SystemExit('backend directory not found')

venv = root / 'venv'

# Patterns to match: from ai.xxx, from storage.xxx, from utils.xxx etc
# and convert to: from backend.ai.xxx, from backend.storage.xxx etc
pattern = r'^(\s*)from\s+(ai|api|auth|database|encryption|models|ocr|security|storage|uploads|utils)\.'

# Also catch: import ai, import storage etc
import_pattern = r'^(\s*)import\s+(ai|api|auth|database|encryption|models|ocr|security|storage|uploads|utils)(?:\s|,|$)'

updated_count = 0

for path in root.rglob('*.py'):
    # Skip venv directory
    if venv in path.parents:
        continue
    
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print(f'Skipped {path} (UnicodeDecodeError)')
        continue
    
    original = text
    
    # Replace "from module." imports
    text = re.sub(pattern, r'\1from backend.\2.', text)
    
    # Replace "import module" imports (but not "import backend")
    text = re.sub(import_pattern, r'\1import backend.\2', text)
    
    if text != original:
        path.write_text(text, encoding='utf-8')
        print(f'Updated {path}')
        updated_count += 1

print(f'\nTotal updated: {updated_count} files')
