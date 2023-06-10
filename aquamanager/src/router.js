import { createRouter, createWebHistory } from 'vue-router';
import NotFoundError404 from './components/NotFoundError404.vue';
import ContadoresQuery from './components/ContadoresQuery.vue';
import Inicio from './components/Inicio.vue';
import LoginForm from './components/LoginForm.vue';

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
    path: '/:catchAll(.*)',
    component: NotFoundError404
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
