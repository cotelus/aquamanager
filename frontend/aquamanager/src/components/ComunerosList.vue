<template>
    <v-card class="mx-auto" max-width="500">
        <v-card-title class="text-white font-weight-bold secondary-bg">
            Comuneros
        </v-card-title>

        <v-divider></v-divider>

        <v-virtual-scroll :items="usuarios" height="80vh" item-height="48">
            <template v-slot:default="{ item }">
                <v-list-item :key="item.id" :title="item.username" :subtitle="`Comunero nº${item.id}`">
                    <template v-slot:prepend>
                        <v-icon class="w-bg elevation-5" color="white">mdi-account</v-icon>
                    </template>

                    <template v-slot:append>
                        <v-btn icon="mdi-pencil" size="x-small" variant="tonal"></v-btn>
                    </template>
                </v-list-item>
            </template>
        </v-virtual-scroll>
    </v-card>
</template>

<script>
import axios from 'axios';
import api_url from '../config.js';
import router from '../router.js';

export default {
    data() {
        return {
            usuarios: [],
        };
    },
    mounted() {
        this.backToLogin();
        this.fetchUsuarios();
    },
    methods: {
        backToLogin() {
            if (!localStorage.getItem('jwtToken')) {
                router.push({ path: '/login' });
            }
        },
        backToRoot() {
            router.push({ path: '/' });
        },
        fetchUsuarios() {
            var jwtToken = localStorage.getItem('jwtToken');

            axios
                .get(`${api_url}/users/`, {
                    headers: {
                        'Authorization': jwtToken,
                    },
                })
                .then((response) => {
                    this.usuarios = response.data.result;
                    console.log(this.usuarios);
                })
                .catch((error) => {
                    console.error(error);
                    this.backToRoot();
                });
        },
    },
};
</script>

<style>
.secondary-bg {
    background-color: #3eb59b;
}
</style>
