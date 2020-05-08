<template>
    <layout>
        <sui-message class="ui error message"
                     v-if="error !== null && errorVisible"
                     :content="error"
                     dismissable
                     @dismiss="handleDismiss"
        />
        <div class="ui text container" v-if="post !== null">
            <div class="ui info message">
                <p>Пост пользователя {{ post[1] }}</p>
                <p>Текст: {{post[2]}}</p>
                <p>Сохранено: {{ new Date(post[4] * 1000).toLocaleString() }}</p>
            </div>
        </div>
    </layout>
</template>
<script>
    import Layout from './Layout';

    export default {
        components: {
            Layout
        },
        data() {
            return {
                post: null,
                error: null,
                errorVisible: false,
            }
        },
        async mounted() {
            await this.getPost();
        },
        methods: {
            async getPost() {
                try {
                    let token = this.$route.params.token;
                    let res = await this.$http.get('posts/token', {params: {token: token}});
                    this.post = res.data;
                } catch (error) {
                    this.error = error.response.data.error;
                    this.errorVisible = true;
                }
            },
            handleDismiss() {
                this.errorVisible = false;
            },
        }
    };
</script>