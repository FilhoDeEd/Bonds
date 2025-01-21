<template>
    <div v-if="isPollOpen" class="modal-overlay">
      <div class="modal">
        <!-- Botão para fechar o modal -->
        <button class="close-btn" @click="closeModal">×</button>
  
        <!-- Título do modal -->
        <h2 class="modal-title">Criar Enquete</h2>
  
        <!-- Formulário -->
        <form @submit.prevent="handleSubmit" class="modal-form">
          <!-- Título da enquete -->
          <div class="form-group">
            <label for="pollTitle">Título</label>
            <input
              type="text"
              id="pollTitle"
              v-model="form.title"
              placeholder="Digite o título da enquete"
              required
            />
          </div>

          <div class="form-group h-200">
            <label for="pollTitle">Descrição</label>
            <input
              type="text"
              id="pollText"
              v-model="form.text"
              placeholder="Digite a descrição da enquete"
              required
            />
          </div>
  
          <!-- Prazo -->
          <div class="form-group">
            <label for="pollDeadline">Prazo</label>
            <input
              type="date"
              id="pollDeadline"
              v-model="form.deadline"
              required
            />
          </div>
  
          <!-- Opções da enquete -->
          <div class="form-group">
            <label>Opções</label>
            <div v-for="(option, index) in pollOptions" :key="index" class="row mb-2">
              <input
                type="text"
                v-model="option.option_text"
                :placeholder="`Opção ${index + 1}`"
                :required="index < 2" 
              />
              <button
                type="button"
                class="cancel-btn"
                @click="removePollOption(index)"
                v-if="index >= 2"
              >
                Remover
              </button>
            </div>
            <button
              type="button"
              class="confirm-btn mt-3"
              @click="addPollOption"
              :disabled="pollOptions.length >= 4"
            >
              Adicionar Opção
            </button>
          </div>
  
          <!-- Ações -->
          <div class="form-actions">
            <button type="submit" class="confirm-btn">Criar Enquete</button>
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
      isPollOpen: Boolean, // Controle do modal (passado do componente pai)
      slug: String, // Slug do fórum ou contexto da enquete
    },
    data() {
      return {
        form: {
          title: '',
          text: '',
          deadline: '',
          options: [],
          slug: this.slug,
        },
        pollOptions: [
          { option_text: '' },
          { option_text: '' },
        ], // Pelo menos duas opções por padrão
        toast: useToast(),
      };
    },
    methods: {
      closeModal() {
        this.$emit('close'); // Emite evento para o pai fechar o modal
        this.resetForm(); // Reseta o formulário
      },
      resetForm() {
        this.form.title = '';
        this.form.deadline = '';
        this.pollOptions = [
          { option_text: '' },
          { option_text: '' },
        ];
      },
      addPollOption() {
        if (this.pollOptions.value.length < 4) {
            this.pollOptions.value.push({ option_text: '' }); // Certifique-se de usar "option_text"
        } else {
            this.toast.error('Não é possível adicionar mais de 4 opções.');
        }
    },
      removePollOption(index) {
        if (index >= 2) {
          this.pollOptions.splice(index, 1);
        }
      },
      async handleSubmit() {
        // Validação do formulário
        if (
          this.form.title.trim() === '' ||
          this.form.deadline === '' ||
          this.pollOptions.filter((option) => option.option_text.trim() !== '').length < 2
        ) {
          this.toast.error('Preencha todos os campos obrigatórios!');
          return;
        }
  
        // Dados para envio
        this.form.options = this.pollOptions.filter((option) => option.option_text.trim() !== '');
  
        try {
          const response = await axios.post(ENDPOINTS.REGISTER_POLL, {
            title: this.form.title,
            content: this.form.text,
            deadline: this.form.deadline,
            forum_slug: this.form.slug,
            options: this.form.options,
          });
  
          if (response.status === 201) {
            this.toast.success('Enquete criada com sucesso!');
            this.closeModal();
          } else {
            this.toast.error('Erro ao criar enquete.');
          }
        } catch (error) {
          this.toast.error('Erro ao se comunicar com o servidor.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  /* Modal */
  .modal {
    background: #fff;
    width: 90%;
    max-width: 500px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    position: relative;
    animation: fadeIn 0.3s ease-in-out;
  }
  
  /* Title */
  .modal-title {
    margin: 0 0 20px;
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    color: #333;
  }
  
  /* Close Button */
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: transparent;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #555;
  }
  
  .close-btn:hover {
    color: #000;
  }
  
  /* Form Group */
  .form-group {
    margin-bottom: 10px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input,
  textarea,
  select {
    width: 100%;
    padding: 8px 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  textarea {
    resize: none;
  }
  
  input:focus,
  textarea:focus,
  select:focus {
    border-color: #007bff;
    outline: none;
  }
  
  /* Two Columns in a Row */
  .row {
    display: flex;
    gap: 20px;
    justify-content: space-between;
  }
  
  .column {
    flex: 1;
  }
  
  /* Radio Group */
  .radio-group {
    display: flex;
    gap: 10px;
  }
  
  /* Error Message */
  .error-message {
    color: red;
    font-size: 0.9rem;
  }
  
  /* Form Actions */
  .form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .confirm-btn,
  .cancel-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
  }
  
  .confirm-btn {
    background: #007bff;
    color: #fff;
  }
  
  .confirm-btn:hover {
    background: #0056b3;
  }
  
  .cancel-btn {
    background: #ddd;
    color: #333;
  }
  
  .cancel-btn:hover {
    background: #bbb;
  }
  
  /* Animations */
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.9);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  </style>
  
  