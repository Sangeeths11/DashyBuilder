<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-90 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-lg w-80 relative">
      <h3 class="text-lg font-bold mb-4">Configure Widget Position</h3>
      <div :style="gridStyle" class="grid-container">
        <div v-for="cell in totalCells" :key="cell" :class="['cell', isSelected(cell) ? 'selected' : '']" @click="toggleCell(cell)">
          <span v-if="isSelected(cell)" class="cross">✕</span>
        </div>
      </div>
      <div class="mt-4">
        <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded float-right">Save</button>
        <button @click="$emit('close')" class=" bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded float-left">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  widget: Object,
  gridSize: String,
});

const selectedCells = ref(props.widget.gridPosition ? props.widget.gridPosition.split(',').map(Number) : []);

const rows = computed(() => props.gridSize.startsWith('3') ? 3 : 4);
const totalCells = computed(() => rows.value * rows.value);

const gridStyle = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(${rows.value}, 1fr)`,
  gap: '5px',
  width: '100%',
  height: 'auto',
  aspectRatio: '1'
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
  $emit('save', selectedCells.value.join(','));
  $emit('close');
}
</script>

<style scoped>
.grid-container {
  width: 200px;
  height: 200px;
}

.cell {
  background-color: #f4f4f4;
  border: 1px solid #ccc;
  position: relative;
  cursor: pointer;
  aspect-ratio: 1;
}

.cell.selected {
  background-color: #bcd;
}

.cross {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: xx-large;
  color: red;
}
</style>
