<template>
  <div class="p-4 bg-blue-200 rounded-lg shadow hover:shadow-md transition-shadow duration-300 flex flex-col items-center justify-center text-lg font-semibold relative">
    <span>{{ widget.name }}</span>
    <p class="text-sm">{{ widget.type }}</p>
    <div class="absolute top-2 right-2 flex space-x-2">
      <button @click="openConfigModal">
        <Icon name="ic:outline-settings" class="text-yellow-700 text-xl hover:text-yellow-500"/>
      </button>
      <button @click="emitDelete">
        <Icon name="carbon:close-outline" class="text-red-700 text-xl hover:text-red-500"/>
      </button>
    </div>
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

<style scoped>
</style>