<template>
  <div>
    <navbar />
    <main class="profile-page">
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

      <section id="dataProfile" class="relative py-16 bg-blueGray-200">

        <div class="container mx-auto px-4" id="infoProfile">
          <form @submit.prevent="handleSubmit">
            <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-xl rounded-lg -mt-64">
              <div class="px-6 justify-end">
                <div class="flex flex-wrap justify-end">
                  <div class="w-full lg:w-3/12 lg:order-2" style="padding-left: 100px;">
                    <div class="relative group">
                      <!-- Exibe a imagem de perfil -->
                      <img alt="Profile Picture" :src="profileImage || team2"
                        :value="userStore.user.username"
                        class="shadow-xl rounded-full h-auto align-middle border-none absolute -m-16 -ml-20 lg:-ml-16 max-w-150-px" />

                      <!-- Botão de upload visível no modo de edição -->
                      <div v-if="editMode"
                        class="absolute inset-0 bg-black bg-opacity-30 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
                        <label for="uploadImage" class="flex flex-col items-center cursor-pointer">
                          <i class="fas fa-upload text-white text-2xl"></i>
                          <span class="text-white text-sm">Editar</span>
                        </label>
                        <!-- Input oculto -->
                        <input id="uploadImage" type="file" accept="image/*" @change="handleImageUpload"
                          class="hidden" />
                      </div>
                    </div>
                  </div>

                  <!-- Edit mode -->
                  <div class="w-full lg:w-4/12 px-4 lg:order-3 lg:text-right lg:self-center">
                    <div class="py-6 px-3 mt-32 sm:mt-0">
                      <button id="editButton"
                        class="bg-emerald-500 active:bg-emerald-600 uppercase text-white font-bold hover:shadow-md shadow text-xs px-4 py-2 rounded outline-none focus:outline-none sm:mr-2 mb-1 ease-linear transition-all duration-150"
                        type="button" @click="toggleEdition">
                        {{ editMode ? 'Salvar' : 'Editar' }} <!-- Mudança aqui -->
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Input nome -->
                <div class="text-center mt-12">
                  <div class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase">
                    <i class="fas mr-2 text-lg text-blueGray-400"></i>
                    <!-- Campo editável para o Nome -->
                    <input type="text" id="name" 
                    v-model="form.name" 
                    :readonly="!editMode" 
                    @focus="onFocus"
                    @blur="onBlur"
                    class="border-none outline-none text-blueGray-700 font-bold uppercase focus:ring-0 focus:outline-none text-center" />
                    
                    <input type="text" id="surname" 
                    v-model="form.surname" 
                    :readonly="!editMode" 
                    @focus="onFocus"
                    @blur="onBlur"
                    class="border-none outline-none text-blueGray-700 font-bold uppercase focus:ring-0 focus:outline-none text-center" />
                  </div>
                  <!-- Input username -->
                  <div class="text-sm leading-normal mt-2 text-blueGray-400 font-semibold uppercase">
                    <!-- Exibição somente leitura do Username -->
                    <span>{{ userStore.user.username }}</span>
                  </div>
                </div>


                <!-- Biografia -->
                <div class="relative mt-6">
                  <label for="bio-textarea" class="block mb-2 text-sm font-medium text-blueGray-700">Biografia</label>
                  <div class="overflow-hidden">
                    <textarea id="bio-textarea" 
                    v-model="form.biography" 
                    :readonly="!editMode"
                    class="w-full resize-none border border-gray-300 rounded-lg px-3 py-2 align-top sm:text-sm focus:ring-blue-500 focus:border-blue-500"
                    rows="4" placeholder="Escreva sua biografia aqui..."></textarea>
                  </div>
                  <p v-if="errors.biography" class="text-red-500 text-xs mt-2">{{ errors.biography }}</p>
                </div>


                <!-- Linha superior: div1, div2, div3 -->
                <div class="rowForProfile mt-10 py-10 border-t border-blueGray-200 text-center">

                  <!-- Phone -->
                  <div class="itemForProfile">
                    <label for="cellphone-input" class="block mb-2 text-sm font-medium text-gray-900 ">Phone
                      number:</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 start-0 flex items-center pl-4 pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                          xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 19 18">
                          <path
                            d="M18 13.446a3.02 3.02 0 0 0-.946-1.985l-1.4-1.4a3.054 3.054 0 0 0-4.218 0l-.7.7a.983.983 0 0 1-1.39 0l-2.1-2.1a.983.983 0 0 1 0-1.389l.7-.7a2.98 2.98 0 0 0 0-4.217l-1.4-1.4a2.824 2.824 0 0 0-4.218 0c-3.619 3.619-3 8.229 1.752 12.979C6.785 16.639 9.45 18 11.912 18a7.175 7.175 0 0 0 5.139-2.325A2.9 2.9 0 0 0 18 13.446Z" />
                        </svg>
                      </div>
                      <input type="text" id="cellphone" 
                      v-model="form.cellphone" 
                      :readonly="!editMode"
                        @change="validateField('phone')" aria-describedby="helper-text-explanation"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400  dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" required />
                      <p v-if="errors.cellphone" class="text-red-500 text-xs">{{ errors.cellphone }}</p>
                    </div>
                  </div>

                  <!-- Email -->
                  <div class="itemForProfile">
                    <label for="UserEmail"
                      class="block mb-2 text-sm font-medium text-gray-900 ">Email:</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 start-0 flex items-center pl-4 pointer-events-none">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-500 dark:text-gray-400"
                          fill="currentColor" viewBox="0 0 20 20">
                          <path d="M2.94 6.94A2.5 2.5 0 015.5 5h9a2.5 2.5 0 012.5 1.94l-7 4.2-7-4.2z" />
                          <path d="M18 8.9l-7 4.2-7-4.2V14.5a2.5 2.5 0 002.5 2.5h9a2.5 2.5 0 002.5-2.5V8.9z" />
                        </svg>
                      </div>
                      <input type="email" id="UserEmail" 
                      v-model="form.email" 
                      :readonly="!editMode"
                        @change="validateField('email')"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400  dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        required />
                      <p v-if="errors.email" class="text-red-500 text-xs">{{ errors.email }}</p>
                    </div>
                  </div>

                  <!-- Senha
                  <div class="itemForProfile">
                    <label for="password-input"
                      class="block mb-2 text-sm font-medium text-gray-900 ">Senha:</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 start-0 flex items-center pl-4 pointer-events-none">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-500 dark:text-gray-400"
                          fill="currentColor" viewBox="0 0 20 20">
                          <path
                            d="M10 2a4 4 0 00-4 4v2a2 2 0 01-2 2v4a4 4 0 004 4h4a4 4 0 004-4v-4a2 2 0 01-2-2V6a4 4 0 00-4-4zm-1 6V6a1 1 0 112 0v2h-2z" />
                        </svg>
                      </div>
                      <input type="password" id="password-input" 
                      v-model="form.password" 
                      :readonly="!editMode"
                      :value="userStore.user.password"
                        @change="validateField('password')" placeholder="Senha"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400  dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        required />
                      <p v-if="errors.password" class="text-red-500 text-xs">{{ errors.password }}</p>
                    </div>
                  </div>
                </div> -->

                <!-- Linha inferior -->
                <div class="rowForProfile mt-10 py-10 text-center">

                  <!-- Data de Nascimento -->
                  <div class="itemForProfile">
                    <label for="birthday-input"
                      class="block mb-2 text-sm font-medium text-gray-900 ">Data
                      de Nascimento:</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 start-0 flex items-center pl-4 pointer-events-none">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-500 dark:text-gray-400"
                          fill="currentColor" viewBox="0 0 20 20">
                          <path
                            d="M6 2a2 2 0 00-2 2v1H2v2h2v9a2 2 0 002 2h8a2 2 0 002-2V7h2V5h-2V4a2 2 0 00-2-2H6zm8 15H6v-9h8v9z" />
                        </svg>
                      </div>
                      <input type="date" id="birthday-input" 
                      v-model="form.birthday" 
                      :readonly="!editMode"
                        @change="validateField('birthday')"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400  dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        required />
                      <p v-if="errors.birthday" class="text-red-500 text-xs">{{ errors.birthday }}</p>
                    </div>
                  </div>

                  <!-- Gênero -->
                  <div class="itemForProfile">
  <label for="gender-select" class="block mb-2 text-sm font-medium text-gray-900">
    Gênero:
  </label>
  <div class="relative">
    <select
      id="gender-select"
      name="gender"
      v-model="form.gender"
      :disabled="!editMode"
      class="custom-bg bg-blue-100 border border-gray-300 text-gray-900 text-sm rounded-lg 
             focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 
             dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400  
             dark:focus:ring-blue-500 dark:focus:border-blue-500"
    >
      <option value="" disabled selected>Selecione um gênero</option>
      <option value="M">Masculino</option>
      <option value="F">Feminino</option>
      <option value="O">Outro</option>
    </select>
  </div>
</div>

                </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </section>

      <section id="dataLocation" class="relative py-16 bg-blueGray-200">
        <div class="container mx-auto px-4">
          <form @submit.prevent="handleSubmit">
            <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-xl rounded-lg -mt-64">
              <div class="px-6 justify-end">
                <div class="relative w-full mb-3">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Estado</label>
                  <select 
                  v-model="form.state"
                  :value="userStore.user.state"
                  @change="[fetchCities, validateField('state')]" 
                  :disabled="!editMode"
                    class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
                    <option v-for="state in states" :key="state.code" :value="state.code">
                      {{ state.name }}
                    </option>
                  </select>
                </div>

                <div class="relative w-full mb-3">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Cidade</label>
                  <select 
                  v-model="form.locality" 
                  @change="[fetchNeighborhoods, validateField('locality')]"
                    :disabled="!editMode"
                    class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
                    <option v-for="city in cities" :key="city.name" :value="city.name">
                      {{ city.name }}

                    </option>
                  </select>
                </div>

                <div class="relative w-full mt-4">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Bairro</label>
                  <select 
                  v-model="form.neighborhood"
                   @change="validateField('neighborhood')" 
                   :disabled="!editMode"
                    class="w-full bg-white border border-gray-300 rounded px-4 py-2 text-gray-700 focus:outline-none focus:ring focus:border-blue-500">
                    <option v-for="neighborhood in neighborhoods" :key="neighborhood.id" :value="neighborhood.id">
                      {{ neighborhood.name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </form>
        </div>
      </section>

    </main>
    <footer-component />
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import Navbar from "@/components/Navbars/AuthNavbar.vue";
import FooterComponent from "@/components/Footers/Footer.vue";
import { onBeforeMount, reactive } from "vue";
import { useUserStore, apiClient } from "@/store/user.js"; // Ajuste o caminho conforme necessário
import { ENDPOINTS } from "../../../api.js";
import team2 from "@/assets/img/team-2-800x800.jpg";

export default {
  components: {
    Navbar,
    FooterComponent,
  },
  data() {
    return {
      form: {
        name: "",
        surname: "",
        email: "",
        cellphone: "",
        gender: "",
        biography: "",
        birthday: "",
        state: "",
        locality: "",
        neighborhood: "",
        neighborhood_id: "",
        neighborhood_changed: "",
      },
      states: [], // Lista de estados
      cities: [], // Lista de cidades
      neighborhoods: [], // Lista de bairros
      profileImage: null, // Variável para armazenar a nova imagem ou a atual
      errors: {},
      editMode: false, // Determina se o formulário está em modo de edição
      team2,
    };
  },
  setup() {
    const userStore = useUserStore();
    
    // // Inicializar o store e configurar o token
    // onBeforeMount(() => {
    //   const token = userStore.user?.access;
    //   if (token) {
    //     axios.defaults.headers.common["Authorization"] = "Bearer " + token;
    //   } else {
    //     axios.defaults.headers.common["Authorization"] = "";
    //   }
    // });
    
    // Reactive form state
    const form = reactive({
      name: userStore.user?.name || "",
      surname: userStore.user?.surname || "",
      email: userStore.user?.email || "",
      cellphone: userStore.user?.cellphone || "",
      gender: userStore.user?.gender || "",
      biography: userStore.user?.biography || "",
      birthday: userStore.user?.birthday || "",
      state: userStore.user?.state || "",
      locality: userStore.user?.locality || "",
      neighborhood: userStore.user?.neighborhood || "",
      neighborhood_id: userStore.user?.neighborhood_id || "",
      neighborhood_changed: false,
    });
    console.log(form)

    return {
      userStore, // Expor o store para uso no template
      form, // Expor o formulário reativo
    };
},

async mounted() {
    await this.fetchStates();
  },


  methods: {
    onStateChange(event){
      this.fetchCities();
      this.validateField('state');
    },
    async fetchStates() {
      try {
        const response = await axios.get(ENDPOINTS.STATES);
        this.states = response.data;
      } catch (error) {
        alert("Erro ao carregar os estados.");
      }
    },
    async fetchCities() {
      if (!this.form.state) {
        this.cities = [];
        this.neighborhoods = [];
        return;
      }
      try {
        const response = await axios.get(`${ENDPOINTS.CITIES}/${this.form.state}/`);
        this.cities = response.data;
        this.neighborhoods = []; // Resetar bairros ao alterar a cidade
      } catch (error) {
        alert("Erro ao carregar as cidades.");
      }
    },
    onCityChange(event){
      this.fetchNeighborhoods();
      this.validateField('locality');
    },
    async fetchNeighborhoods() {
      if (!this.form.locality) {
        this.neighborhoods = [];
        return;
      }
      try {
        const response = await axios.get(`${ENDPOINTS.NEIGHBORHOODS}/${this.form.state}/${this.form.locality}/`);
        this.neighborhoods = response.data;
      } catch (error) {
        alert("Erro ao carregar os bairros.");
      }
    },

    toggleEdition() {
      if (this.editMode) {
        // Salvar: valida campos antes de alternar
        Object.keys(this.form).forEach((field) => this.validateField(field));
        if (Object.keys(this.errors).some((key) => this.errors[key])) {
          alert("Por favor, corrija os erros antes de salvar.");
          return;
        }
      }
      this.editMode = !this.editMode;
      if (this.editMode==false){
        this.handleSubmit()
      }
    },

    onFocus() {
    },
    onBlur() {
    },



    validateField(field) {
      const calculateAge = (birthDate) => {
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDifference = today.getMonth() - birth.getMonth();
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birth.getDate())) {
          age--;
        }
        return age;
      };

      switch (field) {
        case "birthDate":
          if (!this.form.birthDate) {
            this.errors.birthDate = "Birth Date is required.";
          } else if (calculateAge(this.form.birthDate) < 16) {
            this.errors.birthDate = "You must be at least 16 years old.";
          } else {
            this.errors.birthDate = "";
          }
          break;
        case "email":
          if (!this.form.email) {
            this.errors.email = "Email is required.";
          } else if (!/\S+@\S+\.\S+/.test(this.form.email)) {
            this.errors.email = "Invalid email format.";
          } else {
            this.errors.email = "";
          }
          break;
        case "username":
          // this.errors.username = this.form.username ? "" : "Username is required.";
          break;
        case "password":
          this.errors.password = this.form.password
            ? (/[A-Z]/.test(this.form.password) ? "" : "A senha deve conter ao menos uma letra maiúscula.") ||
              (/[a-z]/.test(this.form.password) ? "" : "A senha deve conter ao menos uma letra minúscula.") ||
              (/\d/.test(this.form.password) ? "" : "A senha deve conter ao menos um número.") ||
              (/[\W_]/.test(this.form.password) ? "" : "A senha deve conter ao menos um caractere especial.") ||
              (this.form.password.length >= 8 ? "" : "A senha deve ter no mínimo 8 caracteres.")
            : "A senha é obrigatória.";
          break;
      }
    },

    async handleSubmit() {
      const userStore = useUserStore(); // Acessa o userStore diretamente
      this.form.neighborhood_changed =
        this.form.neighborhood_id !== userStore.user?.neighborhood_id;

      Object.keys(this.form).forEach((field) => this.validateField(field));

      if (Object.keys(this.errors).some((key) => this.errors[key])) return;


      if (userStore.user.isAuthenticated){
          try {
            const response = await apiClient
            .post(ENDPOINTS.EDIT, this.form, {
            headers: { "Content-Type": "application/json" },
          });

          const data = response.data;
          userStore.setUserInfo(this.form); // Atualiza as informações do usuário no store


          if (!response.ok) {
            if (data.errors) {
              for (const [field, messages] of Object.entries(data.errors)) {
                this.errors[field] = messages.join(" ");
              }
            }
            throw new Error(data.message || "Failed to save.");
          }

        } catch (error) {
          alert(error.message || "Something went wrong.");
        }
      }
        else{
          alert("User not authenticated")
        }
    },
  },
};
</script>


<style scoped>
#dataLocation {
  /* Cria espaço suficiente entre dataProfile e dataLocation */
  padding-top: 200px;
}

.custom-bg {
  background-color: #ffffff; /* Cor azul personalizada */
}

.bg-white {
  padding-top: 20px;
  padding-bottom: 2rem;
  /* Adiciona um espaço interno inferior */
}

input {
  background-color: #f9fafb; /* Cor padrão */
  color: #1f2937; /* Cor do texto */
  border: 1px solid transparent; /* Sem borda em modo readonly */
}

input:focus {
  border-color: #60a5fa; /* Ajuste a borda ao focar */
  outline: none;
}

input:not([readonly]) {
  background-color: #ffffff; /* Mantenha a mesma cor de fundo */
  border: 1px solid #d1d5db; /* Adicione borda suave */
}
</style>
