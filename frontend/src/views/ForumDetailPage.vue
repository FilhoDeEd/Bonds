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
                  <button class="hover:text-gray-300 transition-colors">
                    ▲
                  </button>
                  <span class="my-1">0</span>
                  <button class="hover:text-gray-300 transition-colors">
                    ▼
                  </button>
                </div>

                <!-- Imagem do autor do comentário -->
                <div class="w-1/4 flex flex-col">
                  <img src="https://via.placeholder.com/300x200" alt="Imagem do autor" class="object-cover w-full" style="height: 70%;">
                  
                  <!-- Menu dropdown -->
                  <div class="relative mt-2 self-start">
                    <button @click="isMenuOpen = !isMenuOpen" 
                            class="text-white text-xl hover:text-gray-300 rotate-90">
                      ⋮
                    </button>
                    
                    <!-- Dropdown menu -->
                    <div v-if="isMenuOpen" 
                         class="absolute left-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-2 z-10">
                      <button @click="isMenuOpen = false" 
                              class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                        Editar
                      </button>
                      <button @click="isMenuOpen = false" 
                              class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                        Reportar
                      </button>
                      <button @click="isMenuOpen = false" 
                              class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                        Deletar
                      </button>
                    </div>
                  </div>
                </div>
                
                <!-- Conteúdo do comentário -->
                <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                  <a href="#" class="text-white flex flex-col h-full justify-between">
                    <!-- Título ou nome do autor -->
                    <h2 class="text-lg font-semibold mb-8">{{ comment.creator }}</h2>
                    
                    <!-- Texto do comentário -->
                    <div class="text-lg text-gray-100 flex flex-col justify-between flex-grow">
                      <p class="mb-auto leading-relaxed">{{ comment.content }}</p>
                      
                      <!-- Detalhes do comentário -->
                      <p class="mt-8">{{ comment.createdAt }}</p>
                    </div>
                  </a>
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
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import router from '../router/index.js';
import { ENDPOINTS } from '../../../api';
import MainLayout from '../layouts/mainLayout.vue';

const toast = useToast();
const forumData = ref({
  title: '',
  description: '',
  popularity: 0,
  createdAt: '',
  creator: '',
  members: 0,
});

const comments = ref([]);
const newCommentContent = ref('');
const editMode = ref(false);
const route = useRoute();
const slug = ref(localStorage.getItem('currentSlug') || route.params.slug);
const new_slug = ref(false);
const isMenuOpen = ref(false);

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
    const currentSlug = new_slug.value || slug.value;
    const response = await axios.get(`${ENDPOINTS.FORUM_DETAIL}/${currentSlug}/`);
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

    if (commentsResponse.status !== 200) {
      toast.error('Erro ao buscar comentários');
      throw new Error('Erro ao buscar comentários');
    }

    // Acesse os resultados dentro de commentsResponse.data.results
    comments.value = commentsResponse.data.results.map((comment) => ({
      content: comment.content,
      id: comment.id,
      createdAt: formatDate(comment.post_date), // Use a chave correta para a data
      creator: comment.creator,
      upvotes: comment.upvotes,
      downvotes: comment.downvotes,
    }));

    toast.success('Comentários carregados com sucesso');
  } catch (error) {
    console.error(error);
    toast.error('Erro ao carregar comentários');
  }
};

const toggleEdition = async () => {
  editMode.value = !editMode.value;
  if (!editMode.value) {
    try {
      const response = await axios.post(`${ENDPOINTS.EDIT_FORUM}`, {
        title: forumData.value.title,
        description: forumData.value.description,
      });

      if (response.data.slug) {
        new_slug.value = response.data.slug;
        slug.value = new_slug.value;
        localStorage.setItem('currentSlug', new_slug.value);
        toast.success('Fórum atualizado com sucesso');
        await fetchForum();
      }
    } catch (error) {
      console.error(error);
    }
  }
};

const createComment = async () => {
  try {
    const currentSlug = new_slug.value || slug.value;
    const response = await axios.post(`${ENDPOINTS.CREATE_COMMENT}`, {
      content: newCommentContent.value,
      forum_slug: currentSlug,
    });
    console.log(response);
    toast.success('Comentário criado com sucesso');
    newCommentContent.value = '';
    await fetchComments();
  } catch (error) {
    console.error(error);
    toast.error('Erro ao criar comentário');
  }
};

onMounted(() => {
  fetchForum();
});

watch(slug, (newValue) => {
  localStorage.setItem('currentSlug', newValue);
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
