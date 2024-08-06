<template>
    <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-1/2">
        <h2 class="text-2xl font-bold mb-4">AI Suggestions</h2>
        <p class="mb-4">Hier werden AI basierte Vorschläge angezeigt.</p>
        <!-- Hier fügst du die Inhalte und Funktionalitäten des Modals hinzu -->
        <button @click="$emit('close')" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
          Schließen
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    show: {
      type: Boolean,
      required: true
    }
  });
  </script>
  
  <style scoped>
  /* Optional: Style-Anpassungen für das Modal */
  </style>
  