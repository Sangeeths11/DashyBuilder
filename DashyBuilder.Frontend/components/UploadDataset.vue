<template>
  <div class="max-w-full mx-auto h-full">
    <div class="bg-white shadow-lg rounded-lg p-4 h-full flex flex-col">
      <SucessMessageBox :message="successMessage"/>
      <ErrorMessageBox :message="errorMessage"/>
      <h2 class="font-bold text-lg mb-4">Upload Dataset</h2>
      <div class="flex flex-col items-center space-y-4 flex-grow">
        <label for="file-upload" class="w-full flex flex-col items-center px-4 py-16 bg-gray-100 text-blue rounded-lg shadow-lg tracking-wide uppercase border border-blue cursor-pointer hover:bg-blue-500 hover:text-white transition duration-300 ease-in-out">
          <svg class="w-12 h-12" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M16.88 5.5a2 2 0 01.12 0h1a2 2 0 011.72 1.05 2 2 0 01.28.96v7a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h1.1a2 2 0 01.12 0H5a.5.5 0 000 1h10a.5.5 0 000-1h-.12zM9 8a.5.5 0 000 1h2a.5.5 0 000-1H9z"/>
          </svg>
          <span class="mt-2 text-base leading-normal">Select a file</span>
          <span class="text-xs leading-normal">File must be in CSV format</span>
          <input id="file-upload" type="file" class="hidden" @change="handleFileUpload"/>
        </label>
        <button 
          @click="uploadDataset"
          :disabled="!selectedFile || isLoading"
          class="w-full bg-blue-500 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded mt-4 flex items-center justify-center transition duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed">
          <Icon name="mdi:upload" color="white" class="mr-1 text-3xl"/>
          <span v-if="isLoading">Uploading...</span>
          <span v-else>Upload Dataset</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>

const selectedFile = ref(null);
const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const uploadedDatasetId = ref(null);
const router = useRouter();
const emit = defineEmits(['uploaded']);

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0];
};

const exploreDataset = (datasetId) => {
  router.push(`/dataExploration/${datasetId}`);
};

const uploadDataset = async () => {
  if (!selectedFile.value) return;

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  isLoading.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  uploadedDatasetId.value = null;

  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('Failed to upload dataset');

    const result = await response.json();
    successMessage.value = 'Dataset uploaded successfully';
    emit('uploaded', result.datasetId);
    console.log('Dataset ID:', result.datasetId);
    uploadedDatasetId.value = result.datasetId;
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    errorMessage.value = 'Failed to upload dataset';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};
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
</style>
