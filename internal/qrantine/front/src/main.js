import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

Vue.config.productionTip = false;

/* axios configuration */

import { apiUrl } from '@/config';
import axios from 'axios';
axios.defaults.baseURL = apiUrl;
axios.defaults.withCredentials = true;

axios.interceptors.response.use(
    response => response,
    error => {
        const ret = error;
        if (!ret.response) {
            ret.response = { data: { err: 'Api server is down' } };
        } else if (ret.response.status === 500) {
            ret.response.data = { err: 'Api server is down' };
        }
        return Promise.reject(ret);
    }
);

/* utils injection */

import {
    isArray,
    isBoolean,
    isFunction,
    isNull,
    isNumber,
    isObject,
    isRegExp,
    isString,
    isUndefined,
} from '@/utils/types';

Vue.prototype.$http = axios;
Vue.prototype.$types = {
    isArray,
    isBoolean,
    isFunction,
    isNull,
    isNumber,
    isObject,
    isRegExp,
    isString,
    isUndefined,
};
store.$http = axios;

/* internal components */

import Card from '@/components/Card/Index';
import FDetail from '@/components/Form/Detail';
import Full from '@/layouts/Full';

Vue.component('card', Card);
Vue.component('f-detail', FDetail);
Vue.component('full-layout', Full);

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');
