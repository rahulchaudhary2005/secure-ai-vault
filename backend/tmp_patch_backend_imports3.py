from pathlib import Path
import re
root = Path('.').resolve()
patterns = [
    r'\bfrom\s+(ai|auth|api|database|encryption|ocr|security|storage|tasks|uploads|utils|ws)\.',
    r'\bimport\s+(ai|auth|api|database|encryption|ocr|security|storage|tasks|uploads|utils|ws)\b'
]
replacements = {
    r'\bfrom\s+ai\.': 'from backend.ai.',
    r'\bfrom\s+auth\.': 'from backend.auth.',
    r'\bfrom\s+api\.': 'from backend.api.',
    r'\bfrom\s+database\.': 'from backend.database.',
    r'\bfrom\s+encryption\.': 'from backend.encryption.',
    r'\bfrom\s+ocr\.': 'from backend.ocr.',
    r'\bfrom\s+security\.': 'from backend.security.',
    r'\bfrom\s+storage\.': 'from backend.storage.',
    r'\bfrom\s+tasks\.': 'from backend.tasks.',
    r'\bfrom\s+uploads\.': 'from backend.uploads.',
    r'\bfrom\s+utils\.': 'from backend.utils.',
    r'\bfrom\s+ws\.': 'from backend.ws.',
    r'\bimport\s+ai\b': 'import backend.ai',
    r'\bimport\s+auth\b': 'import backend.auth',
    r'\bimport\s+api\b': 'import backend.api',
    r'\bimport\s+database\b': 'import backend.database',
    r'\bimport\s+encryption\b': 'import backend.encryption',
    r'\bimport\s+ocr\b': 'import backend.ocr',
    r'\bimport\s+security\b': 'import backend.security',
    r'\bimport\s+storage\b': 'import backend.storage',
    r'\bimport\s+tasks\b': 'import backend.tasks',
    r'\bimport\s+uploads\b': 'import backend.uploads',
    r'\bimport\s+utils\b': 'import backend.utils',
    r'\bimport\s+ws\b': 'import backend.ws'
]
for path in root.rglob('*.py'):
    if path.name.startswith('tmp_') or 'venv' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    original = text
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    text = text.replace('from backend.backend.', 'from backend.')
    if text != original:
        path.write_text(text, encoding='utf-8')
        print('Patched', path)
