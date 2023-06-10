<template>
    <div class="d-flex align-center justify-center" style="height: 75vh">
        <v-sheet width="500" height="300" class="mx-auto elevation-10 rounded-lg p-6">
            <v-sheet width="400" class="mx-auto">
                <v-form fast-fail @submit.prevent="login">
                    <h1 class="mb-4 mt-4 text-light-blue-darken-2">Inicio de sesión</h1>
                    <v-text-field variant="underlined" color="#3490c9" v-model="username" label="Usuario" class="mb-1"></v-text-field>
                    <v-text-field variant="underlined" color="#3490c9" v-model="password" label="Contraseña"
                        :type="show ? 'text' : 'password'" :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="show_pass" class="mb-1"></v-text-field>

                    <v-btn @click="submitLoginForm" variant="outlined" color="#3490c9" block>Iniciar sesión</v-btn>
                </v-form>
            </v-sheet>
        </v-sheet>
    </div>
</template>
  

<script>
import axios from 'axios';
import api_url from '../config.js';
import router from '../router.js';

export default {
    beforeCreate: function() {
        document.body.className = 'w-bg';
    },
    data() {
        return {
            username: '',
            password: '',
            show: false,
        };
    },
    methods: {
        async submitLoginForm() {
            try {
                const response = await axios.post(`${api_url}/login/`, {
                    username: this.username,
                    password: this.password,
                });
                
                // Se añade el jwt al localStorage
                console.log('Response:', response.data);
                const jwtToken = response.data.token; 
                localStorage.setItem('jwtToken', jwtToken);

            } catch (error) {
                console.error('Error:', error);
            }

            // Finalmente se redirige a '/'
            router.push({path:'/'});
        },
        login() {
            console.log('Username:', this.username);
            console.log('Password:', this.password);
        },
        show_pass() {
            this.show = !this.show;
            return this.show;
        },
    },
}
</script>
