<template>
    <div class="min-h-screen">
        <!-- Navbar fixa -->
        <nav class="fixed top-0 left-0 right-0 h-24 shadow-md z-50" style="background-color: #D76D65;">
            <div class="flex items-center justify-between h-full px-4">
                <!-- Left Side: Logo -->
                <div class="flex items-center space-x-4">
                    <h1 class="text-xl font-bold text-gray-800">Bonds</h1>
                </div>

                <!-- Center: Search Bar -->
                <div class="w-searchbar max-w-sm min-w-[200px]">
                    <div class="relative flex justify-end items-center">
                        <input v-model="searchQuery"
                            class="w-full bg-white placeholder:text-gray-400 text-gray-600 text-sm border border-slate-200 rounded-md pl-3 pr-24 py-2 transition duration-300 ease focus:outline-none focus:border-slate-400 hover:border-slate-300 shadow-sm focus:shadow"
                            placeholder="Busque por fóruns..." />

                        <button @click="handleSearch"
                            class="absolute flex items-center rounded bg-white py-1 px-4 border border-transparent text-center text-sm text-gray-100 transition-all shadow-sm hover:shadow focus:bg-gray-700 focus:shadow-none active:bg-gray-700 hover:bg-gray-700 active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
                            type="button">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                                class="w-4 h-4 mr-2">
                                <path fill-rule="evenodd"
                                    d="M10.5 3.75a6.75 6.75 0 1 0 0 13.5 6.75 6.75 0 0 0 0-13.5ZM2.25 10.5a8.25 8.25 0 1 1 14.59 5.28l4.69 4.69a.75.75 0 1 1-1.06 1.06l-4.69-4.69A8.25 8.25 0 0 1 2.25 10.5Z"
                                    clip-rule="evenodd" />
                            </svg>
                            Buscar
                        </button>
                    </div>
                </div>

                <!-- Right Side: Profile -->
                <div class="flex items-center">
                    <button @click="$router.push('/profile')"
                        class="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 transition overflow-hidden">
                        <img alt="Foto de Perfil" :src="profileImage" class="w-full h-full object-cover">
                    </button>
                </div>
            </div>
        </nav>

        <!-- Container principal -->
        <div class="pt-24 flex">
            <!-- Sidebar fixa -->
            <aside class="fixed left-0 w-64 h-screen" style="background-color: rgb(235, 143, 138);">
                <div class="flex flex-col h-full relative">
                    <nav class="space-y-2 py-6">
                        <MenuItem v-for="item in menuItems" :key="item.id" :icon="item.icon" :title="item.title"
                            :path="item.path" :active="activeItem === item.id" @click="activeItem = item.id"
                            :expanded="true" />
                    </nav>
                    <div class="absolute bottom-0 left-0 right-0 flex justify-center pb-6">
                        <img :src="altLogo" alt="Alt Logo" class="w-32 h-auto" />
                    </div>
                </div>
            </aside>

            <!-- Área de conteúdo -->
            <div class="pl-64 flex-1">
                <div class="p-6">
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import MenuItem from "../components/Sidebar/MenuItem.vue";
import { useForumListStore } from "../store/forumListStore.js";
import router from "../router/index.js";
import { computed } from "vue";
import { useUserStore } from "../store/user.js";
import altLogo from "@/assets/img/altLogo.png";

import profile from "@/assets/img/profilePic.jpg";

const activeItem = ref("home");
const searchQuery = ref("");

const menuItems = [
    { id: "home", icon: "home", title: "Página Inicial", path: "/home" },
    { id: "about", icon: "info", title: "Sobre", path: "/about" }
];

const userStore = useUserStore();
const forumListStore = useForumListStore();

const handleSearch = async () => {
    forumListStore.setSearchQuery(searchQuery.value);
    await forumListStore.fetchForums();
    router.push("/home");
};

const profileImage = computed(() => {
    return userStore.user.account.profile_image || profile;
});
</script>

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.search-input {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' class='h-5 w-5' viewBox='0 0 20 20' fill='%239CA3AF'%3E%3Cpath fill-rule='evenodd' d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z' clip-rule='evenodd'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 20px;
}
</style>