<template>
  <div class="flex flex-col h-screen">
    <!-- Navbar na parte superior -->
    <div class="bg-gray-800 text-white shadow-lg">
      <NavbarHome />
    </div>

    <!-- Conteúdo Principal com Sidebars -->
    <div class="flex flex-1 overflow-hidden justify-between">
      <!-- Sidebar Esquerda -->
      <div class="w-64 bg-gray-900 text-white p-4 hidden lg:block">
        <Sidebar />
      </div>

      <!-- Conteúdo Principal -->
      <div class="flex-1 bg-gray-100 p-6 overflow-y-auto">
        <main>
          <section id="contenido">
            <h1 class="text-xl font-bold mb-4">Postagens</h1>
            <div class="space-y-4">
              <!-- Simulação de Postagens -->
              <article 
                v-for="forum in forumStore.forums" 
                :key="forum.forum_id" 
                class="p-4 bg-white shadow rounded"
              >
                <a href="#">
                  <h2 
                    :value="forum.title" 
                    class="text-lg font-semibold"
                  >
                    {{ forum.title }}
                  </h2>
                  <div class="text-sm text-gray-600 space-between">
                    <p>{{ forum.description }}</p>
                    <p>Popularidade: {{ forum.popularity }}</p>
                  </div>
                </a>
              </article>
            </div>
          </section>
        </main>
      </div>

      <!-- Sidebar Direita -->
      <div class="w-64 bg-gray-100 text-black p-4 hidden lg:block">
        <SidebarSugere />
      </div>
    </div>

    <!-- Rodapé -->
    <div class="bg-gray-800 text-white p-2">
      <FooterComponent />
    </div>
  </div>
</template>


<script>
import { useForumStore } from '@/store/forum.js'; // Certifique-se de ajustar o caminho
import { useUserStore } from '@/store/user.js';
import {onBeforeMount } from "vue";
import NavbarHome from '../components/Navbars/NavbarHome.vue';
import Sidebar from '../components/Sidebar/Sidebar.vue';
import SidebarSugere from '../components/Sidebar/SidebarSugere.vue';
import FooterComponent from '../components/Footers/FooterHome.vue';


export default {
  components: {
    NavbarHome,
    FooterComponent,
    Sidebar,
    SidebarSugere,
  },
  
  setup() {
    const forumStore = useForumStore();
    const userStore = useUserStore();

    // Carrega os fóruns na montagem do componente
    onBeforeMount(() => {
      userStore.initStore();
      if (userStore.user.isAuthenticated) {
        forumStore.fetchForums(1); // Chama a função para carregar os fóruns
      } else {
        alert("Usuário Não Autorizado");
      }
    });

    // Função para chamar a fetch de fóruns
    const fetchForums = (page) => {
      forumStore.fetchForums(page);
    };

    return {
      forumStore,
      userStore,
      fetchForums, // Adiciona a função fetchForums ao template
    };
  },
};
</script>

<style>
/* Global Reset */
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Arial', sans-serif;
}

/* Para garantir que o conteúdo principal não sobreponha a navbar */
main {
  margin-top: 20px; /* Espaço suficiente abaixo da navbar */
}

/* Estilo para o rodapé */
footer {
  margin-top: auto;
}

/* Ajustes de layout */
.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.h-screen {
  height: 100vh;
}

.flex-1 {
  flex: 1;
}

/* Sidebar */
aside {
  transition: transform 0.3s ease-in-out;
}

.w-64 {
  width: 16rem;
}

/* Responsividade para telas grandes */
@media (min-width: 1024px) {
  .hidden {
    display: block;
  }
  .lg\\:block {
    display: block;
  }
  .lg\\:hidden {
    display: none;
  }
}

/* Estilo de conteúdo */
.bg-gray-800 {
  background-color: #2d3748;
}

.bg-gray-100 {
  background-color: #f7fafc;
}

.text-white {
  color: #fff;
}

.text-black {
  color: #000;
}

.p-4 {
  padding: 1rem;
}

.p-6 {
  padding: 1.5rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

/* Estilo para os artigos de postagens */
article {
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 0.375rem;
  padding: 1rem;
}

/* Ajustes específicos para sidebars */
.sidebar {
  position: relative;
}

/* Títulos */
h1, h2 {
  font-size: 1.25rem;
}

.font-bold {
  font-weight: 700;
}

.font-semibold {
  font-weight: 600;
}

/* Estilo para rodapé */
footer {
  background-color: #2d3748;
  color: #fff;
  padding: 1rem;
  text-align: center;
}

</style>
