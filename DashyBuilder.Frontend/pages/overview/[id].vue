<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">{{ name }}</h1>
    <ErrorMessageBox :message="errorMessage"/>
    <ComponentSelector @add-widget="handleAddWidget" @errorMessage="errorMessageModal" class="mb-5"/>
    <DashboardArea :widgets="widgetStore.widgets" :gridSize="gridSize" @delete-widget="handleDeleteWidget"  @update-widget="handleUpdateWidget" />
    <button @click="downloadPythonFile" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
      <Icon name="mdi:download" color="white" class="mr-1 text-2xl"/> Download Python File
    </button>
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
const gridSize = ref('');

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
  if (widgetStore.widgets.length >= 6) {
    errorMessage.value = 'You can only add up to 6 widgets.';
    return;
  }
  await widgetStore.createWidget(widget.type, widget.name, projectId.value);
};

const errorMessageModal = (message) => {
  errorMessage.value = message;
};

const handleDeleteWidget = async (id) => {
  await widgetStore.deleteWidget(id);
};

const handleUpdateWidget = async ({ id, gridPosition }) => {
  await widgetStore.updateWidget(id, { gridPosition });
};

async function downloadPythonFile() {
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
  } catch (error) {
    console.error('Error downloading the python file:', error);
    errorMessage.value = error.message;
  }
}

onMounted(async () => {
  await widgetStore.fetchWidgetsByProjectId(projectId.value);
});
</script>