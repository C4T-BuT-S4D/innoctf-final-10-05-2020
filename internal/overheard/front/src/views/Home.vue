<template>
    <layout>
        <sui-message class="ui error message"
                     v-if="error !== null && errorVisible"
                     :content="error"
                     dismissable
                     @dismiss="handleDismiss"
        />
        <div class="ui text container">
            <p>Добро пожаловать домой, {{ this.$store.state.user }}</p>
            <p>Добавьте новую запись:</p>
            <form @submit="save" class="ui form" method="post" action="">
                <div class="field">
                    <label>Текст: </label>
                    <textarea required rows="3" style="width: 30%" name="content" v-model="content"
                              placeholder="Some text"></textarea>
                </div>
                <div class="field">
                    <sui-checkbox label="Опубликовать" toggle v-model="expose"/>
                </div>

                <button class="ui button" type="submit">Сохранить</button>
            </form>
        </div>

        <br>

        <div class="ui text container">
            <p>Ваши посты: </p>
            <div class="ui info message" v-for="(post) in posts" :key="post[0]">
                <p>Текст: {{post[2]}}</p>
                <p>Сохранено:: {{new Date(post[4] * 1000).toLocaleString()}}</p>
                <sui-checkbox label="Опубликовано" disabled v-model="post[3]"/>
                <div v-if="!post[3]">
                    <sui-button @click.native="getToken(post[0])">Поделиться</sui-button>
                    <sui-button @click.native="openEdit(post[0])">Редактировать</sui-button>
                </div>
            </div>
            <sui-button content="Предыдущие" v-on:click="prevPage" :disabled="pageNum === 0" icon="left arrow"
                        label-position="right"/>
            <sui-button content="Следующие" v-on:click="nextPage" :disabled="lastPage" icon="right arrow"
                        label-position="left"/>

        </div>
        <sui-modal v-model="modalOpen">
            <sui-modal-header>Поделиться</sui-modal-header>
            <sui-modal-content>
                <router-link :to="{name: 'Shared', params: {token: token}}">Отправьте эту ссылку вашему другу, чтобы
                    поделиться с ним записью
                </router-link>
            </sui-modal-content>
            <sui-modal-actions>
                <sui-button positive @click.native="toggle">
                    OK
                </sui-button>
            </sui-modal-actions>
        </sui-modal>
        <sui-modal id="editModal" v-model="edit.modal">
            <sui-modal-header>Редактировать пост: {{ edit.post_id }}</sui-modal-header>
            <sui-message class="ui error message"
                         v-if="error !== null && errorVisible"
                         :content="error"
                         dismissable
                         @dismiss="handleDismiss"
            />
            <sui-modal-content>
                <form @submit="editPost" class="ui form" method="post" action="">
                    <div class="field">
                        <label>Текст: </label>
                        <textarea required rows="3" style="width: 30%" name="content" v-model="edit.post_text"
                                  placeholder="Some text"></textarea>
                    </div>
                    <div class="field">
                        <sui-checkbox label="Опубликовать" toggle v-model="edit.post_publish"/>
                    </div>
                    <button class="ui button" type="submit">Сохранить</button>
                </form>
            </sui-modal-content>
        </sui-modal>
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
                content: null,
                expose: null,
                publicPath: process.env.BASE_URL,
                error: null,
                errorVisible: true,
                pageNum: 0,
                lastPage: false,
                posts: [],
                modalOpen: false,
                token: null,
                edit: {
                    modal: false,
                    post_id: null,
                    post_text: '',
                    post_publish: false,
                }
            }
        },
        async mounted() {
            await this.getUserPosts();
        },
        methods: {
            async save(event) {
                event.preventDefault();
                let expose = 'false';
                if (this.expose) {
                    expose = 'true';
                }
                try {
                    await this.$http.post('posts', {
                        text: this.content,
                        publish: expose,
                    });
                    this.getUserPosts();
                } catch (error) {
                    this.error = error.response.data.error;
                    this.errorVisible = true;
                }
            },
            async getUserPosts() {
                try {
                    let res = await this.$http.get('posts/user?paginate[limit]=5&paginate[offset]=' + (this.pageNum * 5).toString());
                    this.posts = res.data.posts;
                    this.lastPage = this.posts.length < 5;
                    this.posts.forEach((p) => {
                        p[3] = !p[3];
                    });
                } catch (error) {
                    this.error = error.response.data.error;
                    this.errorVisible = true;
                }
            },
            async getToken(post_id) {
                try {
                    let res = await this.$http.get(`posts/${post_id}/token`);
                    this.token = res.data.token[0];
                    this.toggle();
                } catch (error) {
                    this.error = error.response.data.error;
                    this.errorVisible = true;
                }
            },
            async nextPage() {
                this.pageNum++;
                await this.getUserPosts();
            },
            async prevPage() {
                this.pageNum--;
                await this.getUserPosts();
            },
            handleDismiss() {
                this.errorVisible = false;
            },
            toggle() {
                this.modalOpen = !this.modalOpen;
            },
            openEdit(post_id) {
                this.edit.post_id = post_id;
                this.posts.forEach((p) => {
                    if (p[0] === post_id) {
                        this.edit.post_text = p[2];
                        this.edit.post_publish = p[3];
                    }
                });
                this.toggleEdit();
            },
            toggleEdit() {
                this.edit.modal = !this.edit.modal;
            },
            async editPost(event) {
                event.preventDefault();
                let expose = 'false';
                if (this.edit.post_publish) {
                    expose = 'true';
                }
                try {
                    await this.$http.patch(`posts/${this.edit.post_id}`, {
                        text: this.edit.post_text,
                        publish: expose,
                    });
                    this.toggleEdit();
                    await this.getUserPosts();
                } catch (error) {
                    this.error = error.response.data.error;
                    this.errorVisible = true;
                }
            },
        }
    };
</script>