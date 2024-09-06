<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4">
    <div class="relative bg-white w-full max-w-5xl p-6 mx-auto rounded-lg shadow-lg overflow-auto max-h-full">
      <span class="absolute top-0 right-0 p-4">
        <button @click="closeModal" class="text-3xl leading-none hover:text-gray-600">&times;</button>
      </span>
      <h2 class="text-2xl font-bold mb-4 text-center">Chart Configuration</h2>

      <!-- Bar Chart Configuration -->
      <div v-if="widget.chartType === 'Bar'" class="space-y-6">
        <h3 class="text-xl font-semibold mb-2">Bar Chart Configuration</h3>
        <h6 class="text-sm font-semibold mb-2">Select Data Columns</h6>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">X-Axis</label>
            <select v-model="chartConfig.x" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Y-Axis</label>
            <select v-model="chartConfig.y" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Bubble Chart Configuration -->
      <div v-if="widget.chartType === 'Bubble'" class="space-y-6">
        <h3 class="text-xl font-semibold mb-2">Bubble Chart Configuration</h3>
        <h6 class="text-sm font-semibold mb-2">Select Data Columns</h6>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">X-Axis</label>
            <select v-model="chartConfig.x" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Y-Axis</label>
            <select v-model="chartConfig.y" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Size</label>
            <select v-model="chartConfig.size" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Color</label>
            <select v-model="chartConfig.color" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Line Chart Configuration -->
      <div v-if="widget.chartType === 'Line'" class="space-y-6">
        <h3 class="text-xl font-semibold mb-2">Line Chart Configuration</h3>
        <h6 class="text-sm font-semibold mb-2">Select Data Columns</h6>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">X-Axis</label>
            <select v-model="chartConfig.x" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Y-Axis</label>
            <select v-model="chartConfig.y" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Pie Chart Configuration -->
      <div v-if="widget.chartType === 'Pie'" class="space-y-6">
        <h3 class="text-xl font-semibold mb-2">Pie Chart Configuration</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Labels</label>
            <select v-model="chartConfig.labels" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Values</label>
            <select v-model="chartConfig.values" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Scatter Chart Configuration -->
      <div v-if="widget.chartType === 'Scatter'" class="space-y-6">
        <h3 class="text-xl font-semibold mb-2">Scatter Chart Configuration</h3>
        <h6 class="text-sm font-semibold mb-2">Select Data Columns</h6>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">X-Axis</label>
            <select v-model="chartConfig.x" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Y-Axis</label>
            <select v-model="chartConfig.y" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
              <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
            </select>
          </div>
        </div>
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700">Color</label>
          <select v-model="chartConfig.color" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option v-for="column in datasetColumns" :key="column" :value="column">{{ column }}</option>
          </select>
        </div>
      </div>

      <!-- Save Button -->
      <div class="text-center mt-4">
        <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Save Configuration
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  widget: Object,
  uploadedDatasetId: String,
});

const datasetColumns = ref([]);
const emit = defineEmits(['close', 'save']);

const chartConfig = ref({
  x: '',
  y: '',
  size: '',
  color: '',
  labels: '',
  values: '',
});

onMounted(async () => {
  if (props.uploadedDatasetId) {
    await fetchColumns(props.uploadedDatasetId);
  }
});

watch(() => props.uploadedDatasetId, async (newDatasetId) => {
  if (newDatasetId) {
    await fetchColumns(newDatasetId);
  }
});

async function fetchColumns(datasetId) {
  try {
    const response = await fetch(`http://localhost:5000/data/column/${datasetId}`);
    const data = await response.json();
    datasetColumns.value = data.column_info.map(col => col.name); // Assuming you want just the column names
  } catch (error) {
    console.error('Error loading columns:', error);
  }
}

watch(() => props.widget, (newWidget) => {
  if (newWidget) {
    setInitialChartConfig(newWidget.chartConfig);
  }
});

function setInitialChartConfig(config) {
  chartConfig.value = {
    x: config?.x || '',
    y: config?.y || '',
    size: config?.size || '',
    color: config?.color || '',
    labels: config?.labels || '',
    values: config?.values || '',
  };
}

function saveConfig() {
  emit('save', chartConfig.value);
  closeModal();
}

function closeModal() {
  emit('close');
}
</script>

<style scoped>
</style>
