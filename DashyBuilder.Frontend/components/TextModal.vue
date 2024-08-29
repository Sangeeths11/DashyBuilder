<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4">
      <div class="relative bg-white w-full max-w-5xl p-6 mx-auto rounded-lg shadow-lg overflow-auto max-h-full">
        <span class="absolute top-0 right-0 p-4">
          <button @click="closeModal" class="text-3xl leading-none hover:text-gray-600">&times;</button>
        </span>
        <h2 class="text-2xl font-bold mb-4 text-center">Text Block Configuration</h2>
        <div class="space-y-6">
          <h3 class="text-xl font-semibold mb-2">Enter Text Content</h3>
          <textarea v-model="textContent" rows="6" class="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
          <div class="text-center mt-4">
            <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Save Configuration
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  
  const props = defineProps({
    isOpen: Boolean,
    initialText: String,
  });
  
  const emit = defineEmits(['close', 'save']);
  
  const textContent = ref(props.initialText || 'Please give me some text!');
  
  function saveConfig() {
    emit('save', textContent.value);
    closeModal();
  }
  
  function closeModal() {
    emit('close');
  }
  </script>
  
  <style scoped>
  </style>
  