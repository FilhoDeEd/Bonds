import { defineStore } from 'pinia';
import { ENDPOINTS } from '../../api';
import axios from 'axios';


export const useForumStore = defineStore('forum', {
  state: () => ({
    forums: [], 
    currentPage: 1, 
    totalForums: 0, 
    pageSize: 10, 
    next: null, 
    previous: null, 
    isLoading: false, 
    error: null, 
  }),
  actions: {
    async fetchForums(page = 1) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await axios.get(`${ENDPOINTS.LIST_FORUNS}?page=${page}`);
        this.forums = response.data.results;
        this.totalForums = response.data.count;
        this.currentPage = page;
        this.next = response.data.next;
        this.previous = response.data.previous;
        console.log(this.forums)
      } catch (error) {
        this.error = 'Erro ao carregar os fóruns.';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },

    async searchForums(query) {
      this.isLoading = true;
      try {
        const response = await axios.get(`${ENDPOINTS.LIST_FORUNS}?search=${query}`);
        this.forums = response.data.forums;
        this.totalForums = response.data.count;
        this.currentPage = 1; // Reinicia para a página inicial após a busca
        this.next = response.data.next;
        this.previous = response.data.previous;
      } catch (error) {
        this.error = 'Erro ao buscar fóruns.';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },
  },
  getters: {
    totalPages: (state) => Math.ceil(state.totalForums / state.pageSize),
  },
});
