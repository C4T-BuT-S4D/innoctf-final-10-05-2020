<template>
    <layout>
        <div class="ui text container">
            <h1 class="ui header">Добро пожаловать в подслушано</h1>
            <div class="ui one column grid">
                <div class="column">
                    <h3>Сервис для анонимного общения</h3>
                    <img class="ui small image" :src="`${publicPath}olen.jpeg`">
                </div>
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
                publicPath: process.env.BASE_URL
            }
        }
    };
</script>