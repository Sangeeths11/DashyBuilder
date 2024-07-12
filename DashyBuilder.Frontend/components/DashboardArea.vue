<template>
  <div class="bg-white shadow-lg rounded-lg p-4">
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
  </div>
</template>

<script setup>
const props = defineProps({
  widgets: Array,
  gridSize: String
});

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
