<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4">
    <div class="relative bg-white w-full max-w-4xl p-6 mx-auto rounded-lg shadow-lg overflow-auto max-h-full">
      <span class="absolute top-0 right-0 p-4">
        <button @click="closeModal" class="text-3xl leading-none hover:text-gray-600">&times;</button>
      </span>
      <h2 class="text-2xl font-bold mb-4 text-center">Filter Configuration</h2>

      <!-- Numeric Range Filter -->
      <div v-if="widget.filterTypes.includes('Numeric Range')" class="space-y-6">
        <h4 class="text-lg font-semibold text-gray-700 mb-3">Numeric Range Filter</h4>
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Column</label>
        <select v-model="filterConfig.numericRange.column" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          <option v-for="col in numericColumns" :key="col.name" :value="col.name">{{ col.name }}</option>
        </select>
        <label class="block text-sm font-medium text-gray-700 mt-4 mb-2">Step</label>
        <input type="number" v-model="filterConfig.numericRange.step" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" step="any">
      </div>

      <!-- Date Range Filter -->
      <div v-if="widget.filterTypes.includes('Date Range')" class="space-y-6 mt-6">
        <h4 class="text-lg font-semibold text-gray-700 mb-3">Date Range Filter</h4>
        <label class="block text-sm font-medium text-gray-700 mb-2">Start Date:</label>
        <input type="date" v-model="filterConfig.dateRange.startDate" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">End Date:</label>
        <input type="date" v-model="filterConfig.dateRange.endDate" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
      </div>

      <!-- Save Button -->
      <div class="text-center mt-6">
        <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-md transition duration-300 ease-in-out">
          Save Configuration
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: Boolean,
  widget: Object,
  uploadedDatasetId: String,
});

const emit = defineEmits(['close', 'save']);

const numericColumns = ref([]); 

const filterConfig = ref({
  numericRange: {
    column: '',
    min: 0,
    max: 100,
    value: [0, 100],
    step: 0
  },
  dateRange: {
    column: '',
    startDate: '',
    endDate: ''
  }
});

async function loadColumns() {
  try {
    const response = await fetch(`http://localhost:5000/data/column/${props.uploadedDatasetId}`);
    const data = await response.json();
    
    if (data && data.column_info) {
      numericColumns.value = data.column_info;
    } else {
      console.error('Unexpected response structure:', data);
    }
  } catch (error) {
    console.error('Error loading dataset columns:', error);
  }
}

onMounted(() => {
  loadColumns();
  if (props.widget.filterConfig) {
    filterConfig.value = { ...props.widget.filterConfig };
  }
});

watch(() => props.widget, (newWidget) => {
  if (newWidget && newWidget.filterConfig) {
    filterConfig.value = { ...newWidget.filterConfig };
  }
});

function saveConfig() {
  const updatedWidget = { 
    ...props.widget, 
    filterConfig: filterConfig.value
  };
  emit('save', updatedWidget);
  closeModal();
}

function closeModal() {
  emit('close');
}
</script>

<style scoped>
</style>
