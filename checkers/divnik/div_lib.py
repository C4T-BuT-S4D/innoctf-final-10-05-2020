import requests
from checklib import *

PORT = 8910


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}/api'

    def __init__(self, checker):
        self.c = checker
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
        r = requests.post(url, json=user)

        self.c.check_response(r, 'Could not register')
        data = self.c.get_json(r, 'Invalid response from register')
        self.c.assert_in('id', data, 'Could not register')

        return username, password

    def login(self, username, password, st=Status.MUMBLE):
        sess = get_initialized_session()
        url = f'{self.url}/login/'

        data = {
            'username': username,
            'password': password,
        }
        r = sess.post(url, json=data)

        self.c.check_response(r, 'Could not login', status=st)
        data = self.c.get_json(r, 'Invalid response from login')
        self.c.assert_in('token', data, 'Could not login')

        sess.headers['Authorization'] = 'Token ' + data['token']
        # sess.headers['X-CSRFTOKEN'] = sess.cookies['csrftoken']

        return sess

    def get_me(self, sess):
        url = f'{self.url}/me/'

        r = sess.get(url)

        self.c.check_response(r, 'Could not get me page')
        data = self.c.get_json(r, 'Invalid response from me')

        return data

    def get_user_listing(self):
        url = f'{self.url}/users/?page_size=100'

        r = requests.get(url)

        self.c.check_response(r, 'Could not get user listing')
        data = self.c.get_json(r, 'Invalid response from user listing')
        self.c.assert_eq(type(data), dict, 'Invalid response from user listing')
        self.c.assert_in('count', data, 'Invalid response from user listing')
        self.c.assert_in('results', data, 'Invalid response from user listing')

        return data['results']

    def create_course(self, sess, name, description, reward):
        url = f'{self.url}/courses/'
        data = {
            'name': name,
            'description': description,
            'reward': reward,
        }
        r = sess.post(url, json=data)
        self.c.check_response(r, 'Could not create course')
        data = self.c.get_json(r, 'Invalid response from course create')
        self.c.assert_eq(type(data), dict, 'Invalid response from course create')
        self.c.assert_in('id', data, 'Invalid response from course create')

        return data

    def enroll_course(self, sess, course_id):
        url = f'{self.url}/relations/'
        data = {'course': course_id}
        r = sess.post(url, json=data)
        self.c.check_response(r, 'Could not enroll in course')
        data = self.c.get_json(r, 'Invalid response from course enroll')
        self.c.assert_eq(type(data), dict, 'Invalid response from course enroll')
        self.c.assert_in('id', data, 'Invalid response from course enroll')
        self.c.assert_eq(data['course'], course_id, 'Invalid response from course enroll')
        self.c.assert_eq(data['level'], 'P', 'Invalid response from course enroll')

        return data

    def finish_course(self, sess, course_id, st=Status.MUMBLE):
        patch_data = {'is_finished': True}
        url = f'{self.url}/courses/{course_id}/'
        r = sess.patch(url, json=patch_data)
        self.c.check_response(r, 'Could not update course', status=st)
        data = self.c.get_json(r, 'Invalid response from course update', status=st)
        self.c.assert_eq(type(data), dict, 'Invalid response from course update', status=st)
        self.c.assert_in('id', data, 'Invalid response from course update', status=st)
        self.c.assert_eq(data.get('is_finished'), True, 'Invalid response from course update', status=st)

        return data

    def get_course_info(self, sess, course_id):
        url = f'{self.url}/courses/{course_id}/'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get course')
        data = self.c.get_json(r, 'Invalid response from course retrieve')
        self.c.assert_eq(type(data), dict, 'Invalid response from course retrieve')
        return data

    def get_course_reward(self, sess, course_id, st=Status.MUMBLE):
        url = f'{self.url}/courses/{course_id}/reward/'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get course reward', status=st)
        data = self.c.get_json(r, 'Invalid response from course reward', status=st)
        self.c.assert_eq(type(data), dict, 'Invalid response from course reward', status=st)
        self.c.assert_in('reward', data, 'Invalid response from course reward', status=st)
        return data['reward']

    def get_user_relations(self, sess, user_id):
        url = f'{self.url}/relations/?user={user_id}'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get user relations')
        data = self.c.get_json(r, 'Invalid response from user relations list')
        self.c.assert_eq(type(data), list, 'Invalid response from user relations list')
        return data

    def get_course_relations(self, sess, course_id):
        url = f'{self.url}/relations/?course={course_id}'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get course relations')
        data = self.c.get_json(r, 'Invalid response from course relations list')
        self.c.assert_eq(type(data), list, 'Invalid response from course relations list')
        for rel in data:
            self.c.assert_in('user', rel, 'Invalid response from course relations list')
            self.c.assert_in('course', rel, 'Invalid response from course relations list')
            self.c.assert_in('level', rel, 'Invalid response from course relations list')
        return data

    def assign_grade(self, sess, rel_id, value, comment):
        url = f'{self.url}/grades/'
        data = {
            'rel': rel_id,
            'value': value,
            'comment': comment,
        }
        r = sess.post(url, json=data)
        self.c.check_response(r, 'Could not grade create')
        data = self.c.get_json(r, 'Invalid response from grade create')
        self.c.assert_eq(type(data), dict, 'Invalid response from grade create')
        self.c.assert_in('id', data, 'Invalid response from grade create')

        return data

    def get_grade_comment(self, sess, grade_id, st=Status.MUMBLE):
        url = f'{self.url}/grades/{grade_id}/comment/'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get grade comment', status=st)
        data = self.c.get_json(r, 'Invalid response from grade comment', status=st)
        self.c.assert_eq(type(data), dict, 'Invalid response from grade comment', status=st)
        self.c.assert_in('comment', data, 'Invalid response from grade comment', status=st)
        return data['comment']

    def get_grades_by_rel(self, sess, rel_id, st=Status.MUMBLE):
        url = f'{self.url}/grades/?rel={rel_id}'
        r = sess.get(url)
        self.c.check_response(r, 'Could not get grade list', status=st)
        data = self.c.get_json(r, 'Invalid response from grade list', status=st)
        self.c.assert_eq(type(data), list, 'Invalid response from grade list', status=st)
        self.c.assert_gt(len(data), 0, 'Invalid response from grade list', status=st)
        return data
