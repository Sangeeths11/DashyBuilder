<template>
  <div class="p-4 bg-light-blue rounded-lg shadow hover:shadow-md transition-shadow duration-300 flex flex-col items-center justify-center text-lg font-semibold relative">
    <span class="widget-title">{{ widget.name }}</span>
    <p class="text-sm widget-type">{{ widget.type }}</p>
    <div class="absolute top-2 right-2 flex space-x-2">
      <button @click="openConfigModal">
        <Icon name="ic:outline-settings" class="text-primary hover:text-dark-primary"/>
      </button>
      <button @click="emitDelete">
        <Icon name="carbon:close-outline" class="text-danger hover:text-dark-danger"/>
      </button>
    </div>
    <!-- TODO: Add Chart Infomartion -->
    <!-- <div v-if="widget.type === 'Chart'" class="absolute top-2 left-2">
      <button @click="openChartModal">
        <Icon name="mdi:pen" color="white" class="text-orange-300 hover:text-orange-500"/>
      </button>
    </div> -->
    <ConfigModal v-if="isConfigModalOpen" :widget="widget" :isOpen="isConfigModalOpen" :gridSize="gridSize" @close="closeConfigModal" @save="saveGridPosition" />
    <ChartTypeModal v-if="isChartModalOpen" :widget="widget" :isOpen="isChartModalOpen" @close="closeChartModal" @save="saveChartType" />
  </div>
</template>

<script setup>
const props = defineProps({
  widget: Object,
  gridSize: String,
});

const emit = defineEmits(['delete-widget', 'update-widget']);

const isConfigModalOpen = ref(false);
const isChartModalOpen = ref(false);

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
</style>
