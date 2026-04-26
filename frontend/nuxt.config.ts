export default defineNuxtConfig({
  modules: ['@pinia/nuxt'],

  css: [
    '~/assets/css/main.css',
    'primeicons/primeicons.css'
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
    }
  }
})
