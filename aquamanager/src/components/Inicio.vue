<template>
    <v-btn router-link to="/contadores" color="primary">Ir a Contadores</v-btn>
    <div>
        <h1>Objetivos</h1>
    </div>
</template>

<script>
// import axios from 'axios';
// import api_url from '../config.js';
import router from '../router.js';

export default {
    name: 'SeleccionObjetivo',
    data() {
        return {
            contadores: []
        };
    },
    mounted() {
        this.backToLogin();
    },
    methods: {
        backToLogin() {
            if (!localStorage.getItem('jwtToken')) {
                router.push({path:'/login'})
            }
        }
    }
}
</script>
