// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/scss/main.scss'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  monacoEditor: {

  },
  supabase: {
    redirect: false
  },
  compatibilityDate: "2024-07-02",
  modules: ["@nuxt/icon", "@nuxtjs/supabase", "@pinia/nuxt", "nuxt-monaco-editor"]
})