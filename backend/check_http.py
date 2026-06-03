import urllib.request
import urllib.error

url = 'http://127.0.0.1:8000/'
try:
    with urllib.request.urlopen(url, timeout=10) as resp:
        print('Status:', resp.status)
        print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTPError', e.code)
    try:
        print(e.read().decode('utf-8'))
    except Exception:
        pass
except Exception as e:
    print('Error', repr(e))
