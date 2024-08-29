<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4">
      <div class="relative bg-white w-full max-w-5xl p-6 mx-auto rounded-lg shadow-lg overflow-auto max-h-full">
        <span class="absolute top-0 right-0 p-4">
          <button @click="closeModal" class="text-3xl leading-none hover:text-gray-600">&times;</button>
        </span>
        <h2 class="text-2xl font-bold mb-4 text-center">Table Configuration</h2>
        <div v-if="datasetColumns.length" class="space-y-6">
          <h3 class="text-xl font-semibold mb-2">Select Columns to Display</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <div v-for="column in datasetColumns" :key="column.name">
              <label class="inline-flex items-center">
                <input
                  type="checkbox"
                  v-model="localSelectedColumns"
                  :value="column.name"
                  class="form-checkbox h-5 w-5 text-blue-600"
                >
                <span class="ml-2 text-gray-700">{{ column.name }}</span>
              </label>
            </div>
          </div>
          <div class="text-center mt-4">
            <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Save Configuration
            </button>
          </div>
        </div>
        <div v-else class="text-center">
          <p>Loading columns...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue';
  
  const props = defineProps({
    isOpen: Boolean,
    widget: Object,
    uploadedDatasetId: String,
  });
  
  const emit = defineEmits(['close', 'save']);
  
  const datasetColumns = ref([]);
  const localSelectedColumns = ref([]);
  
  async function loadDatasetColumns() {
    try {
      const response = await fetch(`http://localhost:5000/data/column/${props.uploadedDatasetId}`);
      const data = await response.json();
      
      if (data && data.column_info) {
        datasetColumns.value = data.column_info;
      } else {
        console.error('Unexpected response structure:', data);
      }
  
      localSelectedColumns.value = props.widget.selectedColumns || [];
    } catch (error) {
      console.error('Error loading dataset columns:', error);
    }
  }
  
  onMounted(() => {
    loadDatasetColumns();
  });
  
  watch(
    () => props.widget,
    (newWidget) => {
      if (newWidget) {
        localSelectedColumns.value = newWidget.selectedColumns || [];
      }
    }
  );
  
  function saveConfig() {
    const updatedWidget = { ...props.widget, selectedColumns: localSelectedColumns.value };
    emit('save', updatedWidget);
    closeModal();
  }
  
  function closeModal() {
    emit('close');
  }
  </script>
  
  <style scoped>
  </style>
  