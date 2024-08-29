<template>
  <div class="max-w-full mx-auto h-full"> 
    <div class="bg-white shadow-lg rounded-lg p-4 h-full flex flex-col">
      <h2 class="font-bold text-lg mb-4">Components</h2>
      <div class="flex flex-col space-y-4 flex-grow">
        <div class="flex flex-col lg:flex-row lg:space-x-4 space-y-4 lg:space-y-0 mb-5">
          <div class="flex flex-col w-full lg:w-1/2">
            <label for="component-name" class="block text-gray-700 text-sm font-bold mb-2">Component Name</label>
            <input
              id="component-name"
              v-model="componentName"
              type="text"
              placeholder="Component Name"
              class="p-2 border rounded w-full"
            />
          </div>
          <div class="flex flex-col w-full lg:w-1/2 space-y-2">
            <div class="flex space-x-4">
              <div class="flex flex-col w-1/2">
                <label for="columns" class="block text-gray-700 text-sm font-bold">Columns</label>
                <input
                  id="columns"
                  v-model="columns"
                  type="text"
                  disabled
                  class="p-2 border rounded w-full bg-gray-100"
                />
              </div>
              <div class="flex flex-col w-1/2">
                <label for="rows" class="block text-gray-700 text-sm font-bold">Rows</label>
                <input
                  id="rows"
                  v-model="rows"
                  type="text"
                  disabled
                  class="p-2 border rounded w-full bg-gray-100"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="flex flex-col lg:flex-row lg:space-x-4 space-y-4 lg:space-y-0 mb-5">
          <div class="flex flex-col w-full lg:w-1/2">
            <label for="component-type" class="block text-gray-700 text-sm font-bold mb-2">Component Type</label>
            <select id="component-type" v-model="selectedComponent" class="p-2 border rounded w-full">
              <option disabled value="">Please select one</option>
              <option v-for="component in components" :key="component.id" :value="component.id">
                {{ component.name }}
              </option>
            </select>
          </div>
          <!-- Grid Size Selection and Preview -->
          <div class="flex flex-col w-full lg:w-1/2 items-center justify-center">
            <label class="block text-gray-700 text-sm font-bold mb-2">Grid Preview</label>
            <div class="grid-preview" :class="`grid-cols-${columns} grid-rows-${rows}`" :style="gridStyle">
              <div v-for="cell in gridCells" :key="cell" class="grid-cell"></div>
            </div>
          </div>
        </div>

        <!-- Chart Type Selection -->
        <div v-if="selectedComponent === 1" class="flex flex-col lg:flex-row lg:space-x-4 space-y-4 lg:space-y-0 mb-5">
          <div class="flex flex-col w-full lg:w-1/2">
            <label for="chart-type" class="block text-gray-700 text-sm font-bold mb-2">Chart Type</label>
            <select id="chart-type" v-model="selectedChartType" class="p-2 border rounded w-full">
              <option disabled value="">Please select a chart type</option>
              <option v-for="chart in chartTypes" :key="chart" :value="chart">
                {{ chart }}
              </option>
            </select>
          </div>
        </div>

        <!-- Filter Type Selection -->
        <div v-if="selectedComponent === 4" class="flex flex-col lg:flex-row lg:space-x-4 space-y-4 lg:space-y-0 mb-5">
          <div class="flex flex-col w-full lg:w-1/2">
            <label for="filter-types" class="block text-gray-700 text-sm font-bold mb-2">Filter Types</label>
            <div class="flex flex-col space-y-2">
              <div v-for="filter in filterTypes" :key="filter" class="flex items-center space-x-2">
                <input type="checkbox" :value="filter" v-model="selectedFilterTypes" class="form-checkbox h-4 w-4 text-blue-600">
                <span class="text-gray-700 text-sm">{{ filter }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Widget Button -->
        <button 
          @click="addWidget"
          class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
          style="margin-top: 2.3em;">
          <Icon name="mdi:add" color="white" class="mr-1 text-3xl"/>Add Widget
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['add-widget', 'errorMessage']);

const components = ref([
  { id: 1, name: 'Chart' },
  { id: 2, name: 'Table' },
  { id: 3, name: 'Text Block' },
  { id: 4, name: 'Filter Box' },
  { id: 5, name: 'Button' },
]);

const chartTypes = ref(['Scatter', 'Line', 'Bar', 'Pie', 'Bubble']);
const filterTypes = ref(['Date Range', 'Numeric Range']);

const componentName = ref('');
const selectedComponent = ref('');
const selectedChartType = ref('');
const selectedFilterTypes = ref([]);
const gridSize = ref('4x4');
const columns = ref('');
const rows = ref('');
const gridCells = ref([]);
const gridStyle = ref({});
const isGridSizeDisabled = ref(false);
const route = useRoute();
const projectStore = useProjectStore();

watch(gridSize, (newValue) => {
  const [cols, rws] = newValue.split('x');
  columns.value = cols;
  rows.value = rws;
  updateGridCells();
  updateGridStyle();
});

onMounted(async () => {
  const projectId = route.params.id;
  const projectGridSize = await projectStore.fetchProjectGridSize(projectId);
  if (projectGridSize) {
    gridSize.value = projectGridSize;
    isGridSizeDisabled.value = true;
  }
  const [cols, rws] = gridSize.value.split('x');
  columns.value = cols;
  rows.value = rws;
  updateGridCells();
  updateGridStyle();
});

function updateGridCells() {
  gridCells.value = Array.from({ length: columns.value * rows.value });
}

function updateGridStyle() {
  const maxDimension = Math.max(columns.value, rows.value);
  const cellSize = maxDimension > 6 ? '6px' : '12px';
  gridStyle.value = {
    width: `${columns.value * parseInt(cellSize) + (columns.value - 1) * 2}px`,
    height: `${rows.value * parseInt(cellSize) + (rows.value - 1) * 2}px`,
    gridTemplateColumns: `repeat(${columns.value}, ${cellSize})`,
    gridTemplateRows: `repeat(${rows.value}, ${cellSize})`,
  };
}

function addWidget() {
    if (selectedComponent.value && componentName.value) {
      emit('add-widget', {
        id: Date.now(),
        type: components.value.find(c => c.id === selectedComponent.value).name,
        name: componentName.value,
        chartType: selectedComponent.value === 1 ? selectedChartType.value : null,
        filterTypes: selectedComponent.value === 4 ? selectedFilterTypes.value : null,
        gridSize: gridSize.value
      });
      selectedComponent.value = '';
      componentName.value = '';
      selectedChartType.value = '';
      selectedFilterTypes.value = [];
    } else {
      emit('errorMessage', 'Please select a component and enter a name');
    }
}
</script>


<style scoped>
.grid-preview {
  display: grid;
  gap: 2px;
  background-color: #e2e8f0;
  border: 2px solid #cbd5e0;
  margin-top: 4px;
}

.grid-cell {
  background-color: #ffffff;
  border: 1px solid #cbd5e0;
  box-sizing: border-box;
}

.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid-cols-5 { grid-template-columns: repeat(5, 1fr); }
.grid-cols-6 { grid-template-columns: repeat(6, 1fr); }
.grid-cols-12 { grid-template-columns: repeat(12, 1fr); }

.grid-rows-4 { grid-template-rows: repeat(4, 1fr); }
.grid-rows-5 { grid-template-rows: repeat(5, 1fr); }
.grid-rows-6 { grid-template-rows: repeat(6, 1fr); }
.grid-rows-12 { grid-template-rows: repeat(12, 1fr); }
</style>
