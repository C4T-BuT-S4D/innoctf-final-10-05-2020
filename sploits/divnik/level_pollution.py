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

        # can enroll any course as a teacher by passing "level" parameter
        # as CourseRelationshipSerializer accepts it on creation
        cm.enroll_course(sess, course_id, 'T')
        print(cm.get_course_reward(sess, course_id))

        grades = cm.get_grades_by_rel(sess, rel_id=rel['id'])
        for grade in grades:
            print(cm.get_grade_comment(sess, grade['id']))
