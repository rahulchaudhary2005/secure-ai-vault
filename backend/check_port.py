import socket
import http.client

host = '127.0.0.1'
port = 8000

# TCP connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.settimeout(3)
    s.connect((host, port))
    print('TCP connect: OK')
except Exception as e:
    print('TCP connect failed:', e)
finally:
    s.close()

# HTTP GET /
try:
    conn = http.client.HTTPConnection(host, port, timeout=3)
    conn.request('GET', '/')
    res = conn.getresponse()
    print('HTTP status:', res.status)
    print('HTTP body:', res.read().decode('utf-8'))
except Exception as e:
    print('HTTP check failed:', e)
