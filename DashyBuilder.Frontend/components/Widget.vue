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
    <ConfigModal v-if="isConfigModalOpen" :widget="widget" :isOpen="isConfigModalOpen" :gridSize="gridSize" @close="closeConfigModal" @save="saveGridPosition" />
  </div>
</template>

<script setup>
const props = defineProps({
  widget: Object,
  gridSize: String,
});

const emit = defineEmits(['delete-widget', 'update-widget']);

const isConfigModalOpen = ref(false);

function emitDelete() {
  emit('delete-widget', props.widget.id);
}

function openConfigModal() {
  isConfigModalOpen.value = true;
}

function closeConfigModal() {
  isConfigModalOpen.value = false;
}

function saveGridPosition(position) {
  emit('update-widget', { id: props.widget.id, gridPosition: position });
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
