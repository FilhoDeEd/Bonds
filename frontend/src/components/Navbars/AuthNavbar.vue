<template>
  <nav
    class="fixed top-0 z-50 w-full flex flex-wrap items-center justify-between px-2 py-1 navbar-expand-lg"
    style="background-color: #1E293B;"
  >
    <div
      class="container px-4 mx-auto flex flex-wrap items-center justify-between"
    >
      <div
        class="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start"
      >
        <router-link
          class="fredoka text-white text-smleading-relaxed inline-block mr-2 py-2 whitespace-nowrap uppercase"
          to="/"
        >
          Bonds
        </router-link>
        <button
          class="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
          type="button"
          v-on:click="setNavbarOpen"
        >
          <i class="text-white fas fa-bars"></i>
        </button>
      </div>
      <div
        class="lg:flex flex-grow items-center bg-white lg:bg-opacity-0 lg:shadow-none"
        :class="[navbarOpen ? 'block rounded shadow-lg' : 'hidden']"
        id="example-navbar-warning"
      >
        
      </div>
    </div>
  </nav>
</template>
<script>  

export default {
  data() {
    return {
      navbarOpen: false,
    };
  },
  methods: {
    setNavbarOpen: function () {
      this.navbarOpen = !this.navbarOpen;
    },
  },
 
};
</script>

<style>
  .fredoka{
    font-family: 'fredoka';
    font-size: xx-large;
  }
</style>