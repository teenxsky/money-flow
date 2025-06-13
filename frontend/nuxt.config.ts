export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: false },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt', '@vueuse/nuxt', '@nuxtjs/color-mode'],
  css: ['~/assets/css/main.css'],
  colorMode: {
    preference: 'light',
    fallback: 'light',
    classSuffix: ''
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://api.localhost:80'
    }
  },
  app: {
    head: {
      title: 'Money Flow Dashboard',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: 'Personal finance management dashboard'
        }
      ]
    }
  }
})
