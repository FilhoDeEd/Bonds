<template>
  <div v-if="isModalOpen" class="modal-overlay">
    <div class="modal">
    <button class="close-btn" @click="closeModal">×</button>
    <h2>Criar Evento</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
      <label for="title">Título</label>
      <input
        type="text"
        id="title"
        v-model="form.title"
        placeholder="Digite o título do Evento"
        required
      />
      </div>
      
      <div class="form-group">
      <label for="description">Descrição</label>
      <textarea
        id="description"
        v-model="form.description"
        placeholder="Digite a descrição do fórum"
        required
      ></textarea>
      </div>

      <div class="form-group">
      <label for="eventDate">Data do Evento</label>
      <input
        type="date"
        id="eventDate"
        v-model="form.eventDate"
        @change="validateDate"
        required
      />
      <small v-if="dataError" class="error-message">{{ dataError }}</small>
      </div>

      <div class="form-group">
      <label for="location">Localização</label>
      <input
        type="text"
        id="location"
        v-model="form.location"
        placeholder="Digite a localização do evento"
        required
      />
      </div>

      <div class="form-actions">
      <button type="submit" class="confirm-btn">Confirmar</button>
      <button type="button" class="cancel-btn" @click="closeModal">Cancelar</button>
      </div>
    </form>
    </div>
  </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ENDPOINTS } from '../../../api';
  import { useToast } from 'vue-toastification';
  export default {
  props: {
    isModalOpen: Boolean, // Controle do modal (passado do componente pai)
  },
  data() {
    return {
    form: {
      title: '',
      description: '',
      eventDate: '',
      location: '',
    },
    dataError: null,
    toast: useToast(),
    };
  },
  methods: {
    closeModal() {
    this.$emit('close'); // Emite o evento para o componente pai fechar o modal
    },

    validateDate() {
    const today = new Date();
    const eventDate = new Date(this.form.eventDate);
    if (eventDate < today) {
      this.dataError = 'Data inválida';
    } else {
      this.dataError = null;
    }
    },
    
    async handleSubmit() {
    try {
      const response = await axios.post(ENDPOINTS.REGISTER_EVENT,{
      title : this.form.title,
      description : this.form.description,
      eventDate: this.form.eventDate,
      location: this.form.location,
      });
      if(response.status === 201){
        this.toast.success('Evento Criado: ', this.form.title);
        this.closeModal();
        this.$router.push("/forum/event/"+response.data.slug)
      }
      else{
        this.toast.error("Erro ao tentar criar fórum")
        console.log(response.error)
      }

    } catch(error){
      this.toast.error('Erro de comunicação com o servidor.');
    }
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
  background: white;
  padding: 20px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  }
  
  h2 {
  text-align: center;
  }
  .error-message {
  color: #f44336;
  font-size: 12px;
  margin-top: 5px;
  display: block;
}

  
  .form-group {
  margin-bottom: 15px;
  }
  
  label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  }
  
  input,
  textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
  }
  
  .form-actions {
  display: flex;
  justify-content: space-between;
  }
  
  .confirm-btn,
  .cancel-btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  }
  
  .confirm-btn {
  background-color: #4caf50;
  color: white;
  }
  
  .cancel-btn {
  background-color: #f44336;
  color: white;
  }
  </style>