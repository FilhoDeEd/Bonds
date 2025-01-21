import { createRouter, createWebHistory } from 'vue-router';
//import Home from '../views/Landing.vue';
import Login from '../views/auth/Login.vue';
import Register from '../views/auth/Register.vue';
import Profile from '../views/Profile.vue'
import AboutPage from '../views/AboutPage.vue'
// layouts
import mainLayout from '@/layouts/mainLayout.vue'
//visualizar forum
import ForumDetailPage from "@/views/ForumDetailPage.vue";

import Landing from '@/views/Landing.vue'
import Admin from "@/layouts/Admin.vue";
import Auth from "@/layouts/Auth.vue";
// views for Admin layout

import Dashboard from "@/views/admin/Dashboard.vue";
import Settings from "@/views/admin/Settings.vue";
import Tables from "@/views/admin/Tables.vue";
import Maps from "@/views/admin/Maps.vue";


// views without layouts
import Index from "@/views/Index.vue";
import EventDetailPage from '../views/EventDetailPage.vue';
import { useUserStore } from '../store/user';

/* eslint-disable */

const routes = [
  
  {
    path: "/admin",
    redirect: "/admin/dashboard",
    component: Admin,
    children: [
      {
        path: "/admin/dashboard",
        component: Dashboard,
      },
      {
        path: "/admin/settings",
        component: Settings,
      },
      {
        path: "/admin/tables",
        component: Tables,
      },
      {
        path: "/admin/maps",
        component: Maps,
      },
    ],
  },
  {
    path: "/auth",
    redirect: "/auth/login",
    component: Auth,
    beforeEnter: (to, from, next) => {
      const userStore = useUserStore(); // Acessa a store
      userStore.removeToken(); // Remove o token
      next(); // Prossegue para a rota
    },

    children: [
      {
        path: "/auth/login",
        component: Login,
      },
      {
        path: "/auth/register",
        component: Register,
      },
      {
        path: "/",
        component: Login
      },
    ],
  },
  // {
  //   path: "/home",
  //   component: Home,
  // },
  {
    path: '/home',
    component: Landing,
    children: [
      {
        path: '',
        component: mainLayout,  // Mudança aqui
        name: 'mainLayout'  // Opcional: também atualizei o nome
      },
      // Outras rotas permanecem iguais
    ]
  },
  {
    path: "/index",
    component: Index,
  },
  {
    path: "/profile",
    component: Profile,
    name: 'Profile',
  },
  //para o Edson ter algo com que trabalhar.
  {
    path: "/forum/:slug",
    component: ForumDetailPage,
    name: 'ForumDetailPage',
    props: true,
  },
  {
    path: "/forum/event/:slug",
    component: EventDetailPage,
    name: 'EventDetailPage',
    props: true,
  },
  {
    path: "/about",
    component: AboutPage,
    name: 'AboutPage',
  },


  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;