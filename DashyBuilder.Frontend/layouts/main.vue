<template>
  <div>
    <header class="bg-blue-500 text-white p-4 text-lg flex justify-between items-center">
      <div class="flex items-center space-x-4">
        <span class="text-3xl mr-1 cursor-pointer" @click="redirectToIndex"><Icon name="mdi:chart-box-outline" color="white" /></span>
        <span class="font-bold cursor-pointer" @click="redirectToIndex">Dashybuilder</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-white">{{ user?.email ?? 'No email provided' }}</span>
        <img src="assets/dashybuilder.png" alt="Profil" class="h-10 w-10 rounded-full cursor-pointer" @click="toggleLogoutPopup">
      </div>
      <div v-if="showLogoutPopup" class="fixed inset-0 bg-gray-600 bg-opacity-50 z-50 flex justify-center items-center">
        <div class="bg-white p-5 rounded-lg shadow-lg">
          <h3 class="text-lg font-semibold mb-4 text-black">Möchtest du dich ausloggen?</h3>
          <div class="flex justify-end space-x-4">
            <button @click="toggleLogoutPopup" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Abbrechen</button>
            <button @click="logout" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">Ausloggen</button>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-grow p-4">
      <slot />
    </main>
  </div>
</template>

<script lang="ts" setup>
const showLogoutPopup = ref(false)
const router = useRouter()
const user = useSupabaseUser()
const supabase = useSupabaseClient()

async function logout() {
  const { error } = await supabase.auth.signOut();
  if (error) console.error('Logout-Fehler', error.message);
  showLogoutPopup.value = false;
  router.push('/login')
}

function toggleLogoutPopup() {
  showLogoutPopup.value = !showLogoutPopup.value
}

function redirectToIndex() {
  router.push('/')
}
</script>

<style>
</style>
