import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
// import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
})

// Uso de extensiones
const app = createApp(App)
app.use(vuetify)
app.use(router)
app.mount('#app')
