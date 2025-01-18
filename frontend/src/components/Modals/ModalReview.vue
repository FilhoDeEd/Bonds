<template>
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal">
        <button class="close-btn" @click="closeModal">×</button>
        <h2>Avalie o Evento</h2>
        <div class="stars-container">
          <StarRating
            :rating="selectedStars"
            @rating-selected="handleRating"
            star-size="40"
            :show-rating="false"
            active-color="gold"
            inactive-color="#ccc"
          />
        </div>
        <div class="form-actions">
          <button
            :disabled="!selectedStars"
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
  import StarRating from "vue-star-rating";
  
  export default {
    components: { StarRating },
    props: {
      isModalOpen: Boolean,
    },
    data() {
      return {
        selectedStars: 0, // Armazena o valor da avaliação
      };
    },
    methods: {
      closeModal() {
        this.$emit("close");
      },
      handleRating(stars) {
        this.selectedStars = stars;
      },
      confirmRating() {
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
  