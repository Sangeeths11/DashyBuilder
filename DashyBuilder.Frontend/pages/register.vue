<script setup lang="ts">

definePageMeta({
  title: 'DashyBuilder - Register',
  middleware: ['auth-index'],
})

const { signUp, errorMessage } = useAuth();
const router = useRouter();

const email = ref('');
const password = ref('');
const confirmPassword = ref('');

const register = async () => {
  console.log(email.value, password.value, confirmPassword.value)
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }
  else if (password.value.length < 6) {
    errorMessage.value = "Password must be at least 6 characters long.";
    return;
  }
  else {
    await signUp(email.value, password.value);
  }

  if (!errorMessage.value) {
    router.push('/login');
  }
};
</script>
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
    <div class="bg-white p-6 rounded shadow-md w-full max-w-md">
      <AuthCompErrorMessageBox :message="errorMessage" />
      <h1 class="text-2xl md:text-3xl font-bold mb-4 text-center">Sign Up</h1>
      <div class="flex items-center justify-center mb-6">
        <img src="assets/dashybuilder.png" alt="Logo" class="w-16 h-16 rounded-full">
      </div>
      <form @submit.prevent="register" class="flex flex-col items-center">
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
        <AuthCompInputField
          label="Confirm Password"
          id="confirm_password"
          type="password"
          placeholder="******************"
          iconName="carbon:password"
          :modelValue="confirmPassword"
          @update:modelValue="value => confirmPassword = value"
        />
        <div class="mb-4 w-full">
          <AuthCompSubmitButton>Sign Up</AuthCompSubmitButton>
        </div>
        <div class="flex flex-col items-center md:flex-row w-full justify-center">
          <span class="text-gray-600 text-sm">Already have an account?</span>
          <NuxtLink to="/login" class="text-blue-500 text-sm">Login here</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
</style>