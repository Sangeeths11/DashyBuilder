<template>
  <ErrorMessageBox :message="errorMessage"/>
  <SucessMessageBox :message="successMessage"/>
  <div class="bg-white shadow-lg rounded-lg p-4 relative">
    <h2 class="font-bold text-lg mb-4">Dashboard</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <Widget
        v-for="widget in widgets"
        :key="widget.id"
        :widget="widget"
        :gridSize="gridSize"
        @delete-widget="emitDeleteWidget"
        @update-widget="emitUpdateWidget"
      />
    </div>
    <button v-if="uploadedDatasetId" @click="showAISuggestion = true" class="absolute top-4 right-28 bg-purple-600 hover:bg-purple-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
      <Icon name="mdi:robot" color="white" class="text-2xl"/>
    </button>
    <button @click="downloadPythonFile" class="absolute top-4 right-16 bg-blue-600 hover:bg-blue-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
        <Icon name="mdi:download" color="white" class="text-2xl"/>
    </button>
    <button @click="hostDashboard" class="absolute top-4 right-4 bg-green-600 hover:bg-green-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
        <Icon name="mdi:cloud-upload" color="white" class="text-2xl"/>
    </button>
    <HostingModal :show="showHostingModal" :url="hostedUrl" @close="showHostingModal = false"/>
    <AISuggestionModal :show="showAISuggestion" @close="showAISuggestion = false" :uploadedDatasetId="uploadedDatasetId" :researchQuestion="researchQuestion" :projectId="projectId"/>
    <div v-if="loadingDashboard" class="fixed inset-0 bg-gray-100 bg-opacity-75 flex items-center justify-center">
      <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  widgets: Array,
  gridSize: String,
  uploadedDatasetId: String,
  projectId: String,
});

const errorMessage = ref('');
const successMessage = ref('');
const loadingDashboard = ref(false);
const researchQuestion = ref('');
const projectStore = useProjectStore();

researchQuestion.value = await projectStore.fetchProjectResearchQuestionById(props.projectId);
console.log('Research question:', researchQuestion.value);

watch(() => props.widgets, () => {
  console.log('Widgets changed');
  console.log(props.widgets);
  console.log('Project ID:', props.projectId);
  
});
const hostedUrl = ref('');
const showHostingModal = ref(false);
const showAISuggestion = ref(false); // Hinzugefügt
const emit = defineEmits(['delete-widget', 'update-widget']);
const widgetStore = useWidgetStore();

async function hostDashboard() {
  const invalidWidgets = widgetStore.widgets.filter(widget => !widget.gridPosition || !widget.gridPosition.gridPosition);

  if (invalidWidgets.length > 0) {
    errorMessage.value = 'Please set the grid position for all widgets before hosting the dashboard.';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
    return;
  }
  console.log('Host dashboard');
  loadingDashboard.value = true;
  
  console.log('Exporting dashboard', widgetStore.widgets, props.gridSize);
  try {
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        widgets: widgetStore.widgets,
        grid_size: props.gridSize,
        save: true,
      })
    });

    if (!response.ok) throw new Error('Network response was not ok.');
  } catch (error) {
    console.error('Error exporting the dashboard:', error);
    errorMessage.value = error.message;
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  } finally {
    try {
      const response = await fetch('http://localhost:5000/upload_to_pythonanywhere', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          file_path: 'dashboards\\Dashboard.py'
        })
      });
      if (!response.ok) throw new Error('Network response was not ok.');
      const result = await response.json();
      hostedUrl.value = result.stdout;
      showHostingModal.value = true;
      successMessage.value = 'Dashboard hosted successfully';
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } catch (error) {
      console.error('Error hosting the dashboard:', error);
      errorMessage.value = error.message;
      setTimeout(() => {
        errorMessage.value = '';
      }, 3000);
    }
    loadingDashboard.value = false;
  }
}

async function downloadPythonFile() {
  const invalidWidgets = widgetStore.widgets.filter(widget => !widget.gridPosition || !widget.gridPosition.gridPosition);
  
  if (invalidWidgets.length > 0) {
    errorMessage.value = 'Please set the grid position for all widgets before downloading the python file.';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
    return;
  }
  console.log('Download python file');
  console.log('Exporting dashboard', widgetStore.widgets, props.gridSize);
  try {
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        widgets: widgetStore.widgets,
        grid_size: props.gridSize,
        save: false,
      })
    });

    if (!response.ok) throw new Error('Network response was not ok.');

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'dashboard.py');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    successMessage.value = 'Python file downloaded successfully';
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error downloading the python file:', error);
    errorMessage.value = error.message;
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  }
}

function emitDeleteWidget(id) {
  emit('delete-widget', id);
}

function emitUpdateWidget(data) {
  emit('update-widget', data);
}
</script>

<style scoped>
.loader {
  border-top-color: #3498db;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
