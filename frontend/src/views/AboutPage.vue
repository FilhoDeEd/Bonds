<template>
  <MainLayout>
    <div class="bg-gradient-to-b from-green-300 via-blue-200 to-blue-400 min-h-screen text-gray-800">
      <div class="container mx-auto py-12 px-6">
        <!-- Header -->
        <header class="text-center mb-12">
          <h1 class="text-4xl font-extrabold text-gray-800 sm:text-5xl">Sobre o Bonds</h1>
          <p class="mt-4 text-lg text-gray-700">
            Unindo bairros e comunidades. Promovendo inclusão e pertencimento para todos.
          </p>
        </header>

        <!-- Mission Section -->
        <section class="bg-white shadow-lg rounded-lg p-8 mb-12">
          <h2 class="text-2xl font-bold text-center text-blue-600 mb-4">Nossa Missão</h2>
          <p class="text-gray-700 text-center text-lg">
            No Bonds, acreditamos que a verdadeira força de uma comunidade vem da conexão entre as pessoas. 
            Nosso objetivo é criar um espaço inclusivo onde todos se sintam bem-vindos, valorizados e 
            conectados ao que há de melhor em seus bairros.
          </p>
        </section>

        <!-- Features Section -->
        <section class="grid grid-cols-1 md:grid-cols-2 gap-y-8 gap-x-6 p-5">
          <div class="bg-indigo-500 text-white shadow-md rounded-lg p-6 text-center">
            <h3 class="text-xl font-semibold text-white-500 mb-3">Para Todos</h3>
            <p class="text-gray-300">
              Bonds é para todas as idades, culturas e histórias. Nosso foco é construir um espaço onde cada voz 
              seja ouvida e respeitada.
            </p>
          </div>
          <div class="bg-indigo-500 text-white shadow-md rounded-lg p-6 text-center">
            <h3 class="text-xl font-semibold text-white-500 mb-3">Fortalecendo Laços</h3>
            <p class="text-gray-300">
              Promovemos conexões entre vizinhos e organizações locais, fortalecendo a cooperação e o bem-estar coletivo.
            </p>
          </div>
          <div class="bg-indigo-500 text-white shadow-md rounded-lg p-6 text-center">
            <h3 class="text-xl font-semibold text-white-500 mb-3">Inclusão</h3>
            <p class="text-gray-300">
              Valorizamos a diversidade. Bonds é um lugar para todos, independentemente de suas origens ou trajetórias.
            </p>
          </div>
          <div class="bg-indigo-500 text-white shadow-md rounded-lg p-6 text-center">
            <h3 class="text-xl font-semibold text-white-500 mb-3">Comunicação</h3>
            <p class="text-gray-300">
              Facilitamos conversas construtivas e informativas para melhorar a convivência em cada bairro.
            </p>
          </div>
        </section>

        <!-- Call to Action -->
        <div class="mt-12 text-center">
          <h3 class="text-2xl font-semibold text-gray-800 mb-4">
            Junte-se ao Bonds e seja parte da mudança!
          </h3>
          <p class="text-gray-700 mb-6">
            Descubra, conecte-se e transforme sua comunidade com a gente.
          </p>
          <router-link :to="{ path: '/auth/register' }">
          <button class="bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-red-700 hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 transition-transform">
            Comece Agora
          </button>
        </router-link>

          
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
/*eslint-disable*/
import router from "../router";
import MainLayout from "../layouts/mainLayout.vue";
</script>
