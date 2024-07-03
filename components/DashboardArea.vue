<template>
  <div class="col-span-2 bg-white shadow-lg rounded-lg p-4">
    <h2 class="font-bold text-lg mb-4">Dashboard</h2>
    <div class="grid grid-cols-3 gap-4">
      <Widget
        v-for="widget in widgets"
        :key="widget.id"
        :widget="widget"
        @delete-widget="emitDeleteWidget"
      />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  widgets: Array
});

const emit = defineEmits(['delete-widget']);

function emitDeleteWidget(id) {
  emit('delete-widget', id);
}
</script>
