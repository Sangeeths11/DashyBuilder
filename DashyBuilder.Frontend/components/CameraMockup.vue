<template>
  <div class="w-full h-full flex flex-col justify-between">
    <SucessMessageBox :message="successMessage" />
    <ErrorMessageBox :message="errorMessage" />
    <div class="bg-white shadow-lg rounded-lg p-4 h-full flex flex-col relative">
      <h2 class="font-bold text-lg mb-4">Capture Mockup</h2>
      <div class="flex flex-col items-center flex-grow w-full">
        <div class="camera-container w-full bg-gray-100 rounded-lg overflow-hidden border border-gray-200 mb-6">
          <video ref="videoElement" 
            class="w-full h-full min-h-[250px] max-h-80 object-cover" 
            autoplay 
            playsinline
            v-show="!capturedImage"></video>
          <canvas ref="canvasElement" class="hidden"></canvas>
          <img v-if="capturedImage" :src="capturedImage" class="w-full h-full min-h-[250px] max-h-80 object-cover" />
        </div>
        
        <div class="flex space-x-4 w-full justify-center mt-auto">
          <button v-if="!capturedImage"
            @click="captureImage"
            class="w-full bg-blue-500 hover:bg-blue-800 text-white font-bold py-3 px-4 rounded flex items-center justify-center transition duration-300 ease-in-out h-14">
            <Icon name="mdi:camera" color="white" class="mr-2 text-3xl" />
            <span>Capture Photo</span>
          </button>
          <button v-if="capturedImage"
            @click="resetCamera"
            class="w-full bg-gray-500 hover:bg-gray-800 text-white font-bold py-3 px-4 rounded flex items-center justify-center transition duration-300 ease-in-out h-14">
            <Icon name="mdi:refresh" color="white" class="mr-2 text-3xl" />
            <span>Retake Photo</span>
          </button>
          <button v-if="capturedImage"
            @click="uploadImage" 
            :disabled="isLoading"
            class="w-full bg-blue-500 hover:bg-blue-800 text-white font-bold py-3 px-4 rounded flex items-center justify-center transition duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed h-14">
            <Icon name="mdi:upload" color="white" class="mr-2 text-3xl" />
            <span v-if="isLoading">Uploading...</span>
            <span v-else>Upload Photo</span>
          </button>
        </div>

        <div v-if="!cameraAvailable" class="mt-4 text-red-500 text-center">
          Camera access is not available. Please check your browser permissions or try another device.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const videoElement = ref(null);
const canvasElement = ref(null);
const capturedImage = ref(null);
const isLoading = ref(false);
const cameraAvailable = ref(true);
const successMessage = ref('');
const errorMessage = ref('');
const uploadedMockupId = ref(null);
const emit = defineEmits(['uploaded', 'loading']);
const projectStore = useProjectStore();

const props = defineProps({
  projectId: String
});

let stream = null;

onMounted(async () => {
  try {
    await initCamera();
  } catch (error) {
    console.error('Error accessing camera:', error);
    cameraAvailable.value = false;
    errorMessage.value = 'Unable to access camera. Please check permissions.';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  }
});

onUnmounted(() => {
  stopCamera();
});

async function initCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        facingMode: 'environment',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      } 
    });
    
    if (videoElement.value) {
      videoElement.value.srcObject = stream;
    }
    
    cameraAvailable.value = true;
  } catch (error) {
    cameraAvailable.value = false;
    throw error;
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  
  if (videoElement.value) {
    videoElement.value.srcObject = null;
  }
}

function captureImage() {
  if (!videoElement.value || !canvasElement.value) return;
  
  const video = videoElement.value;
  const canvas = canvasElement.value;
  
  // Set canvas dimensions to match video
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  // Draw the current video frame onto the canvas
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  // Convert canvas to data URL (PNG format by default)
  capturedImage.value = canvas.toDataURL('image/png');
}

function resetCamera() {
  capturedImage.value = null;
  initCamera();
}

function dataURLtoBlob(dataURL) {
  const parts = dataURL.split(';base64,');
  const contentType = parts[0].split(':')[1];
  const raw = window.atob(parts[1]);
  const rawLength = raw.length;
  const uInt8Array = new Uint8Array(rawLength);
  
  for (let i = 0; i < rawLength; ++i) {
    uInt8Array[i] = raw.charCodeAt(i);
  }
  
  return new Blob([uInt8Array], { type: contentType });
}

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

const uploadImage = async () => {
  if (!capturedImage.value) return;
  
  isLoading.value = true;
  emit('loading', true);
  successMessage.value = '';
  errorMessage.value = '';
  
  try {
    // Convert data URL to Blob
    const imageBlob = dataURLtoBlob(capturedImage.value);
    const filename = `camera_capture_${Date.now()}.png`;
    
    // Use the same chunk upload logic as in UploadMockup
    const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB
    const totalChunks = Math.ceil(imageBlob.size / CHUNK_SIZE);
    
    for (let i = 0; i < totalChunks; i++) {
      const chunk = imageBlob.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
      await uploadChunk(chunk, i, totalChunks, filename);
    }
    
    const finalizeResponse = await fetch('http://127.0.0.1:5000/finalize_upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename })
    });
    
    if (!finalizeResponse.ok) throw new Error('Failed to finalize upload');
    
    const result = await finalizeResponse.json();
    successMessage.value = 'Camera capture uploaded successfully';
    emit('uploaded', result.datasetId);
    uploadedMockupId.value = result.datasetId;
    await projectStore.updateProject(props.projectId, { filePath: uploadedMockupId.value });
    
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Upload error:', error);
    errorMessage.value = 'Failed to upload image';
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  } finally {
    isLoading.value = false;
    emit('loading', false);
  }
};
</script>

<style scoped>
.camera-container {
  position: relative;
  min-height: 250px;
  border: 2px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hidden {
  display: none;
}
</style> 