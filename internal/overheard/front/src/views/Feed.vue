<template>
    <layout>
        <sui-message class="ui error message"
                     v-if="error !== null && errorVisible"
                     :content="error"
                     dismissable
                     @dismiss="handleDismiss"
        />
        <div class="ui text container">
            <p>Последние записи: </p>
            <div class="ui info message" v-for="(post) in posts" :key="post[0]">
                <p>Текст: {{post[2]}}</p>
                <p>Написал {{ post[1] }} {{ new Date(post[4] * 1000).toLocaleString() }}</p>
            </div>
            <sui-button content="Предыдущие" v-on:click="prevPage" :disabled="pageNum === 0" icon="left arrow"
                        label-position="right"/>
            <sui-button content="Следующие" v-on:click="nextPage" :disabled="lastPage" icon="right arrow"
                        label-position="left"/>

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
                pageNum: 0,
                lastPage: false,
                posts: [],
                error: null,
                errorVisible: false,
            }
        },
        async mounted() {
            await this.getPosts();
        },
        methods: {
            async getPosts() {
                try {
                    let res = await this.$http.get('posts/latest?paginate[limit]=10&paginate[offset]=' + (this.pageNum * 10).toString());
                    console.log(res.data);
                    this.posts = res.data.posts;
                    this.lastPage = this.posts.length < 10;
                } catch (error) {
                    this.error = error.response.data.error;
                    this.errorVisible = true;
                }
            },
            async nextPage() {
                this.pageNum++;
                await this.getPosts();
            },
            async prevPage() {
                this.pageNum--;
                await this.getPosts();
            },
            handleDismiss() {
                this.errorVisible = false;
            },
        }
    };
</script>