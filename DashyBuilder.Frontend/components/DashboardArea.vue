<template>
  <ErrorMessageBox :message="errorMessage" />
  <SucessMessageBox :message="successMessage" />
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
    <div class="absolute top-4 right-4 flex space-x-4">
      <div class="relative group">
        <button v-if="uploadedDatasetId" @click="showAISuggestion = true" class="bg-purple-600 hover:bg-purple-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
          <Icon name="mdi:robot" color="white" class="text-2xl" />
        </button>
        <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2">
          AI Suggestions
        </div>
      </div>

      <div class="relative group">
        <button @click="downloadPythonFile" class="bg-blue-600 hover:bg-blue-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
          <Icon name="mdi:download" color="white" class="text-2xl" />
        </button>
        <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2">
          Download Python File
        </div>
      </div>

      <div class="relative group">
        <button @click="hostDashboard" class="bg-green-600 hover:bg-green-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
          <Icon name="mdi:cloud-upload" color="white" class="text-2xl" />
        </button>
        <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2">
          Host Dashboard
        </div>
      </div>

      <div class="relative group">
        <button @click="toggleCodeViewer" class="bg-gray-600 hover:bg-gray-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
          <Icon name="mdi:code-braces" color="white" class="text-2xl" />
        </button>
        <div class="absolute bottom-full mb-2 hidden group-hover:block bg-gray-700 text-white text-xs rounded py-1 px-2">
          Code Viewer
        </div>
      </div>
    </div>
    <HostingModal :show="showHostingModal" :url="hostedUrl" @close="showHostingModal = false" />
    <AISuggestionModal :show="showAISuggestion" @close="showAISuggestion = false" :uploadedDatasetId="uploadedDatasetId" :researchQuestion="researchQuestion" :projectId="projectId" />
    <div v-if="loadingDashboard" class="fixed inset-0 bg-gray-100 bg-opacity-75 flex items-center justify-center">
      <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"></div>
    </div>

    <!-- Code Viewer Slider -->
    <div :class="['fixed inset-y-0 right-0 transform transition-transform duration-300', showCodeViewer ? 'translate-x-0' : 'translate-x-full']" class="w-1/2 bg-white shadow-lg z-50 flex flex-col">
      <!-- Close Button -->
      <button @click="toggleCodeViewer" class="absolute top-4 right-4 text-gray-500 hover:text-gray-800">
        <Icon name="mdi:close" class="text-2xl" />
      </button>
      <h2 class="font-bold text-lg mb-4 mt-10 mx-4">Code Viewer</h2>
      <ClientOnly>
        <div class="flex-grow p-4 overflow-hidden">
          <MonacoEditor v-model="val" :lang="lang" :options="options" class="w-full h-full editor">
            Loading...
          </MonacoEditor>
        </div>
      </ClientOnly>
    </div>
  </div>
</template>

<script setup>
const lang = ref('python');

const options = {
  automaticLayout: true
};

const val = ref(''); // Startet leer, wird beim Öffnen des Editors geladen

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
const showCodeViewer = ref(false);

researchQuestion.value = await projectStore.fetchProjectResearchQuestionById(props.projectId);

const hostedUrl = ref('');
const showHostingModal = ref(false);
const showAISuggestion = ref(false);
const emit = defineEmits(['delete-widget', 'update-widget']);
const widgetStore = useWidgetStore();

async function fetchDashboardCode() {
  try {
    const file_path = await projectStore.getFileName(props.projectId);
    if (file_path === null) {
      errorMessage.value = "Please upload a dataset before seeing the code.";
      showCodeViewer.value = false;
      setTimeout(() => {
        errorMessage.value = '';
      }, 3000);
      return;
    }
    
    const response = await fetch('http://localhost:5000/exportCode', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        widgets: widgetStore.widgets,
        grid_size: props.gridSize,
        file_path: file_path,
        save: false, // Nicht speichern, nur abrufen
      })
    });

    if (!response.ok) throw new Error('Network response was not ok.');

    const code = await response.text();
    val.value = code; // Lade den Code in den Editor
  } catch (error) {
    errorMessage.value = "Please set the grid position for all widgets before seeing the code.";
    showCodeViewer.value = false;
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  }
}

function toggleCodeViewer() {
  if (!showCodeViewer.value) {
    // Lade den Code, wenn der Slider geöffnet wird
    fetchDashboardCode();
  }
  showCodeViewer.value = !showCodeViewer.value;
}

async function hostDashboard() {
  const invalidWidgets = widgetStore.widgets.filter(widget => !widget.gridPosition || !widget.gridPosition.gridPosition);

  if (invalidWidgets.length > 0) {
    errorMessage.value = 'Please set the grid position for all widgets before hosting the dashboard.';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
    return;
  }
  loadingDashboard.value = true;

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
      hostedUrl.value = result.url;
      showHostingModal.value = true;
      successMessage.value = 'Dashboard hosted successfully';
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } catch (error) {
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
  try {
    const file_path = await projectStore.getFileName(props.projectId);
    if (file_path === null) {
      errorMessage.value = "Please upload a dataset before seeing the code.";
      showCodeViewer.value = false;
      setTimeout(() => {
        errorMessage.value = '';
      }, 3000);
      return;
    }
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        widgets: widgetStore.widgets,
        grid_size: props.gridSize,
        file_path: file_path,
        save: false,
      })
    });

    if (!response.ok) throw new Error('Network response was not ok.');

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'dashboard_export.zip'); // Updated filename to 'dashboard_export.zip'
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    successMessage.value = 'ZIP file downloaded successfully';
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
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

.container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  max-width: 960px;
  height: 100%;
  margin: 0 auto;
  padding: 24px;
}

.editor {
  width: 100%;
  height: 100%;
}

.fixed {
  z-index: 9999;
}
</style>
