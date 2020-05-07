import Index from '@/views/Index/Index/Index';
import Login from '@/views/Index/Login/Index';
import Register from '@/views/Index/Register/Index';

import CodeIndex from '@/views/Index/Code/Index/Index';
import CodeCreate from '@/views/Index/Code/Create/Index';

const routes = [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
    },
    {
        path: '/code/create',
        name: 'code_create',
        component: CodeCreate,
        meta: {
            auth: true,
        },
    },
    {
        path: '/code/:id',
        name: 'code_index',
        component: CodeIndex,
    },
];

export default routes;
