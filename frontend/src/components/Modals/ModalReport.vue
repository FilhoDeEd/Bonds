<template>
  <div v-if="isModalOpen" class="modal-overlay">
    <div class="modal">
      <button class="close-btn" @click="closeModal">×</button>
      <h2 class="modal-title">Criar Report</h2>
      <form @submit.prevent="handleSubmit" class="modal-form">
        <!-- Título -->
        <div class="form-group">
          <label for="title">Título</label>
          <input
            type="text"
            id="title"
            v-model="form.title"
            placeholder="Digite o título do Reporte"
            required
          />
        </div>

        <!-- Descrição -->
        <div class="form-group">
          <label for="description">Descrição</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="Digite a descrição do ocorrido"
          ></textarea>
        </div>

        <!-- Data e Localização -->
        <div class="form-group row">
          <div class="column">
            <label for="eventDate">Data do ocorrido</label>
            <input type="date" id="eventDate" v-model="form.eventDate" />
            <small v-if="dataError" class="error-message">{{ dataError }}</small>
          </div>
          <div class="column">
            <label for="location">Localização</label>
            <input
              type="text"
              id="location"
              v-model="form.location"
              placeholder="Digite a localização do ocorrido"
              required
            />
          </div>
        </div>

        <!-- Tags e Resolvido -->
        <div class="form-group row">
          <div class="column">
            <label for="tags">Tags</label>
            <select id="tags" v-model="form.tags" required>
              <option disabled value="">Selecione uma tag</option>
              <option v-for="tag in tags" :key="tag.id" :value="tag.id">
                {{ tag.name }}
              </option>
            </select>
          </div>
          <div class="column">
            <label>Foi resolvido?</label>
            <div class="radio-group">
              <label for="solvedYes">
                <input type="radio" id="solvedYes" value="true" v-model="form.solved" />
                Sim
              </label>
              <label for="solvedNo">
                <input type="radio" id="solvedNo" value="false" v-model="form.solved" />
                Não
              </label>
            </div>
          </div>
        </div>

        <!-- Ações -->
        <div class="form-actions">
          <button type="submit" class="confirm-btn">Confirmar</button>
          <button type="button" class="cancel-btn" @click="closeModal">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

    
    <script>/*eslint-disable*/
    import axios from 'axios';
    import { ENDPOINTS } from '../../../api';
    import { useToast } from 'vue-toastification';
    import { onMounted } from 'vue';
    export default {
    props: {
      isModalOpen: Boolean, // Controle do modal (passado do componente pai)
      slug: String,
    },
    data() {
      return {
      form: {
        title: '',
        description: '',
        eventDate: '',
        location: '',
        solved: false,
        tags:'',
        slug: this.slug,
      },
      dataError: null,
      toast: useToast(),
      tags: [
        { id: 'SA', name: 'Saúde' },
        { id: 'L', name: 'Lixo' },
        { id: 'I', name: 'Infraestrutura' },
        { id: 'SG', name: 'Segurança' },
        { id: 'E', name: 'Educação' },
        { id: 'T', name: 'Transporte' },
        { id: 'IL', name: 'Iluminação' },
        { id: 'O', name: 'Outros' }
      ],
      };
    },
    methods: {
      closeModal() {
      this.$emit('close'); // Emite o evento para o componente pai fechar o modal
      },
  
      
      async handleSubmit() {
      try {
        const response = await axios.post(ENDPOINTS.REGISTER_REPORT,{
        title : this.form.title,
        content : this.form.description,
        //date: new Date(this.form.eventDate),
        location: this.form.location,
        tags: this.form.tags,
        solved: this.form.solved === 'true',
        forum_slug: this.form.slug,
        });

        if(response.status === 201){
          this.toast.success('Reporte Criado');
          this.closeModal();
          this.$router.push("/forum/"+this.slug)
        }
        else{
          this.toast.error("Erro ao tentar criar reporte: " + response.error)
          console.log(response.error)
        }
  
      } catch(error){
        this.toast.error('Erro de comunicação com o servidor.');
      }
      },
    },
    };
    onMounted(() => {
        console.log('Modal carregado:', slug);
    });
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
      margin-bottom: 15px;
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
    