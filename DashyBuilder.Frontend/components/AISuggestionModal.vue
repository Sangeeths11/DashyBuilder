<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-1/2 relative">
      <ErrorMessageBox :message="errorMessage"/>
      <SucessMessageBox :message="successMessage"/>
      <h2 class="text-3xl font-bold mb-4 text-gray-800">AI Suggestions</h2>
      <div>
        <div class="p-4 bg-gray-100 rounded-lg mb-6">
          <h3 class="text-lg font-semibold text-gray-700">Research Question:</h3>
          <p class="text-gray-600">{{ researchQuestion }}</p>
        </div>
      </div>
      
      <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-50">
        <div class="flex flex-col items-center">
          <div class="loader"></div>
          <p class="ml-4 text-gray-700 font-semibold mt-4">AI is generating the best 4 widgets for you...</p>
        </div>
      </div>
      
      <div v-else>
        <div v-if="error" class="text-red-500 font-bold">
          <p>{{ error }}</p>
          <button 
              @click="$emit('close')" 
              class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out float-right"
            >
              Close
            </button>
        </div>
        
        <div v-else-if="parsedResult.error" class="text-red-500 font-bold">
          <p>{{ parsedResult.error }}</p>
          <button 
              @click="$emit('close')" 
              class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out float-right"
            >
              Close
            </button>
        </div>
        
        <div v-else>
          <h3 class="font-semibold mb-2 text-gray-800">Select Widgets to Include:</h3>
          <ul class="space-y-2">
            <li v-for="(widget, index) in parsedResult.widgets" :key="index" class="flex items-center">
              <input 
                type="checkbox" 
                v-model="selectedWidgets" 
                :value="widget" 
                :disabled="isWidgetSaved(widget)"
                class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label :class="{ 'line-through text-gray-400': isWidgetSaved(widget) }">
                {{ widget.widgetType }}: {{ widget.widgetName }}
              </label>
            </li>
          </ul>
          
          <div class="mt-6 flex justify-end space-x-4">
            <button 
              @click="applyWidgets" 
              class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"
            >
              Apply Widgets
            </button>
            <button 
              @click="$emit('close')" 
              class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close']);

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  uploadedDatasetId: String,
  researchQuestion: String,
  projectId: String
});

const loading = ref(false);
const error = ref(null);
const columnInfo = ref([]);
const previewData = ref([]);
const aiResult = ref({});
const selectedWidgets = ref([]);
const savedWidgets = ref([]);
const widgetStore = useWidgetStore();
const parsedResult = ref({});
const errorMessage = ref('');
const successMessage = ref(''); 

watch(() => props.show, async (newValue) => {
  if (newValue && props.uploadedDatasetId) {
    if (Object.keys(parsedResult.value).length === 0) {
      // Falls kein Ergebnis vorhanden ist, mache die API-Aufrufe
      await fetchDatasetInfo();
      await callOpenAI();
    }
    selectedWidgets.value = [];
    updateSavedWidgets();
  }
});

async function callOpenAI() {
    loading.value = true; // Ladezustand starten
    try {
      const response = await fetch('http://localhost:5000/ai/openai-process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          column_info: columnInfo.value,
          preview_data: previewData.value,
          research_question: props.researchQuestion
        })
      });

      if (!response.ok) {
        errorMessage.value = 'Failed to fetch AI suggestions';
      }

      const result = await response.json();
      aiResult.value = result;
      parsedResult.value = JSON.parse(aiResult.value.result);
    } catch (err) {
      errorMessage.value = err;
    } finally {
      loading.value = false; // Ladezustand beenden
    }
}

async function fetchDatasetInfo() {
  loading.value = true;
  error.value = null;
  errorMessage.value = null;

  try {
    const response = await fetch(`http://localhost:5000/ai/${props.uploadedDatasetId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch dataset info');
    }

    const data = await response.json();
    columnInfo.value = data.column_info || [];
    previewData.value = data.preview_data || [];
  } catch (err) {
    error.value = `Error: ${err.message}`;
    errorMessage.value = err;
  } finally {
    loading.value = false;
  }
}

async function applyWidgets() {
  try {
    for (const widget of selectedWidgets.value) {
      await widgetStore.createWidget(widget.widgetType, widget.widgetName, props.projectId, widget.chartType, widget.filterTypes);
      savedWidgets.value.push(widget);
    }
    successMessage.value = 'Widgets successfully saved';
    closeModal();
  } catch (err) {
    errorMessage.value = err;
  }
}

function closeModal() {
  selectedWidgets.value = [];
  emit('close');
}

function updateSavedWidgets() {
  savedWidgets.value = widgetStore.widgets;
}

function isWidgetSaved(widget) {
  savedWidgets.value = widgetStore.widgets;
  return savedWidgets.value.some(saved => saved.name === widget.widgetName);
}
</script>

<style scoped>
.loader {
  border: 8px solid #f3f3f3;
  border-top: 8px solid #3498db;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
