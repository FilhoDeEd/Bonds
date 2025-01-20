<template>
  <mainLayout>
    <!-- Navbar específica da Landing -->
    <div class="mx-auto  bg-white">
      <div class="w-full flex justify-end h-[40px] py-4" style="background-color: rgba(124, 122, 187, 1);">
        <button class="px-6 py-2 mr-10 text-white font-semibold rounded-lg transition-all duration-200 hover:bg-opacity-90"
          style="background-color: rgb(240, 117, 117);"
          @click="openModalEvent"
          >
          <span>Criar Evento</span>
        </button>
        <button class="px-6 py-2 mr-10 text-white font-semibold rounded-lg transition-all duration-200 hover:bg-opacity-90"
          style="background-color: rgb(240, 117, 117);"
          @click="openModal"
          >
          <span>Criar Fórum</span>
        </button>
      </div>

      <main class="flex-1">
        <section id="conteudo ">

          <div v-infinite-scroll="onLoadMore" class="space-y-4 ml-[-120px]">

            <div v-for="forum in forumListStore.forums" :key="forum.forum_id"
              class="p-4 shadow rounded hover:shadow-lg transition-shadow duration-200 w-[70%] mx-auto"
              
              :style="{ backgroundColor: getColor(forum) }">
              <div class="flex h-full">
                <!-- Imagem à esquerda -->
                <div class="w-1/4 flex items-center">
                  <img 
                    :src="forum.banner_image_low || banner_list_default" 
                    alt="Forum image" 
                    class="object-fit w-full h-48" 
                    style="max-width: 100%; max-height: 150px;" />
                </div>
                  <!-- Conteúdo à direita -->
                  <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                    <div v-if="forum.type === 'E'">
                      <router-link  :to="{ name: 'EventDetailPage', params: { slug: forum.slug } }"
                        class="text-white flex flex-col h-full justify-between">
                        <h2 :value="forum.title" class="text-4xl font-semibold mb-8">
                          {{ forum.title }}
                        </h2>
                        <h3>Evento</h3>
                        <div class="text-2xl text-gray-100 flex flex-col justify-between flex-grow">
                          <p class="mb-auto leading-relaxed">{{ forum.description }}</p>
                          <p class="mt-8">Popularidade: {{ forum.popularity }}</p>
                        </div>
                      </router-link>
                  </div>
                  <div v-else>
                    <router-link  :to="{ name: 'ForumDetailPage', params: { slug: forum.slug } }"
                      class="text-white flex flex-col h-full justify-between">
                      <h2 :value="forum.title" class="text-4xl font-semibold mb-8">
                        {{ forum.title }}
                      </h2>
                      <h3>Fórum</h3>
                      <div class="text-2xl text-gray-100 flex flex-col justify-between flex-grow">
                        <p class="mb-auto leading-relaxed">{{ forum.description }}</p>
                        <p class="mt-8">Popularidade: {{ forum.popularity }}</p>
                      </div>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Componente de carregamento infinito -->
          <InfiniteLoading @infinite="onLoadMore" spinner="waveDots" :identifier="forumListStore.next">
            <template #complete>
              <div class="text-center text-gray-500 mt-4">
                <span>"Isso é tudo, pessoal" ~ Pernalonga</span>
              </div>
            </template>
          </InfiniteLoading>
        </section>
        <div>
          <ModalCreateForum
            v-if="isModalOpen"
            :isModalOpen="isModalOpen"
            @close="isModalOpen = false"
          />
        </div>
        <div>
          <ModalCreateEvent
            v-if="isModalEventOpen"
            :isModalOpen="isModalEventOpen"
            @close="isModalEventOpen = false"
          />
        </div>
      </main>
    </div>
  </mainLayout>
</template>


<script>
import mainLayout from "@/layouts/mainLayout.vue";
import { useForumListStore } from "@/store/forumListStore.js";
import { useUserStore } from "@/store/user.js";
import { onBeforeMount } from "vue";
import InfiniteLoading from "v3-infinite-loading/lib/v3-infinite-loading.es.js";
import "v3-infinite-loading/lib/style.css";
import ModalCreateForum from "../components/Modals/ModalCreateForum.vue";
import ModalCreateEvent from "../components/Modals/ModalCreateEvent.vue";
import banner_list_default from "@/assets/img/placeholder_banner_list.png";

export default {
  name: "Landing",
  components: {
    mainLayout,
    InfiniteLoading,
    ModalCreateForum,
    ModalCreateEvent,
  },
  data() {
    return {
      isModalOpen: false, // Defina aqui no data
      isModalEventOpen: false,
    };
  },
  setup() {
    const forumListStore = useForumListStore();
    const userStore = useUserStore();

    // Função para carregar mais itens
    const onLoadMore = async ($state) => {
      if (!forumListStore.next) {
        $state.complete(); // Finaliza o carregamento se não houver mais páginas
        return;
      }

      try {
        await forumListStore.fetchForums();
        $state.loaded(); // Indica que os itens foram carregados
      } catch (error) {
        $state.error(); // Indica erro no carregamento
      }
    };

    onBeforeMount(() => {
      if (userStore.user.isAuthenticated) {
        if (forumListStore.forums.length === 0) {
          forumListStore.fetchForums();
        }
      } else {
        alert("Usuário Não Autorizado");
      }
    });

    return {
      forumListStore,
      banner_list_default,
      onLoadMore,
    };
  },
  methods: {
    openModal() {
      this.isModalOpen = true; // Abre o modal
    },
    closeModal() {
      this.isModalOpen = false; // Fecha o modal
    },
    openModalEvent() {
      this.isModalEventOpen = true; // Abre o modal
    },
    closeModalEvent() {
      this.isModalEventOpen = false; // Fecha o modal
    },
    getColor(forum) {
      // Replace this with your logic to determine the color based on the forum
      return forum.type === 'U' || forum.type === 'D' ? 'rgba(124, 122, 187, 1)' : 'rgb(240, 117, 117)';
    },


  },

};
</script>

<style>
/* Global Reset */
body,
html {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Arial', sans-serif;
}

/* Para garantir que o conteúdo principal não sobreponha a navbar */
main {
  margin-top: 20px;
  /* Espaço suficiente abaixo da navbar */
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

.space-y-4>*+* {
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
h1,
h2 {
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

/* Estilo adicional para o botão */
button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
