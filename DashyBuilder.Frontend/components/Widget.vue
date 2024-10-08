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
      <button @click="deleteGridPosition" title="Grid-Position löschen">
        <Icon name="carbon:delete" class="text-danger hover:text-dark-danger"/>
      </button>
      <button @click="openConfigModal" title="Konfiguration bearbeiten">
        <Icon name="ic:outline-settings" class="text-primary hover:text-dark-primary"/>
      </button>
      <button @click="emitDelete" title="Widget löschen">
        <Icon name="carbon:close-outline" class="text-danger hover:text-dark-danger"/>
      </button>
    </div>
    <div class="absolute top-2 left-2 flex space-x-2">
      <button
        @click="openChartModal"
        v-if="hasValidGridPosition && widget.type==='Chart'"
        title="Chart bearbeiten"
      >
        <Icon name="carbon:chart-line" class="text-primary hover:text-dark-primary"/>
      </button>
      <button
        @click="openTableModal"
        v-if="hasValidGridPosition && widget.type==='Table'"
        title="Tabelle bearbeiten"
      >
        <Icon name="carbon:table" class="text-primary hover:text-dark-primary"/>
      </button>
      <button
        @click="openTextModal"
        v-if="hasValidGridPosition && widget.type==='Text Block'"
        title="Textblock bearbeiten"
      >
        <Icon name="solar:text-bold" class="text-primary hover:text-dark-primary"/>
      </button>
      <button
        @click="openButtonModal"
        v-if="hasValidGridPosition && widget.type==='Button'"
        title="Button bearbeiten"
      >
        <Icon name="dashicons:button" class="text-primary hover:text-dark-primary"/>
      </button>
      <button
        @click="openFilterBoxModal"
        v-if="hasValidGridPosition && widget.type==='Filter Box'"
        title="Filterbox bearbeiten"
      >
        <Icon name="mdi:filter-outline" class="text-primary hover:text-dark-primary"/>
      </button>
    </div>
    <!-- Modals bleiben unverändert -->
    <ConfigModal
      v-if="isConfigModalOpen"
      :widget="widget"
      :isOpen="isConfigModalOpen"
      :gridSize="gridSize"
      @close="closeConfigModal"
      @save="saveGridPosition"
    />
    <ChartTypeModal
      v-if="isChartModalOpen"
      :widget="widget"
      :uploadedDatasetId="uploadedDatasetId"
      :isOpen="isChartModalOpen"
      @close="closeChartModal"
      @save="saveChartType"
    />
    <TableModal
      v-if="isTableModalOpen"
      :widget="widget"
      :uploadedDatasetId="uploadedDatasetId"
      :isOpen="isTableModalOpen"
      @close="closeTableModal"
      @save="saveChartType"
    />
    <TextModal
      v-if="isTextModalOpen"
      :widget="widget"
      :uploadedDatasetId="uploadedDatasetId"
      :isOpen="isTextModalOpen"
      @close="closeTextModal"
      @save="saveChartType"
    />
    <ButtonModal
      v-if="isButtonModalOpen"
      :widget="widget"
      :uploadedDatasetId="uploadedDatasetId"
      :isOpen="isButtonModalOpen"
      @close="closeButtonModal"
      @save="saveChartType"
    />
    <FilterBoxModal
      v-if="isFilterBoxModalOpen"
      :widget="widget"
      :uploadedDatasetId="uploadedDatasetId"
      :isOpen="isFilterBoxModalOpen"
      @close="closeFilterBoxModal"
      @save="saveChartType"
    />
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
const isTableModalOpen = ref(false);
const isTextModalOpen = ref(false);
const isButtonModalOpen = ref(false);
const isFilterBoxModalOpen = ref(false);

const hasValidGridPosition = computed(() => {
  return (
    props.widget.gridPosition &&
    props.widget.gridPosition.gridPosition &&
    props.widget.gridPosition.gridPosition.length > 0 &&
    props.widget.gridPosition.gridPosition !== "[]"
  );
});

const deleteGridPosition = () => {
  emit('update-widget', { id: props.widget.id, gridPosition: null });
};

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

function openTableModal() {
  isTableModalOpen.value = true;
}

function openTextModal() {
  isTextModalOpen.value = true;

}

function openButtonModal() {
  isButtonModalOpen.value = true;
}

function openFilterBoxModal() {
  isFilterBoxModalOpen.value = true;
}

function closeConfigModal() {
  isConfigModalOpen.value = false;
}

function closeChartModal() {
  isChartModalOpen.value = false;
}

function closeTableModal() {
  isTableModalOpen.value = false;
}

function closeTextModal() {
  isTextModalOpen.value = false;
}

function closeButtonModal() {
  isButtonModalOpen.value = false;
}

function closeFilterBoxModal() {
  isFilterBoxModalOpen.value = false;
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
