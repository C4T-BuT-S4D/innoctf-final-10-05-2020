import requests
from checklib import *

PORT = 8080


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker):
        self.c = checker
        self.port = PORT

    def register(self, username=None):
        url = f'{self.url}/api/register'
        if username is None:
            username = rnd_username()
        password = rnd_password()
        user = {
            'login': username,
            'password': password,

        }
        r = requests.post(url, data=user)

        self.c.check_response(r, 'Could not register')
        data = self.c.get_json(r, 'Invalid response from register')
        self.c.assert_in('user', data, 'Could not register')
        return username, password

    def login(self, username, password, st=Status.MUMBLE):
        sess = get_initialized_session()
        url = f'{self.url}/api/login'

        data = {
            'login': username,
            'password': password,
        }
        r = sess.post(url, data=data)

        self.c.check_response(r, 'Could not login')
        data = self.c.get_json(r, 'Invalid response from login')
        self.c.assert_in('user', data, 'Could not login')
        return sess

    def add_post(self, sess, text, publish):
        url = f'{self.url}/api/posts'
        if publish:
            publish = 'true'
        else:
            publish = 'false'

        data = {
            'text': text,
            'publish': publish,
        }

        r = sess.post(url, data=data)
        self.c.check_response(r, 'Could not create post')
        p_id = self.c.get_json(r, 'Invalid response on post create')

        self.c.assert_gt(p_id, 0, 'Could not create post')

        return p_id

    def update_post(self, sess, post_id, text, publish):
        url = f'{self.url}/api/posts/{post_id}'
        if publish:
            publish = 'true'
        else:
            publish = 'false'

        data = {
            'text': text,
            'publish': publish,
        }

        r = sess.patch(url, data=data)
        self.c.check_response(r, 'Could not update post')
        data = self.c.get_json(r, 'Invalid response on post update')
        return data

    def get_user_posts(self, sess, limit=None, offset=None):
        url = f'{self.url}/api/posts/user'
        params = {}
        if limit:
            params['paginate[limit]'] = limit
        if offset:
            params['paginate[offset]'] = offset

        r = sess.get(url, params=params)

        self.c.check_response(r, 'Could not get user posts')
        data = self.c.get_json(r, 'Invalid response on user posts')
        return data

    def get_latest_posts(self, sess, limit=None, offset=None):
        url = f'{self.url}/api/posts/latest'
        params = {}
        if limit:
            params['paginate[limit]'] = limit
        if offset:
            params['paginate[offset]'] = offset
        r = sess.get(url, params=params)
        self.c.check_response(r, 'Could not get latest posts')
        data = self.c.get_json(r, 'Invalid response on user posts')
        return data

    def get_sharing_token(self, sess, post_id):
        url = f'{self.url}/api/posts/{post_id}/token'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get sharing token')
        data = self.c.get_json(r, 'Invalid response on sharing token')
        return data

    def get_post_by_token(self, sess, token):
        url = f'{self.url}/api/posts/token'
        r = sess.get(url, params={'token': token})
        self.c.check_response(r, 'Could not get post by token')
        data = self.c.get_json(r, 'Invalid response on getting post by sharing token')
        return data


