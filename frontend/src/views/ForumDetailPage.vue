<template>
  <MainLayout>
    <div class="w-8/12 h-full py-8 pr-20 pl-20 bg-gray-50">
      <!-- Banner Section -->
      <div class="bg-white h-400-px p-6 rounded-lg shadow mb-8">
        <div class="relative h-full">
          <!-- Área colorida do banner - aumentada para 85% -->
          <div class="absolute top-0 left-0 right-0 h-85" 
               style="background-color: rgba(124, 122, 187, 1);">
          </div>

          <!-- Conteúdo do banner -->
          <div class="relative h-full flex flex-col justify-between">
            <!-- Área de título e descrição -->
            <div class="px-6 py-8">
              <div class="container mx-auto flex flex-col items-start">
                <!-- Título editável -->
                <input 
                  type="text" 
                  v-model="forumData.title" 
                  :readonly="!editMode"
                  class="text-white text-3xl font-bold mb-4 bg-transparent border-none w-full"
                  :class="{'hover:bg-gray-700/30': editMode}"
                  placeholder="Título do Fórum"
                >
                
                <!-- Descrição editável -->
                <textarea 
                  v-model="forumData.description" 
                  :readonly="!editMode"
                  class="text-white text-base mb-4 bg-transparent border-none w-full resize-none"
                  :class="{'hover:bg-gray-700/30': editMode}"
                  placeholder="Descrição do fórum"
                  rows="3"
                ></textarea>
              </div>
            </div>

            <!-- Botões alinhados ao bottom -->
            <div class="px-6 pb-4 flex space-x-4 relative z-10">
              <button type="button" 
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200"
                style="background-color: rgb(252, 3, 94);">
                Participar
              </button>
              
              <button type="button" 
                @click="toggleEdition"
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200"
                style="background-color: rgb(252, 3, 94);">
                {{ editMode ? 'Salvar' : 'Editar' }}
              </button>

              <button type="button" 
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200"
                style="background-color: rgb(252, 3, 94);">
                Denunciar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow mb-8">
        <div class="container mx-auto">
          <h2 class="text-2xl font-bold mb-4">Engaje no fórum!</h2>

          <!-- Área de criação de post -->
          <div class="border rounded-lg p-4">
            <div class="flex items-start space-x-4">
              <img src="https://via.placeholder.com/40" class="w-10 h-10 rounded-full" alt="Seu perfil">
              <div class="flex-1">
                <textarea
                  v-model="newCommentContent"
                  class="w-full p-3 rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none"
                  placeholder="No que você está pensando?" rows="3"></textarea>

                <!-- Botões de ação -->
                <div class="flex items-center mt-4 pt-3 border-t">
                  <div class="flex space-x-2">
                    <button class="p-2 hover:bg-gray-100 rounded-full" title="Adicionar foto/vídeo">
                      <span>📷</span>
                    </button>
                    <button class="p-2 hover:bg-gray-100 rounded-full" title="Localização">
                      <span>📍</span>
                    </button>
                  </div>

                  <button 
                  @click="createComment"
                  class="ml-auto px-6 py-2 bg-blue-500 text-Black rounded-lg hover:bg-blue-600 font-semibold">
                    Publicar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Section with Posts and Sidebar -->
      <div class="flex gap-8 space-x-4 ">
        <!-- Posts Section -->
        <div class="w-3/4">
          <div class="space-y-4">
            <article v-for="comment in comments" :key="comment.createdAt" class="p-4 shadow rounded hover:shadow-lg transition-shadow duration-200" style="background-color: rgba(124, 122, 187, 1);">
              <div class="flex h-full">

                <!-- Área de votação -->
                <div class="flex flex-col items-center text-white text-2xl font-bold w-12">
                  <button class="hover:opacity-80 transition-opacity">
                    <img :src="upvoteIcon" alt="Upvote" class="w-6 h-6">
                  </button>
                  <span class="my-1">0</span>
                  <button class="hover:opacity-80 transition-opacity">
                    <img :src="downvoteIcon" alt="Downvote" class="w-6 h-6">
                  </button>
                </div>

                <!-- Imagem do autor do comentário -->
                <div class="w-1/4 h-70-px flex flex-col pt-12 ">
                  <img src="https://via.placeholder.com/300x200" alt="Imagem do autor" class="object-cover w-full" style="height: 70%;">
                  
                  <!-- Menu dropdown -->
                  
                </div>
                
                <!-- Conteúdo do comentário -->
                <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                  <div class="text-white flex flex-col h-full justify-between">
                    <!-- Menu dropdown -->
                    <div class="relative self-end mb-2">
                      <button @click="toggleMenu(comment.id)" 
                              class="text-white text-xl hover:text-gray-300">
                        ⋯
                      </button>
                      
                      <!-- Dropdown menu -->
                      <div v-if="menuStates[comment.id]" 
                           class="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-2 z-10">
                        <button @click="menuStates[comment.id] = false" 
                                class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                          Deletar
                        </button>
                        <button @click="menuStates[comment.id] = false" 
                                class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                          Reportar
                        </button>
                      </div>
                    </div>

                    <!-- Título ou nome do autor -->
                    <h2 class="text-lg font-semibold mb-8">{{ comment.creator }}</h2>
                    
                    <!-- Texto do comentário -->
                    <div class="text-lg text-gray-100 flex flex-col justify-between flex-grow">
                      <p class="mb-auto leading-relaxed">{{ comment.content }}</p>
                      
                      <!-- Detalhes do comentário -->
                      <p class="mt-8">{{ comment.createdAt }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>

        <!-- Sidebar -->
        <aside class="w-1/4 bg-white p-4 rounded-lg shadow-lg h-fit">
          <h3 class="text-lg font-semibold mb-4">Informações Adicionais</h3>
          <div class="space-y-4">
            <div class="p-3 bg-gray-50 rounded">
              <h4 class="font-medium">Participantes</h4>
              <p class="text-gray-600">{{ forumData.members }} membros ativos</p>
            </div>
            <div class="p-3 bg-gray-50 rounded">
              <h4 class="font-medium">Criado em</h4>
              <p class="text-gray-600">{{ forumData.createdAt }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded">
              <h4 class="font-medium">Criado por</h4>
              <p class="text-gray-600">{{ forumData.creator }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded">
              <h4 class="font-medium">Popularidade</h4>
              <div class="flex flex-wrap gap-2 mt-2">
                <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">{{ forumData.popularity }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
/* eslint-disable */
import { ref, onMounted, watch, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import router from '../router/index.js';
import { ENDPOINTS } from '../../../api';
import MainLayout from '../layouts/mainLayout.vue';
import upvoteIcon from '@/assets/img/upvote.png';
import downvoteIcon from '@/assets/img/downvote.png';

const toast = useToast();
const forumData = ref({
  title: '',
  description: '',
  popularity: 0,
  createdAt: '',
  creator: '',
  members: 0,
});

const toggleEdition = async () => {
  editMode.value = !editMode.value;

  if (!editMode.value) {
    try {
      const response = await axios.post(`${ENDPOINTS.EDIT_FORUM}/${slug.value}/`, {
        title: forumData.value.title,
        description: forumData.value.description,
      });

      if (response.data.slug) {
        // Atualiza o slug na rota diretamente
        await router.push({ name: 'ForumDetailPage', params: { slug: response.data.slug } });
        toast.success('Fórum atualizado com sucesso');
        await fetchForum(); // Recarrega os dados do fórum com o novo slug
      }
    } catch (error) {
      console.error(error);
      toast.error('Erro ao atualizar o fórum');
    }
  }
};

const comments = ref([]);
const newCommentContent = ref('');
const editMode = ref(false);
const route = useRoute();
const slug = ref(route.params.slug);

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
};

const fetchForum = async () => {
  try {
    const response = await axios.get(`${ENDPOINTS.FORUM_DETAIL}/${slug.value}/`);
    forumData.value = {
      title: response.data.title,
      description: response.data.description,
      popularity: response.data.popularity,
      createdAt: formatDate(response.data.creation_date),
      creator: response.data.creator,
      members: response.data.subscribers_count,
    };
    await fetchComments();
  } catch (error) {
    console.error(error);
    toast.error('Erro ao buscar dados do fórum');
    router.push('/home');
  }
};

const fetchComments = async () => {
  try {
    const commentsResponse = await axios.get(`${ENDPOINTS.LIST_COMMENTS}/${slug.value}/`);
    comments.value = commentsResponse.data.results.map((comment) => ({
      content: comment.content,
      id: comment.id,
      createdAt: formatDate(comment.post_date),
      creator: comment.creator,
      trust_rate: comment.trust_rate,
      has_liked: comment.has_liked,
    }));
    //toast.success('Comentários carregados com sucesso');
  } catch (error) {
    console.error(error);
    toast.error('Erro ao carregar comentários');
  }
};

const createComment = async () => {
  try {
    // Usamos diretamente o valor de `slug`, que reflete a rota atual
    const response = await axios.post(`${ENDPOINTS.CREATE_COMMENT}`, {
      content: newCommentContent.value,
      forum_slug: slug.value, // `slug` já é atualizado via rota
    });

    console.log(response);
    toast.success('Comentário criado com sucesso');
    newCommentContent.value = ''; // Limpa o campo de comentário
    await fetchComments(); // Recarrega os comentários
  } catch (error) {
    console.error(error);
    toast.error('Erro ao criar comentário');
  }
};

const likeComment = async (comment) => {
  try {
    let response;
    if (comment.has_liked === 1) {
      // Já está curtido, então "unlike"
      response = await axios.delete(`${ENDPOINTS.UNLIKE_COMMENT}${comment.id}/`);
    } else {
      // Envia like
      response = await axios.post(`${ENDPOINTS.LIKE_COMMENT}${comment.id}/`);
    }

    // Atualiza o trust_rate e o estado de like do comentário
    comment.trust_rate = response.data.trust_rate;
    comment.has_liked = comment.has_liked === 1 ? 0 : 1;
  } catch (error) {
    console.error("Erro ao curtir o comentário:", error);
  }
};

const dislikeComment = async (comment) => {
  try {
    let response;
    if (comment.has_liked === -1) {
      // Já está descurtido, então "unlike"
      response = await axios.delete(`${ENDPOINTS.UNLIKE_COMMENT}${comment.id}/`);
    } else {
      // Envia dislike
      response = await axios.post(`${ENDPOINTS.DISLIKE_COMMENT}${comment.id}/`);
    }

    // Atualiza o trust_rate e o estado de dislike do comentário
    comment.trust_rate = response.data.trust_rate;
    comment.has_liked = comment.has_liked === -1 ? 0 : -1;
  } catch (error) {
    console.error("Erro ao descurtir o comentário:", error);
  }
};

// Adicione um map para controlar o estado do menu de cada comentário
const menuStates = ref({});

// Função para alternar o menu de um comentário específico
const toggleMenu = (commentId) => {
  menuStates.value[commentId] = !menuStates.value[commentId];
};

onMounted(() => {
  fetchForum();
});

watch(
  () => route.params.slug,
  (newSlug) => {
    slug.value = newSlug;
    fetchForum();
  }
);

onUnmounted(() => {
  slug.value = null; // Reseta o slug ao desmontar
});

</script>


<style scoped>
.h-85 {
  height: 85%;
}

.h-400-px {
  height: 400px;
}

input:focus, textarea:focus {
  outline: none;
}

input::placeholder, textarea::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

/* Adicionando transição suave para hover dos botões */
button {
  transition: all 0.2s ease-in-out;
}

button:hover {
  transform: translateY(-1px);
}
</style>
