import { defineStore } from "pinia";
import axios from "axios";
import { useForumListStore } from "./forumListStore";


export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    user: {
      isAuthenticated: false,
      access: null,

      account: {
        id: null,
        username: null,
        name: null,
        surname: null,
        gender: null,
        birthday: null,
        email: null,
        cellphone: null,
        agree_policy: null,
        biography: null,
        status: null
      },

      user_profle: {
        id: null,
        trust_rate: null,
        active: null,
        status: null
      },

      address: {
        id: null,
        state: null,
        locality: null,
        neighborhood: null
      }
    },
  }),

  actions: {
    initStore() {
      if (localStorage.getItem("user.access")) {
          this.user.access = localStorage.getItem("user.access");
      
          this.user.account.id = localStorage.getItem("user.account.id");
          this.user.account.username = localStorage.getItem("user.account.username");
          this.user.account.name = localStorage.getItem("user.account.name");
          this.user.account.surname = localStorage.getItem("user.account.surname");
          this.user.account.gender = localStorage.getItem("user.account.gender");
          this.user.account.birthday = localStorage.getItem("user.account.birthday");
          this.user.account.email = localStorage.getItem("user.account.email");
          this.user.account.cellphone = localStorage.getItem("user.account.cellphone");
          this.user.account.agree_policy = localStorage.getItem("user.account.agree_policy");
          this.user.account.biography = localStorage.getItem("user.account.biography");
          this.user.account.status = localStorage.getItem("user.account.status");
      
          this.user.user_profle.id = localStorage.getItem("user.user_profle.id");
          this.user.user_profle.trust_rate = localStorage.getItem("user.user_profle.trust_rate");
          this.user.user_profle.active = localStorage.getItem("user.user_profle.active");
          this.user.user_profle.status = localStorage.getItem("user.user_profle.status");
      
          this.user.address.id = localStorage.getItem("user.address.id");
          this.user.address.state = localStorage.getItem("user.address.state");
          this.user.address.locality = localStorage.getItem("user.address.locality");
          this.user.address.neighborhood = localStorage.getItem("user.address.neighborhood");
      
          this.user.isAuthenticated = true;
    
          axios.defaults.headers.common["Authorization"] = `Token ${this.user.access}`;
          console.log("User initialized", this.user);
      }
    },

    setToken(data) {
      console.log("setToken", data);

      this.user.access = data.access;
      this.user.isAuthenticated = true;
      localStorage.setItem("user.access", data.access);

      axios.defaults.headers.common["Authorization"] = `Token ${data.access}`;
    },

    removeToken() {
      this.user.access = null;
      this.user.isAuthenticated = false;

      this.user.account = {
        id: null,
        username: null,
        name: null,
        surname: null,
        gender: null,
        birthday: null,
        email: null,
        cellphone: null,
        agree_policy: null,
        biography: null,
        status: null
      };

      this.user.user_profle = {
        id: null,
        trust_rate: null,
        active: null,
        status: null
      };

      this.user.address = {
        id: null,
        state: null,
        locality: null,
        neighborhood: null
      };
    
      localStorage.setItem("user.access", "");
    
      localStorage.setItem("user.account.id", "");
      localStorage.setItem("user.account.username", "");
      localStorage.setItem("user.account.name", "");
      localStorage.setItem("user.account.surname", "");
      localStorage.setItem("user.account.gender", "");
      localStorage.setItem("user.account.birthday", "");
      localStorage.setItem("user.account.email", "");
      localStorage.setItem("user.account.cellphone", "");
      localStorage.setItem("user.account.agree_policy", "");
      localStorage.setItem("user.account.biography", "");
      localStorage.setItem("user.account.status", "");
    
      localStorage.setItem("user.user_profle.id", "");
      localStorage.setItem("user.user_profle.trust_rate", "");
      localStorage.setItem("user.user_profle.active", "");
      localStorage.setItem("user.user_profle.status", "");
    
      localStorage.setItem("user.address.id", "");
      localStorage.setItem("user.address.state", "");
      localStorage.setItem("user.address.locality", "");
      localStorage.setItem("user.address.neighborhood", "");
      
      const forumListStore = useForumListStore();
      forumListStore.clearForums();
      axios.defaults.headers.common["Authorization"] = "";
    
      console.log("Logged Out");
    },

    setUserInfo(data) {
      console.log("setUserInfo", data);
  
      // Atualizar os dados de forma segura
      this.user.account = {
          ...this.user.account, // Preserva valores existentes
          id: data.account_id || this.user.account.id,
          username: data.username || this.user.account.username,
          name: data.name || this.user.account.name,
          surname: data.surname || this.user.account.surname,
          gender: data.gender || this.user.account.gender,
          birthday: data.birthday || this.user.account.birthday,
          email: data.email || this.user.account.email,
          cellphone: data.cellphone || this.user.account.cellphone,
          agree_policy: data.agree_policy || this.user.account.agree_policy,
          biography: data.biography || this.user.account.biography,
          status: data.status || this.user.account.status,
      };
  
      this.user.user_profle = {
          ...this.user.user_profle, // Preserva valores existentes
          id: data.user_profile_id || this.user.user_profle.id,
          trust_rate: data.trust_rate || this.user.user_profle.trust_rate,
          active: data.active || this.user.user_profle.active,
          status: data.status || this.user.user_profle.status,
      };
  
      this.user.address = {
          ...this.user.address, // Preserva valores existentes
          id: data.neighborhood_id || this.user.address.id,
          state: data.state || this.user.address.state,
          locality: data.locality || this.user.address.locality,
          neighborhood: data.neighborhood || this.user.address.neighborhood,
      };
  
      // Salvar no localStorage apenas as propriedades atualizadas
      localStorage.setItem("user.access", this.user.access || "");
      localStorage.setItem("user.account.id", this.user.account.id || "");
      localStorage.setItem("user.account.username", this.user.account.username || "");
      localStorage.setItem("user.account.name", this.user.account.name || "");
      localStorage.setItem("user.account.surname", this.user.account.surname || "");
      localStorage.setItem("user.account.gender", this.user.account.gender || "");
      localStorage.setItem("user.account.birthday", this.user.account.birthday || "");
      localStorage.setItem("user.account.email", this.user.account.email || "");
      localStorage.setItem("user.account.cellphone", this.user.account.cellphone || "");
      localStorage.setItem("user.account.agree_policy", this.user.account.agree_policy || "");
      localStorage.setItem("user.account.biography", this.user.account.biography || "");
      localStorage.setItem("user.account.status", this.user.account.status || "");
  
      localStorage.setItem("user.user_profle.id", this.user.user_profle.id || "");
      localStorage.setItem("user.user_profle.trust_rate", this.user.user_profle.trust_rate || "");
      localStorage.setItem("user.user_profle.active", this.user.user_profle.active || "");
      localStorage.setItem("user.user_profle.status", this.user.user_profle.status || "");
  
      localStorage.setItem("user.address.id", this.user.address.id || "");
      localStorage.setItem("user.address.state", this.user.address.state || "");
      localStorage.setItem("user.address.locality", this.user.address.locality || "");
      localStorage.setItem("user.address.neighborhood", this.user.address.neighborhood || "");
  
      console.log("User updated", this.user);
  }
}
  
});

