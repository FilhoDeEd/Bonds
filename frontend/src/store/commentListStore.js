import { defineStore } from "pinia";
import { ENDPOINTS } from '../../api';
import axios from "axios";

export const useCommentListStore = defineStore("commentListStore", {
    state: () => ({
        comments: [],          // Lista de comentários carregados
        count: 0,              // Total de comentários disponíveis
        currentPage: 1,        // Página atual da listagem
        loading: false,        // Flag para controle de carregamento
        error: null,           // Mensagem de erro
        next: null,            // Link para a próxima página, usado para scroll infinito
        forum_id: null,        // ID do tópico ao qual os comentários pertencem
    }),

    actions: {
        /**
         * Define o ID do fórum para carregar os comentários.
         * @param {string} id - ID do tópico.
         */
        setForumId(id) {
            this.forum_id = id;
            this.comments = []; // Reseta os comentários ao trocar de tópico
            this.currentPage = 1;
            this.next = null;
            this.count = 0;
        },

        /**
         * Faz o fetch dos comentários da API com base no estado atual.
         * Adiciona os novos resultados à lista existente.
         */
        async fetchComments() {
            if (this.loading || (this.next === null && this.currentPage > 1)) return;

            this.loading = true;
            this.error = null;

            try {
                const params = {
                    page: this.currentPage
                };

                if (!this.forum_id) {
                    throw new Error("Thread ID não definido.");
                }

                const response = await axios.get(`${ENDPOINTS.LIST_COMMENTS}/${this.forum_id}/`, {
                    params
                });

                const { results, count, next } = response.data;
                this.comments = this.currentPage === 1 ? results : [...this.comments, ...results];
                this.count = count;
                this.next = next;
                this.currentPage += 1;
            } catch (error) {
                this.error = error.response?.data?.detail || "Erro ao carregar comentários.";
            } finally {
                this.loading = false;
            }
        }
    }
});
