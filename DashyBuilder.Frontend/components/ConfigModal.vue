<template>
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
      <div class="bg-white p-6 rounded shadow-lg">
        <h3 class="text-lg font-bold mb-4">Configure Widget Position</h3>
        <div :style="gridStyle" class="relative">
          <div v-for="cell in totalCells" :key="cell" :class="['cell', isSelected(cell) ? 'selected' : '']" @click="toggleCell(cell)">
            <span v-if="isSelected(cell)" class="cross">✕</span>
          </div>
        </div>
        <div class="mt-4">
          <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Save</button>
          <button @click="$emit('close')" class="ml-2 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    widget: Object
  });
  
  const selectedCells = ref([]);
  
  const rows = computed(() => props.widget.gridSize.startsWith('3') ? 3 : 4);
  const totalCells = computed(() => rows.value * rows.value);
  
  const gridStyle = computed(() => ({
    display: 'grid',
    gridTemplateColumns: `repeat(${rows.value}, 1fr)`,
    gap: '5px',
    width: '200px', // Adjust based on your layout
    height: '200px' // Adjust based on your layout
  }));
  
  function toggleCell(cell) {
    const index = selectedCells.value.indexOf(cell);
    if (index === -1) {
      selectedCells.value.push(cell);
    } else {
      selectedCells.value.splice(index, 1);
    }
  }
  
  function isSelected(cell) {
    return selectedCells.value.includes(cell);
  }
  
  function saveConfig() {
    console.log('Configuration saved:', selectedCells.value);
    $emit('close');
  }
  </script>
  
  <style scoped>
  .cell {
    background-color: #f4f4f4;
    border: 1px solid #ccc;
    position: relative;
    cursor: pointer;
  }
  
  .cell.selected {
    background-color: #bcd;
  }
  
  .cross {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: large;
    color: red;
  }
  </style>
  