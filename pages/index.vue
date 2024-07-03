<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <header class="bg-blue-500 text-white p-4 text-lg flex items-center">
      <div class="flex items-center">
        <span class="text-3xl mr-1"><Icon name="mdi:chart-box-outline" color="white" /></span>
        <span class="font-bold">Dashybuilder</span>
      </div>
    </header>
    <main class="flex-grow p-4">
      <ErrorMessageBox :message="errorMessage"/>
      <ComponentSelector @add-widget="handleAddWidget" class="mb-5"/>
      <DashboardArea :widgets="widgets" @delete-widget="handleDeleteWidget" />
      <button @click="downloadPythonFile" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center">
        <Icon name="mdi:download" color="white" class="mr-1 text-2xl"/> Download Python File
      </button>
    </main>
  </div>
</template>

<script setup>
const components = [
  { id: 1, name: 'Chart' },
  { id: 2, name: 'Table' },
  { id: 3, name: 'Text Block' }
];

const widgets = ref([]);
const errorMessage = ref('');

function handleAddWidget(componentId) {
  if (widgets.value.length >= 6) {
    errorMessage.value = 'You can only add up to 6 widgets.';
    return;
  }
  const component = components.find(c => c.id === componentId);
  widgets.value.push({
    id: widgets.value.length + 1,
    name: component.name,
    content: 'Content for ' + component.name,
    x: 0,
    y: 0,
    width: 100,
    height: 100
  });
}

function handleDeleteWidget(id) {
  widgets.value = widgets.value.filter(w => w.id !== id);
}

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
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error('Error downloading the python file:', error);
    errorMessage.value = error.message;
  }
}
</script>
