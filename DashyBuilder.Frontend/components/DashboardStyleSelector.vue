<template>
  <div class="w-full mb-5">
    <div class="bg-white shadow-lg rounded-lg p-4 h-full flex flex-col">
      <h2 class="font-bold text-lg mb-4">Dashboard Options</h2>
      <div class="flex flex-col">
        <label for="mockup-style" class="text-gray-700 text-sm font-bold mb-2 flex align-middle">
          <Icon name="mdi:color" class="text-xl" /> Style
        </label>
        <select id="mockup-style" v-model="selectedMockupStyle"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2"
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