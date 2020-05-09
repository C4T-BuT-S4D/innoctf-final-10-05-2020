<template>
    <div>
        <div class="ui inverted segment">
            <div class="ui inverted secondary menu">
                <a href="/" class="active item">
                    Главная
                </a>
                <a href="/feed" class="active item">Последние посты</a>

                <a href="/login" v-if="!loggedIn" class="active item">Войти</a>
                <a href="/register" v-if="!loggedIn" class="active item">Зарегистрироваться</a>
                <a href="/home" v-if="loggedIn" class="active item">Моя страница</a>
                <div class="right menu">
                    <a href="#" v-on:click="logout" class="ui active item">
                        Выйти
                    </a>
                </div>
            </div>
        </div>
        <slot>

        </slot>
    </div>
</template>
<script>
    export default {
        computed: {
            loggedIn() {
                return this.$store.state.user != null;
            },
            user() {
                return this.$store.state.user;
            }
        },
        methods: {
            logout() {
                this.$store.commit('logout');
            }
        }
    };
</script>