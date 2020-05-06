import * as models from './models.mjs';
global.models = models;

function inject() {
    Object.getPrototypeOf(0).i__serialize = function () {
        return {
            i__type: 'i',
            i__value: Number(0 + this),
        };
    };

    Object.getPrototypeOf('').i__serialize = function () {
        return {
            i__type: 's',
            i__value: String('' + this),
        };
    };

    Object.getPrototypeOf(false).i__serialize = function () {
        return {
            i__type: 'b',
            i__value: Boolean(false + this),
        };
    };

    Object.getPrototypeOf([]).i__detector = 'return';
    Object.getPrototypeOf([]).i__serialize = function () {
        let result = [];
        for (const item of this) {
            result.push(serialize(item));
        }
        return {
            i__type: 'a',
            i__value: result,
        };
    };

    Object.getPrototypeOf({}).i__serialize = function () {
        let result = {};
        let className = null;
        for (const key in this) {
            if (key === 'i__class') {
                className = this[key];
                continue;
            }
            if (this.hasOwnProperty(key)) {
                result[key] = serialize(this[key]);
            }
        }
        if (className !== null) {
            return {
                i__type: 'c',
                i__value: result,
                i__class: className,
            };
        }
        return this;
    };
}

function serialize(value) {
    if (value === null) {
        return {
            i__type: 'n',
            i__value: null,
        };
    }

    if (value === undefined) {
        return {
            i__type: 'u',
            i__value: undefined,
        };
    }

    return value.i__serialize();
}

function deserialize(value) {
    if (value.i__type === 'n') {
        return null;
    }

    if (value.i__type === 'i') {
        return Number(value.i__value);
    }

    if (value.i__type === 's') {
        return String(value.i__value);
    }

    if (value.i__type === 'b') {
        return Boolean(value.i__value);
    }

    if (value.i__type === 'o') {
        let result = {};
        for (const key in value.i__value) {
            if (value.i__value.hasOwnProperty(key)) {
                result[key] = deserialize(value.i__value[key]);
            }
        }
        return result;
    }

    if (value.i__type === 'c') {
        let result = { i__class: value.i__class };
        let classD = Function([].i__detector + value.i__class)();
        for (const key in value.i__value) {
            if (value.i__value.hasOwnProperty(key)) {
                result[key] = deserialize(value.i__value[key]);
            }
        }
        Object.setPrototypeOf(result, classD.prototype);
        return result;
    }

    if (value.i__type === 'a') {
        let result = [];
        for (const item of value.i__value) {
            result.push(deserialize(item));
        }
        return result;
    }

    return undefined;
}

export { serialize, deserialize, inject };
