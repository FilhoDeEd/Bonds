<template>
  <footer
    class="pb-6"
    :class="[
      absolute ? 'absolute w-full bottom-0 bg-blueGray-800' : 'relative',
    ]"
  >
    <div class="container mx-auto px-4">
      <hr class="mb-6 border-b-1 border-blueGray-600" />
      <div
        class="flex flex-wrap items-center md:justify-between justify-center"
      >
        <div class="w-full md:w-4/12 px-4">
          <div
            class="text-sm text-blueGray-500 font-semibold py-1 text-center md:text-left"
          >
            Copyright © {{ date }}  |  
            <router-link to="/about" >
            <a
              class="fredoka text-white hover:text-blueGray-300 text-sm font-semibold py-1"
            >
            | Bonds
            </a>
            </router-link>
          </div>
        </div>
        <div class="w-full md:w-8/12 px-4">
          <ul class="flex flex-wrap list-none md:justify-end justify-center">
            <li>
              <router-link to="/about" >
              <a
                class="text-white hover:text-blueGray-300 text-sm font-semibold block py-1 px-3"
              >
                About Us
              </a>
              </router-link>
            </li>
            <li>
              <a
                href="https://github.com/FilhoDeEd/Bonds/blob/main/LICENSE"
                class="text-white hover:text-blueGray-300 text-sm font-semibold block py-1 px-3"
              >
                MIT License
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      date: new Date().getFullYear(),
    };
  },
  props: {
    absolute: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style>
.fredoka{
  font-family: 'fredoka';
  font-size: 150%;
}
</style>
