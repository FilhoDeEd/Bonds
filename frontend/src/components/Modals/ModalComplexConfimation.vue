<template>
  <div v-if="isModalDeleteAccountOpen" class="modal-overlay">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">X</button>

      <!-- Conteúdo do modal -->
      <form @submit.prevent="handleConfirmation">
        <div class="relative w-full mb-3">
          <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2">Usuário ou Email</label>
          <input type="text" v-model="form.emailOrUsername" @blur="validateField('emailOrUsername')"
            class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
            placeholder="Usuário ou Email" />
          <span v-if="errors.emailOrUsername" class="text-red-500 text-xs">{{ errors.emailOrUsername }}</span>
        </div>

        <div class="relative w-full mb-3">
          <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2">Senha</label>
          <input type="password" v-model="form.password" @blur="validateField('password')"
            class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
            placeholder="Senha" />
          <span v-if="errors.password" class="text-red-500 text-xs">{{ errors.password }}</span>
        </div>

        <div class="text-center mt-6">
          <button
            class="bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
                   focus:outline-none focus:ring-2 focus:ring-emerald-500 
                   transition duration-300 transform hover:scale-105 w-full"
            type="submit">
            Logar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
/* eslint-disable */

import axios from "axios";
import { ENDPOINTS } from "../../../api.js";
import { useToast } from "vue-toastification";
import { useUserStore } from "../../store/user.js";

export default {
  data() {
    return {
      form: {
        emailOrUsername: "",
        password: "",
      },
      errors: {},
      toast: useToast(),
      useStore: useUserStore(),
    };
  },
  props: {
    isModalDeleteAccountOpen: Boolean,
  },
  methods: {

    closeModal() {
      this.$emit("close");
    },

    // Validação de campos
    validateField(field) {
      if (!this.form[field]) {
        this.errors[field] = "Este campo é obrigatório.";
      } else if (
        field === "emailOrUsername" &&
        this.form.emailOrUsername.includes("@") &&
        !/\S+@\S+\.\S+/.test(this.form.emailOrUsername)
      ) {
        this.errors.emailOrUsername = "Formato de email inválido.";
      } else {
        delete this.errors[field];
      }
    },

    // No método handleConfirmation do modal de login e senha
    async handleConfirmation() {
      Object.keys(this.form).forEach((field) => this.validateField(field));
      if (Object.keys(this.errors).some((key) => this.errors[key])) return;
      try {

        const loginResponse = await axios.post(ENDPOINTS.LOGIN, this.form);

        if (loginResponse.status === 200) {
          console.log(loginResponse)
          if (loginResponse.data.access === this.useStore.user.access) {
            this.$emit('confirm', true);
            this.closeModal();
          } else {
            this.toast.error("Login e/ou Senha inválidos");
          }
        } else {
          this.$emit('confirm', false);
        }
      } catch (error) {
        this.toast.error("Erro ao autenticar. Tente novamente.");
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