<template>
  <div class="container mx-auto px-4 h-full">
    <div class="flex content-center items-end justify-center h-full mt-reg">
      <div class="w-full lg:w-6/12 px-4">
        <div
          class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-200 border-0">
          <div class="flex-auto px-4 lg:px-10 py-10">
            <form @submit.prevent="handleSubmit">
              <!-- Nome e Sobrenome -->
              <div class="flex gap-4 space-x-4">
                <div class="relative w-full mb-3">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Nome</label>
                  <input type="text" v-model="form.name" @change="validateField('name')"
                    class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                    placeholder="Nome" />
                  <p v-if="errors.name" class="text-red-500 text-xs">{{ errors.name }}</p>
                </div>
                <div class="relative w-full mb-3">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Sobrenome</label>
                  <input type="text" v-model="form.surname" @change="validateField('surname')"
                    class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                    placeholder="Sobrenome" />
                  <p v-if="errors.surname" class="text-red-500 text-xs">{{ errors.surname }}</p>
                </div>
              </div>

              <!-- Data de Nascimento -->
              <div class="relative w-full mb-3">
                <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Data de Nascimento</label>
                <input type="date" v-model="form.birthday" @change="validateField('birthday')"
                  class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
                <p v-if="errors.birthday" class="text-red-500 text-xs">{{ errors.birthday }}</p>
              </div>

              <!-- Email -->
              <div class="relative w-full mb-3">
                <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Email</label>
                <input type="email" v-model="form.email" @change="validateField('email')"
                  class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  placeholder="Email" />
                <p v-if="errors.email" class="text-red-500 text-xs">{{ errors.email }}</p>
              </div>

              <!-- Nome de Usuário -->
              <div class="relative w-full mb-3">
                <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Nome de Usuário</label>
                <input type="text" v-model="form.username" @change="validateField('username')"
                  class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                  placeholder="Nome de Usuário" />
                <p v-if="errors.username" class="text-red-500 text-xs">{{ errors.username }}</p>
              </div>

              <!-- Senha e Confirmar Senha -->
              <div class="flex gap-4 space-x-4">
                <div class="relative w-full mb-3">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Senha</label>
                  <input type="password" v-model="form.password" @change="validateField('password')"
                    class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
                  <p v-if="errors.password" class="text-red-500 text-xs">{{ errors.password }}</p>
                </div>
                <div class="relative w-full mb-3">
                  <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Confirmar senha</label>
                  <input type="password" v-model="form.confirmPassword" @change="validateField('confirmPassword')"
                    class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
                  <p v-if="errors.confirmPassword" class="text-red-500 text-xs">{{ errors.confirmPassword }}</p>
                </div>
              </div>

              <!-- Concordar com Políticas -->
              <div>
                <label class="inline-flex items-center cursor-pointer">
                  <input id="customCheckLogin" type="checkbox" v-model="form.agree_policy"
                    @change="validateField('agree_policy')"
                    class="form-checkbox border-0 rounded text-blueGray-700 ml-1 w-5 h-5 ease-linear transition-all duration-150" />
                  <span class="ml-2 text-sm font-semibold text-blueGray-600">
                    Concordo com as
                    <a href="javascript:void(0)" class="text-emerald-500">Políticas de Privacidade</a>
                  </span>
                </label>
                <p v-if="errors.agree_policy" class="text-red-500 text-xs">{{ errors.agree_policy }}</p>
              </div>

              <!-- Botão de Enviar -->
              <div class="text-center mt-6">
                <button
                  class="bg-blueGray-800 text-white active:bg-blueGray-600 text-sm font-varela uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
                  type="submit">
                  Criar conta
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>


      <div class="w-full lg:w-6/12 px-4">
        <div class="w-full h-half flex flex-col items-center justify-center min-h-[200px] relative ">
          <img src="@/assets/img/registerLogo.png" alt="Register Logo" class="w-32 h-half mb-4 relative">
        </div>
        <div
          class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-200 border-0">
          <div class="flex-auto px-4 lg:px-10 py-10">
            <form @submit.prevent="handleLocationSubmit">
              <div class="relative w-full mb-3">
                <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Estado</label>
                <select v-model="form.state" @change="onStateChange"
                  class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
                  <option value="">Selecione um Estado</option>
                  <option v-for="state in states" :key="state.code" :value="state.code">
                    {{ state.name }}
                  </option>
                </select>
              </div>

              <div class="relative w-full mb-3">
                <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Cidade</label>
                <select v-model="form.locality" @change="onCityChange"
                  class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
                  <option value="">Selecione uma Cidade</option>
                  <option v-for="city in cities" :key="city.name" :value="city.name">
                    {{ city.name }}
                  </option>
                </select>
              </div>

              <div class="relative w-full mt-4">
                <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Bairro</label>
                <select v-model="form.neighborhood" @change="validateField('neighborhood')"
                  class="w-full bg-white border border-gray-300 rounded px-4 py-2 text-gray-700 focus:outline-none focus:ring focus:border-blue-500">
                  <option value="">Selecione um Bairro</option>
                  <option v-for="neighborhood in neighborhoods" :key="neighborhood.id" :value="neighborhood.id">
                    {{ neighborhood.name }}
                  </option>
                </select>
              </div>
            </form>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ENDPOINTS } from '../../../api.js';
import { useToast } from 'vue-toastification';


/*eslint-disable*/
export default {
  data() {
    return {
      form: {
        name: "",
        surname: "",
        birthday: "",
        email: "",
        username: "",
        password: "",
        confirmPassword: "",
        agree_policy: false,
        state: "", // Estado selecionado
        locality: "", // Cidade selecionada
        neighborhood: "", // Bairro selecionado
      },
      errors: {},
      states: [], // Lista de estados
      cities: [], // Lista de cidades
      neighborhoods: [], // Lista de bairros
    };
  },
  setup() {
    const router = useRouter();
    const toast = useToast();
    return { router, toast };

  },
  async mounted() {
    await this.fetchStates();
  },
  methods: {
    onStateChange(event) {
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
    onCityChange(event) {
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
        case "name":
          this.errors.name = this.form.name
            ? (/^[a-zA-Z\s]+$/.test(this.form.name) ? "" : "O nome deve conter apenas letras e espaços.")
            : "O nome é obrigatório.";
          break;
        case "surname":
          this.errors.surname = this.form.surname
            ? (/^[a-zA-Z\s]+$/.test(this.form.surname) ? "" : "O sobrenome deve conter apenas letras e espaços.")
            : "O sobrenome é obrigatório.";
          break;
        case "birthday":
          if (!this.form.birthday) {
            this.errors.birthday = "A data de nascimento é obrigatória.";
          } else if (calculateAge(this.form.birthday) < 16) {
            this.errors.birthday = "Você deve ter pelo menos 16 anos.";
          } else {
            this.errors.birthday = "";
          }
          break;
        case "email":
          if (!this.form.email) {
            this.errors.email = "O email é obrigatório.";
          } else if (!/\S+@\S+\.\S+/.test(this.form.email)) {
            this.errors.email = "Formato de email inválido.";
          } else {
            this.errors.email = "";
          }
          break;
        case "username":
          this.errors.username = this.form.username ? "" : "O nome de usuário é obrigatório.";
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
        case "confirmPassword":
          if (!this.form.confirmPassword) {
            this.errors.confirmPassword = "A confirmação de senha é obrigatória.";
          } else if (this.form.password !== this.form.confirmPassword) {
            this.errors.confirmPassword = "As senhas não coincidem.";
          } else {
            this.errors.confirmPassword = "";
          }
          break;
        case "agree_policy":
          this.errors.agree_policy = this.form.agree_policy ? "" : "Você deve concordar com a Política de Privacidade.";
          break;
        case "state":
          this.errors.state = this.form.state ? "" : "Você deve selecionar um estado.";
          break;
        case "locality":
          this.errors.locality = this.form.locality ? "" : "Você deve selecionar uma cidade.";
          break;
        case "neighborhood":
          this.errors.neighborhood = this.form.neighborhood ? "" : "Você deve selecionar um bairro.";
          break;
      }
    },
    async handleSubmit() {
      Object.keys(this.form).forEach((field) => this.validateField(field));

      if (Object.keys(this.errors).some((key) => this.errors[key])) return;

      try {
        const response = await axios.post(ENDPOINTS.REGISTER, this.form, {
          headers: { "Content-Type": "application/json" },
        });

        this.toast.success("Conta criada com sucesso! Faça o login!")
        this.router.push('/auth/login');
      } catch (error) {
        if (error.response && error.response.data.errors) {
          for (const [field, messages] of Object.entries(error.response.data.errors)) {
            this.errors[field] = messages.join(" ");
          }
        } else {
          this.toast.error(error.message || "Algo deu errado.");
        }
      }
    },
  },
};
</script>
