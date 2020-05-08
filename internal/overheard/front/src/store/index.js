import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {},
    mutations: {
        login(state, payload) {
            state.user = payload.user;
        },
        logout(state) {
            state.user = null;
        }
    },
    actions: {},
    modules: {},
    plugins: [createPersistedState()]
});
