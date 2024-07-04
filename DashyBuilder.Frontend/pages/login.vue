<script setup lang="ts">

definePageMeta({
  title: 'DashyBuilder - Login',
  middleware: ['auth-index'],
})

const supabase = useSupabaseClient()
const router = useRouter()
const { signIn, errorMessage } = useAuth()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  await signIn(email.value, password.value);
};
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 px-4 py-0"> <!-- Reduziertes Padding Y -->
    <div class="bg-white p-6 rounded shadow-md w-full max-w-md mx-auto"> <!-- Entfernt margin-bottom -->
      <AuthCompErrorMessageBox :message="errorMessage" />
      <h1 class="text-2xl md:text-3xl font-bold mb-4 text-center">Login</h1>
      <div class="flex items-center justify-center mb-6">
        <img src="assets/dashybuilder.png" alt="Logo" class="w-16 h-16 rounded-full">
      </div>
      <form @submit.prevent="handleLogin" class="flex flex-col items-center">
        <AuthCompInputField 
          label="Email" 
          id="email" 
          type="email" 
          placeholder="Email" 
          iconName="ic:baseline-email" 
          :modelValue="email" 
          @update:modelValue="value => email = value"
        />
        <AuthCompInputField 
          label="Password" 
          id="password" 
          type="password" 
          placeholder="******************" 
          iconName="carbon:password" 
          :modelValue="password" 
          @update:modelValue="value => password = value"
        />
        <div class="mb-4 w-full"> <!-- Überprüfen ob dieser Margin notwendig ist -->
          <AuthCompLoginSubmitButton />
        </div>
        <div class="flex flex-col items-center md:flex-row w-full justify-center mb-4"> <!-- Entfernte unnötige Margins -->
          <span class="text-gray-600 text-sm">
            Don't have an account?
          </span>
          <NuxtLink to="/register" class="text-blue-500 text-sm ml-2">
            Register here
          </NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>


<style>

</style>