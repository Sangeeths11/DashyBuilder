<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">{{ name }}</h1>
    <ErrorMessageBox :message="errorMessage"/>
    <ComponentSelector @add-widget="handleAddWidget" class="mb-5"/>
    <DashboardArea :widgets="widgetStore.widgets" @delete-widget="handleDeleteWidget" />
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

watch(projectId, async (newId, oldId) => {
  if (newId !== oldId) {
    projectId.value = newId;
    const projectName = await projectStore.fetchProjectNameById(newId);
    if (projectName) {
      name.value = projectName;
    } else {
      name.value = 'Projekt nicht gefunden';
    }
  }
}, { immediate: true });

const handleAddWidget = async (widget) => {
  if (widgets.length >= 6) {
    errorMessage.value = 'You can only add up to 6 widgets.';
    return;
  }
  await widgetStore.createWidget(widget.type, widget.name, projectId.value);
};

const handleDeleteWidget = async (id) => {
  await widgetStore.deleteWidget(id);
};

async function downloadPythonFile() {
  try {
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(widgets.value)
    });

    if (!response.ok) throw new Error('Network response was not ok.');

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'dashboard.py');
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