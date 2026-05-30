import sys
from pathlib import Path
print('cwd:', Path.cwd())
print('sys.path[0]:', sys.path[0])
print('top-level backend exists:', Path('backend').exists())
try:
    import backend.database.database as bdb
    print('backend.database.database __file__:', bdb.__file__)
    print('backend.database.database package path:', bdb.__package__)
    import backend
    print('backend __file__:', backend.__file__)
except Exception as e:
    print('import error:', type(e).__name__, e)

print('backend path in sys.path:', [p for p in sys.path if 'backend' in str(p)])
