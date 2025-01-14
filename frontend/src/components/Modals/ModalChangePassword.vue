<template>
  <div v-if="isModalChangePasswordOpen" class="modal-overlay">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">X</button>

      <!-- Conteúdo do modal -->
      <form @submit.prevent="handlePasswordChange">
        <div class="flex gap-4 space-x-4">

          <div class="relative w-full mb-3">
            <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Senha</label>
            <input type="password" v-model="form.password" @change="validateField('password')"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
            <p v-if="errors.password" class="text-red-500 text-xs">{{ errors.password }}</p>
          </div>

          <div class="relative w-full mb-3">
            <label class="block uppercase text-blueGray-600 text-xs font-varela mb-2">Confirmar senha</label>
            <input type="password" v-model="form.confirm_password" @change="validateField('confirm_password')"
              class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" />
            <p v-if="errors.confirm_password" class="text-red-500 text-xs">{{ errors.confirm_password }}</p>
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
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      form: {
        password: "",
        confirm_password: "",
      },
      errors: {}, // Erros de validação
      router,
      toast: useToast(),
    };
  },
  props: {
    isModalChangePasswordOpen: Boolean, // Propriedade para controlar se o modal está aberto
  },

  methods: {

    closeModal() {
      this.$emit('close'); // Emite evento para o componente pai fechar o modal
    },

    // Validação de campo
    validateField(field) {
      this.errors = {}; // Limpar erros anteriores
      switch (field) {
        case "password":
          this.errors.password = this.form.password
            ? (/[A-Z]/.test(this.form.password) ? "" : "A senha deve conter ao menos uma letra maiúscula.") ||
            (/[a-z]/.test(this.form.password) ? "" : "A senha deve conter ao menos uma letra minúscula.") ||
            (/\d/.test(this.form.password) ? "" : "A senha deve conter ao menos um número.") ||
            (/[\W_]/.test(this.form.password) ? "" : "A senha deve conter ao menos um caractere especial.") ||
            (this.form.password.length >= 8 ? "" : "A senha deve ter no mínimo 8 caracteres.")
            : "A senha é obrigatória.";
          break;
        case "confirm_password":
          this.errors.confirm_password = this.form.confirm_password
            ? (this.form.confirm_password === this.form.password ? "" : "As senhas não coincidem.")
            : "A confirmação de senha obrigatória.";
          break;

        default:
          this.errors[field] = "";
      }
    },
    // Submissão do formulário
    async handlePasswordChange() {
      this.errors = {}
      if (Object.keys(this.errors).length > 0) return; // Não continuar se houver erros

      try {
        const response = await axios.post(ENDPOINTS.EDIT_PASSWORD, {
          password: this.form.password,
        });

        if (response.status === 200) {
          this.toast.success("Senha trocada. Refaça o Login!")
          this.router.push('/login');
        } else {
          this.toast.error('Erro ao salvar a senha. Tente novamente.');
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