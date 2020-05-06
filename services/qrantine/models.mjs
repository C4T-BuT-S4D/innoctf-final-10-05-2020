class Serializer {
    constructor() {
        this.i__class = ` models.${this.constructor.name}`;
    }
}

class Address extends Serializer {
    constructor(addr) {
        super();
        this.addr = addr;
    }
}

class Home extends Serializer {
    constructor(address) {
        super();
        this.address = address;
    }
}

class Work extends Serializer {
    constructor(address) {
        super();
        this.address = address;
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

export { Address, Home, Work, User, Code };
