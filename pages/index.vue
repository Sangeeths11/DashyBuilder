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
  if (!componentId) {
    return;
  } else if (widgets.value.length >= 6) {
    alert('You can only have 6 widgets in the dashboard');
    return;
  }
  
  const componentName = components.find(c => c.id === componentId)?.name || 'Unknown Component';
  const newWidget = {
    id: widgets.value.length + 1,
    name: componentName,
    content: 'Content for ' + componentName
  };
  widgets.value.push(newWidget);
}

function handleDeleteWidget(id) {
  widgets.value = widgets.value.filter(w => w.id !== id);
}
</script>
