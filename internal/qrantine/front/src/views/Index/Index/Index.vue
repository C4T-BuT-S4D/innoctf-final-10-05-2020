<template>
    <full-layout>
        <card>
            <div v-if="!$types.isNull(codes)">
                <router-link
                    class="nlnk link"
                    :to="{ name: 'code_index', params: { id: code } }"
                    v-for="code of codes"
                    :key="code"
                >
                    <card class="vc mb-1 cp">
                        {{ code }}
                    </card>
                </router-link>
            </div>
            <f-detail :errors="[errors['err']]" />
        </card>
    </full-layout>
</template>

<script>
export default {
    data: function() {
        return {
            codes: null,
            errors: {},
        };
    },

    created: async function() {
        try {
            this.codes = (await this.$http.get('/codes/')).data.ok;
        } catch (error) {
            this.errors = error.response.data;
        }
    },
};
</script>

<style lang="scss" scoped>
.cp {
    cursor: pointer;
}
</style>
