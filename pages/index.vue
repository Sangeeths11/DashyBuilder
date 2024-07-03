<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <header class="bg-blue-500 text-white p-4 text-lg flex justify-between items-center">
      <span>Dashboard Designer Tool</span>
      <span class="text-2xl"><Icon name="mdi:chart-box-outline" color="black" /></span>
    </header>
    <main class="flex-grow p-4">
      <ComponentSelector @add-widget="handleAddWidget" class="mb-5"/>
      <DashboardArea :widgets="widgets" @delete-widget="handleDeleteWidget" />
    </main>
  </div>
</template>

<script setup>
const widgets = ref([]);


function handleAddWidget(componentId) {

  if (!componentId) {
    return;
  }
  else if (widgets.value.length >= 6) {
    alert('You can only have 6 widgets in the dashboard');
    return;
  }
  const newWidget = {
    id: widgets.value.length + 1,
    name: 'Widget ' + componentId,
    content: 'Content for ' + componentId
  };
  widgets.value.push(newWidget);
}

function handleDeleteWidget(id) {
  widgets.value = widgets.value.filter(w => w.id !== id);
}
</script>
