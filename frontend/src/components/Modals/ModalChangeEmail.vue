<template>
  <div v-if="isModalChangeEmailOpen" class="modal-overlay">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">X</button>

      <!-- Conteúdo do modal -->
      <form @submit.prevent="handleEmailChange">
        <div class="flex gap-4 space-x-4">

          <div class="relative w-full mb-3">
            <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Email</label>
            <input type="email" v-model="form.email" @change="validateField('email')"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
            <p v-if="errors.email" class="text-red-500 text-xs">{{ errors.email }}</p>
          </div>

          <div class="relative w-full mb-3">
            <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Confirmar Email</label>
            <input type="email" v-model="form.confirm_email" @change="validateField('confirm_email')"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
            <p v-if="errors.confirm_email" class="text-red-500 text-xs">{{ errors.confirm_email }}</p>
          </div>

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
    </div>
  </div>
</template>



<script>
/* eslint-disable */

import axios from 'axios';
import  router  from "../../router/index.js";
import { ENDPOINTS } from '../../../api.js';
import { useUserStore } from '../../store/user.js';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      userStore: useUserStore(),
      toast: useToast(),
      form: {
        email: "",
        confirm_email: "",
      },
      errors: {}, // Erros de validação
      router,
    };
  },
  props: {
    isModalChangeEmailOpen: Boolean, // Propriedade para controlar se o modal está aberto
  },

  methods: {

    closeModal() {
      this.$emit('close'); // Emite evento para o componente pai fechar o modal
    },

    // Validação de campo
    validateField(field) {
      this.errors = {}; // Limpar erros anteriores
      switch (field) {
        case "email": //remove
          if (!this.form.email) {
            this.errors.email = "Email é obrigatório.";
          } else if (!/\S+@\S+\.\S+/.test(this.form.email)) {
            this.errors.email = "Formato de email inválido.";
          } else {
            this.errors.email = "";
          }
          break;
        case "confirm_email":
          this.errors.confirm_email = this.form.confirm_email
            ? (this.form.confirm_email === this.form.email ? "" : "Os emails não coincidem.")
            : "A confirmação de email obrigatória.";
          break;

        default:
          this.errors[field] = "";
      }
    },

    // Submissão do formulário
    async handleEmailChange() {
      this.errors = {}
      if (Object.keys(this.errors).length > 0) return; // Não continuar se houver erros

      try {
        const response = await axios.post(ENDPOINTS.EDIT_EMAIL, {
          email: this.form.email,
        });
        if (response.status === 200) {
          this.userStore.setUserInfo(this.form.email)
          this.userStore.removeToken();
          this.toast.success("Email trocado com sucesso, refaça o login!")
          router.push('/login');
        } else {
          this.toast.error('Erro ao salvar o email. Tente novamente.');
        }
      } catch (error) {
        this.toast.error('Erro de comunicação com o servidor.');
      }
    },
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