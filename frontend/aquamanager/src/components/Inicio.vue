<template>
    <h1 class="text-white">Inicio</h1>
    <v-card max-width="500" class="mx-auto elevation-10 rounded-lg p-6">
        <v-container fluid>
            <v-row>
                <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
                    <v-card @click="navigateToPage(card.route)">
                        <v-img :src="card.src" class="align-end" height="200px">
                        </v-img>
                        <v-card-title class="w-bg text-white font-weight-bold" v-text="card.title"></v-card-title>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-card>
</template>

<script>
import router from '../router.js';

export default {
    name: 'SeleccionObjetivo',
    data: () => ({
        cards: [
            { title: 'Comuneros', src: require("@/assets/svg/persons.svg"), flex: 6, route: "/comuneros/" },
            { title: 'Hidrantes', src: require("@/assets/svg/hydrants.svg"), flex: 6, route: "/contadores/" },
            { title: 'Lecturas', src: require("@/assets/svg/reading.svg"), flex: 6, route: "/lecturas/" },
            { title: 'Consumo', src: require("@/assets/svg/consumption.svg"), flex: 6, route: "/consumos/" },
        ],
    }),
    mounted() {
        this.backToLogin();
    },
    methods: {
        backToLogin() {
            if (!localStorage.getItem('jwtToken')) {
                router.push({ path: '/login' })
            }
        },
        navigateToPage(route) {
            router.push({ path: route });
        },
    }
}
</script>

<style>
.custom-background {
    background: linear-gradient(rgba(62, 181, 155, 0.5), rgba(54, 155, 201, 0.5)), center center / cover no-repeat;
}
</style>
