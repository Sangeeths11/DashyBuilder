<template>
  <div class="p-4 bg-blue-200 rounded-lg shadow flex items-center justify-center text-lg font-semibold relative">
    <span>{{ widget.name }}</span>
    <button @click="emitDelete" class="absolute top-1 right-1">
      <Icon name="carbon:close-outline" class="text-red-700 text-xl"/>
    </button>
    <button @click="emitConfig" class="absolute top-1 left-1">
      <Icon name="ic:outline-settings" class="text-yellow-700 text-xl"/>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  widget: Object
});

const emit = defineEmits(['delete-widget']);

function emitDelete() {
  emit('delete-widget', props.widget.id);
}
</script>
