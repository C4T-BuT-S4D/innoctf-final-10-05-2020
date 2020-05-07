#!/usr/bin/env python3
import sys
import secrets
from requests import Session
ip = sys.argv[1]

url = f'http://{ip}:8080'
login = secrets.token_hex(10)
password = login

s = Session()
resp = s.post(url + '/api/register', data = {'login':login, 'password': password})

latest_posts = s.get(url + '/api/posts/latest?paginate[limit]=20').json()['posts']


for p in latest_posts:
    r = s.patch(url + '/api/posts/' + str(p[0]))
    print(r.json(), flush=True)


