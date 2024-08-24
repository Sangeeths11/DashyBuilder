<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-90 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-lg w-[700px] h-[700px] relative flex flex-col"> 
      <!-- Feste Größe des Modals -->
      <button @click="close" class="absolute top-3 right-3 text-gray-600 hover:text-gray-900">
        &times;
      </button>
      <ErrorMessageBox :message="errorMessage"/>
      <h3 class="text-lg font-bold mb-4 text-center">Configure Widget Position</h3>
      <p class="text-sm text-gray-600 mb-4 text-center">Please select the position for the widget: 
        <strong class="text-sm text-gray-600 mb-2">
          {{ widget.name }} ({{ widget.type }})
        </strong>
      </p>
      
      <div :style="gridStyle" class="grid-container flex-grow" @mousedown="startSelection" @mousemove="throttledMoveSelection" @mouseup="endSelection" @mouseleave="endSelection">
        <div v-for="cell in totalCells" :key="cell"
            :class="['cell', isSelected(cell) ? 'selected' : '',
            isOriginal(cell) ? 'original' : '',
            isDisabled(cell) ? 'disabled' : '']"
            :style="isDisabled(cell) ? { backgroundColor: '#D3D3D3' } : {}"
            @mouseenter="updateTooltipText(cell)" @mouseleave="hoverCell(null)">
          <span v-if="hoveredCell === cell" class="tooltip">{{ tooltipText }}</span>
        </div>
      </div>
      <div class="mt-4 flex justify-center"> <!-- Button zentriert -->
        <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Save</button>
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
const hoveredCell = ref(null); // Ref für die hover-Zelle
const tooltipText = ref(''); // Ref für den Tooltip-Text
const widgetStore = useWidgetStore();

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

// Dynamische Berechnung von Spalten und Reihen
const [cols, rows] = props.gridSize.split('x').map(Number);

const totalCells = computed(() => rows * cols);

const cellSize = computed(() => {
  const maxModalSize = 450; // Basisgröße des verfügbaren Platzes im Modal (abzüglich Paddings)
  const maxGridDimension = Math.max(cols, rows);
  return Math.floor(maxModalSize / maxGridDimension);
});

const gridStyle = computed(() => {
  return {
    display: 'grid',
    gridTemplateColumns: `repeat(${cols}, ${cellSize.value}px)`,
    gridTemplateRows: `repeat(${rows}, ${cellSize.value}px)`,
    gap: '4px', // Kleinerer Abstand zwischen den Zellen, um mehr Platz zu nutzen
    justifyContent: 'center',
    alignContent: 'center',
  };
});

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

const throttledMoveSelection = throttle(moveSelection, 50);

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
  const startRow = Math.floor((min - 1) / cols);
  const startCol = (min - 1) % cols;
  const endRow = Math.floor((max - 1) / cols);
  const endCol = (max - 1) % cols;

  selectedCells.value = [];
  originalCells.value = [];

  for (let row = startRow; row <= endRow; row++) {
    for (let col = startCol; col <= endCol; col++) {
      const cell = row * cols + col + 1;
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

function hoverCell(cell) {
  hoveredCell.value = cell; // Setzt die aktuelle hover-Zelle
}

async function updateTooltipText(cell) {
  hoverCell(cell); // Updates the hovered cell
  if (isOriginal(cell)) {
    tooltipText.value = `Original Widget Position: ${cell}`;
  } else if (isDisabled(cell)) {
    const widgetTooltip = await widgetStore.getWidgetByGridPosition(cell, props.widget.project_id);
    if (widgetTooltip) {
      tooltipText.value = `Reserved Cell: ${cell} (${widgetTooltip.name})`;
    } else {
      tooltipText.value = `Reserved Cell: ${cell} (Unknown Widget)`;
    }
  } else {
    hoverCell(null);
  }
}

function validateGridPattern(selectedCells, gridSize) {
  selectedCells = selectedCells.filter(cell => cell !== 0);

  const [cols, rows] = gridSize.split('x').map(Number);
  const grid = new Array(rows).fill(null).map(() => new Array(cols).fill(false));

  selectedCells.forEach(cell => {
    const row = Math.floor((cell - 1) / cols);
    const col = (cell - 1) % cols;
    grid[row][col] = true;
  });

  function dfs(row, col, visited) {
    if (row < 0 || row >= rows || col < 0 || col >= cols || !grid[row][col] || visited.has(`${row},${col}`)) {
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
    for (let col = 0; col < cols; col++) {
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

  const selectedRows = selectedCells.map(cell => Math.floor((cell - 1) / cols));
  const selectedCols = selectedCells.map(cell => (cell - 1) % cols);
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
  if (selectedCells.value.length === 0) {
    selectedCells.value = originalCells.value;
  }
  if (validateGridPattern(selectedCells.value, props.gridSize)) {
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
  width: 100%;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
.cell {
  background-color: #f4f4f4;
  border: 1px solid #ccc;
  position: relative;
  cursor: pointer;
  aspect-ratio: 1;
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out;
  border-radius: 4px;
}
.cell.original {
  background-color: #4caf50;
}
.cell.selected {
  background-color: #bcd;
}
.cell.disabled {
  background-color: #ddd;
  cursor: not-allowed;
}
.tooltip {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.75);
  color: #fff;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 10;
}
</style>
