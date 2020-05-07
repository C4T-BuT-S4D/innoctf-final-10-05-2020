class Serializer {
    constructor() {
        this.i__class = ` models.${this.constructor.name}`;
    }
}

class User extends Serializer {
    constructor(username, password, home) {
        super();
        this.username = username;
        this.password = password;
        this.home = home;
    }
}

class Code extends Serializer {
    constructor(qr, home, work) {
        super();
        this.qr = qr;
        this.home = home;
        this.work = work;
    }
}

export { User, Code };
