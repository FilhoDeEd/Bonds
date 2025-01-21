<template>
  <MainLayout>
    <div class="w-8/12 h-full py-8 pr-20 pl-20 bg-gray-50">
      <!-- Banner Section -->
      <div class="bg-basic h-600-px p-6 rounded-lg shadow mb-8">
        <div class="relative h-full">
          <!-- Área colorida do banner -->
          <div class="absolute top-0 left-0 right-0 h-90 rounded-lg" style="background-color: rgba(124, 122, 187, 1);">
            <div class="relative h-full flex flex-col justify-between">
              <!-- Área de título e descrição -->
              <div class="px-6 py-6">
                <div class="container mx-auto flex flex-col items-start space-y-4">
                  <!-- Título do Fórum -->
                  <div class="flex justify-center w-full relative">
                    <!-- Campo de arquivo oculto -->
                    <input type="file" ref="fileInput" accept="image/*" style="display: none;" @change="updateBanner">
                    <!-- Imagem do banner -->
                    <img :src="forumData.banner_image || require('@/assets/img/1200x400.png')" alt="Event banner"
                      class="w-4/5 max-h-300-px  object-fill rounded-lg shadow-lg cursor-pointer mb-4"
                      :class="{ 'hover:opacity-80': editMode }" @click="editMode && $refs.fileInput.click()">
                  </div>

                  <div class="grid gap-4 w-full">
                    <textarea v-model="forumData.title" :readonly="!editMode"
                      class="text-white text-3xl font-bold bg-transparent border-none w-full resize-none h-12"
                      :placeholder="editMode ? 'Título do Fórum' : ''"
                      style="line-height: 1.2; padding: 4px 8px; min-height: 40px; outline: none;"
                      :class="{ 'cursor-text hover:bg-gray-700/30': editMode }">
                    </textarea>

                    <!-- Descrição do Fórum -->
                    <textarea v-model="forumData.description" :readonly="!editMode"
                      class="text-white text-base bg-transparent border-none w-full resize-none"
                      :class="{ 'hover:bg-gray-700/30': editMode }" placeholder="Descrição do Fórum" rows="2"
                      style="line-height: 1.4; padding: 4px 8px; height: auto; min-height: 60px;">
                    </textarea>
                  </div>
                </div>
              </div>
            </div>

            <!-- Botões alinhados ao bottom -->
            <div class=" flex space-x-4 relative z-10">
              <button type="button" @click="toggleSubscribe"
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200 mt-4"
                style="background-color: rgb(252, 3, 94);">
                {{ isSubscribed ? 'Desinscrever' : 'Inscrever' }}
              </button>

              <button type="button" @click="toggleEdition"
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200 mt-4"
                style="background-color: rgb(252, 3, 94);">
                {{ editMode ? 'Salvar' : 'Editar' }}
              </button>

              <button type="button"
                class="px-6 py-3 rounded-lg hover:bg-gray-100 text-white transition-colors duration-200 mt-4"
                style="background-color: rgb(252, 3, 94);">
                Denunciar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-basic p-6 rounded-lg shadow mb-8">
        <div class="container mx-auto">
          <h2 class="text-2xl font-bold mb-4">Engaje no fórum!</h2>

          <!-- Área de criação de post -->
          <div class="border rounded-lg p-4">
            <div class="flex items-start space-x-4">
              <img :src="profileImage" class="w-10 h-10 rounded-full" alt="Seu perfil">
              <div class="flex-1">
                <textarea v-model="newCommentContent"
                  class="w-full p-3 rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none"
                  placeholder="No que você está pensando?" rows="3"></textarea>

                <!-- Botões de ação -->
                <div class="flex items-center mt-4 pt-3 border-t">
                  <div class="flex space-x-2">
                    <button class="p-2 hover:bg-gray-100 rounded-full" title="Adicionar foto"
                      @click="$refs.imageInput.click()">
                      <span>📷</span>
                    </button>
                    <input type="file" ref="imageInput" accept="image/*" style="display: none;"
                      @change="handleImageUpload">

                    <button v-show="showReportCreator" @click="openModal" class="p-2 hover:bg-gray-100 rounded-full"
                      title="Adicionar um Reporte">
                      <span>📢</span>
                    </button>

                    <button @click="openPoll" class="p-2 hover:bg-gray-100 rounded-full" title="Enquete"
                      id="pollButton">
                      <span>📊</span>
                    </button>
                  </div>
                  <!-- Prévia da imagem -->
                  <div v-if="imagePreview" class="mb-4 relative">
                    <img :src="imagePreview" alt="Preview" class="max-h-48 rounded-lg object-contain">
                    <button @click="removeImage"
                      class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                      title="Remover imagem">
                      ❌
                    </button>
                  </div>
                  <button v-show="showPostButton" @click="createComment"
                    class="ml-auto px-6 py-2 bg-blue-500 text-Black rounded-lg hover:bg-blue-600 font-semibold">
                    ✔️
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>



      <button v-show="showReportCreator" @click="commentOrReport"
        class="px-4 py-2 bg-black text-white rounded-lg hover:bg-blue-600">
        <span v-if="comment_list">Veja os Reports 📢</span>
        <span v-else>Veja os Comentários 💬</span>
      </button>
      <!-- Content Section with Posts and Sidebar -->
      <div class="flex gap-8 space-x-4 ">

        <!-- Comments Section -->
        <div class="w-3/4" v-if="comment_list">
          <div class="space-y-4">
            <article v-for="item in combinedItems" :key="item.createdAt"
              class="p-4 shadow rounded hover:shadow-lg transition-shadow duration-200"
              :class="item.type === 'comment' ? 'bg-basic' : 'bg-red-400'">
              <div class="flex h-full">

                <!-- Área de votação (se for comment ou poll) -->
                <div v-if="item.type === 'comment'" class="flex flex-col items-center text-2xl font-bold w-12">
                  <button @click="likeComment(item)" class="vote" :class="{
                    'on-up': item.has_liked === 1,
                    'hover:text-gray-300': item.has_liked !== 1
                  }">
                    <svg width="36" height="36" viewBox="0 0 36 36">
                      <path d="M2 26h32L18 10 2 26z" stroke="white" stroke-width="2" fill="none" class="svg-path">
                      </path>
                    </svg>
                  </button>
                  <span class="my-1 text-white">{{ item.trust_rate }}</span>
                  <button @click="dislikeComment(item)" class="vote" :class="{
                    'on-down': item.has_liked === -1,
                    'hover:text-gray-300': item.has_liked !== -1
                  }">
                    <svg width="36" height="36" viewBox="0 0 36 36">
                      <path d="M2 10h32L18 26 2 10z" stroke="white" stroke-width="2" fill="none" class="svg-path">
                      </path>
                    </svg>
                  </button>
                </div>

                <!-- Conteúdo do comentário ou poll -->
                <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                  <div class="text-black flex flex-col h-full justify-between">
                    <div v-if="item.type === 'comment'">
                      <div class="comment-image-container" style="display: inline-block; margin-left: 10px;">
                        <img v-if="selectedImage" :src="imagePreview" alt="Uploaded Image" class="rounded-lg max-h-48">
                      </div>
                      <!-- Menu dropdown -->
                      <div class="relative self-end mb-2">
                        <button @click="toggleMenu(item.id)" class="text-black  text-xl hover:text-gray-300">
                          ⋯
                        </button>

                        <!-- Dropdown menu -->
                        <div v-if="menuStates[item.id]"
                          class="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-2 z-10">
                          <button @click="() => { menuStates[item.id] = false; item.isEditing = true }"
                            v-show="checkOwnership(item.creator)"
                            class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                            Editar
                          </button>
                          <button v-show="checkOwnership(item.creator)"
                            @click="() => { menuStates[item.id] = false; deleteComment(item); item.isEditing = true }"
                            class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                            Deletar
                          </button>
                          <button @click="menuStates[item.id] = false"
                            class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                            Reportar
                          </button>

                        </div>
                      </div>

                      <!-- Título ou nome do autor -->
                      <div class="flex items-center mb-8 ml-auto">
                        <!-- Imagem do autor (à direita) -->
                        <img :src="item.author_image || profile" alt="Imagem do autor"
                          class="w-10 h-10 rounded-full object-cover mr-3">

                        <!-- Nome do criador -->
                        <h2 class="text-lg font-semibold">{{ item.creator }}</h2>
                      </div>

                      <div class="text-lg text-black flex flex-col justify-between flex-grow">
                        <!-- Exibição do comentário -->
                        <p v-if="!item.isEditing" class="mb-auto leading-relaxed text-black  cursor-pointer"
                          @dblclick="() => { item.isEditing = true; }" title="Clique duas vezes para editar">
                          {{ item.content }}
                        </p>

                        <!-- Edição do comentário -->
                        <textarea v-else v-model="item.tempContent" @blur="cancelEdit(item)"
                          @keyup.enter="saveEdit(item)"
                          class="w-full text-black  sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">                      >
                          </textarea>
                      </div>
                      <!-- Detalhes do comentário -->
                      <p class="mt-8 text-black ">{{ item.createdAt }}</p>
                    </div>
                    <div v-else>
                      <div class="relative self-end mb-2">
                        <button @click="toggleMenu(item.id)" class="text-black  text-xl hover:text-gray-300">
                          ⋯
                        </button>

                        <!-- Dropdown menu -->
                        <div v-if="menuStates[item.id]"
                          class="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-2 z-10">
                          <button @click="() => { menuStates[item.id] = false; item.isEditing = true }" v-show="false"
                            class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                            Editar
                          </button>
                          <button v-show="checkOwnership(item.creator)"
                            @click="() => { menuStates[item.id] = false; deletePoll(item); }"
                            class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                            Deletar
                          </button>
                          <button @click="menuStates[item.id] = false"
                            class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                            Reportar
                          </button>

                        </div>
                      </div>
                      <!-- Container do item de enquete -->
                      <div class="border rounded-lg shadow-lg p-6 bg-white mb-6">
                        <!-- Título da enquete -->
                        <h2 class="text-2xl font-semibold text-gray-800 mb-4">{{ item.title || "Título da Enquete" }}
                        </h2>

                        <!-- Texto descritivo -->
                        <p class="text-gray-700 mb-4">
                          {{ item.content || "Adicione aqui uma descrição da enquete." }}
                        </p>

                        <!-- Prazo -->
                        <p class="text-sm text-gray-500 mb-6">
                          Prazo: {{ item.deadline ? `Até ${new Date(item.deadline).toLocaleDateString()}` : "Nenhum
                          prazo definido" }}
                        </p>

                        <!-- Opções da enquete -->
                        <h3 class="text-lg font-medium text-gray-800 mb-3">Opções:</h3>
                        <ul class="space-y-4">
                          <li v-for="option in item.options" :key="option.id" class="flex items-center justify-between">
                            <!-- Radio para votar -->
                            <div class="flex items-center">
                              <input type="radio" :id="`option-${option.id}`" :value="option.id"
                                :name="`poll-${item.slug}`" :disabled="new Date(item.deadline) <= new Date()"
                                v-model="selectedItem"
                                class="w-5 h-5 text-green-500 border-gray-300 focus:ring-green-400" />
                              <label :for="`option-${option.id}`" class="ml-3 text-gray-700 cursor-pointer">
                                {{ option.option_text || "Opção não definida" }}
                              </label>
                            </div>
                            <!-- Contagem de votos -->
                            <div class="text-gray-700">
                              {{ option.votes || 0 }} votos
                            </div>
                          </li>
                        </ul>

                        <!-- Botão de envio -->
                        <button v-show="new Date(item.deadline) > new Date()" @click="voteIn()"
                          class="mt-6 bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
                          Enviar Voto
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>

        <!-- Reports Section -->
        <div class="w-3/4 " v-else>
          <div class="space-y-4 ">
            <article v-for="comment in reports" :key="comment.createdAt"
              class="p-4 shadow rounded hover:shadow-lg transition-shadow duration-200 bg-red-400">
              <div class="flex h-full">

                <!-- Área de votação -->
                <div class="flex flex-col items-center text-2xl font-bold w-12">
                  <button @click="likeComment(comment)" class="vote" :class="{
                    'on-up': comment.has_liked === 1,
                    'hover:text-gray-300': comment.has_liked !== 1}">
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
                </div>

                <!-- Conteúdo do comentário -->
                <div class="flex-1 pl-8 text-right flex flex-col justify-between h-full">
                  <div class="text-white flex flex-col h-full justify-between">
                    <!-- Campo de imagem -->
                    <div class="comment-image-container" style="display: inline-block; margin-left: 10px;">
                      <img v-if="selectedImage" :src="imagePreview" alt="Uploaded Image" class="rounded-lg max-h-48">
                    </div>
                    <!-- Menu dropdown -->
                    <div class="relative self-end mb-2">
                      <button @click="toggleMenu(comment.id)" class="text-white text-xl hover:text-gray-300">
                        ⋯
                      </button>

                      <!-- Dropdown menu -->
                      <div v-if="menuStates[comment.id]"
                        class="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-2 z-10">
                        <button @click="() => { menuStates[comment.id] = false; comment.isEditing = true }"
                          class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100"
                          v-show="checkOwnership(comment.creator)">

                          Editar
                        </button>
                        <button v-show="checkOwnership(comment.creator)"
                          @click="() => { menuStates[comment.id] = false; deleteComment(comment) }"
                          class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                          Deletar
                        </button>
                        <button @click="menuStates[comment.id] = false"
                          class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100">
                          Reportar
                        </button>

                      </div>
                    </div>

                    <div class="text-lg flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <h3 v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        {{ comment.title }}
                      </h3>

                      <!-- Edição do comentário -->
                      <textarea v-else v-model="comment.title" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEditReport(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">                      >
                      </textarea>
                    </div>

                    <div class="text-lg flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <p v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        {{ comment.content }}
                      </p>

                      <!-- Edição do comentário -->
                      <textarea v-else v-model="comment.content" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEditReport(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">                      >
                      </textarea>
                    </div>
                    <div class="text-lg flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <p v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        {{ comment.location }}
                      </p>

                      <!-- Edição do comentário -->
                      <textarea v-else v-model="comment.location" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEditReport(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">                      >
                      </textarea>
                    </div>
                    <div class="text-xs flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <p v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        Reporte realizado em: {{ comment.date }}
                      </p>

                      <!-- Edição do comentário -->
                      <textarea v-else v-model="comment.date" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEditReport(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">
                      </textarea>
                    </div>
                    <div class="text-xs flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <p v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        Reporte resolvido? {{ comment.solved ? "Sim" : "Não" }}
                      </p>

                      <!-- Edição do comentário -->
                      <select v-else v-model="comment.solved" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEditReport(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">
                        <option value="true">Sim</option>
                        <option value="false">Não</option>
                      </select>
                    </div>
                    <div class="text-xs flex flex-col justify-between flex-grow">
                      <!-- Exibição do comentário -->
                      <p v-if="!comment.isEditing" class="mb-auto leading-relaxed cursor-pointer"
                        @dblclick="() => { comment.isEditing = true; }" title="Clique duas vezes para editar">
                        Tag: {{ comment.tag }}
                      </p>

                      <!-- Edição do comentário -->
                      <select v-else v-model="comment.tag" @blur="cancelEdit(comment)"
                        @keyup.enter="saveEditReport(comment)"
                        class="w-full sm:w-11/12 md:w-10/12 lg:w-8/12 max-w-4xl p-3 bg-pattern rounded-lg border border-gray-200 focus:outline-none focus:border-gray-300 resize-none ml-auto">
                        <option disabled :value="comment.tag"></option>
                        <option v-for="tag in tags" :key="tag.id" :value="tag.id">
                          {{ tag.name }}
                        </option>
                      </select>

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
        <aside class="w-1/4 bg-banner p-4 rounded-lg shadow-lg sticky top-24 max-h-265-px ">

          <div class="bg-banner p-4 rounded-lg shadow sticky top-24">
            <h3 class="text-xl font-semibold mb-4 text-white">Mais informações</h3>

            <div class="space-y-3 ">
              <div class="text-sm mb-4">
                <p class="text-white">
                  <span class="josefin-sans-bold-italic">Participantes: </span>
                  <span class="inconsolata-regular">{{ forumData.members }}</span>
                </p>
              </div>

              <div class="text-sm mb-4">
                <p class="text-white ">
                  <span class="josefin-sans-bold-italic">Criado em: </span>
                  <span class="inconsolata-regular"> {{ forumData.createdAt }}</span>
                </p>
              </div>

              <div class="text-sm mb-4">
                <p class="text-white">
                  <span class="josefin-sans-bold-italic">Criado por: </span>
                  <span class="inconsolata-regular"> {{ forumData.creator }}</span>
                </p>
              </div>

              <div class="text-sm mb-4">
                <p class="text-white">
                  <span class="josefin-sans-bold-italic">Popularidade: </span>
                  <span class="inconsolata-regular"> {{ forumData.popularity }}</span>
                </p>
              </div>
            </div>
          </div>
        </aside>

      </div>
      <ModalReport v-if="isModalOpen" :isModalOpen="isModalOpen" @close="closeModal" :slug="slug" />
      <ModalPoll v-if="isPollOpen" :isPollOpen="isPollOpen" @close="closePoll" :slug="slug" />
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
import { ENDPOINTS } from '../../api';
import MainLayout from '../layouts/mainLayout.vue';
import ModalReport from '../components/Modals/ModalReport.vue';
import { computed } from "vue";
import { useUserStore } from "../store/user.js";
import ModalPoll from '../components/Modals/ModalPoll.vue';
import profile from "@/assets/img/profilePic.jpg";

const isPollOpen = ref(false)
const openPoll = () => {
  isPollOpen.value = true;
}

const selectedItem = ref()
const closePoll = () => {
  isPollOpen.value = false;
  fetchPolls();
}
const deletePoll = async (item) => {
  try {
    const response = await axios.post(`${ENDPOINTS.DELETE_POLL}/${item.id}/`);
    if (response.status === 204) {
      toast.success("Enquete excluída com sucesso")
      fetchPolls()
    } else {
      toast.error("Erro ao excluir enquete")
    }
  } catch (err) {
    console.log(err);
    toast.error("Erro ao excluir enquete")
  }
}

const voteIn = async () => {
  try {
    const response = await axios.post(`${ENDPOINTS.VOTE_POLL}/${selectedItem.value}/`);
    if (response.status === 201) {
      toast.success("Seu voto foi computado!")
      fetchPolls()
    }
    else {
      console.log(response)
      toast.error("Algo deu errado")
    }
  } catch (err) {
    if (err.response.data.detail === "Você já votou nesta opção.") {
      toast.info("Você já votou nesta opção!")
    }
    else {
      console.log(err)
      toast.error("Algo deu errado")

    }
  }
}


const showPostButton = ref(true)

const toast = useToast();
const forumData = ref({
  title: '',
  description: '',
  popularity: 0,
  createdAt: '',
  creator: '',
  members: 0,
  type: '',
  isSubscribed: false,
});
const tags = [
  { id: 'SA', name: 'Saúde' },
  { id: 'L', name: 'Lixo' },
  { id: 'I', name: 'Infraestrutura' },
  { id: 'SG', name: 'Segurança' },
  { id: 'E', name: 'Educação' },
  { id: 'T', name: 'Transporte' },
  { id: 'IL', name: 'Iluminação' },
  { id: 'O', name: 'Outros' }
];


const comment_list = ref(true);
const showReportCreator = ref(true)

const commentOrReport = async () => {
  comment_list.value = !comment_list.value;
  if (comment_list.value) {
    await fetchComments();
    await fetchPolls();

  } else {
    await fetchReports();
  }
}

const activeReportCreator = () => {
  if (forumData.value.creator === "Sistema") {
    showReportCreator.value = true;
  }
  else {
    showReportCreator.value = false;
  }
};
const isModalOpen = ref(false); // Referência reativa
const openModal = () => {
  isModalOpen.value = true; // Atualiza a propriedade `.value` do ref
};

const closeModal = async () => {
  isModalOpen.value = false; // Fecha o modal corretamente
  await router.push({ name: 'ForumDetailPage', params: { slug: slug.value } });
};

const userStore = useUserStore();

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
      if (error.response.data.detail == "You do not have permission to edit this forum.") {
        toast.error("Você não tem permissão para editar este fórum");
      } else {
        toast.error(error.response.data.detail || 'Erro ao editar fórum');
      }
    }
  }
};

const comments = ref([]);
const reports = ref([]);
const newCommentContent = ref('');
const editMode = ref(false);
const route = useRoute();
const slug = ref(route.params.slug);
const isOwner = ref(true);

const checkOwnership = (name) => {
  if ((userStore.user.account.name + " " + userStore.user.account.surname) === name || userStore.user.account.username === name) {
    isOwner.value = true;
    return true
  } else {
    isOwner.value = false;
    return false
  }
};

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
    const currentBanner = forumData.value.banner_image;

    forumData.value = {
      ...forumData.value,
      title: response.data.title,
      description: response.data.description,
      popularity: response.data.popularity,
      createdAt: formatDate(response.data.creation_date),
      creator: response.data.creator,
      members: response.data.subscribers_count,
      isSubscribed: response.data.is_sub,
      banner_image: response.data.banner_image || currentBanner,
    };
    await fetchComments();
    await fetchPolls();
    subscribed();
    activeReportCreator();
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

const polls = ref([]);
const fetchPolls = async () => {
  try {
    const response = await axios.get(`${ENDPOINTS.LIST_POLL}/${slug.value}/`);
    if (response.status === 200) {
      polls.value = response.data.results;
    }

    else {
      toast.error("Erro ao carregar as enquetes")
    }
  }
  catch (err) {
    toast.error("Erro ao carregar as enquetes")
  }
}
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
      image: comment.image,
      author_image: comment.author_image
    }));
    //toast.success('Comentários carregados com sucesso');
  } catch (error) {
    console.error(error);
    toast.error('Erro ao carregar comentários');
  }
  fetchPolls();
};
const combinedItems = computed(() => {
  return [...polls.value.map((poll) => ({ ...poll, type: "poll" })),
  ...comments.value.map((comment) => ({ ...comment, type: "comment" }))].sort((a, b) =>
    new Date(b.post_date || b.createdAt) - new Date(a.post_date || a.createdAt)
  );
});
const fetchReports = async () => {
  try {
    const reportsResponse = await axios.get(`${ENDPOINTS.REPORT_LIST}/${slug.value}/`);
    reports.value = reportsResponse.data.results.map((reports) => ({
      content: reports.content,
      id: reports.id,
      createdAt: formatDate(reports.post_date),
      date: formatDate(reports.date),
      creator: reports.creator,
      trust_rate: reports.trust_rate,
      has_liked: reports.has_liked,
      title: reports.title,
      tag: reports.tag,
      solved: reports.solved,
      location: reports.location,
      image: reports.image,
      author_image: reports.author_image
    }));
    //toast.success('Comentários carregados com sucesso');
  } catch (error) {
    console.error(error);
    toast.error('Erro ao carregar reports');
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
const editReport = async (report) => {
  try {
    const response = await axios.post(`${ENDPOINTS.REPORT_EDIT}/${report.id}/`, {
      content: report.content,
      title: report.title,
      location: report.location,
      tag: report.tag,
      solved: report.solved,
      forum_slug: slug
    });

    // Atualiza o conteúdo do comentário com a resposta do servidor
    toast.success('Reporte editado com sucesso');
    await fetchReports();
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
const saveEditReport = async (comment) => {
  try {
    if (comment.tempContent !== comment.content && comment.tempContent) {
      comment.content = comment.tempContent;
    }
    editReport(comment);
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
    await fetchReports();
    await fetchPolls();
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

const imagePreview = ref(null);
const selectedImage = ref(null);
const imageInput = ref(null);

// Função para lidar com o upload da imagem
const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) {
    toast.error("Nenhuma imagem selecionada");
    return;
  }

  // Validações de arquivo
  const maxSize = 5 * 1024 * 1024; // 5MB
  const validTypes = ['image/jpeg', 'image/png', 'image/gif'];

  if (file.size > maxSize) {
    toast.error("A imagem deve ter menos de 5MB");
    return;
  }

  if (!validTypes.includes(file.type)) {
    toast.error("Formato de imagem inválido. Use JPG, PNG ou GIF");
    return;
  }

  // Cria a prévia da imagem
  selectedImage.value = file;
  imagePreview.value = URL.createObjectURL(file);
};

// Função para remover a imagem
const removeImage = () => {
  imagePreview.value = null;
  selectedImage.value = null;
  if (imageInput.value) {
    imageInput.value.value = '';
  }
};


onMounted(() => {
  fetchForum();
  activeReportCreator();
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

const profileImage = computed(() => {
  return userStore.user.account.profile_image || profile;
});

const updateBanner = async (event) => {
  const file = event.target.files[0];
  if (!file) {
    toast.error("Nenhum arquivo selecionado");
    return;
  }

  // Validação do arquivo (opcional)
  const maxFileSize = 5 * 1024 * 1024; // 5 MB
  const allowedTypes = ["image/jpeg", "image/png"];

  if (file.size > maxFileSize) {
    toast.error("O arquivo excede o limite de 5 MB");
    return;
  }

  if (!allowedTypes.includes(file.type)) {
    toast.error("Formato de arquivo inválido. Apenas JPEG e PNG são permitidos.");
    return;
  }

  try {
    const formData = new FormData();
    formData.append("image", file);

    const response = await axios.post(
      `${ENDPOINTS.EDIT_BANNER_IMAGE}/${slug.value}/`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    // Atualiza a imagem do banner no frontend
    forumData.value.banner_image = response.data.image_url;
    toast.success("Banner atualizado com sucesso!");
  } catch (error) {
    console.error("Erro ao atualizar o banner:", error.response || error);
    toast.error(error.response?.data?.detail || "Erro ao atualizar o banner.");
  }



};
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
