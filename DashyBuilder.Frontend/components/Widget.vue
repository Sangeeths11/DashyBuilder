<template>
  <div
    :class="[
      'p-4 rounded-lg shadow hover:shadow-md transition-shadow duration-300 flex flex-col items-center justify-center text-lg font-semibold relative',
      hasValidGridPosition ? 'bg-light-blue' : 'bg-red-100 border border-red-400'
    ]"
  >
    <span :class="[hasValidGridPosition ? 'widget-title' : 'text-red-500']">
      {{ widget.name }}
    </span>
    <p :class="[hasValidGridPosition ? 'text-sm widget-type' : 'text-sm text-red-500']">
      {{ widget.type }}
      {{ widget.chartType ? `(${widget.chartType})` : '' }}
      <span v-if="computedFilterTypes.length > 0">
        ({{ computedFilterTypes.join(', ') }})
      </span>
    </p>
    <p v-if="hasValidGridPosition" class="text-sm text-green-500">
      Position zugewiesen
    </p>
    <p v-else class="text-sm text-red-500">
      Keine Position zugewiesen
    </p>
    <div class="absolute top-2 right-2 flex space-x-2">
      <button @click="openConfigModal">
        <Icon name="ic:outline-settings" class="text-primary hover:text-dark-primary"/>
      </button>
      <button @click="emitDelete">
        <Icon name="carbon:close-outline" class="text-danger hover:text-dark-danger"/>
      </button>
    </div>
    <div class="absolute top-2 left-2 flex space-x-2">
      <button @click="openChartModal" v-if="hasValidGridPosition && widget.type==='Chart'">
        <Icon name="carbon:chart-line" class="text-primary hover:text-dark-primary"/>
      </button>
    </div>
    <ConfigModal v-if="isConfigModalOpen" :widget="widget" :isOpen="isConfigModalOpen" :gridSize="gridSize" @close="closeConfigModal" @save="saveGridPosition" />
    <ChartTypeModal v-if="isChartModalOpen" :widget="widget" :uploadedDatasetId="uploadedDatasetId" :isOpen="isChartModalOpen" @close="closeChartModal" @save="saveChartType" />
  </div>
</template>

<script setup>
import UploadDataset from './UploadDataset.vue';

const props = defineProps({
  widget: Object,
  gridSize: String,
  uploadedDatasetId: String,
});

const emit = defineEmits(['delete-widget', 'update-widget']);

const isConfigModalOpen = ref(false);
const isChartModalOpen = ref(false);

const hasValidGridPosition = computed(() => {
  return (
    props.widget.gridPosition &&
    props.widget.gridPosition.gridPosition &&
    props.widget.gridPosition.gridPosition.length > 0 &&
    props.widget.gridPosition.gridPosition !== "[]"
  );
});

const computedFilterTypes = computed(() => {
  if (Array.isArray(props.widget.filterTypes)) {
    return props.widget.filterTypes;
  } else if (typeof props.widget.filterTypes === 'string') {
    try {
      return JSON.parse(props.widget.filterTypes);
    } catch (e) {
      console.error('Failed to parse filterTypes:', e);
      return [];
    }
  } else {
    return [];
  }
});

function emitDelete() {
  emit('delete-widget', props.widget.id);
}

function openConfigModal() {
  isConfigModalOpen.value = true;
}

function openChartModal() {
  isChartModalOpen.value = true;
}

function closeConfigModal() {
  isConfigModalOpen.value = false;
}

function closeChartModal() {
  isChartModalOpen.value = false;
}

function saveGridPosition(position) {
  emit('update-widget', { id: props.widget.id, gridPosition: position });
}

function saveChartType(type) {
  emit('update-widget', { id: props.widget.id, chartType: type });
}
</script>

<style scoped>
.bg-light-blue {
  background-color: #E7F1FF;
}

.widget-title {
  color: #007BFF;
}

.widget-type {
  color: #6C757D; 
}

.text-primary {
  color: #007BFF;
}

.hover\:text-dark-primary:hover {
  color: #0056b3;
}

.text-danger {
  color: #dc3545;
}

.hover\:text-dark-danger:hover {
  color: #b61a2a;
}

/* Neuer Stil für Widgets ohne Position */
.bg-red-100 {
  background-color: #FDE8E8;
}

.text-red-500 {
  color: #B71C1C;
}

.border-red-400 {
  border-color: #EF5350;
}
</style>
