import { defineStore } from "pinia";
import { ENDPOINTS } from '../../api';
import axios from "axios";

export const useForumListStore = defineStore("forumListStore", {
    state: () => ({
        forums: [],           // Lista de fóruns
        count: 0,             // Total de fóruns disponíveis
        currentPage: 1,       // Página atual da listagem
        searchQuery: "",      // Termo de busca
        loading: false,       // Flag para controle de carregamento
        error: null,          // Mensagem de erro
        next: null,           // Link para a próxima página, usado para scroll infinito
    }),

    actions: {
        /**
         * Atualiza o termo de busca e reseta a página.
         * @param {string} query - Termo de busca.
         */
        setSearchQuery(query) {
            this.searchQuery = query;
            this.currentPage = 1;  // Reinicia a páginação
            this.forums = [];      // Limpa os resultados anteriores
            this.next = null;      // Reseta o próximo link
        },

        /**
         * Define a página atual para paginação.
         * @param {number} page - Número da página.
         */
        setPage(page) {
            this.currentPage = page; // Atualiza a página atual
        },

        /**
         * Faz o fetch dos fóruns da API com base no estado atual.
         * Adiciona os novos resultados à lista existente.
         */
        async fetchForums() {
            if (this.loading || (this.next === null && this.currentPage > 1)) return;

            this.loading = true;
            this.error = null;

            try {
                const params = {
                    page: this.currentPage
                };

                if (this.searchQuery.trim() !== "") {
                    params.search = this.searchQuery;
                }

                const response = await axios.get(`${ENDPOINTS.LIST_FORUNS}`, {
                    params
                });

                const { results, count, next } = response.data;
                this.forums = this.currentPage === 1 ? results : [...this.forums, ...results];
                this.count = count;
                this.next = next;
                this.currentPage += 1;
            } catch (error) {
                this.error = error.response?.data?.detail || "Erro ao carregar fóruns.";
            } finally {
                this.loading = false;
            }
        }
    }
});
