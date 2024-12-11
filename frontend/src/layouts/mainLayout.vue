<template>
    <div class="flex flex-col min-h-screen w-full bg-blueGray-600">
        <!-- Navbar -->
        <nav class="w-full h-24 shadow-md" style="background-color: #D76D65;">
            <div class="flex items-center justify-between h-full px-4">
                <!-- Left Side: Logo -->
                <div class="flex items-center space-x-4">
                    <h1 class="text-xl font-bold text-gray-800">MyApp</h1>
                </div>

                <!-- Center: Search Bar -->
                <div class="flex-grow mx-4">
                    <div class="relative flex w-full items-center justify-center">
                        <input type="text" placeholder="Pesquisar..."
                            class="w-10/12 px-4 py-2 pr-10 rounded-full border border-gray-300 focus:outline-none focus:border-blue-500 search-input">
                    </div>
                </div>

                <!-- Right Side: Profile -->
                <div class="flex items-center">
                    <button @click="$router.push('/profile')" class="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 transition overflow-hidden">
                        <img src="https://via.placeholder.com/40" alt="Profile" class="w-full h-full object-cover">
                    </button>
                </div>
            </div>
        </nav>

        <!-- Container principal com flex row -->
        <div class="flex flex-1 ">
            <!-- Sidebar sempre visível -->
            <aside class="w-64 border-r shadow-lg" style="background-color: #D76D65;">
                <div class="flex flex-col h-full py-6">
                    <nav class="space-y-2">
                        <MenuItem v-for="item in menuItems" :key="item.id" :icon="item.icon" :title="item.title"
                            :active="activeItem === item.id" @click="activeItem = item.id" :expanded="true" />
                    </nav>
                </div>
            </aside>

            <!-- Área de conteúdo -->
            <div class="flex-1">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import MenuItem from '../components/MenuItem.vue'

const activeItem = ref('home')

const menuItems = [
    { id: 'home', icon: 'home', title: 'Página Inicial' },
    { id: 'forums', icon: 'forum', title: 'Fóruns' },
    { id: 'events', icon: 'event', title: 'Eventos' },
    { id: 'reports', icon: 'report', title: 'Denúncias' },
    { id: 'about', icon: 'info', title: 'Sobre' }
]
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