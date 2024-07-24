<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">{{ name }}</h1>
    <SucessMessageBox :message="successMessage"/>
    <ErrorMessageBox :message="errorMessage"/>
    <div class="flex flex-wrap mb-5">
      <div class="w-full lg:w-1/2 px-2 h-full">
        <UploadDataset @uploaded="handleDatasetUploaded" class="mb-5"/>
        <!-- button who will open the DataExplorationModal -->
        <button @click="showDataExploration = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
          <Icon name="mdi:table" color="white" class="mr-1 text-2xl"/> Data Exploration
        </button>
      </div>
      <div class="w-full lg:w-1/2 px-2 h-full">
        <ComponentSelector @add-widget="handleAddWidget" @errorMessage="errorMessageModal" class="mb-5"/>
      </div>
    </div>
    <DashboardArea :widgets="widgetStore.widgets" :gridSize="gridSize" @delete-widget="handleDeleteWidget" @update-widget="handleUpdateWidget" />
    <button @click="downloadPythonFile" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
      <Icon name="mdi:download" color="white" class="mr-1 text-2xl"/> Download Python File
    </button>

    <!-- Data Exploration Modal -->
    <DataExplorationModal :show="showDataExploration" :datasetId="uploadedDatasetId" @close="showDataExploration = false"/>
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

const handleDatasetUploaded = (datasetId) => {
  uploadedDatasetId.value = datasetId;
  showDataExploration.value = true;
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
        grid_size: gridSize.value
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

onMounted(async () => {
  await widgetStore.fetchWidgetsByProjectId(projectId.value);
});
</script>
