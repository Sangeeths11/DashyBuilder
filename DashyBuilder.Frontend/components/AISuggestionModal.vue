<template>
  <div v-if="show" class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg p-6 w-1/2">
      <h2 class="text-2xl font-bold mb-4">AI Suggestions</h2>
      <p class="mb-4">Research question: {{ researchQuestion }}</p>
      <div v-if="loading">Loading data...</div>
      <div v-else>
        <div v-if="error">{{ error }}</div>
        <div v-else>
          <h3 class="font-semibold mb-2">AI Result</h3>
          <pre>{{ aiResult }}</pre>
        </div>
      </div>
      <button @click="$emit('close')" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-4">
        Close
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  uploadedDatasetId: String,
  researchQuestion: String
});

const loading = ref(false);
const error = ref(null);
const columnInfo = ref([]);
const previewData = ref([]);
const aiResult = ref('')

watch(() => props.show, async (newValue) => {
  if (newValue && props.uploadedDatasetId) {
    // Modal wurde geöffnet und DatasetId ist verfügbar
    await fetchDatasetInfo();
    await callOpenAI();
  }
});

async function callOpenAI() {
  if(!aiResult.value) {
    try {
      const response = await fetch('http://localhost:5000/ai/openai-process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          column_info: columnInfo.value,
          preview_data: previewData.value,
          research_question: props.researchQuestion
        })
      });

      if (!response.ok) {
        throw new Error('Failed to call OpenAI API');
      }

      const result = await response.json();
      aiResult.value = result.result;
    } catch (err) {
      error.value = `Error: ${err.message}`;
    }
  }
}

async function fetchDatasetInfo() {
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch(`http://localhost:5000/ai/${props.uploadedDatasetId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch dataset info');
    }

    const data = await response.json();
    columnInfo.value = data.column_info || [];
    previewData.value = data.preview_data || [];
  } catch (err) {
    error.value = `Error: ${err.message}`;
  } finally {
    loading.value = false;
  }
  console.log('Column info:', columnInfo.value);
  console.log('Preview data:', previewData.value);
}
</script>

<style scoped>
/* Optional: Style-Anpassungen für das Modal */
</style>
