import { createRouter, createWebHistory } from 'vue-router';
import ContadoresQuery from './components/ContadoresQuery.vue';
import Inicio from './components/Inicio.vue';

const routes = [
  {
    path: '/',
    component: Inicio
  },
  {
    path: '/contadores',
    component: ContadoresQuery
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
