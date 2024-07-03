<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <header class="bg-blue-500 text-white p-4 text-lg flex justify-between items-center">
      <span>Dashboard Designer Tool</span>
      <span class="text-2xl"><iconify-icon icon="mdi:chart-box-outline"></iconify-icon></span>
    </header>
    <main class="flex-grow p-4">
      <div class="grid grid-cols-3 gap-4">
        <div class="col-span-1 bg-white shadow-lg rounded-lg p-4">
          <h2 class="font-bold text-lg mb-4">Components</h2>
          <select v-model="selectedComponent" class="w-full p-2 border rounded mb-4">
            <option disabled value="">Please select one</option>
            <option v-for="component in components" :key="component.id" :value="component">
              {{ component.name }}
            </option>
          </select>
          <button 
            @click="addWidget"
            class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition duration-200"
          >
            Add Widget
          </button>
        </div>
        <div class="col-span-2 bg-white shadow-lg rounded-lg p-4">
          <h2 class="font-bold text-lg mb-4">Dashboard</h2>
          <div class="grid grid-cols-3 gap-4">
            <div 
              v-for="widget in widgets" 
              :key="widget.id" 
              class="p-4 bg-blue-200 rounded-lg shadow flex items-center justify-center text-lg font-semibold"
            >
              <span>{{ widget.name }}</span>
              <span class="ml-2 text-2xl"><iconify-icon icon="mdi:widgets-outline"></iconify-icon></span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const components = ref([
  { id: 1, name: 'Chart' },
  { id: 2, name: 'Table' },
  { id: 3, name: 'Text Block' }
]);

const widgets = ref([]);
const selectedComponent = ref('');

function addWidget() {
  if (selectedComponent.value) {
    widgets.value.push({ ...selectedComponent.value, id: widgets.value.length + 1 });
    selectedComponent.value = '';
  }
}
</script>

<style scoped>
</style>
