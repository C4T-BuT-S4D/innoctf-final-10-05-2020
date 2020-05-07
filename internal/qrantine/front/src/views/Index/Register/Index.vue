<template>
    <full-layout>
        <card>
            <f-header text="Register" />
            <form class="mt-3" @submit.prevent="register">
                <div class="ff">
                    <f-input
                        type="text"
                        name="username"
                        v-model="username"
                        :errors="errors['username']"
                        placeholder="Username"
                    />
                </div>
                <div class="ff">
                    <f-input
                        type="password"
                        name="password"
                        v-model="password"
                        :errors="errors['password']"
                        placeholder="Password"
                    />
                </div>
                <div class="ff">
                    <f-input
                        type="test"
                        name="home"
                        v-model="home"
                        :errors="errors['home']"
                        placeholder="Home"
                    />
                </div>
                <div class="ff">
                    <f-detail :errors="[errors['err']]" />
                </div>
                <div class="ff">
                    <input type="submit" value="Register" class="btn" />
                </div>
            </form>
        </card>
    </full-layout>
</template>

<script>
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';

export default {
    components: {
        FInput,
        FHeader,
    },

    data: function() {
        return {
            username: null,
            password: null,
            home: null,
            errors: {},
        };
    },

    methods: {
        register: async function() {
            try {
                await this.$http.post('/register/', {
                    username: this.username,
                    password: this.password,
                    home: this.home,
                });
                this.$router.push({ name: 'login' }).catch(() => {});
            } catch (error) {
                this.errors = error.response.data;
            }
        },
    },
};
</script>
