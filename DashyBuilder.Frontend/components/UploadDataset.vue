<template>
  <div class="w-full h-full flex flex-col justify-between">
    <SucessMessageBox :message="successMessage"/>
    <ErrorMessageBox :message="errorMessage"/>
    <div class="bg-white shadow-lg rounded-lg p-4 h-full flex flex-col relative">
      <h2 class="font-bold text-lg mb-4">Upload Dataset</h2>
      <div class="flex flex-col items-center flex-grow w-full">
        <label for="file-upload" class="w-full flex flex-col items-center justify-center px-4 py-20 bg-gray-100 text-blue rounded-lg shadow-lg tracking-wide uppercase border border-gray-200 cursor-pointer hover:bg-blue-500 hover:text-white transition duration-300 ease-in-out mb-6">
          <svg class="w-16 h-16" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M16.88 5.5a2 2 0 01.12 0h1a2 2 0 011.72 1.05 2 2 0 01.28.96v7a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h1.1a2 2 0 01.12 0H5a.5.5 0 000 1h10a.5.5 0 000-1h-.12zM9 8a.5.5 0 000 1h2a.5.5 0 000-1H9z"/>
          </svg>
          <span class="mt-3 text-lg font-semibold leading-normal">SELECT A FILE</span>
          <span class="text-sm leading-normal mt-1">File must be in CSV format</span>
          <input id="file-upload" type="file" class="hidden" @change="handleFileUpload"/>
        </label>
        <div class="w-full mt-auto">
          <button
            @click="uploadDataset"
            :disabled="!selectedFile || isLoading"
            class="w-full bg-blue-500 hover:bg-blue-800 text-white font-bold py-3 px-4 rounded flex items-center justify-center transition duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed h-14">
            <Icon name="mdi:upload" color="white" class="mr-2 text-3xl"/>
            <span v-if="isLoading">Uploading...</span>
            <span v-else>Upload Dataset</span>
          </button>
        </div>
      </div>

      <!-- Fancy Data Exploration Button -->
      <button v-if="uploadedDatasetId" @click="showDataExploration = true" class="absolute top-4 right-4 bg-blue-600 hover:bg-blue-800 text-white font-bold p-2 rounded-full flex items-center justify-center shadow-lg transition duration-300 ease-in-out">
        <Icon name="mdi:table" color="white" class="text-2xl"/>
      </button>

    </div>

    <!-- DataExplorationModal -->
    <DataExplorationModal :show="showDataExploration" :datasetId="uploadedDatasetId" @close="showDataExploration = false"/>
    <div v-if="loadingDashboard" class="fixed inset-0 bg-gray-100 bg-opacity-75 flex items-center justify-center">
      <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"></div>
    </div>
  </div>
</template>

<script setup>
const selectedFile = ref(null);
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const uploadedDatasetId = ref(null);
const showDataExploration = ref(false); // Hinzugefügt
const router = useRouter();
const emit = defineEmits(['uploaded', 'loading']);  // Hinzugefügt
const projectStore = useProjectStore();
const loadingDashboard = ref(false);

const props = defineProps({
  projectId: String
});

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0];
};

const exploreDataset = (datasetId) => {
  router.push(`/dataExploration/${datasetId}`);
};

const uploadChunk = async (chunk, chunkNumber, totalChunks, filename) => {
  const formData = new FormData();
  formData.append('chunk', chunk);
  formData.append('chunkNumber', chunkNumber);
  formData.append('totalChunks', totalChunks);
  formData.append('filename', filename);

  const response = await fetch('http://127.0.0.1:5000/upload_chunk', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) throw new Error('Failed to upload chunk');
};

const uploadDataset = async () => {
  if (!selectedFile.value) return;
  loadingDashboard.value = true;
  const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB
  const totalChunks = Math.ceil(selectedFile.value.size / CHUNK_SIZE);
  const filename = selectedFile.value.name;

  isLoading.value = true;
  emit('loading', true);  // Hinzugefügt
  successMessage.value = '';
  errorMessage.value = '';
  uploadedDatasetId.value = null;

  try {
    for (let i = 0; i < totalChunks; i++) {
      const chunk = selectedFile.value.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
      await uploadChunk(chunk, i, totalChunks, filename);
    }

    const finalizeResponse = await fetch('http://127.0.0.1:5000/finalize_upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename })
    });

    if (!finalizeResponse.ok) throw new Error('Failed to finalize upload');

    const result = await finalizeResponse.json();
    successMessage.value = 'Dataset uploaded successfully';
    emit('uploaded', result.datasetId);
    emit('loading', false);  // Hinzugefügt
    console.log('Dataset ID:', result.datasetId);
    uploadedDatasetId.value = result.datasetId;
    await projectStore.updateProject(props.projectId, { filePath: uploadedDatasetId.value });
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    errorMessage.value = 'Failed to upload dataset';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  } finally {
    loadingDashboard.value = false;
    isLoading.value = false;
    emit('loading', false);  // Hinzugefügt
  }
};

onMounted(async () => {
   uploadedDatasetId.value = await projectStore.fetchProjectFilePath(props.projectId);
});
</script>

<style scoped>
label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

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
