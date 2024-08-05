<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-90 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-lg w-80 relative">
      <ErrorMessageBox :message="errorMessage"/>
      <h3 class="text-lg font-bold mb-4">Configure Widget Position</h3>
      <p class="text-sm text-gray-600 mb-4">Please select the position for the widget: 
        <strong class="text-sm text-gray-600 mb-2">
          {{ widget.name }} ({{ widget.type }})
        </strong>
      </p>
      
      <div :style="gridStyle" class="grid-container" @mousedown="startSelection" @mousemove="throttledMoveSelection" @mouseup="endSelection" @mouseleave="endSelection">
        <div v-for="cell in totalCells" :key="cell"
            :class="['cell', isSelected(cell) ? 'selected' : '', isOriginal(cell) ? 'original' : '', isDisabled(cell) ? 'disabled' : '']">
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
import { ref, computed, onMounted } from 'vue';
import { throttle } from 'lodash';

const props = defineProps({
  widget: Object,
  gridSize: String,
  projectId: Number
});

const { fetchReservedPositions } = useWidgetStore();
const reservedPositions = ref([]);
const errorMessage = ref('');

let gridPositionData;
try {
  if (props.widget.gridPosition && typeof props.widget.gridPosition.gridPosition === 'string') {
    gridPositionData = props.widget.gridPosition.gridPosition.split(',').map(Number).filter(num => !isNaN(num));
  } else {
    gridPositionData = [];
  }
} catch (e) {
  console.error('Invalid gridPosition data:', props.widget.gridPosition);
  errorMessage.value = 'Invalid gridPosition data.';
  setTimeout(() => {
    errorMessage.value = '';
  }, 3000);
  gridPositionData = [];
}

const selectedCells = ref([]);
const originalCells = ref([...gridPositionData]);

onMounted(async () => {
  reservedPositions.value = await fetchReservedPositions(props.widget.project_id);
  reservedPositions.value = reservedPositions.value.filter(pos => !originalCells.value.includes(pos));
});

const emit = defineEmits(['close', 'save']);

const rows = computed(() => {
  if (props.gridSize.startsWith('4')) {
    return 4;
  } else if (props.gridSize.startsWith('5')) {
    return 5;
  } else if (props.gridSize.startsWith('6')) {
    return 6;
  } else if (props.gridSize.startsWith('12')) {
    return 12;
  } else {
    return 4;
  }
});

const totalCells = computed(() => rows.value * rows.value);

const gridStyle = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(${rows.value}, 1fr)`,
  gap: '5px',
  width: '100%',
  height: 'auto',
  aspectRatio: '1'
}));

let isSelecting = ref(false);
let startCell = ref(null);

function startSelection(event) {
  const cell = getCellFromEvent(event);
  if (cell && !isDisabled(cell)) {
    isSelecting.value = true;
    startCell.value = cell;
    selectRange(cell, cell);
  }
}

function moveSelection(event) {
  if (isSelecting.value && startCell.value) {
    const endCell = getCellFromEvent(event);
    if (endCell && !isDisabled(endCell)) {
      selectRange(startCell.value, endCell);
    }
  }
}

// Verwende Throttle für die moveSelection-Funktion
const throttledMoveSelection = throttle(moveSelection, 50); // Throttle auf 50ms setzen

function endSelection() {
  isSelecting.value = false;
  startCell.value = null;
}

function getCellFromEvent(event) {
  const cellElement = event.target.closest('.cell');
  if (cellElement) {
    const index = [...cellElement.parentElement.children].indexOf(cellElement);
    return index + 1;
  }
  return null;
}

function selectRange(start, end) {
  const min = Math.min(start, end);
  const max = Math.max(start, end);
  const startRow = Math.floor((min - 1) / rows.value);
  const startCol = (min - 1) % rows.value;
  const endRow = Math.floor((max - 1) / rows.value);
  const endCol = (max - 1) % rows.value;

  selectedCells.value = [];

  originalCells.value = [];

  for (let row = startRow; row <= endRow; row++) {
    for (let col = startCol; col <= endCol; col++) {
      const cell = row * rows.value + col + 1;
      if (!isDisabled(cell)) {
        selectedCells.value.push(cell);
      }
    }
  }
}

function isOriginal(cell) {
  return originalCells.value.includes(cell);
}

function isSelected(cell) {
  return selectedCells.value.includes(cell);
}

function isDisabled(cell) {
  return reservedPositions.value.includes(cell) && !isOriginal(cell);
}

function validateGridPattern(selectedCells, gridSize) {
  selectedCells = selectedCells.filter(cell => cell !== 0);

  const rows = gridSize.startsWith('4') ? 4 : gridSize.startsWith('5') ? 5 : gridSize.startsWith('6') ? 6 : gridSize.startsWith('12') ? 12 : 4;
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

function saveConfig() {
  if (validateGridPattern(selectedCells.value, props.gridSize)) {
    // Neue Positionen hinzufügen
    reservedPositions.value.push(...selectedCells.value);

    emit('save', selectedCells.value.join(','));
    emit('close');
  } else {
    errorMessage.value = 'Invalid pattern.';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  }
}

function close() {
  reservedPositions.value.push(...originalCells.value);
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
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out;
}
.cell.original {
  background-color: #4caf50; /* Grün für Originalposition */
}
.cell.selected {
  background-color: #bcd; /* Blau für neue Auswahl */
}
.cell.disabled {
  background-color: #ddd;
  cursor: not-allowed;
}
</style>
