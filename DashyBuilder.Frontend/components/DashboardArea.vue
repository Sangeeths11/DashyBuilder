<template>
  <div class="bg-white shadow-lg rounded-lg p-4 relative">
    <h2 class="font-bold text-lg mb-4">Dashboard</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <Widget
        v-for="widget in widgets"
        :key="widget.id"
        :widget="widget"
        :gridSize="gridSize"
        @delete-widget="emitDeleteWidget"
        @update-widget="emitUpdateWidget"
      />
    </div>
    <button v-if="uploadedDatasetId" @click="showAISuggestion = true" class="absolute top-4 right-4 bg-purple-600 hover:bg-purple-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
      <Icon name="mdi:robot" color="white" class="text-2xl"/>
    </button>

    <AISuggestionModal :show="showAISuggestion" @close="showAISuggestion = false"/>
  </div>
</template>

<script setup>
const props = defineProps({
  widgets: Array,
  gridSize: String,
  uploadedDatasetId: String
});
const showAISuggestion = ref(false); // Hinzugefügt
const emit = defineEmits(['delete-widget', 'update-widget']);

function emitDeleteWidget(id) {
  emit('delete-widget', id);
}

function emitUpdateWidget(data) {
  emit('update-widget', data);
}
</script>

<style scoped>
</style>
