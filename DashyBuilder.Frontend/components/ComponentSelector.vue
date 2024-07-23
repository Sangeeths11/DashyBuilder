<template>
  <div class="max-w-full mx-auto">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <h2 class="font-bold text-lg mb-4">Components</h2>
      <div class="flex flex-col space-y-4">
        <div class="flex flex-col lg:flex-row lg:space-x-4 space-y-4 lg:space-y-0">
          <div class="flex flex-col w-full lg:w-1/3">
            <label for="component-name" class="block text-gray-700 text-sm font-bold mb-2">Component Name</label>
            <input
              id="component-name"
              v-model="componentName"
              type="text"
              placeholder="Component Name"
              class="p-2 border rounded w-full"
            />
          </div>
          <div class="flex flex-col w-full lg:w-1/3">
            <label for="component-type" class="block text-gray-700 text-sm font-bold mb-2">Component Type</label>
            <select id="component-type" v-model="selectedComponent" class="p-2 border rounded w-full">
              <option disabled value="">Please select one</option>
              <option v-for="component in components" :key="component.id" :value="component.id">
                {{ component.name }}
              </option>
            </select>
          </div>
          <div class="flex flex-col w-full lg:w-auto">
            <label class="block text-gray-700 text-sm font-bold mb-2">Grid Size</label>
            <div class="flex flex-wrap space-x-2">
              <label class="inline-flex items-center mb-2">
                <input type="radio" class="form-radio text-blue-600" name="gridSize" value="4x4" v-model="gridSize" :disabled="isGridSizeDisabled">
                <span class="ml-2">4x4 <Icon name="mdi:grid" class="ml-1 w-8 h-8 text-blue-600"/></span>
              </label>
              <label class="inline-flex items-center mb-2">
                <input type="radio" class="form-radio text-blue-600" name="gridSize" value="5x5" v-model="gridSize" :disabled="isGridSizeDisabled">
                <span class="ml-2">5x5 <Icon name="mdi:grid" class="ml-1 w-10 h-10 text-blue-600"/></span>
              </label>
              <label class="inline-flex items-center mb-2">
                <input type="radio" class="form-radio text-blue-600" name="gridSize" value="6x6" v-model="gridSize" :disabled="isGridSizeDisabled">
                <span class="ml-2">6x6 <Icon name="mdi:grid" class="ml-1 w-12 h-12 text-blue-600"/></span>
              </label>
              <label class="inline-flex items-center mb-2">
                <input type="radio" class="form-radio text-blue-600" name="gridSize" value="12x12" v-model="gridSize" :disabled="isGridSizeDisabled">
                <span class="ml-2">12x12 <Icon name="mdi:grid" class="ml-1 w-16 h-16 text-blue-600"/></span>
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
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['add-widget']);

const components = ref([
  { id: 1, name: 'Chart' },
  { id: 2, name: 'Table' },
  { id: 3, name: 'Text Block' },
  { id: 4, name: 'Filter Box' }
]);

const componentName = ref('');
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
  if (selectedComponent.value && componentName.value) {
    emit('add-widget', {
      id: Date.now(),
      type: components.value.find(c => c.id === selectedComponent.value).name,
      name: componentName.value,
      gridSize: gridSize.value
    });
    selectedComponent.value = '';
    componentName.value = '';
  } else {
    alert("Bitte wählen Sie eine Komponente und geben Sie einen Namen ein");
  }
}
</script>

<style scoped>
</style>
