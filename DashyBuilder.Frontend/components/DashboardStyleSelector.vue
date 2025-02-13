<template>
  <div class="w-full mb-5">
    <div class="bg-white shadow-lg rounded-lg p-4 h-full flex flex-col">
      <h2 class="font-bold text-lg mb-4">Dashboard Options</h2>
      <div class="flex flex-col w-full lg:w-1/2">
        <label for="mockup-style" class="block text-gray-700 text-sm font-bold mb-2">Style</label>
        <select id="mockup-style" v-model="selectedMockupStyle" class="p-2 border rounded w-full"
          @change="emitSelectedStyle">
          <option v-for="mockupStyle in mockupStyles" :key="mockupStyle.id" :value="mockupStyle.id">
            {{ mockupStyle.name }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['selected-style']);
const mockupStyles = ref([
  { id: 'components', name: 'Put own dashboard with components together' },
  { id: 'mockup', name: 'Upload dashboard mockup' },
]);
const selectedMockupStyle = ref('components');

function emitSelectedStyle() {
  if (selectedMockupStyle.value) {
    emit('selected-style', selectedMockupStyle.value);
  }
}
</script>