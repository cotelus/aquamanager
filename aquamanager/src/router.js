import { createRouter, createWebHistory } from 'vue-router';
import NotFoundError404 from './components/NotFoundError404.vue';
import ContadoresQuery from './components/ContadoresQuery.vue';
import ComuneroDetalle from './components/ComuneroDetalle.vue';
import ComunerosList from './components/ComunerosList.vue';
import Inicio from './components/Inicio.vue';
import LoginForm from './components/LoginForm.vue';
import LecturasTable from './components/LecturasTable.vue';

const routes = [
  {
    path: '/',
    component: Inicio
  },
  {
    path: '/login',
    component: LoginForm
  },
  {
    path: '/contadores',
    component: ContadoresQuery
  },
  {
    path: '/comuneros',
    component: ComunerosList
  },
  {
    path: '/comuneros/:id',
    component: ComuneroDetalle
  },
  {
    path: '/lecturas',
    component: LecturasTable
  },
  {
    path: '/:catchAll(.*)',
    component: NotFoundError404
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
