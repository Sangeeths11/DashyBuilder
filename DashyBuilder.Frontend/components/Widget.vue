<template>
  <div class="p-4 bg-blue-200 rounded-lg shadow flex flex-col items-center justify-center text-lg font-semibold relative">
    <span>{{ widget.name }}</span>
    <p class="text-sm">{{ widget.type }}</p>
    <button @click="emitDelete" class="absolute top-1 right-1">
      <Icon name="carbon:close-outline" class="text-red-700 text-xl"/>
    </button>
    <button @click="openConfigModal" class="absolute top-1 left-1">
      <Icon name="ic:outline-settings" class="text-yellow-700 text-xl"/>
    </button>
    <ConfigModal v-if="isConfigModalOpen" @close="isConfigModalOpen = false" :widget="widget" />
  </div>
</template>

<script setup>
const props = defineProps({
  widget: Object
});

const emit = defineEmits(['delete-widget']);
const isConfigModalOpen = ref(false);

function emitDelete() {
  emit('delete-widget', props.widget.id);
}

function openConfigModal() {
  isConfigModalOpen.value = true;
}
</script>
