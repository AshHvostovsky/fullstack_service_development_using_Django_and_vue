import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Dropdown } from 'bootstrap/dist/js/bootstrap.bundle.min.js'

import "bootstrap/dist/css/bootstrap.css" // Стили Bootstrap
import "bootstrap-icons/font/bootstrap-icons.min.css" // Иконки Bootstrap
import "bootstrap/dist/js/bootstrap.min.js" // Скрипты Bootstrap (включая Popper.js)

import "bootstrap/dist/css/bootstrap.min.css";





import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia();


app.use(pinia)
app.use(router)

app.mount('#app')
