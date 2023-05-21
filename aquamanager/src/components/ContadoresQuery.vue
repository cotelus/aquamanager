<template>
    <div>
        <h1>Contadores</h1>
        <ul>
            <li v-for="contador in contadores" :key="contador.id">{{ contador.nombre }}: {{ contador.valor }}</li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';

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
            axios.get('http://192.168.1.128/contadores/')
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
