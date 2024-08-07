<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">{{ name }}</h1>
    <SucessMessageBox :message="successMessage"/>
    <ErrorMessageBox :message="errorMessage"/>
    <div class="flex flex-wrap mb-5">
      <div class="w-full lg:w-1/2 px-2 h-full">
        <UploadDataset 
          @uploaded="handleDatasetUploaded" 
          @loading="loadingData = $event" 
          class="mb-5"
          :projectId="projectId"
        />
      </div>
      <div class="w-full lg:w-1/2 px-2 h-full">
        <ComponentSelector @add-widget="handleAddWidget" @errorMessage="errorMessageModal" class="mb-5"/>
      </div>
    </div>
    <DashboardArea 
      :widgets="widgetStore.widgets" 
      :gridSize="gridSize"
      :uploadedDatasetId="uploadedDatasetId" 
      @delete-widget="handleDeleteWidget" 
      @update-widget="handleUpdateWidget" 
    />
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
const uploadedDatasetId = ref(null);
const loadingData = ref(false);

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
    } else {
      errorMessage.value = 'Fehler beim Laden der Daten.';
    }
  } catch (error) {
    errorMessage.value = 'Fehler beim Laden der Daten: ' + error.message;
  } finally {
    loadingData.value = false;
  }
};

onMounted(async () => {
  await widgetStore.fetchWidgetsByProjectId(projectId.value);
  uploadedDatasetId.value = await projectStore.fetchProjectFilePath(projectId.value);
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