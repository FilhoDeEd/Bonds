import { createApp } from "vue";
import { createPinia } from 'pinia'


/* eslint-disable */
// styles

import "@fortawesome/fontawesome-free/css/all.min.css";
import "@/assets/styles/tailwind.css";

// mouting point for the whole app
import App from "@/App.vue";
import axios from 'axios'
import router from "./router";



axios.defaults.baseURL = 'https//127.0.0.1:8000'

const app = createApp(App)
app.use(createPinia())
app.use(router,axios)


app.mount("#app");
