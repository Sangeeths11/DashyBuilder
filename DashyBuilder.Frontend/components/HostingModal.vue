<template>
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-11/12 md:w-1/3">
        <h2 class="text-2xl font-bold mb-4">Dashboard Hosted</h2>
        <p class="mb-4">Your dashboard has been successfully hosted. You can view it at the following link:</p>
        <a :href="url" target="_blank" class="text-blue-500 underline">{{ url }}</a>
        <div class="mt-6 flex justify-end">
          <button @click="$emit('close')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Close
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: {
        type: Boolean,
        required: true
      },
      url: {
        type: String,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  /* Optional: Add any additional styling here */
  </style>
  