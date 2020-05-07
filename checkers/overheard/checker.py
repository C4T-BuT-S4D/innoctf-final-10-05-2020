#!/usr/bin/env python3

from gevent import monkey

monkey.patch_all()

import sys
import json
import os
import random
from faker import Faker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from over_lib import *


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

        post_text = self.f.sentence(nb_words=20)

        post_id = self.mch.add_post(sess, post_text, publish=True)

        latest = self.mch.get_latest_posts(sess, limit=50)

        texts = [x[2] for x in latest['posts']]
        self.assert_in(post_text, texts, 'Failed to find published post')

        # create draft
        post_text = self.f.sentence(nb_words=20)
        post_id = self.mch.add_post(sess, post_text, publish=False)

        # get draft
        latest = self.mch.get_user_posts(sess, limit=50)
        texts = [x[2] for x in latest['posts']]
        self.assert_in(post_text, texts, 'Failed to get users post')

        # get token
        token = self.mch.get_sharing_token(sess, post_id).get('token')
        self.assert_neq(token, None, 'Failed to receive sharing token')

        # fetch post by token
        new_sess = get_initialized_session()
        post = self.mch.get_post_by_token(new_sess, token)
        self.assert_eq(post_text, post[2], 'Failed to get post by sharing token')
        self.assert_eq(post[1], u, 'Invalid post returned', status=status.Status.CORRUPT)

        new_text = self.f.sentence(nb_words=20)
        self.assert_gt(self.mch.update_post(sess, post_id, new_text, publish=True), 0, "Failed to update post")

        latest = self.mch.get_latest_posts(sess, limit=50)

        texts = [x[2] for x in latest['posts']]
        self.assert_in(new_text, texts, 'Failed to find updated published post')

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        username = None
        if int(vuln) == 1:  # flag in login
            username = flag
        u, p = self.mch.register(username)
        session = self.mch.login(u, p)

        post_text = self.f.sentence(nb_words=20)
        publish = True
        if int(vuln) == 2:  # flag in post text
            post_text = flag
            publish = False

        post_id = self.mch.add_post(session, post_text, publish)

        full_data = {
            'u': u,
            'p': p,
            'post_id': post_id,
            'text': post_text,
        }

        self.cquit(Status.OK, f'post_{post_id}', json.dumps(full_data))

    def get(self, flag_id, flag, vuln):
        data = json.loads(flag_id)
        u, p = data['u'], data['p']

        sess = self.mch.login(u, p)

        posts = self.mch.get_user_posts(sess, limit=10).get('posts')
        self.assert_neq(posts, None, 'Failed to receive user posts', status=status.Status.CORRUPT)
        self.assert_eq(len(posts), 1, 'Failed to receive user posts', status=status.Status.CORRUPT)

        post = posts[0]

        self.assert_eq(post[1], u, 'Invalid post returned', status=status.Status.CORRUPT)
        self.assert_eq(post[2], data['text'], 'Invalid post returned', status=Status.CORRUPT)
        if post[3]:
            token = self.mch.get_sharing_token(sess, post[0]).get('token')
            sess = get_initialized_session()
            post = self.mch.get_post_by_token(sess, token)
            self.assert_eq(post[1], u, 'Invalid post returned', status=status.Status.CORRUPT)
            self.assert_eq(post[2], data['text'], 'Invalid post returned', status=Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
