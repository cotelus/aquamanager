<template>
    <h1 class="text-white">Lecturas</h1>
    <v-card :loading="loading" class="mx-auto elevation-10" max-width="90vw">
        <v-data-table :header-props="headerProps" :headers="headers" :items="lecturas"
            :sort-by="[{ key: 'fecha', order: 'desc' }]" :search="search" :custom-filter="filterOnlyCapsText" item-value="name">
            <template v-slot:top>
                <v-toolbar flat>
                    <v-text-field v-model="search" label="Buscar lectura (Fecha)" class="pa-4 mt-4 mx-auto"
                        :prepend-icon="search ? 'mdi-magnify' : null" :append-icon="search ? 'mdi-close' : null"
                        @click:append="clearFilter" @input="convertToUpperCase"></v-text-field>
                    <v-dialog v-model="dialog" max-width="500px">
                        <template v-slot:activator="{ props }">
                            <v-btn color="primary" dark class="mb-2" v-bind="props">
                                Insertar hidrante
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title>
                                <span class="text-h5">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text>
                                <v-container>
                                    <v-row>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.name" label="Nombre"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.counter" label="Contador" type="number"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.topic" label="Tópico"></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue-darken-1" variant="text" @click="close">
                                    Cancelar
                                </v-btn>
                                <v-btn color="blue-darken-1" variant="text" @click="save">
                                    Guardar
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialogDelete" max-width="500px">
                        <v-card>
                            <v-card-title class="text-h5">¿Está seguro de borrar el hidrante?</v-card-title>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Calcelar</v-btn>
                                <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">Sí</v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>
            <template v-slot:[`item.valve_open`]="{ item }">
                <!-- <span v-html="changeValveText(item.raw)"></span> -->
                <v-img :src="changeValveText(item.raw)"  class="align-center" max-height="40px"></v-img>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
                <v-icon size="small" class="me-2" @click="editItem(item.raw)">
                    mdi-pencil
                </v-icon>
                <v-icon size="small" @click="deleteItem(item.raw)">
                    mdi-delete
                </v-icon>
            </template>
            <template v-slot:no-data>
                <v-btn color="primary" @click="initialize">
                    Reset
                </v-btn>
            </template>
        </v-data-table>
    </v-card>
</template>
  
<script setup>
import { VDataTable } from 'vuetify/labs/VDataTable'
</script>


<script>
import axios from 'axios';
import api_url from '../config.js';
import router from '../router.js';

export default {
    data: () => ({
        search: '',
        dialog: false,
        dialogDelete: false,
        headers: [
            {
                title: 'Valor',
                align: 'center',
                key: 'valor',
            },
            { title: 'Fecha', align: 'center', key: 'fecha' },
            { title: 'Hidrante', align: 'center', key: 'hidrante_id' },
            { title: 'Usuario', align: 'center', key: 'user_id' },
            { title: 'Acciones', key: 'actions', align: 'center', sortable: false },
        ],
        lecturas: [],
        editedIndex: -1,
        editedItem: {
            fecha: "2000-01-01 00:00:00",
            valor: 0,
            hidrante_id: -1,
            user_id: -1
        },
        defaultItem: {
            fecha: "2000-01-01 00:00:00",
            valor: 0,
            hidrante_id: -1,
            user_id: -1
        },
        headerProps: {
            class: 'font-weight-bold', // Aplica el estilo de negrita
        },
    }),
    mounted() {
        this.backToLogin();
        this.fetchLecturas();
    },
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'Nueva Lectura' : 'Editar Lectura'
        },
    },

    watch: {
        dialog(val) {
            val || this.close()
        },
        dialogDelete(val) {
            val || this.closeDelete()
        },
    },

    created() {
        this.initialize()
    },

    methods: {
        backToLogin() {
            if (!localStorage.getItem('jwtToken')) {
                router.push({ path: '/login' })
            }
        },
        changeValveText(value) {
            var bool = Boolean(value.valve_open)
            if (bool) {
                return require("@/assets/png/hydrant_on.png");
            } else {
                return require("@/assets/png/hydrant_off.png");

            }
        },
        fetchLecturas() {
            var jwtToken = localStorage.getItem('jwtToken');

            axios.get(`${api_url}/lecturas/`, {
                headers: {
                    'Authorization': jwtToken
                }
            })
                .then(response => {
                    this.lecturas = response.data['result'];
                    console.log(this.lecturas);
                })
                .catch(error => {
                    console.error(error);
                });
        },
        updateHydrant() {
            var jwtToken = localStorage.getItem('jwtToken');
            var updatedHydrant = this.editedItem;

            axios.put(`${api_url}/lecturas/`, updatedHydrant, {
            headers: {
                'Authorization': jwtToken
            }
            })
            .then(response => {
                console.log('Lectura actualizada:', response.data);
                this.close();
                this.fetchLecturas();
            })
            .catch(error => {
                console.error('Error al actualizar la lectura:', error);
            });
        },
        deleteItemConfirm() {
            var jwtToken = localStorage.getItem('jwtToken');
            var deleteHydrant = {
                "hydrant_id": this.editedItem.id
            };

            axios.delete(`${api_url}/lecturas/`, {
                headers: {
                    'Authorization': jwtToken
                },
                data: deleteHydrant,
                })
            .then(response => {
                console.log('Hidrante eliminado:', response.data);
                this.closeDelete();
                this.fetchLecturas();
            })
            .catch(error => {
                console.error(error);
            });
        },
        initialize() {
            this.clearFilter();
        },

        clearFilter() {
            this.search = '';
        },

        editItem(item) {
            this.editedIndex = this.lecturas.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem(item) {
            this.editedIndex = this.lecturas.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },
        close() {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        closeDelete() {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        save() {
            if (this.editedIndex > -1) {
                this.updateHydrant();
            } else {
                this.lecturas.push(this.editedItem);
            }
            this.close();
        },
        filterOnlyCapsText(value, query) {
            return value != null &&
                query != null &&
                typeof value === 'string' &&
                value.toString().toLocaleUpperCase().indexOf(query) !== -1
        },
        convertToUpperCase() {
            this.search = this.search.toUpperCase();
        },
    },
}
</script>

<style>
.v-data-table-header__content {
    font-weight: bold;
}
</style>
