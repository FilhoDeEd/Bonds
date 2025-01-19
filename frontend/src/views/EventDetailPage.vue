<template>
  <MainLayout>
    <div class="w-8/12 h-full py-8 pr-20 pl-20 bg-gray-50">
      <!-- Banner Section -->
      <div class="bg-white h-400-px p-6 rounded-lg shadow mb-8">
        <div class="relative h-full">
          <!-- Área colorida do banner - aumentada para 85% -->
          <div class="absolute top-0 left-0 right-0 h-85" style="background-color: rgba(124, 122, 187, 1);">
          </div>

          <!-- Conteúdo do banner -->
          <div class="relative h-full flex flex-col justify-between">
            <!-- Área de título e descrição -->
            <div class="px-6 py-8">
              <div class="container mx-auto flex flex-col items-start">
                <!-- Título editável -->
                <div class="grid grid-cols-2 gap-4 w-full">
                  <input type="text" v-model="forumData.title" :readonly="!editMode"
                  class="text-white text-3xl font-bold mb-4 bg-transparent border-none w-full col-span-2"
                  :class="{ 'hover:bg-gray-700/30': editMode }" placeholder="Título do Evento">

                  <!-- Descrição editável -->
                  <textarea v-model="forumData.description" :readonly="!editMode"
                  class="text-white text-base mb-4 bg-transparent border-none w-full resize-none"
                  :class="{ 'hover:bg-gray-700/30': editMode }" placeholder="Descrição do Evento" rows="3"></textarea>

                  <textarea v-model="forumData.date" :readonly="!editMode"
                  class="text-white text-base mb-4 bg-transparent border-none w-full resize-none"
                  :class="{ 'hover:bg-gray-700/30': editMode }" placeholder="Data do Evento" rows="3"></textarea>

                  <textarea v-model="forumData.localization" :readonly="!editMode"
                  class="text-white text-base mb-4 bg-transparent border-none w-full resize-none"
                  :class="{ 'hover:bg-gray-700/30': editMode }" placeholder="Localização" rows="3"></textarea>
                </div>
                <p class="text-white text-lg">{{ forumData.five_star_mean }}</p>
                </div>
            </div>

            <!-- Botões alinhados ao bottom -->
            <div class="px-6 pb-4 flex space-x-4 relative z-10">
              <button type="button" @click="toggleSubscribe"
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200"
                style="background-color: rgb(252, 3, 94);">
                {{ isSubscribed ? 'Desinscrever' : 'Inscrever' }}
              </button>

              <button type="button" @click="toggleEdition"
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
          <h2 class="text-2xl font-bold mb-4">Engaje no Evento!</h2>

          <!-- Área de criação de post -->
          <div class="border rounded-lg p-4">
            <div class="flex items-start space-x-4">
              <img src="https://via.placeholder.com/40" class="w-10 h-10 rounded-full" alt="Seu perfil">
              <div class="flex-1">
                <textarea v-model="newCommentContent"
                  class="w-full p-3 rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none"
                  placeholder="No que você está pensando?" rows="3"></textarea>

                <!-- Botões de ação -->
                <div class="flex items-center mt-4 pt-3 border-t">
                  <div class="flex space-x-2">
                    <button class="p-2 hover:bg-gray-100 rounded-full" title="Adicionar foto/vídeo">
                      <span>📷</span>
                    </button>
                    <button class="p-2 hover:bg-gray-100 rounded-full" title="Enquete">
                      <span>📊</span>
                    </button>
                  <button v-show="checkDate" @click="callReview"
                    class="p-2 hover:bg-gray-100 rounded-full" title="Avaliar Evento">
                    <span>⭐</span>
                  </button>
                  </div>

                  <button @click="createComment"
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
            <article v-for="comment in comments" :key="comment.createdAt"
              class="p-4 shadow rounded hover:shadow-lg transition-shadow duration-200"
              style="background-color: rgba(124, 122, 187, 1);">
              <div class="flex h-full">

                <!-- Área de votação -->
                <div class="flex flex-col items-center text-2xl font-bold w-12">
                  <button @click="likeComment(comment)" class="vote" :class="{
                    'on-up': comment.has_liked === 1,
                    'hover:text-gray-300': comment.has_liked !== 1
                  }">
                    <svg width="36" height="36" viewBox="0 0 36 36">
                      <path d="M2 26h32L18 10 2 26z" stroke="white" stroke-width="2" fill="none" class="svg-path">
                      </path>
                    </svg>
                  </button>
                  <span class="my-1 text-white">{{ comment.trust_rate }}</span>
                  <button @click="dislikeComment(comment)" class="vote" :class="{
                    'on-down': comment.has_liked === -1,
                    'hover:text-gray-300': comment.has_liked !== -1
                  }">
                    <svg width="36" height="36" viewBox="0 0 36 36">
                      <path d="M2 10h32L18 26 2 10z" stroke="white" stroke-width="2" fill="none" class="svg-path">
                      </path>
                    </svg>
                  </button>

                  <!-- Botão para criar enquete -->
                  <button @click="showPollCreator = true" class="p-2 hover:bg-gray-100 rounded-full"
                    title="Criar Enquete">
                    <span>📊</span>
                  </button>
                </div>

                <!-- Imagem do autor do comentário -->
                <div class="w-1/4 h-70-px flex flex-col pt-12 ">
                  <img src="https://via.placeholder.com/300x200" alt="Imagem do autor" class="object-cover w-full"
                    style="height: 70%;">


                </div>

                <!-- Conteúdo do comentário -->
                <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                  <div class="text-white flex flex-col h-full justify-between">
                    <!-- Menu dropdown -->
                    <div class="relative self-end mb-2">
                      <button @click="toggleMenu(comment.id)" class="text-white text-xl hover:text-gray-300">
                        ⋯
                      </button>

                      <!-- Dropdown menu -->
                      <div v-if="menuStates[comment.id]"
                        class="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-2 z-10">
                        <button @click="() => { menuStates[comment.id] = false; comment.isEditing = true }"
                          class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                          Editar
                        </button>
                        <button
                          @click="() => { menuStates[comment.id] = false; deleteComment(comment); comment.isEditing = true }"
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

                    <div class="text-lg flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <p v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        {{ comment.content }}
                      </p>

                      <!-- Edição do comentário -->
                      <textarea v-else v-model="comment.tempContent" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEdit(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">                      >
                      </textarea>
                    </div>
                    <!-- Detalhes do comentário -->
                    <p class="mt-8">{{ comment.createdAt }}</p>
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
              <h4 class="font-medium">Avaliação </h4>
              <p class="text-gray-600">{{ forumData.five_star_mean }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded">
              <h4 class="font-medium">Data do Evento</h4>
              <p class="text-gray-600">{{ forumData.date }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded">
              <h4 class="font-medium">Local do Evento</h4>
              <p class="text-gray-600">{{ forumData.localization }}</p>
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
      <ModalReview
        v-if="isModalOpen"
        :isModalOpen="isModalOpen"
        @submitRating="handleRating"
        @close="isModalOpen = false"
        @showToast="handleShowToast"
      />
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
import { ENDPOINTS } from '../../api.js';
import MainLayout from '../layouts/mainLayout.vue';
import ModalReview from '../components/Modals/ModalReview.vue';
import upvoteIcon from '@/assets/img/upvote.png';
import downvoteIcon from '@/assets/img/downvote.png';

const checkDate = ()=>{
  if (forumData.value.date <= new Date()){
      return true
    }
    return false;
  }

const isModalOpen = ref(false);
const stars = ref(0);

const callReview = () => {
  isModalOpen.value = true;
};

const handleRating = async (rating) => {
  stars.value = rating;
  try {
    const response = await axios.post(ENDPOINTS.REVIEW_EVENT, {
      five_star: stars.value,
      forum_slug: slug.value,
    });
    if (response.data.success) {
      toast.success("Evento avaliado com sucesso!");
      isModalOpen.value = false;
    }
    if (response.detail == "User already subscribed to this forum.") {
      toast.error("Você já avaliou este evento.");
    }
  } catch (error) {
    toast.error("Você já avaliou este evento.");
  }
};

const toast = useToast();
const forumData = ref({
  title: '',
  date:'',
  localization:'',
  description: '',
  popularity: 0,
  createdAt: '',
  creator: '',
  members: 0,
  five_star_mean:	0,
});

const toggleEdition = async () => {
  editMode.value = !editMode.value;
  if (!editMode.value) {
    if(new Date(formatDateToISO(forumData.value.date)) <= new Date()){
      toast.error('Não é possível editar a data de um evento que já ocorreu, ou mover para o passado');
      editMode.value = false;
      return;
    }
    try {
      const response = await axios.post(`${ENDPOINTS.EDIT_EVENT}/${slug.value}/`, {
        title: forumData.value.title,
        description: forumData.value.description,
        date: formatDateToISO(forumData.value.date),
        location: forumData.value.localization,

      });
      if (response.data.slug) {
        // Atualiza o slug na rota diretamente
        await router.push({ name: 'EventDetailPage', params: { slug: response.data.slug } });
        toast.success('Evento atualizado com sucesso');
        await fetchEvent(); // Recarrega os dados do fórum com o novo slug
      }
    } catch (error) {
      console.error(error);
      if (error.response.data.detail == "You do not have permission to edit this forum.") {
        toast.error("Você não tem permissão para editar este Evento");
      } else {
        toast.error(error.response.data.detail || 'Erro ao editar Event');
      }
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
  date.setDate(date.getDate() + 1); // Add one day to the date
  return new Intl.DateTimeFormat('pt-BR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
};

const fetchEvent = async () => {
  try {
    const response = await axios.get(`${ENDPOINTS.EVENT_DETAIL}/${slug.value}/`);
    forumData.value = {
      title: response.data.title,
      description: response.data.description,
      popularity: response.data.popularity,
      createdAt: formatDate(response.data.creation_date),
      creator: response.data.creator,
      members: response.data.subscribers_count,
      tempContent: "",
      date: formatDate(response.data.date),
      localization: response.data.location,
      five_star_mean: response.data.five_star_mean,
      isSubscribed: response.data.is_sub,
    };
    await fetchComments();
    subscribed();
  } catch (error) {
    console.error(error);
    toast.error('Erro ao buscar dados do fórum');
    router.push('/home');
  }
};
const subscribed = () => {
  if (forumData.value.isSubscribed == 1) {
    isSubscribed.value = true;
  }
  else {
    isSubscribed.value = false;
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

const editComment = async (comment) => {
  try {
    const response = await axios.post(`${ENDPOINTS.EDIT_COMMENT}/${comment.id}/`, {
      content: comment.content,
    });

    // Atualiza o conteúdo do comentário com a resposta do servidor
    toast.success('Comentário editado com sucesso');
  }
  catch (err) {
    console.log(err);
    toast.error("Algo deu errado!");
  }
};

const cancelEdit = async (comment) => {
  try {
    comment.isEditing = false;
    comment.tempContent = comment.content;
  }
  catch (err) {
    console.log(err)
  }
};

const saveEdit = async (comment) => {
  try {
    if (comment.tempContent !== comment.content && comment.tempContent) {
      comment.content = comment.tempContent;
      editComment(comment);
    }
    comment.isEditing = false;
  }
  catch (err) {
    console.log(err)
  }
};

const deleteComment = async (comment) => {
  try {
    await axios.post(`${ENDPOINTS.DELETE_COMMENT}/${comment.id}/`);
    toast.success('Comentário deletado com sucesso');
    await fetchComments(); // Recarrega os comentários
  } catch (error) {
    console.error("Erro ao deletar o comentário:", error);
    toast.error('Erro ao deletar comentário');
  }
};

const toggleSubscribe = async () => {
  try {
    if (isSubscribed.value) {
      await axios.post(`${ENDPOINTS.UNSUBSCRIBE_FORUM}/${slug.value}/`);
      toast.success("Você cancelou sua inscrição no fórum!");
      forumData.value.members -= 1;
    } else {
      await axios.post(`${ENDPOINTS.SUBSCRIBE_FORUM}/${slug.value}/`);
      toast.success("Você se inscreveu no fórum!");
      forumData.value.members += 1;
    }
    isSubscribed.value = !isSubscribed.value;
  } catch (err) {
    console.log(err);
    toast.error("Algo deu errado!");
  }
};

const isSubscribed = ref(false);

// Adicione um map para controlar o estado do menu de cada comentário
const menuStates = ref({});

// Função para alternar o menu de um comentário específico
const toggleMenu = (commentId) => {
  menuStates.value[commentId] = !menuStates.value[commentId];
};


onMounted(() => {
  fetchEvent();
});

function formatDateToISO(dateString) {
  // Mapeia os meses para seus valores numéricos
  const months = {
    janeiro: "01",
    fevereiro: "02",
    março: "03",
    abril: "04",
    maio: "05",
    junho: "06",
    julho: "07",
    agosto: "08",
    setembro: "09",
    outubro: "10",
    novembro: "11",
    dezembro: "12",
  };

  // Divide a string em partes (dia, mês, ano)
  const [day, monthText, year] = dateString.split(" de ");
  console.log(day, monthText, year);
  //const day = (parseInt(day_before) + 1).toString().padStart(2, "0");
  // Formata para YYYY-MM-DD
  const month = months[monthText.toLowerCase()];
  console.log(`${year}-${month}-${day.padStart(2, "0")}`);
  return `${year}-${month}-${day.padStart(2, "0")}`;
};

watch(
  () => route.params.slug,
  (newSlug) => {
    slug.value = newSlug;
    fetchEvent();
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

.bg-pattern {
  background-color: #363474;
}

.h-400-px {
  height: 400px;
}

input:focus,
textarea:focus {
  outline: none;
}

input::placeholder,
textarea::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

/* Adicionando transição suave para hover dos botões */
button {
  transition: all 0.2s ease-in-out;
}

button:hover {
  transform: translateY(-1px);
}

.vote {
  display: inline-block;
  cursor: pointer;
  color: #687074;
  transition: all 0.2s ease;
}

.vote.on-up {
  color: #22c55e;
  /* verde */
}

.vote.on-down {
  color: #ef4444;
  /* vermelho */
}

.vote.on-up .svg-path,
.vote.on-down .svg-path {
  fill: currentColor;
  stroke: currentColor;
}
</style>
