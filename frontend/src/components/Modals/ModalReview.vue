<template>
  <div v-if="isModalOpen" class="modal-overlay">
    <div class="modal">
      <button class="close-btn" @click="closeModal">×</button>
      <h2>Avalie o Evento</h2>

      <!-- Estrelas -->
      <div class="stars-container">
        <span
          v-for="star in 5"
          :key="star"
          class="star"
          :class="{ active: selectedStars >= star }"
          @mouseover="handleMouseOver(star)"
          @mouseleave="handleMouseLeave"
          @click="handleStarClick(star)"
        >
          ★
        </span>
      </div>

      <div class="form-actions">
        <button
          :disabled="selectedStars === 0"
          class="confirm-btn"
          @click="confirmRating"
        >
          Confirmar
        </button>
        <button class="cancel-btn" @click="closeModal">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isModalOpen: Boolean,
  },
  data() {
    return {
      selectedStars: 0, // Armazena a quantidade de estrelas selecionadas
      hoverStars: 0,    // Armazena as estrelas sendo "hovered" (para efeito visual)
    };
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    handleMouseOver(star) {
      this.hoverStars = star;
    },
    handleMouseLeave() {
      this.hoverStars = 0;
    },
    handleStarClick(star) {
      this.selectedStars = star;
    },
    confirmRating() {
      if (this.selectedStars === 0) {
        this.$toast.error("Por favor, selecione uma avaliação.");
        return;
      }
      this.$emit("submitRating", this.selectedStars);
      this.closeModal();
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #007bff;
  color: white;
  padding: 20px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: white;
}

h2 {
  margin-bottom: 20px;
}

.stars-container {
  margin: 20px 0;
}

.star {
  font-size: 40px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.3s ease;
}

.star.active,
.star:hover {
  color: gold;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-btn,
.cancel-btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: 2px solid white;
  background: transparent;
  color: white;
  cursor: pointer;
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
