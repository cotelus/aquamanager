<template>
    <v-btn router-link to="/contadores" color="primary">Ir a Contadores</v-btn>
    <div>
        <h1>Objetivos</h1>
    </div>
</template>

<script>
import axios from 'axios';
import api_url from '../config.js';

export default {
    name: 'SeleccionObjetivo',
    data() {
        return {
            contadores: []
        };
    },
    mounted() {
        this.fetchContadores();
    },
    methods: {
        fetchContadores() {
            axios.get(`${api_url}/contadores/`)
                .then(response => {
                    this.contadores = response.data;
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }
}
</script>
