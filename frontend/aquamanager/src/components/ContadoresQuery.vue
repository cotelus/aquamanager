<template>
    <v-card :loading="loading" class="mx-auto elevation-10" max-width="90vw">
        <v-data-table :header-props="headerProps" :headers="headers" :items="contadores"
            :sort-by="[{ key: 'id', order: 'asc' }]" :search="search" :custom-filter="filterOnlyCapsText" item-value="name">
            <template v-slot:top>
                <v-toolbar flat>
                    <v-text-field v-model="search" label="Buscar hidrante (MAYUS)" class="pa-4 mt-4 mx-auto"
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
                                            <v-text-field v-model="editedItem.counter" label="Contador"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.topic" label="Tópico"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.userId" label="Usuario"></v-text-field>
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

export default {
    data: () => ({
        search: '',
        dialog: false,
        dialogDelete: false,
        headers: [
            {
                title: 'ID',
                align: 'center',
                key: 'id',
            },
            { title: 'Nombre', align: 'center', key: 'name' },
            { title: 'Totalizador', align: 'center', key: 'counter' },
            { title: 'Válvula abierta', align: 'center', key: 'valve_open' },
            { title: 'Tópico', align: 'center', key: 'topic' },
            { title: 'Acciones', key: 'actions', align: 'center', sortable: false },
        ],
        contadores: [],
        editedIndex: -1,
        editedItem: {
            name: '',
            calories: 0,
            fat: 0,
            carbs: 0,
            protein: 0,
        },
        defaultItem: {
            name: '',
            calories: 0,
            fat: 0,
            carbs: 0,
            protein: 0,
        },
        headerProps: {
            class: 'font-weight-bold', // Aplica el estilo de negrita
        },
    }),
    mounted() {
        this.fetchContadores();
    },
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'Nuevo Hidrante' : 'Editar Hidrante'
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
        changeValveText(value) {
            var bool = Boolean(value.valve_open)
            if (bool) {
                return require("@/assets/png/hydrant_on.png");
            } else {
                return require("@/assets/png/hydrant_off.png");

            }
        },
        fetchContadores() {
            axios.get(`${api_url}/hidrantes/`)
                .then(response => {
                    this.contadores = response.data['result'];
                    console.log(this.contadores);
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
            this.editedIndex = this.desserts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem(item) {
            this.editedIndex = this.desserts.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialogDelete = true
        },

        deleteItemConfirm() {
            this.desserts.splice(this.editedIndex, 1)
            this.closeDelete()
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
                Object.assign(this.contadores[this.editedIndex], this.editedItem)
            } else {
                this.contadores.push(this.editedItem)
            }
            this.close()
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
