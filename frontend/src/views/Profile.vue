<template>
  <MainLayout>
    <div class="bg-blueGray-200 -mt-24 ">
      <section class="relative block h-600-px">
        <div class="absolute top-0 w-full h-full bg-center bg-cover" style="
            background-image: url('https://images.unsplash.com/photo-1499336315816-097655dcfbda?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2710&q=80');
          ">
          <span id="blackOverlay" class="w-full h-full absolute opacity-50 bg-black"></span>
        </div>
        <div class="top-auto bottom-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden h-70-px"
          style="transform: translateZ(0);">
          <svg class="absolute bottom-0 overflow-hidden" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
            version="1.1" viewBox="0 0 2560 100" x="0" y="0">
            <polygon class="text-blueGray-200 fill-current" points="2560 0 2560 100 0 100"></polygon>
          </svg>
        </div>
      </section>

      <section id="dataProfile" class="flex bg-blueGray-200 min-h-[calc(100vh-600px)]">
        <div class="container mx-auto px-4 -pt-8 " id="infoProfile">
          
          <form @submit.prevent="openModalConfirmEdit">
            <div class="relative flex flex-col h-850-px  min-w-0 break-words bg-white w-full mb-6 shadow-xl rounded-lg -mt-64">
              <!-- Container da Imagem de Perfil -->
              <div class="relative pt-16 pb-8">
                <div class="flex flex-wrap justify-center">
                  <div class="w-full flex justify-center">
                    <div class="relative">
                      <input 
                        type="file" 
                        ref="fileInput"
                        accept="image/*"
                        style="display: none;"
                        @change="handleImageUpload"
                      >
                      <img 
                        alt="Foto de Perfil" 
                        :src="profileImageUrl"
                        :value="userStore.user.username"
                        style="width: 200px; height: 200px; min-width: 200px; min-height: 200px; max-width: 200px; max-height: 200px;"
                        class="shadow-xl rounded-full object-cover border-4 border-white transition-transform duration-300"
                        :class="{ 'cursor-pointer hover:opacity-80': editMode }"
                        @click="editMode && $refs.fileInput.click()"
                      >
                    </div>
                  </div>
                  
                  <!-- Botão de Editar -->
                  <div class="w-full flex justify-end px-6 absolute top-4 right-0">
                    <button 
                      id="editButton"
                      class="bg-emerald-500 active:bg-emerald-600 uppercase text-white 
                             font-bold hover:shadow-md shadow text-xs px-6 py-3 
                             rounded outline-none focus:outline-none
                             transition-all duration-150 transform hover:scale-105"
                      type="button" 
                      @click="editMode ? saveChanges() : enterEditMode()"
                    >
                      {{ editMode ? 'Salvar' : 'Editar' }}
                    </button>
                  </div>
                </div>
              </div>

              <div class="px-6 justify-end">
                <!-- Input nome -->
                <div class="text-center mt-12">
                  <div class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase">
                    <i class="fas mr-2 text-lg text-blueGray-400"></i>
                    <!-- Campo editável para o Nome -->
                    <input type="text" id="name" v-model="form.name" :readonly="!editMode" @focus="onFocus"
                      @blur="onBlur"
                      class="border-none outline-none text-blueGray-700 font-bold uppercase focus:ring-0 focus:outline-none text-center" />

                    <input type="text" id="surname" v-model="form.surname" :readonly="!editMode" @focus="onFocus"
                      @blur="onBlur"
                      class="border-none outline-none text-blueGray-700 font-bold uppercase focus:ring-0 focus:outline-none text-center" />
                  </div>
                  <!-- Input username -->
                  <div class="text-sm leading-normal mt-2 text-blueGray-400 font-semibold uppercase">
                    <!-- Exibição somente leitura do Username -->
                    <span>@{{ userStore.user.account.username }}</span>
                  </div>
                  
                  <!-- Título/Recompensa -->
                  <div class="text-xl leading-normal mt-2 text-blue-500 font-semibold">
                    <span>{{ userStore.user.account.status }}</span>
                  </div>
                </div>


                <!-- Biografia -->
                <div class="relative mt-6">
                  <label for="bio-textarea" class="block mb-2 text-sm font-medium text-gray-900">Biografia</label>
                  <div class="overflow-hidden">
                    <textarea id="bio-textarea" v-model="form.biography" :readonly="!editMode"
                      class="w-full resize-none border border-gray-300 rounded-lg px-3 py-2 align-top sm:text-sm focus:ring-blue-500 focus:border-blue-500"
                      rows="4" placeholder="Escreva sua biografia aqui..."></textarea>
                  </div>
                  <p v-if="errors.biography" class="text-red-500 text-xs mt-2">{{ errors.biography }}</p>
                </div>


                <!-- Linha com 3 colunas -->
                <div class="flex flex-row gap-4 mt-10 py-10 border-t border-blueGray-200">
                  <!-- Coluna 1: Celular -->
                  <div class="flex-1 px-4">
                    <label for="cellphone-input" class="block mb-2 text-sm font-medium text-gray-900">Nº Celular:</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 start-0 flex items-center pl-4 pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                          xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 19 18">
                          <path
                            d="M18 13.446a3.02 3.02 0 0 0-.946-1.985l-1.4-1.4a3.054 3.054 0 0 0-4.218 0l-.7.7a.983.983 0 0 1-1.39 0l-2.1-2.1a.983.983 0 0 1 0-1.389l.7-.7a2.98 2.98 0 0 0 0-4.217l-1.4-1.4a2.824 2.824 0 0 0-4.218 0c-3.619 3.619-3 8.229 1.752 12.979C6.785 16.639 9.45 18 11.912 18a7.175 7.175 0 0 0 5.139-2.325A2.9 2.9 0 0 0 18 13.446Z" />
                        </svg>
                      </div>
                      <input type="text" id="cellphone" v-model="form.cellphone" :readonly="!editMode"
                        @change="validateField('cellphone')" aria-describedby="helper-text-explanation"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                        pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" required />
                      <p v-if="errors.cellphone" class="text-red-500 text-xs">{{ errors.cellphone }}</p>
                    </div>
                  </div>

                  <!-- Coluna 2: Data de Nascimento -->
                  <div class="flex-1 px-4">
                    <label for="birthday-input" class="block mb-2 text-sm font-medium text-gray-900">Data de Nascimento:</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 start-0 flex items-center pl-4 pointer-events-none">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-500 dark:text-gray-400"
                          fill="currentColor" viewBox="0 0 20 20">
                          <path d="M6 2a2 2 0 00-2 2v1H2v2h2v9a2 2 0 002 2h8a2 2 0 002-2V7h2V5h-2V4a2 2 0 00-2-2H6zm8 15H6v-9h8v9z" />
                        </svg>
                      </div>
                      <input type="date" id="birthday-input" v-model="form.birthday" :readonly="!editMode"
                        @change="validateField('birthday')"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                        required />
                      <p v-if="errors.birthday" class="text-red-500 text-xs">{{ errors.birthday }}</p>
                    </div>
                  </div>

                  <!-- Coluna 3: Gênero -->
                  <div class="flex-1 px-4">
                    <label for="gender-select" class="block mb-2 text-sm font-medium text-gray-900">Gênero:</label>
                    <div class="relative">
                      <select id="gender-select" name="gender" v-model="form.gender" :disabled="!editMode" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg 
                               focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                        <option value="" disabled selected>Selecione um gênero</option>
                        <option value="M">Masculino</option>
                        <option value="F">Feminino</option>
                        <option value="O">Outro</option>
                      </select>
                    </div>
                  </div>
                </div>
                <section class="flex justify-center items-center">
                  <div class="flex space-x-4">
                    <button type="button"
                      class="bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
                             focus:outline-none focus:ring-2 focus:ring-emerald-500 
                             transition duration-300 transform hover:scale-105"
                      @click="openModalNeighChange()">
                      Alterar Bairro
                    </button>

                    <button type="button"
                      class="bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
                             focus:outline-none focus:ring-2 focus:ring-emerald-500 
                             transition duration-300 transform hover:scale-105"
                      @click="openModalPasswordChange()">
                      Alterar Senha
                    </button>

                    <button type="button"
                      class="bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
                             focus:outline-none focus:ring-2 focus:ring-emerald-500 
                             transition duration-300 transform hover:scale-105"
                      @click="openModalEmailChange()">
                      Alterar Email
                    </button>

                    <button type="button"
                      class="bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
                             focus:outline-none focus:ring-2 focus:ring-emerald-500 
                             transition duration-300 transform hover:scale-105"
                      @click="logout()">
                      Deslogar
                    </button>

                    <button type="button"
                      class="bg-red-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-red-600 
                             focus:outline-none focus:ring-2 focus:ring-red-500 
                             transition duration-300 transform hover:scale-105"
                      @click="openModalConfirmDelete()">
                      Excluir conta
                    </button>
                  </div>
                </section>
              </div>
            </div>
          </form>
        </div>

      </section>
      <ModalChangeEmail :isModalChangeEmailOpen="isModalChangeEmailOpen" @close="closeModalEmailChange" />

      <ModalChangePassword :isModalChangePasswordOpen="isModalChangePasswordOpen" @close="closeModalChangePassword" />

      <ModalChangeNeighborhood :isModalNeighChangeOpen="isModalNeighChangeOpen" @close="closeModalNeighChange" />

      <ModalComplexConfimation v-if="isConfirmationModalOpen" :isModalDeleteAccountOpen="isConfirmationModalOpen"
        @close="closeModalConfirmDelete" @confirm="handleConfirmation" />

      <ModalSimpleConfirmation :isSimpleConfirmModalOpen="isEditConfirmationModalOpen" @close="closeModalConfirmEdit"
        @confirm="handleEditConfirmation" />

    </div>
  </MainLayout>
</template>

<script>
/* eslint-disable */
import MainLayout from "@/layouts/mainLayout.vue";
import ModalChangeNeighborhood from "../components/Modals/ModalChangeNeighborhood.vue";
import ModalChangePassword from "../components/Modals/ModalChangePassword.vue";
import ModalChangeEmail from "../components/Modals/ModalChangeEmail.vue";
import ModalComplexConfimation from "../components/Modals/ModalComplexConfimation.vue";
import ModalSimpleConfirmation from "../components/Modals/ModalSimpleConfirmation.vue";
import { onBeforeMount, reactive, ref } from "vue";
import { useUserStore } from "../store/user.js";
import axios from "axios";
import router from "../router/index.js";
import { ENDPOINTS } from "../../api.js";
import profile from "@/assets/img/profilePic.jpg";
import { useToast } from "vue-toastification";

export default {

  components: {
    MainLayout,
    ModalChangeNeighborhood,
    ModalChangePassword,
    ModalChangeEmail,
    ModalComplexConfimation,
    ModalSimpleConfirmation,
  },
  data() {

    return {
      errors: {},
      editMode: false,
      profile,
      isModalNeighChangeOpen: false,
      isModalChangePasswordOpen: false,
      isModalChangeEmailOpen: false,
      isConfirmationModalOpen: false,
      isEditConfirmationModalOpen: false,
      router,
    };
  },
  setup() {
    const userStore = useUserStore();
    const toast = useToast();
    const fileInput = ref(null);

    onBeforeMount(() => {
      if (!userStore.user.isAuthenticated) {
        toast.info("Autenticação necessária");
        router.push("/login");
      }
    });

    // Reactive form state
    const form = reactive({
      name: userStore.user.account.name || "",
      surname: userStore.user.account.surname || "",
      birthday: userStore.user.account.birthday || "",
      cellphone: userStore.user.account.cellphone || "",
      gender: userStore.user.account.gender || "",
      biography: userStore.user.account.biography || "",
      status: userStore.user.account.status || "",
    });

    return {
      userStore,
      form,
      toast,
      fileInput
    };
  },

  methods: {
    // Abre o modal
    openModalNeighChange() {
      this.isModalNeighChangeOpen = true;
    },

    // Fecha o modal
    closeModalNeighChange() {
      this.isModalNeighChangeOpen = false;
    },

    // Abre o modal
    openModalPasswordChange() {
      this.isModalChangePasswordOpen = true;
    },

    // Fecha o modal
    closeModalChangePassword() {
      this.isModalChangePasswordOpen = false;
    },

    // Abre o modal
    openModalEmailChange() {
      this.isModalChangeEmailOpen = true;
    },

    // Fecha o modal
    closeModalEmailChange() {
      this.isModalChangeEmailOpen = false;
    },

    // Abre o modal
    openModalConfirmDelete() {
      this.isConfirmationModalOpen = true;
    },

    // Fecha o modal
    closeModalConfirmDelete() {
      this.isConfirmationModalOpen = false;
    },

    // Abre o modal
    openModalConfirmEdit() {
      this.isEditConfirmationModalOpen = true;
    },

    // Fecha o modal
    closeModalConfirmEdit() {
      this.isEditConfirmationModalOpen = false;

    },

    enterEditMode() {
      this.editMode = true;
    },

    saveChanges() {
      this.editMode = false;
      this.toast.info("Salvando as alterações...", { timeout: 7000 });
      this.openModalConfirmEdit()
    },


    //Logout
    logout() {
      this.userStore.removeToken()
      router.push('/login')
    },

    async delete_account() {
      try {
        const response_delete = await axios.post(ENDPOINTS.DELETE_ACCOUNT);
        if (response_delete.success) {
          this.toast.success("Conta Excluída com sucesso");
          this.logout();
        } else {
          this.toast.error("Erro ao excluir a conta")
        }
      } catch (error) {
        this.toast.error("Erro de conexão com o servidor ")
      }
    },


    validateField(field) {
      const calculateAge = (birthday) => {
        const today = new Date();
        const birth = new Date(birthday);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDifference = today.getMonth() - birth.getMonth();
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birth.getDate())) {
          age--;
        }
        return age;
      };

      switch (field) {
        case "name":
          if (!this.form.name) {
            this.errors.name = "Nome é obrigatório.";
          } else if (!/^[A-Za-zÀ-ÿ\s]+$/.test(this.form.name)) {
            this.errors.name = "Nome inválido. Apenas letras e espaços são permitidos.";
          } else {
            this.errors.name = "";
          }
          break;

        case "surname":
          if (!this.form.surname) {
            this.errors.surname = "Sobrenome é obrigatório.";
          } else if (!/^[A-Za-zÀ-ÿ\s]+$/.test(this.form.surname)) {
            this.errors.surname = "Sobrenome inválido. Apenas letras e espaços são permitidos.";
          } else {
            this.errors.surname = "";
          }
          break;

        case "cellphone":
          if (this.form.cellphone === "") {
            this.errors.cellphone = ""; // Permite campo vazio (se necessário)
          } else if (!/^(?:\+55\s?)?(\(?\d{2}\)?[\s\-]?)?\d{4,5}[\s\-]?\d{4}$/.test(this.form.cellphone)) {
            this.errors.cellphone = "Formato de celular inválido. Exemplo: (xx) xxxxx-xxxx";
          } else {
            this.errors.cellphone = "";
          }
          break;

        case "birthday":
          if (!this.form.birthday) {
            this.errors.birthday = "Data de nascimento é obrigatória.";
          } else if (calculateAge(this.form.birthday) < 16) {
            this.errors.birthday = "Você deve ter pelo menos 16 anos.";
          } else {
            this.errors.birthday = "";
          }
          break;

        case "biography":
          if (this.form.biography.length > 300) {
            this.errors.biography = "A biografia deve ter no máximo 300 caracteres.";
          } else {
            this.errors.biography = "";
          }
          break;

        default:
          this.errors[field] = "";
      }
    },

    handleConfirmation(isConfirmed) {
      this.closeModalConfirmDelete();
      if (!isConfirmed) {
        return;
      }
      this.delete_account()
    },

    handleEditConfirmation() {
      this.editMode = false;
      this.handleSubmit()
      this.closeModalConfirmEdit();
    },

    async handleSubmit() {
      const userStore = this.userStore;

      try {
        const response = await axios.post(ENDPOINTS.EDIT, this.form);
        this.userStore.setUserInfo(this.form)
        this.toast.success("Suas informações foram atualizadas!")
      } catch (error) {
        // Verifique se error.response existe antes de acessar os campos de erro
        if (error.response && error.response.data && error.response.data.errors) {
          for (const [field, messages] of Object.entries(error.response.data.errors)) {
            this.errors[field] = Array.isArray(messages) ? messages.join(" ") : messages;
          }
        } else {
          // Caso a resposta de erro seja indefinida
          this.toast.error(error.response?.data?.message || "Erro ao salvar as alterações.");
        }
      }
    },
    
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        this.toast.error('Por favor, selecione apenas arquivos de imagem.');
        return;
      }

      const maxSize = 5 * 1024 * 1024;
      if (file.size > maxSize) {
        this.toast.error('A imagem deve ter menos de 5MB.');
        return;
      }

      try {
        const formData = new FormData();
        formData.append('image', file);

        const response = await axios.post(`${ENDPOINTS.EDIT_PROFILE_IMAGE}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.status === 200) {
          // Atualiza diretamente o store
          this.userStore.user.account.profile_image = response.data.image_url;

          this.toast.success('Foto de perfil atualizada com sucesso!');
        }
      } catch (error) {
        console.error('Erro ao fazer upload da imagem:', error);
        this.toast.error('Erro ao atualizar a foto de perfil. Tente novamente.');
      }
    },
    
  },
  
  computed: {
    profileImageUrl() {
      return this.userStore.user.account.profile_image || this.profile;
    }
  }
};
</script>


<style scoped>
#dataLocation {
  /* Cria espaço suficiente entre dataProfile e dataLocation */
  padding-top: 200px;
}

.custom-bg {
  background-color: #ffffff;
  /* Cor azul personalizada */
}
  

input {
  background-color: #f9fafb;
  /* Cor padrão */
  color: #1f2937;
  /* Cor do texto */
  border: 1px solid transparent;
  /* Sem borda em modo readonly */
}

input:focus {
  border-color: #60a5fa;
  /* Ajuste a borda ao focar */
  outline: none;
}

input:not([readonly]) {
  background-color: #ffffff;
  /* Mantenha a mesma cor de fundo */
  border: 1px solid #d1d5db;
  /* Adicione borda suave */
}

#infoProfile form > div {
  min-height: 800px;
}

#dataProfile {
  padding-top: 0;
}
</style>
