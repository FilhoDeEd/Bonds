import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Landing.vue';
import Login from '../views/auth/Login.vue';
import Register from '../views/auth/Register.vue';
import Profile from '../views/Profile.vue'
// layouts

import Admin from "@/layouts/Admin.vue";
import Auth from "@/layouts/Auth.vue";

// views for Admin layout

import Dashboard from "@/views/admin/Dashboard.vue";
import Settings from "@/views/admin/Settings.vue";
import Tables from "@/views/admin/Tables.vue";
import Maps from "@/views/admin/Maps.vue";



// views without layouts
import Index from "@/views/Index.vue";

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
          path:"/",
          component: Login
        },
      ],
    },
    {
      path: "/home",
      component: Home,
    },
    {
      path: "/index",
      component: Index,
    },
    {
      path: "/profile",
      component: Profile,
    },
    // {
    //   path: "/",
    //   component: Index,
    // },
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
