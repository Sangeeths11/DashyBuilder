<template>
  <div class="col-span-1 bg-white shadow-lg rounded-lg p-4">
    <h2 class="font-bold text-lg mb-4">Components</h2>
    <div class="flex items-center mb-4">
      <select v-model="selectedComponent" class="w-1/2 p-2 border rounded mr-4">
        <option disabled value="">Please select one</option>
        <option v-for="component in components" :key="component.id" :value="component.id">
          {{ component.name }}
        </option>
      </select>
      <div class="pl-5">
        <label class="block text-gray-700 text-sm font-bold mb-2">Grid Size</label>
        <div class="flex items-center">
          <label class="inline-flex items-center mr-4">
            <input type="radio" class="form-radio text-blue-600" name="gridSize" value="3x3" v-model="gridSize" :disabled="isGridSizeDisabled">
            <span class="ml-2">3x3 <Icon name="mdi:grid" class="ml-1 w-7 h-7 text-blue-600"/></span>
          </label>
          <label class="inline-flex items-center">
            <input type="radio" class="form-radio text-blue-600" name="gridSize" value="4x4" v-model="gridSize" :disabled="isGridSizeDisabled">
            <span class="ml-2">4x4 <Icon name="material-symbols-light:background-grid-small-outline-sharp" class="ml-1 w-10 h-10 text-blue-600"/></span>
          </label>
        </div>
      </div>
    </div>
    <button 
      @click="addWidget"
      class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
      <Icon name="mdi:add" color="white" class="mr-1 text-3xl"/>Add Widget
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
const gridSize = ref('3x3');
const isGridSizeDisabled = ref(false);
const route = useRoute();
const projectStore = useProjectStore();

onMounted(async () => {
  const projectId = route.params.id;
  const projectGridSize = await projectStore.fetchProjectGridSize(projectId);
  if (projectGridSize) {
    gridSize.value = projectGridSize;
    isGridSizeDisabled.value = true;
  }
});

function addWidget() {
  if (selectedComponent.value) {
    emit('add-widget', {
      id: components.value.length + 1,
      name: components.value.find(c => c.id === selectedComponent.value).name,
      gridSize: gridSize.value
    });
    selectedComponent.value = '';
  }
}
</script>
