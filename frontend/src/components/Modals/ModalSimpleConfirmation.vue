<template>
  <div v-if="isSimpleConfirmModalOpen" class="modal-overlay">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">X</button>
      <h2>Confirmar Ação?</h2>
      
      <!-- Container para os botões lado a lado -->
      <div class="flex gap-4 mt-4">
        <!-- Confirmar ação -->
        <button 
          class="flex-1 bg-emerald-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-emerald-600 
           focus:outline-none focus:ring-2 focus:ring-emerald-500 
           transition duration-300 transform hover:scale-105"
          @click="handleConfirm"
        >
          Confirmar
        </button>

        <!-- Cancelar ação -->
        <button 
          class="flex-1 bg-red-500 text-white py-2 px-6 rounded-lg shadow-md hover:bg-red-600 
           focus:outline-none focus:ring-2 focus:ring-red-500 
           transition duration-300 transform hover:scale-105"
          @click="closeModal"
        >
          Cancelar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isSimpleConfirmModalOpen: Boolean, 
  },

  methods: {
    closeModal() {
      this.$emit('close'); 
    },

    handleConfirm() {
      this.$emit('confirm'); 
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
  background: rgba(0, 0, 0, 0.5); /* Fundo opaco */
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
