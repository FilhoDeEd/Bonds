<template>
    <MainLayout>
        <div class="w-8/12 h-full py-8 pr-20 pl-20 bg-gray-50 space-y-4">
          <main>
          <section id="contenido">
            <h1 class="text-xl font-bold mb-4">Postagens</h1>
            <div class="space-y-4">
              <article 
                v-for="forum in forumStore.forums" 
                :key="forum.forum_id"  
                class="p-4 shadow rounded hover:shadow-lg transition-shadow duration-200"
                style="background-color: rgba(124, 122, 187, 1); width: 1500px; height: 415px;"
              >
                <div class="flex h-full">
                  <!-- Imagem à esquerda -->
                  <div class="w-1/4 flex items-center">
                    <img 
                      src="https://via.placeholder.com/300x200" 
                      alt="Forum image" 
                      class="object-cover w-full"
                      style="height: 70%;"
                    >
                  </div>
                  
                  <!-- Conteúdo à direita - agora ocupando todo o espaço restante -->
                  <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                    <a href="#" class="text-white flex flex-col h-full justify-between">
                      <h2 
                        :value="forum.title" 
                        class="text-4xl font-semibold mb-8"
                      >
                        {{ forum.title }}
                      </h2>
                      <div class="text-2xl text-gray-100 flex flex-col justify-between flex-grow">
                        <p class="mb-auto leading-relaxed">{{ forum.description }}</p>
                        <p class="mt-8">Popularidade: {{ forum.popularity }}</p>
                      </div>
                    </a>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </main>
        </div>
    </MainLayout>
</template>


<script>
import { useForumStore } from '@/store/forum.js'; // Certifique-se de ajustar o caminho
import { useUserStore } from '@/store/user.js';
import {onBeforeMount } from "vue";
import MainLayout from '../layouts/mainLayout.vue';


export default {
  components: {
    MainLayout
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
