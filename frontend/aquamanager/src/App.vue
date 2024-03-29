<template>
  <div id="app">
    <!-- Barra de navegación que será heredada para todas las demás vistas -->
    <div v-if="drawerOpen" class="drawer-overlay" @click="toggleDrawer"></div>
    <v-layout>
      <v-navigation-drawer v-model="drawerOpen" color="#3490c9" app>
        <v-list>
          <v-list-item v-for="route in drawerRoutes" :key="route.path" @click="navigateToPage(route.path)">
            <v-list-item-icon>
              <v-icon class="text-white font-weight-bold">{{ route.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title class="text-white font-weight-bold">{{ route.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-app-bar color="#3490c9" density="compact" class="text-white font-weight-bold">
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click="toggleDrawer"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title style="cursor: default;">
          <span @mouseover="changeCursor" @mouseleave="resetCursor" @click="navigateToPage('/', false)" span
            style="cursor: pointer;">AquaManager</span>
        </v-app-bar-title>

        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon>
              <v-icon v-bind="props">mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in threeDotsItems" :key="index" :value="index"
              @click="handleItemClick(item)">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>
    </v-layout>

    <router-view></router-view>
  </div>
</template>

<script>
import router from './router.js';

export default {
  name: 'App',
  beforeCreate: function () {
    document.body.className = 'w-bg';
  },
  data() {
    return {
      drawerOpen: false,
      drawerRoutes: [
        { path: '/', name: 'Inicio', icon: 'mdi-home' },
        { path: '/comuneros', name: 'Comuneros', icon: 'mdi-account-group-outline' },
        { path: '/contadores', name: 'Hidrantes', icon: 'mdi-water-outline' },
        { path: '/lecturas', name: 'Lecturas', icon: 'mdi-book-open-outline' },
        { path: '/consumos', name: 'Consumo', icon: 'mdi-cash-multiple' },
        { path: '/about', name: 'Sobre mi', icon: 'mdi-information' }
      ],
      threeDotsItems: [
        { title: 'Perfil', action: 'toUser' },
        { title: 'Cerrar sesión', action: 'logout' },
      ],
    };
  },
  methods: {
    navigateToPage(route, toggle = true) {
      if (toggle) {
        this.toggleDrawer();
      }
      router.push({ path: route });
    },
    toggleDrawer() {
      this.drawerOpen = !this.drawerOpen;
    },
    changeCursor() {
      document.body.style.cursor = 'pointer';
    },
    resetCursor() {
      document.body.style.cursor = 'default';
    },
    logout() {
      console.log('Cerrando sesión de usuario');
      localStorage.removeItem('jwtToken');
      router.push({ path: '/login' });
    },
    handleItemClick(item) {
      const action = item.action;
      if (action && typeof this[action] === 'function') {
        this[action]();
      }
    },
    toUser() {
      router.push({ path: '/contadores' });
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');

#app {
  font-family: Montserrat;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 40px;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

@keyframes waveAnimation {
  0% {
    background-position: 0% 50%
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

@-webkit-keyframes waveAnimation {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.w-bg {
  height: 100%;
  justify-content: center;
  background-size: 300% 300%;
  background-image: linear-gradient(-45deg, rgba(62, 181, 155, 0.5) 0%, rgba(54, 155, 201, 0.5) 25%, rgba(62, 181, 155, 0.5) 51%, rgba(54, 155, 201, 0.5) 100%);
  -webkit-animation: waveAnimation 10s ease infinite;
  animation: waveAnimation 10s ease infinite;
}
</style>
