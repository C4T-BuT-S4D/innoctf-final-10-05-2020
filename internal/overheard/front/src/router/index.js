import Vue from 'vue';
import VueRouter from 'vue-router';
import Index from '@/views/Index';
import Register from "@/views/Register";
import Login from "@/views/Login";
import Home from "@/views/Home";
import Feed from "@/views/Feed";
import Share from "@/views/Share";

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Index',
        component: Index
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
    },
    {
        path: '/feed',
        name: 'Feed',
        component: Feed,
    },
    {
        path: '/shared/:token',
        name: 'Shared',
        component: Share,
    }
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router;
