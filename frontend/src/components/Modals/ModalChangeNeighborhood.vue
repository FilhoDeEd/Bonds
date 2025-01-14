<template>
  <div v-if="isModalNeighChangeOpen" class="modal-overlay">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">X</button>

      <!-- Conteúdo do modal -->
      <form @submit.prevent="handleNeighborhoodChange">
        <div class="relative w-full mb-3">
          <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2">Estado</label>
          <select v-model="form.state" @change="onStateChange"
            class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
            <option value="">Selecione um Estado</option>
            <option v-for="state in states" :key="state.code" :value="state.code">
              {{ state.name }}
            </option>
          </select>
          <span v-if="errors.state" class="text-red-500 text-xs">{{ errors.state }}</span>
        </div>

        <!-- Cidade -->
        <div class="relative w-full mb-3">
          <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2">Cidade</label>
          <select v-model="form.locality" @change="onCityChange"
            class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
            <option value="">Selecione uma Cidade</option>
            <option v-for="city in cities" :key="city.name" :value="city.name">
              {{ city.name }}
            </option>
          </select>
          <span v-if="errors.locality" class="text-red-500 text-xs">{{ errors.locality }}</span>
        </div>

        <!-- Bairro -->
        <div class="relative w-full mb-3">
          <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2">Bairro</label>
          <select v-model="form.neighborhood" @change="validateField('neighborhood')"
            class="border-0 px-3 py-3 bg-white text-blueGray-600 rounded text-sm shadow focus:outline-none focus:ring w-full">
            <option value="">Selecione um Bairro</option>
            <option v-for="neighborhood in neighborhoods" :key="neighborhood.id" :value="neighborhood.id">
              {{ neighborhood.name }}
            </option>
          </select>
          <span v-if="errors.neighborhood" class="text-red-500 text-xs">{{ errors.neighborhood }}</span>
        </div>

        <!-- Botão Confirmar -->
        <div class="text-center mt-6">
          <button type="submit"
            class="bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
                   focus:outline-none focus:ring-2 focus:ring-emerald-500 
                   transition duration-300 transform hover:scale-105">
            Confirmar
          </button>
        </div>
      </form>
      <ModalComplexConfimation v-if="isConfirmationModalOpen" :isModalDeleteAccountOpen="isConfirmationModalOpen"
        @close="isConfirmationModalOpen = false" @confirm="handleConfirmation" />
    </div>
  </div>
</template>



<script>
/* eslint-disable */

import axios from 'axios';
import router from "../../router/index.js";
import { ENDPOINTS } from '../../../api.js';
import { useUserStore } from '../../store/user.js';
import ModalComplexConfimation from './ModalComplexConfimation.vue';
import { useToast } from 'vue-toastification';
import { useForumListStore } from '../../store/forumListStore.js';

export default {
  data() {
    return {
      states: [],
      cities: [],
      neighborhoods: [],
      form: {
        state: null,
        locality: null,
        neighborhood: null,
        neighborhood_name: null,
      },
      errors: {},
      router,
      isConfirmationModalOpen: false,
      userStore: useUserStore(),
      toast: useToast(),
      useForumList: useForumListStore(),
    };
  },
  props: {
    isModalNeighChangeOpen: Boolean, // Propriedade para controlar se o modal está aberto
  },

  components: {
    ModalComplexConfimation,
  },

  computed: {
    selectedNeighborhoodName() {
      const selectedNeighborhood = this.neighborhoods.find(
        neighborhood => neighborhood.id === this.form.neighborhood
      );
      return selectedNeighborhood ? selectedNeighborhood.name : '';
    }
  },

  watch: {
    'form.neighborhood'(newValue) {
      const selectedNeighborhood = this.neighborhoods.find(
        neighborhood => neighborhood.id === newValue
      );
      this.form.neighborhood_name = selectedNeighborhood ? selectedNeighborhood.name : '';
    }
  },


  methods: {

    closeModal() {
      this.$emit('close'); // Emite evento para o componente pai fechar o modal
    },


    // Buscar lista de estados
    async fetchStates() {
      try {
        const response = await axios.get(ENDPOINTS.STATES);
        this.states = response.data;
      } catch {
        this.toast.error('Erro ao carregar os estados.');
      }
    },

    // Buscar lista de cidades
    async fetchCities() {
      if (!this.form.state) {
        this.cities = [];
        this.neighborhoods = [];
        return;
      }
      try {
        const response = await axios.get(`${ENDPOINTS.CITIES}/${this.form.state}/`);
        this.cities = response.data;
        this.neighborhoods = [];
      } catch {
        this.toast.error('Erro ao carregar as cidades.');
      }
    },

    // Buscar lista de bairros
    async fetchNeighborhoods() {
      if (!this.form.locality) {
        this.neighborhoods = [];
        return;
      }
      try {
        const response = await axios.get(`${ENDPOINTS.NEIGHBORHOODS}/${this.form.state}/${this.form.locality}/`);
        this.neighborhoods = response.data;
      } catch {
        this.toast.error('Erro ao carregar os bairros.');
      }
    },

    // Quando o estado muda
    onStateChange() {
      this.fetchCities();
      this.validateField('state');
    },

    // Quando a cidade muda
    onCityChange() {
      this.fetchNeighborhoods();
      this.validateField('locality');
    },

    // Validação de campo
    validateField(field) {
      this.errors = {}; // Limpar erros anteriores
      if (!this.form[field]) {
        this.errors[field] = 'Campo obrigatório.';
      } else {
        delete this.errors[field];
      }
    },

    async handleNeighborhoodChange() {
      this.errors = {};
      if (!this.form.neighborhood) {
        this.errors.neighborhood = 'Selecione um bairro.';
        return;
      }

      // Abrir o modal de confirmação
      this.isConfirmationModalOpen = true;
    },
    handleConfirmation(isConfirmed) {
      this.isConfirmationModalOpen = false; // Fecha o modal de confirmação
      if (!isConfirmed) {
        this.toast.error('Confirmação falhou. Tente novamente.');
        return;
      }

      // Prosseguir com a lógica original
      this.submitNeighborhoodChange();
    },
    async submitNeighborhoodChange() {
      try {
        const response = await axios.post(ENDPOINTS.EDIT_NEIGHBORHOOD, {
          neighborhood_id: this.form.neighborhood,
        });

        if (response.status === 200) {
          this.userStore.setUserInfo({ 'state': this.form.state, 'locality': this.form.locality, 'neighborhood': this.form.neighborhood_name, 'id': this.form.neighborhood })
          this.toast.success("Bairro trocado com sucesso!")
          this.useForumList.setSearchQuery("")
          this.useForumList.fetchForums()
          router.push('/home');
        } else {
          this.toast.error('Erro ao salvar o bairro. ' + response.errors);
        }
      } catch (error) {
        this.toast.error('Erro ao enviar os dados. ' + error);
      }
    },
  },

  mounted() {
    // Buscar estados ao carregar o componente
    this.fetchStates();
  },
};
</script>

<style scoped>
/* Estilo para o modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  /* Fundo opaco */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #333;
}
</style>