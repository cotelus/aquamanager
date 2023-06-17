<template>
    <v-btn router-link to="/" color="primary">Ir a Inicio</v-btn>
    <div>
        <h1>Contadores</h1>
        <ul>
            <li v-for="contador in contadores" :key="contador.id">{{ contador.nombre }}: {{ contador.valor }}</li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';
import api_url from '../config.js';

export default {
    name: 'ContadoresQuery',
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
