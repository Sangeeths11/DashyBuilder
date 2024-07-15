<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-90 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-lg w-80 relative">
      <h3 class="text-lg font-bold mb-4">Configure Widget Position</h3>
      <div :style="gridStyle" class="grid-container">
        <div v-for="cell in totalCells" :key="cell"
            :class="['cell', isSelected(cell) ? 'selected' : '', isDisabled(cell) ? 'disabled' : '']"
            @click="toggleCell(cell)">
          <span v-if="isSelected(cell)" class="cross">✕</span>
        </div>
      </div>
      <div class="mt-4">
        <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded float-right">Save</button>
        <button @click="close" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded float-left">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  widget: Object,
  gridSize: String,
  projectId: Number
});

const { fetchReservedPositions } = useWidgetStore();
const reservedPositions = ref([]);

onMounted(async () => {
  reservedPositions.value = await fetchReservedPositions(props.widget.project_id);
  reservedPositions.value = reservedPositions.value.filter(pos => pos !== props.widget.gridPosition);
});

const emit = defineEmits(['close', 'save']);

let gridPositionData;
try {
  if (props.widget.gridPosition && typeof props.widget.gridPosition.gridPosition === 'string') {
    gridPositionData = props.widget.gridPosition.gridPosition.split(',').map(Number).filter(num => !isNaN(num));
  } else {
    gridPositionData = [];
  }
} catch (e) {
  console.error('Invalid gridPosition data:', props.widget.gridPosition);
  gridPositionData = [];
}

const selectedCells = ref(gridPositionData);

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
  if (!isDisabled(cell) || isSelected(cell)) {
    const index = selectedCells.value.indexOf(cell);
    if (index === -1) {
      selectedCells.value.push(cell);
      reservedPositions.value.push(cell);
    } else {
      selectedCells.value.splice(index, 1);
      reservedPositions.value = reservedPositions.value.filter(pos => pos !== cell);
    }
  }
}

function validateGridPattern(selectedCells, gridSize) {
  const rows = gridSize.startsWith('3') ? 3 : 4;
  const grid = new Array(rows).fill(null).map(() => new Array(rows).fill(false));

  selectedCells.forEach(cell => {
    const row = Math.floor((cell - 1) / rows);
    const col = (cell - 1) % rows;
    grid[row][col] = true;
  });

  function dfs(row, col, visited) {
    if (row < 0 || row >= rows || col < 0 || col >= rows || !grid[row][col] || visited.has(`${row},${col}`)) {
      return;
    }
    visited.add(`${row},${col}`);
    dfs(row + 1, col, visited); 
    dfs(row - 1, col, visited); 
    dfs(row, col + 1, visited);
    dfs(row, col - 1, visited); 
  }

  // Starte DFS von der ersten gefundenen ausgewählten Zelle
  let found = false;
  const visited = new Set();
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < rows; col++) {
      if (grid[row][col]) {
        dfs(row, col, visited);
        found = true;
        break;
      }
    }
    if (found) break;
  }

  if (visited.size !== selectedCells.length) {
    return false;
  }

  // Prüfe auf rechteckige oder quadratische Form
  const selectedRows = selectedCells.map(cell => Math.floor((cell - 1) / rows));
  const selectedCols = selectedCells.map(cell => (cell - 1) % rows);
  const minRow = Math.min(...selectedRows);
  const maxRow = Math.max(...selectedRows);
  const minCol = Math.min(...selectedCols);
  const maxCol = Math.max(...selectedCols);

  for (let row = minRow; row <= maxRow; row++) {
    for (let col = minCol; col <= maxCol; col++) {
      if (!grid[row][col]) {
        return false;
      }
    }
  }

  return true;
}

function isSelected(cell) {
  return selectedCells.value.includes(cell);
}

function isDisabled(cell) {
  return reservedPositions.value.includes(cell) && !isSelected(cell);
}

function saveConfig() {
  if (validateGridPattern(selectedCells.value, props.gridSize)) {
    emit('save', selectedCells.value.join(','));
    emit('close');
  } else {
    alert('Invalid grid pattern. Please select a valid pattern.');
  }
}

function close() {
  emit('close');
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
.cell.disabled {
  background-color: #ddd;
  cursor: not-allowed;
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
