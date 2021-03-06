import * as models from './models.mjs';
import { inject, serialize, deserialize } from './serializer.mjs';

import { isString } from './utils.mjs';

import mongo from 'mongodb';
import express from 'express';
import cors from 'cors';
import session from 'express-session';
import ConnectMongo from 'connect-mongo';

const app = express();
app.use(
    cors({
        origin: 'http://127.0.0.1:8080',
        methods: ['GET', 'POST'],
        allowedHeaders: ['Content-Type'],
        credentials: true,
    })
);
const MongoStore = ConnectMongo(session);

const go = async (request) => {
    let cnt = 20;
    while (cnt > 0) {
        try {
            const res = await request();
            return res;
        } catch (err) {
            console.error('ERROR', err);
            cnt -= 1;
            if (cnt < 0) {
                throw "Can't process requet";
            }
            inject();
        }
    }
};

mongo.MongoClient.connect(
    'mongodb://mongo:27017',
    {
        poolSize: 10,
        useUnifiedTopology: true,
    },
    function (err, client) {
        if (err) throw err;

        const db = client.db('main');

        app.use(
            session({
                store: new MongoStore({ client: client, dbName: 'sessions' }),
                secret:
                    "hm. I've lost a machine.. literally _lost_. it responds to ping, it works completely, I just can't figure out where in my apartment it is.",
                saveUninitialized: true,
                resave: false,
            })
        );

        app.use(express.json());

        app.use((req, res, next) => {
            req.db = db;
            next();
        });

        app.post('/api/register', async function (req, res) {
            const { username = null, password = null, home = null } = req.body;

            if (!username) {
                res.status(400).json({
                    err: 'No username field',
                });
                return;
            }

            if (!password) {
                res.status(400).json({
                    err: 'No password field',
                });
                return;
            }

            if (!home) {
                res.status(400).json({
                    err: 'No home field',
                });
                return;
            }

            if (!isString(username)) {
                res.status(400).json({
                    err: 'Invalid username',
                });
                return;
            }

            const user = await req.db.collection('users').findOne({
                username,
            });

            if (user) {
                res.status(400).json({
                    err: 'Username already exists',
                });
                return;
            }

            await req.db.collection('users').insertOne({
                username,
                user: await go(() =>
                    serialize(new models.User(username, password, home))
                ),
            });

            res.json({
                ok: username,
            });
        });

        app.post('/api/login', async function (req, res) {
            const { username = null, password = null } = req.body;

            if (!username) {
                res.status(400).json({
                    err: 'No username field',
                });
                return;
            }

            if (!password) {
                res.status(400).json({
                    err: 'No password field',
                });
                return;
            }

            if (!isString(username)) {
                res.status(400).json({
                    err: 'Invalid username',
                });
                return;
            }

            const user = await req.db.collection('users').findOne({
                username,
            });

            if (!user) {
                res.status(400).json({
                    err: 'No such user',
                });
                return;
            }

            const userD = await go(() => deserialize(user.user));

            if (userD.password !== password) {
                res.status(400).json({
                    err: 'Invalid password',
                });
                return;
            }

            req.session.username = username;
            req.session.home = userD.home;

            res.json({
                ok: username,
            });
        });

        app.get('/api/me', function (req, res) {
            if (!req.session.username) {
                res.status(403).json({
                    err: 'No auth',
                });
                return;
            }

            res.json({
                ok: {
                    username: req.session.username,
                    home: req.session.home,
                },
            });
        });

        app.post('/api/logout', function (req, res) {
            if (!req.session.username) {
                res.status(403).json({
                    err: 'No auth',
                });
                return;
            }

            req.session.destroy();

            res.json({
                ok: true,
            });
        });

        app.post('/api/code', async function (req, res) {
            if (!req.session.username) {
                res.status(403).json({
                    err: 'No auth',
                });
                return;
            }

            const { work = null, code: qr = null } = req.body;

            if (!work) {
                res.status(400).json({
                    err: 'No work field',
                });
                return;
            }

            if (!qr) {
                res.status(400).json({
                    err: 'No code field',
                });
                return;
            }

            const home = (
                await go(async () =>
                    deserialize(
                        (
                            await req.db.collection('users').findOne({
                                username: req.session.username,
                            })
                        ).user
                    )
                )
            ).home;

            const id = (
                await req.db.collection('codes').insertOne({
                    time: new Date().getTime(),
                    code: await go(() =>
                        serialize(new models.Code(qr, home, work))
                    ),
                })
            ).insertedId;

            res.json({
                ok: id,
            });
        });

        app.get('/api/codes', async function (req, res) {
            const codes = await req.db
                .collection('codes')
                .find({})
                .sort({ time: -1 })
                .limit(500)
                .toArray();
            const ids = [];
            for (const code of codes) {
                ids.push(code._id);
            }
            res.json({
                ok: ids,
            });
        });

        app.get('/api/code/:id', async function (req, res) {
            const { id } = req.params;

            if (!isString(id)) {
                res.status(400).json({
                    err: 'Invalid id',
                });
                return;
            }

            const code = await req.db
                .collection('codes')
                .findOne({ _id: new mongo.ObjectID(id) });

            if (!code) {
                res.status(400).json({
                    err: 'No such code',
                });
                return;
            }

            const codeD = await go(() => deserialize(code.code));

            res.json({
                ok: codeD.qr,
            });
        });

        app.listen(process.env.PORT, () => {
            console.log(`Listening on port ${process.env.PORT}`);
        });
    }
);
