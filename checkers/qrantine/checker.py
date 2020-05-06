#!/usr/bin/env python3

from gevent import monkey

monkey.patch_all()

import sys
import json
import os
import random
from checklib import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qr_lib import *

class Checker(BaseChecker):
    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        s = get_initialized_session()

        u = rnd_username()
        p = rnd_password()
        h = rnd_string(32)
        w = rnd_string(32)

        self.mch.register(s, u, p, h)
        self.mch.login(s, u, p)
        self.mch.me(s, u, h)

        code = self.mch.create_code(h, w)

        cid = self.mch.upload_code(s, code, w)

        self.mch.list_codes(s, cid)

        self.mch.verify_code(s, cid, h, w)

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        s = get_initialized_session()

        u = rnd_username()
        p = rnd_password()
        w = rnd_string(32)

        self.mch.register(s, u, p, flag)
        self.mch.login(s, u, p)
        self.mch.me(s, u, flag)

        code = self.mch.create_code(flag, w)

        cid = self.mch.upload_code(s, code, w)

        self.cquit(Status.OK, f'{u}:{p}:{cid}:{w}')

    def get(self, flag_id, flag, vuln):
        s = get_initialized_session()

        u, p, cid, w = flag_id.split(':')

        self.mch.login(s, u, p)
        self.mch.verify_code(s, cid, flag, w)

        self.cquit(Status.OK)

if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
