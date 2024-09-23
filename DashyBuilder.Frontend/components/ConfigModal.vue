<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-90 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-lg w-[700px] h-[700px] relative flex flex-col">
      <!-- Fixed size of the modal -->
      <button @click="close" class="absolute top-3 right-3 text-gray-600 hover:text-gray-900">
        &times;
      </button>
      <ErrorMessageBox :message="errorMessage" />
      <h3 class="text-lg font-bold mb-4 text-center">Configure Widget Position</h3>
      <p class="text-sm text-gray-600 mb-4 text-center">
        Please select the position for the widget:
        <strong class="text-sm text-gray-600 mb-2">
          {{ widget.name }} ({{ widget.type }})
        </strong>
      </p>

      <div
        :style="gridStyle"
        class="grid-container flex-grow"
        @mousedown="startSelection"
        @mousemove="throttledMoveSelection"
        @mouseup="endSelection"
        @mouseleave="endSelection"
      >
        <div
          v-for="cell in totalCells"
          :key="cell"
          :data-index="cell"
          :class="[
            'cell',
            isSelected(cell) ? 'selected' : '',
            isOriginal(cell) ? 'original' : '',
            isDisabled(cell) ? 'disabled' : '',
            isReserved(cell) ? 'reserved' : '',
          ]"
          :style="getCellStyle(cell)"
          @mouseenter="updateTooltipText(cell)"
          @mouseleave="hoverCell(null)"
        >
          <span v-if="hoveredCell === cell" class="tooltip">{{ tooltipText }}</span>
        </div>
      </div>
      <div class="mt-4 flex justify-center">
        <!-- Centered button -->
        <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Save
        </button>
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
  projectId: Number,
});

const widgetStore = useWidgetStore();
const { fetchReservedPositions, getWidgetByGridPosition } = widgetStore;

const reservedPositions = ref([]);
const errorMessage = ref('');
const hoveredCell = ref(null);
const tooltipText = ref('');
const reservedGroups = ref({});

const originalCells = ref([]);

try {
  if (props.widget.gridPosition && typeof props.widget.gridPosition.gridPosition === 'string') {
    originalCells.value = props.widget.gridPosition.gridPosition
      .split(',')
      .map(Number)
      .filter((num) => !isNaN(num));
  } else {
    originalCells.value = [];
  }
} catch (e) {
  errorMessage.value = 'Invalid gridPosition data.';
  setTimeout(() => {
    errorMessage.value = '';
  }, 3000);
  originalCells.value = [];
}

const selectedCells = ref([...originalCells.value]);

onMounted(async () => {
  const positions = await fetchReservedPositions(props.widget.project_id);
  reservedPositions.value = positions.filter((pos) => !originalCells.value.includes(pos));
  reservedGroups.value = await groupReservedPositions(reservedPositions.value);
});

const emit = defineEmits(['close', 'save']);

const [cols, rows] = props.gridSize.split('x').map(Number);

const totalCells = computed(() => rows * cols);

const cellSize = computed(() => {
  const maxModalSize = 450;
  const maxGridDimension = Math.max(cols, rows);
  return Math.floor(maxModalSize / maxGridDimension);
});

function isReserved(cell) {
  return Object.values(reservedGroups.value).some((group) => group.cells.includes(cell));
}

function getCellStyle(cell) {
  for (const group of Object.values(reservedGroups.value)) {
    if (group.cells.includes(cell)) {
      return {
        border: `2px solid ${group.color}`,
      };
    }
  }
  return {};
}

const gridStyle = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(${cols}, ${cellSize.value}px)`,
  gridTemplateRows: `repeat(${rows}, ${cellSize.value}px)`,
  gap: '4px',
  justifyContent: 'center',
  alignContent: 'center',
}));

const isSelecting = ref(false);
const startCell = ref(null);

function startSelection(event) {
  const cell = getCellFromEvent(event);
  if (cell && !isDisabled(cell)) {
    isSelecting.value = true;
    startCell.value = cell;
    selectRange(cell, cell);
  }
}

function moveSelection(event) {
  if (!isSelecting.value) return;
  const cell = getCellFromEvent(event);
  if (cell && !isDisabled(cell)) {
    selectRange(startCell.value, cell);
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
    return Number(cellElement.dataset.index);
  }
  return null;
}

function selectRange(start, end) {
  const startRow = Math.floor((start - 1) / cols);
  const startCol = (start - 1) % cols;
  const endRow = Math.floor((end - 1) / cols);
  const endCol = (end - 1) % cols;

  const minRow = Math.min(startRow, endRow);
  const maxRow = Math.max(startRow, endRow);
  const minCol = Math.min(startCol, endCol);
  const maxCol = Math.max(startCol, endCol);

  const newSelectedCells = [];

  for (let row = minRow; row <= maxRow; row++) {
    for (let col = minCol; col <= maxCol; col++) {
      const cell = row * cols + col + 1;
      if (!isDisabled(cell)) {
        newSelectedCells.push(cell);
      }
    }
  }

  selectedCells.value = newSelectedCells;
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
  hoveredCell.value = cell;
}

async function updateTooltipText(cell) {
  hoverCell(cell);
  if (isOriginal(cell)) {
    tooltipText.value = `Original Widget Position: ${cell}`;
  } else if (isDisabled(cell)) {
    const widgetTooltip = await getCachedWidgetByGridPosition(cell, props.widget.project_id);
    tooltipText.value = widgetTooltip
      ? `Reserved Cell: ${cell} (${widgetTooltip.name})`
      : `Reserved Cell: ${cell} (Unknown Widget)`;
  } else {
    hoverCell(null);
  }
}

function validateGridPattern(selectedCells, gridSize) {
  selectedCells = selectedCells.filter((cell) => cell !== 0);
  const [cols, rows] = gridSize.split('x').map(Number);
  const grid = Array.from({ length: rows }, () => Array(cols).fill(false));

  selectedCells.forEach((cell) => {
    const row = Math.floor((cell - 1) / cols);
    const col = (cell - 1) % cols;
    grid[row][col] = true;
  });

  function dfs(row, col, visited) {
    if (
      row < 0 ||
      row >= rows ||
      col < 0 ||
      col >= cols ||
      !grid[row][col] ||
      visited.has(`${row},${col}`)
    ) {
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

  const selectedRows = selectedCells.map((cell) => Math.floor((cell - 1) / cols));
  const selectedCols = selectedCells.map((cell) => (cell - 1) % cols);
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

const borderColors = ['blue', 'purple', 'orange', 'teal', 'pink', 'brown', 'cyan', 'magenta'];

const widgetCache = new Map();

async function getCachedWidgetByGridPosition(cell, projectId) {
  const cacheKey = `${projectId}-${cell}`;
  if (widgetCache.has(cacheKey)) {
    return widgetCache.get(cacheKey);
  }

  const widget = await getWidgetByGridPosition(cell, projectId);
  widgetCache.set(cacheKey, widget);
  return widget;
}

async function groupReservedPositions(positions) {
  const groups = {};
  let colorIndex = 0;

  const widgetPromises = positions.map((cell) => getCachedWidgetByGridPosition(cell, props.widget.project_id));
  const widgets = await Promise.all(widgetPromises);

  widgets.forEach((widget, index) => {
    const cell = positions[index];
    if (widget) {
      const widgetId = widget.name + widget.type;
      if (!groups[widgetId]) {
        groups[widgetId] = {
          cells: [],
          color: borderColors[colorIndex % borderColors.length],
        };
        colorIndex++;
      }
      groups[widgetId].cells.push(cell);
    }
  });

  return groups;
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
.cell.reserved {
  border-width: 2px;
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
