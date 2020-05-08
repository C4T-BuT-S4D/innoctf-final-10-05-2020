import requests
from checklib import *

PORT = 8910


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.host}:{self.port}/api'

    def __init__(self, host):
        self.host = host
        self.port = PORT

    def register(self):
        url = f'{self.url}/users/'
        username = rnd_username()
        password = rnd_password()
        user = {
            'username': username,
            'password': password,
            'first_name': rnd_string(20),
            'last_name': rnd_string(20),
        }
        requests.post(url, json=user)
        return username, password

    def login(self, username, password):
        sess = get_initialized_session()
        url = f'{self.url}/login/'

        data = {
            'username': username,
            'password': password,
        }
        r = sess.post(url, json=data)

        sess.headers['Authorization'] = 'Token ' + r.json()['token']

        return sess

    def get_user_listing(self):
        url = f'{self.url}/users/?page_size=100'

        r = requests.get(url)
        return r.json()['results']

    def create_course(self, sess, name, description, reward):
        url = f'{self.url}/courses/'
        data = {
            'name': name,
            'description': description,
            'reward': reward,
        }
        r = sess.post(url, json=data)
        return r.json()

    def enroll_course(self, sess, course_id, level):
        url = f'{self.url}/relations/'
        data = {'course': course_id, 'level': level}
        r = sess.post(url, json=data)
        return r.json()

    def get_course_reward(self, sess, course_id):
        url = f'{self.url}/courses/{course_id}/reward/'
        r = sess.get(url)
        return r.json()

    def get_course_relations(self, sess, course_id):
        url = f'{self.url}/relations/?course={course_id}'
        r = sess.get(url)
        return r.json()

    def get_user_relations(self, sess, user_id):
        url = f'{self.url}/relations/?user={user_id}'
        r = sess.get(url)
        return r.json()

    def get_grade_comment(self, sess, grade_id):
        url = f'{self.url}/grades/{grade_id}/comment/'
        r = sess.get(url)
        return r.json()['comment']

    def get_grades_by_rel(self, sess, rel_id, st=Status.MUMBLE):
        url = f'{self.url}/grades/?rel={rel_id}'
        r = sess.get(url)
        return r.json()
