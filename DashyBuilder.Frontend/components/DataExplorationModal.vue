<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4">
    <div class="relative bg-white w-full max-w-5xl p-6 mx-auto rounded-lg shadow-lg overflow-auto max-h-full">
      <span class="absolute top-0 right-0 p-4">
        <button @click="$emit('close')" class="text-3xl leading-none hover:text-gray-600">&times;</button>
      </span>
      <h2 class="text-2xl font-bold mb-4 text-center">Data Exploration</h2>
      <div v-if="dataInfo" class="space-y-6">
        <div>
          <h3 class="text-xl font-semibold mb-2">Dataset Overview</h3>
          <div class="grid grid-cols-2 gap-4">
            <p><span class="font-bold">Number of Rows:</span> {{ dataInfo.num_rows }}</p>
            <p><span class="font-bold">Number of Columns:</span> {{ dataInfo.num_cols }}</p>
          </div>
        </div>
        <div>
          <h3 class="text-xl font-semibold mb-2">Columns</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <div v-for="col in dataInfo.column_info" :key="col.name" class="bg-gray-100 p-3 rounded shadow-sm">
              <p class="font-bold">{{ col.name }}</p>
              <p class="text-xs text-gray-600">{{ col.dtype }}</p>
            </div>
          </div>
        </div>
        <div>
          <h3 class="text-xl font-semibold mb-2">Missing Values</h3>
          <div class="bg-gray-100 p-4 rounded shadow-sm">
            <ul class="list-disc pl-5">
              <li v-for="(value, key) in dataInfo.missing_values" :key="key">
                <span class="font-semibold">{{ key }}:</span> <span class="text-red-500">{{ value }}</span>
              </li>
            </ul>
          </div>
        </div>
        <div>
          <h3 class="text-xl font-semibold mb-2">Data Preview</h3>
          <div class="overflow-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th v-for="(value, key) in dataInfo.preview_data[0]" :key="key" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {{ key }}
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(row, index) in dataInfo.preview_data" :key="index">
                  <td v-for="(value, key) in row" :key="key" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ value }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div v-else class="text-center">
        <p>No data available. Please upload a dataset.</p>
      </div>
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  show: Boolean,
  datasetId: String,
});

const dataInfo = ref(null);

watch(() => props.datasetId, async (newDatasetId) => {
  if (newDatasetId) {
    const response = await fetch(`http://localhost:5000/data/${newDatasetId}`);
    if (response.ok) {
      const result = await response.json();
      dataInfo.value = result;
    }
  }
});
</script>

<style scoped>
</style>
