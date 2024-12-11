<template>
  <div v-if="isOpen" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <h2 class="text-lg font-bold mb-4">Alterar Bairro</h2>
      <form @submit.prevent="submitForm">
        <div class="relative w-full mb-4">
          <label class="block uppercase text-blueGray-600 text-xs font-medium mb-2">Estado</label>
          <select
            v-model="localForm.state"
            @change="onStateChange"
            class="w-full border border-gray-300 rounded px-4 py-2 bg-white text-gray-700 focus:outline-none focus:ring focus:border-blue-500"
          >
            <option value="">Selecione um Estado</option>
            <option v-for="state in states" :key="state.id" :value="state.id">{{ state.name }}</option>
          </select>
        </div>
        <div class="relative w-full mb-4">
          <label class="block uppercase text-blueGray-600 text-xs font-medium mb-2">Cidade</label>
          <select
            v-model="localForm.locality"
            @change="onCityChange"
            class="w-full border border-gray-300 rounded px-4 py-2 bg-white text-gray-700 focus:outline-none focus:ring focus:border-blue-500"
          >
            <option value="">Selecione uma Cidade</option>
            <option v-for="city in cities" :key="city.name" :value="city.name">{{ city.name }}</option>
          </select>
        </div>
        <div class="relative w-full mb-4">
          <label class="block uppercase text-blueGray-600 text-xs font-medium mb-2">Bairro</label>
          <select
            v-model="localForm.neighborhood"
            class="w-full border border-gray-300 rounded px-4 py-2 bg-white text-gray-700 focus:outline-none focus:ring focus:border-blue-500"
          >
            <option value="">Selecione um Bairro</option>
            <option v-for="neighborhood in neighborhoods" :key="neighborhood.id" :value="neighborhood.id">
              {{ neighborhood.name }}
            </option>
          </select>
        </div>
        <div class="flex justify-end gap-4">
          <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-500 rounded-md">Cancelar</button>
          <button type="submit" class="px-4 py-2 bg-blue-600 rounded-md">Salvar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
    props: {
      isOpen: {
        type: Boolean,
        required: true,
      },
      formData: {
        type: Object,
        required: true,
      },
      states: {
        type: Array,
        default: () => [],
      },
      cities: {
        type: Array,
        default: () => [],
      },
      neighborhoods: {
        type: Array,
        default: () => [],
      },
    },

  data() {
    return {
      localForm: {
        state: "",
        locality: "",
        neighborhood: "",
        neighborhood_id: null,
      },
    };
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    submitForm() {
      const updatedData = { ...this.localForm };
      this.$emit("save", updatedData);
    },
    onStateChange() {
      this.localForm.locality = "";
      this.localForm.neighborhood = "";
      this.$emit("state-change", this.localForm.state);
    },
    onCityChange() {
      this.localForm.neighborhood = "";
      this.$emit("city-change", this.localForm.locality);
    },
  },
};
</script>
