<template>
  <ErrorMessageBox :message="errorMessage"/>
  <SucessMessageBox :message="successMessage"/>
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
    <button v-if="uploadedDatasetId" @click="showAISuggestion = true" class="absolute top-4 right-16 bg-purple-600 hover:bg-purple-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
      <Icon name="mdi:robot" color="white" class="text-2xl"/>
    </button>
    <button @click="hostDashboard" class="absolute top-4 right-4 bg-green-600 hover:bg-green-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
        <Icon name="mdi:cloud-upload" color="white" class="text-2xl"/>
    </button>
    <HostingModal :show="showHostingModal" :url="hostedUrl" @close="showHostingModal = false"/>
    <AISuggestionModal :show="showAISuggestion" @close="showAISuggestion = false"/>
  </div>
</template>

<script setup>
const props = defineProps({
  widgets: Array,
  gridSize: String,
  uploadedDatasetId: String
});

const errorMessage = ref('');
const successMessage = ref('');
const loadingDashboard = ref(false);

watch(() => props.widgets, () => {
  console.log('Widgets changed');
  console.log(props.widgets);
});

watch(() => props.gridSize, () => {
  console.log('Grid size changed');
  console.log(props.gridSize);
});

watch(() => props.uploadedDatasetId, () => {
  console.log('Uploaded dataset ID changed');
  console.log(props.uploadedDatasetId);
});

const hostedUrl = ref('');
const showHostingModal = ref(false);
const showAISuggestion = ref(false); // Hinzugefügt
const emit = defineEmits(['delete-widget', 'update-widget']);
const widgetStore = useWidgetStore();

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
  loadingDashboard.value = true;
  
  console.log('Exporting dashboard', widgetStore.widgets, props.gridSize);
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

function emitDeleteWidget(id) {
  emit('delete-widget', id);
}

function emitUpdateWidget(data) {
  emit('update-widget', data);
}
</script>

<style scoped>
</style>
