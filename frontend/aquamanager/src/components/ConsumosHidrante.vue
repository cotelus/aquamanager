<template>
  <h1 class="text-white">Consumos</h1>
  <v-card :loading="loading" class="mx-auto elevation-10" max-width="80vw">
    <v-card-text>
      <v-row>
        <v-col cols="4" class="d-flex align-center">
          <v-text-field type="date" id="datepicker" v-model="lowDate" label="Fecha Inferior"></v-text-field>
        </v-col>
        <v-col cols="4" class="d-flex align-center">
          <v-text-field type="date" id="datepicker" v-model="highDate" label="Fecha Superior"></v-text-field>
        </v-col>
        <v-col cols="2" class="d-flex align-center">
          <v-select v-model="selectedHydrant" :items="hydrantsNames" item-text="name" label="Hidrante"></v-select>
        </v-col>
        <v-col cols="2" class="pt-6 align-center">
          <v-btn @click="calcularConsumos" color="primary" dark>Calcular<br>consumo</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <p>Consumo: {{ hydrantConsumptionValue }}</p>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios';
import api_url from '../config.js';
import router from '../router.js';

export default {
  data() {
    return {
      hydrantConsumption: null,
      lowDate: null,
      highDate: null,
      startReading: 0,
      endReading: 0,
      selectedHydrant: '',
      hydrantName: '',
      hydrantConsumptionValue: '',
      hydrants: [],
      hydrantsNames: [],
      data: [],
      headers: [
        { text: 'Fecha Inicial', value: 'lowDate' },
        { text: 'Fecha Final', value: 'highDate' },
        { text: 'Lectura Inicial', value: 'startReading' },
        { text: 'Lectura Final', value: 'endReading' },
        { text: 'Hidrante', value: 'hydrantName' },
        { text: 'Consumo', value: 'hydrantConsumptionValue' },
      ],
    };
  },
  mounted() {
    this.backToLogin();
    this.fetchContadores();
  },
  methods: {
    calcularConsumos() {
      var jwtToken = localStorage.getItem('jwtToken');
      var sendData = {
        "fecha_inicial": this.getTimestamp(this.lowDate),
        "fecha_final": this.getTimestamp(this.highDate),
        "nombre_hidrante": this.selectedHydrant
      };

      axios.post(`${api_url}/consumos/`, sendData, {
        headers: {
          'Authorization': jwtToken
        },
      })
        .then((response) => {
          this.data = response.data;
          this.hydrantConsumption = response.data['result'];
          this.hydrantConsumptionValue = response.data['result']['valor'];
          console.log(response.data['result']['valor']);
        })
        .catch((error) => {
          console.error(error);
          console.log(sendData);
          console.log(jwtToken);
        });
    },
    fetchContadores() {
      var jwtToken = localStorage.getItem('jwtToken');

      axios.get(`${api_url}/hidrantes/`, {
        headers: {
          'Authorization': jwtToken
        }
      })
        .then(response => {
          this.hydrants = response.data['result'];

          this.hydrants.forEach((hydrant) => {
            this.hydrantsNames.push(hydrant.name);
          });
          console.log(this.hydrants);
        })
        .catch(error => {
          console.error(error);
        });
    },
    getTimestamp(date) {
      if (!date) return null;
      const timestamp = new Date(date).getTime();
      return timestamp;
    },
    backToLogin() {
      if (!localStorage.getItem('jwtToken')) {
        router.push({ path: '/login' })
      }
    },
  },
};
</script>
