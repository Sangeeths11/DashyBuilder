<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">{{ name }}</h1>
    <SucessMessageBox :message="successMessage"/>
    <ErrorMessageBox :message="errorMessage"/>
    <div class="flex flex-wrap mb-5">
      <div class="w-full lg:w-1/2 px-2 h-full">
        <UploadDataset @uploaded="handleDatasetUploaded" @loading="loadingData = $event" class="mb-5"/>
        <button v-if="uploadedDatasetId && !loadingData" @click="showDataExploration = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
          <Icon name="mdi:table" color="white" class="mr-1 text-2xl"/> Data Exploration
        </button>
      </div>
      <div class="w-full lg:w-1/2 px-2 h-full">
        <ComponentSelector @add-widget="handleAddWidget" @errorMessage="errorMessageModal" class="mb-5"/>
      </div>
    </div>
    <DashboardArea :widgets="widgetStore.widgets" :gridSize="gridSize" @delete-widget="handleDeleteWidget" @update-widget="handleUpdateWidget" />
    <div class="flex justify-between mt-4">
      <button @click="downloadPythonFile" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
        <Icon name="mdi:download" color="white" class="mr-1 text-2xl"/> Download Python File
      </button>
      <button @click="hostDashboard" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
        <Icon name="mdi:cloud-upload" color="white" class="mr-1 text-2xl"/> Host Dashboard
      </button>
    </div>
    <div v-if="loadingDashboard" class="fixed inset-0 bg-gray-100 bg-opacity-75 flex items-center justify-center">
      <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"></div>
    </div>
    <DataExplorationModal :show="showDataExploration" :datasetId="uploadedDatasetId" @close="showDataExploration = false"/>
    <HostingModal :show="showHostingModal" :url="hostedUrl" @close="showHostingModal = false"/>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'DashyBuilder - Home',
  layout: 'main',
  middleware: ['auth-index'],
});

const route = useRoute();
const projectId = ref(route.params.id);
const name = ref('');
const projectStore = useProjectStore();
const widgetStore = useWidgetStore();
const errorMessage = ref('');
const successMessage = ref('');
const gridSize = ref('');
const showDataExploration = ref(false);
const uploadedDatasetId = ref(null);
const showHostingModal = ref(false);
const hostedUrl = ref('');
const loadingData = ref(false);
const loadingDashboard = ref(false);

watch(projectId, async (newId, oldId) => {
  if (newId !== oldId) {
    projectId.value = newId;
    const projectName = await projectStore.fetchProjectNameById(newId);
    if (projectName) {
      name.value = projectName;
      gridSize.value = await projectStore.fetchProjectGridSizeById(newId);
      console.log('Grid size:', gridSize.value);
    } else {
      name.value = 'Projekt nicht gefunden';
    }
  }
}, { immediate: true });

const handleAddWidget = async (widget) => {
  const gridSizeArray = gridSize.value.split('x');
  const gridSizeValue = parseInt(gridSizeArray[0]) * parseInt(gridSizeArray[1]);
  console.log('Grid size:', gridSizeValue);
  if (widgetStore.widgets.length >= gridSizeValue) {
    errorMessage.value = `You can only add up to ${gridSizeValue} widgets.`;
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
    return;
  }
  await widgetStore.createWidget(widget.type, widget.name, projectId.value);
  successMessage.value = 'Widget added successfully';
  setTimeout(() => {
    successMessage.value = '';
  }, 3000);
};

const errorMessageModal = (message) => {
  errorMessage.value = message;
  setTimeout(() => {
    errorMessage.value = '';
    }, 3000);
};

const handleDeleteWidget = async (id) => {
  await widgetStore.deleteWidget(id);
  successMessage.value = 'Widget deleted successfully';
  setTimeout(() => {
    successMessage.value = '';
  }, 3000);
};

const handleUpdateWidget = async ({ id, gridPosition }) => {
  await widgetStore.updateWidget(id, { gridPosition });
  successMessage.value = 'Grid position updated successfully';
  setTimeout(() => {
    successMessage.value = '';
  }, 3000);
};

const handleDatasetUploaded = async (datasetId) => {
  uploadedDatasetId.value = datasetId;
  loadingData.value = true;  // Daten werden geladen

  try {
    const response = await fetch(`http://localhost:5000/data/${datasetId}`);
    if (response.ok) {
      showDataExploration.value = true;
    } else {
      errorMessage.value = 'Fehler beim Laden der Daten.';
    }
  } catch (error) {
    errorMessage.value = 'Fehler beim Laden der Daten: ' + error.message;
  } finally {
    loadingData.value = false;
  }
};

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
  console.log(widgetStore.widgets);
  console.log(gridSize.value);
  try {
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        widgets: widgetStore.widgets,
        grid_size: gridSize.value,
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
  console.log(widgetStore.widgets);
  console.log(gridSize.value);
  
  loadingDashboard.value = true;
  
  try {
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        widgets: widgetStore.widgets,
        grid_size: gridSize.value,
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

onMounted(async () => {
  await widgetStore.fetchWidgetsByProjectId(projectId.value);
});
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