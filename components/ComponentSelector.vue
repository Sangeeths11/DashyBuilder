<template>
  <div class="col-span-1 bg-white shadow-lg rounded-lg p-4">
    <h2 class="font-bold text-lg mb-4">Components</h2>
    <select v-model="selectedComponent" class="w-full p-2 border rounded mb-4">
      <option disabled value="">Please select one</option>
      <option v-for="component in components" :key="component.id" :value="component.id">
        {{ component.name }}
      </option>
    </select>
    <button 
      @click="addWidget"
      class="mt-4 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    >
      Add Widget
    </button>
  </div>
</template>

<script setup>
const emit = defineEmits(['add-widget']);

const components = ref([
  { id: 1, name: 'Chart' },
  { id: 2, name: 'Table' },
  { id: 3, name: 'Text Block' }
]);
const selectedComponent = ref('');

function addWidget() {
  if (selectedComponent.value) {
    emit('add-widget', selectedComponent.value);
    selectedComponent.value = '';
  }
}
</script>
