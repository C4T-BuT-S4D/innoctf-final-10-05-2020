#!/usr/bin/env python3

from gevent import monkey

monkey.patch_all()

from collections import defaultdict
import sys
import json
import os
import random
from faker import Faker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from div_lib import *


class Checker(BaseChecker):
    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)
        self.f = Faker()

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        u, p = self.mch.register()
        sess = self.mch.login(u, p)
        me = self.mch.get_me(sess)

        course_name = self.f.sentence(nb_words=5)
        course_description = self.f.text()
        course_reward = rnd_string(random.randint(20, 40))
        course = self.mch.create_course(sess, course_name, course_description, course_reward)

        self.assert_eq(course_reward, self.mch.get_course_reward(sess, course['id']), 'Invalid course reward')

        user_courses = self.mch.get_user_relations(sess, me['id'])
        self.assert_in_list_dicts(user_courses, 'user', me['id'], 'Invalid user course list')
        self.assert_in_list_dicts(user_courses, 'course', course['id'], 'Invalid user course list')

        me_list = []
        sess_list = {}
        for _ in range(random.randint(2, 10)):
            tmp_sess = self.mch.login(*self.mch.register())
            tmp_me = self.mch.get_me(tmp_sess)
            self.mch.enroll_course(tmp_sess, course['id'])
            me_list.append(tmp_me)
            sess_list[tmp_me['id']] = tmp_sess

        course_parts = self.mch.get_course_relations(sess, course['id'])
        for tmp_me in me_list:
            cur = list(filter(lambda x: x['user'] == tmp_me['id'], course_parts))
            self.assert_gt(len(cur), 0, 'Invalid course participants')
            self.assert_eq(cur[0]['level'], 'P', 'Invalid course participants')

        cur = list(filter(lambda x: x['user'] == me['id'], course_parts))
        self.assert_gt(len(cur), 0, 'Invalid course participants')
        self.assert_eq(cur[0]['level'], 'T', 'Invalid course participants')

        all_grades = defaultdict(list)
        for rel in course_parts * random.randint(1, 3):
            user_id = rel['user']
            if rel['level'] == 'T' or self.f.boolean(25):
                continue

            if self.f.boolean(80):
                value = 5.0
            else:
                value = self.f.pyfloat(min_value=0, max_value=5.0, right_digits=1)

            comm = rnd_string(random.randint(20, 40))
            grade = self.mch.assign_grade(sess, rel['id'], value, comm)
            self.assert_eq(grade['value'], value, 'Invalid grade response')
            self.assert_eq(comm, self.mch.get_grade_comment(sess, grade['id']), 'Invalid grade comment')
            self.assert_eq(comm, self.mch.get_grade_comment(sess_list[user_id], grade['id']), 'Invalid grade comment')
            by_rel = self.mch.get_grades_by_rel(sess, rel['id'])
            self.assert_in(grade, by_rel, 'Invalid grades listing')

            all_grades[rel['user']].append(grade)

        self.mch.finish_course(sess, course['id'])

        for (user_id, grades) in all_grades.items():
            total_value = sum((grade['value'] for grade in grades)) / len(grades)
            if total_value == 5.0:
                user_sess = sess_list[user_id]
                rew = self.mch.get_course_reward(user_sess, course['id'])
                self.assert_eq(rew, course_reward, 'Invalid course reward')

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        u, p = self.mch.register()
        sess = self.mch.login(u, p)
        parts_data = {}

        if int(vuln) == 1:  # flag in course reward
            course_reward = flag
            comment = rnd_string(random.randint(20, 40))
        else:  # flag in grade comment
            comment = flag
            course_reward = rnd_string(random.randint(20, 40))

        course_name = self.f.sentence(nb_words=5)
        course_description = self.f.text()

        course = self.mch.create_course(sess, course_name, course_description, course_reward)

        for _ in range(random.randint(3, 5)):
            tu, tp = self.mch.register()
            tmp_sess = self.mch.login(tu, tp)
            tmp_me = self.mch.get_me(tmp_sess)
            self.mch.enroll_course(tmp_sess, course['id'])
            tmp_me['password'] = tp
            parts_data[tmp_me['id']] = tmp_me

        course_parts = self.mch.get_course_relations(sess, course['id'])
        random.shuffle(course_parts)
        count_flags = random.randint(1, 3)
        for i, rel in enumerate(course_parts):
            if rel['level'] == 'T':
                continue

            self.assert_in(rel['user'], parts_data, 'Invalid course relations')
            if i < count_flags:
                value = 5.0
            else:
                value = self.f.pyfloat(min_value=0, max_value=5.0, right_digits=1)
            grade = self.mch.assign_grade(sess, rel['id'], value, comment)
            self.assert_eq(grade['value'], value, 'Invalid grade response')
            self.assert_eq(comment, self.mch.get_grade_comment(sess, grade['id']), 'Invalid grade comment')
            parts_data[rel['user']]['value'] = value
            parts_data[rel['user']]['rel_id'] = rel["id"]

        full_data = {
            'username': u,
            'password': p,
            'course_id': course['id'],
            'participants': list(parts_data.values()),
        }
        self.cquit(Status.OK, f'course_{course["id"]}', json.dumps(full_data))

    def get(self, flag_id, flag, vuln):
        data = json.loads(flag_id)
        participants = data['participants']
        course_id = data['course_id']

        sess = self.mch.login(data['username'], data['password'], st=Status.CORRUPT)

        p_sess = []
        for each in participants:
            p_sess.append(self.mch.login(each['username'], each['password'], st=Status.CORRUPT))

        if int(vuln) == 1:
            self.mch.finish_course(sess, course_id)
            reward = self.mch.get_course_reward(sess, course_id, st=Status.CORRUPT)
            self.assert_eq(reward, flag, 'Invalid course reward', status=Status.CORRUPT)

            for (part, s) in zip(participants, p_sess):
                if part['value'] == 5.0:
                    reward = self.mch.get_course_reward(s, course_id, st=Status.CORRUPT)
                    self.assert_eq(reward, flag, 'Invalid course reward', status=Status.CORRUPT)

        else:
            for (part, s) in zip(participants, p_sess):
                cur_grades = self.mch.get_grades_by_rel(s, part['rel_id'], st=Status.CORRUPT)
                for grade in cur_grades:
                    if self.f.boolean(25):
                        comm = self.mch.get_grade_comment(sess, grade['id'], st=Status.CORRUPT)
                        self.assert_eq(comm, flag, 'Invalid grade comment', status=Status.CORRUPT)
                    if self.f.boolean(50):
                        comm = self.mch.get_grade_comment(s, grade['id'], st=Status.CORRUPT)
                        self.assert_eq(comm, flag, 'Invalid grade comment', status=Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
