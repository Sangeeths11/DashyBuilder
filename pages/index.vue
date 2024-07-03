<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <header class="bg-blue-500 text-white p-4 text-lg flex items-center">
      <div class="flex items-center">
        <span class="text-3xl mr-1"><Icon name="mdi:chart-box-outline" color="white" /></span>
        <span class="font-bold">Dashybuilder</span>
      </div>
    </header>
    <main class="flex-grow p-4">
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

function handleAddWidget(componentId) {
  if (widgets.value.length >= 6) {
    alert('You can only have 6 widgets in the dashboard');
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

async function exportLayout() {
  console.log(widgets.value);
  try {
    const response = await fetch('http://localhost:5000/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(widgets.value)
    });
    const data = await response.json();
    console.log(data);
    alert('Dashboard exported successfully!');
  } catch (error) {
    console.error('Error exporting the dashboard:', error);
    alert('Failed to export dashboard.');
  }
}
const downloadPythonFile = async () => {
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
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading the python file:', error);
    alert('Failed to download python file.');
  }
};
</script>
