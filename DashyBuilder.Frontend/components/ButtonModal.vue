<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4">
    <div class="relative bg-white w-full max-w-3xl p-6 mx-auto rounded-lg shadow-lg overflow-auto max-h-full">
      <span class="absolute top-0 right-0 p-4">
        <button @click="closeModal" class="text-3xl leading-none hover:text-gray-600">&times;</button>
      </span>
      <h2 class="text-2xl font-bold mb-4 text-center">Button Configuration</h2>
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700">Button Text</label>
          <input type="text" v-model="localButtonConfig.text" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Button Color</label>
          <select v-model="localButtonConfig.color" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="primary">Primary</option>
            <option value="secondary">Secondary</option>
            <option value="success">Success</option>
            <option value="danger">Danger</option>
            <option value="warning">Warning</option>
            <option value="info">Info</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Button Size</label>
          <select v-model="localButtonConfig.size" class="mt-1 block w-full pl-3 pr-10 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="sm">Small</option>
            <option value="md">Medium</option>
            <option value="lg">Large</option>
          </select>
        </div>
        <div class="text-center mt-4">
          <button @click="saveConfig" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Save Configuration
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  widget: Object,
});

const emit = defineEmits(['close', 'save']);
const configCompStore = useConfigCompStore();

const localButtonConfig = ref({
  text: '',
  color: 'primary',
  size: 'md',
});
const buttonConfigId = ref(null);

async function loadButtonConfig() {
  if (props.widget && props.widget.id) {
    const savedButtonConfig = await configCompStore.fetchButtonConfig(props.widget.id);
    if (savedButtonConfig) {
      buttonConfigId.value = savedButtonConfig.buttonConfig_id;
      console.log(savedButtonConfig);
      localButtonConfig.value = {
        text: savedButtonConfig.buttonText.buttonText || '',
        color: savedButtonConfig.buttonColor.buttonColor || 'primary',
        size: savedButtonConfig.buttonSize.buttonSize || 'md',
      };
    }
  }
}

watch(() => props.isOpen, async (newVal) => {
  if (newVal) {
    await loadButtonConfig();
  }
});

async function saveConfig() {
  if (buttonConfigId.value) {
    await configCompStore.updateButton(buttonConfigId.value, localButtonConfig.value);
  } else {
    await configCompStore.createButton(props.widget.id, localButtonConfig.value);
  }
  closeModal();
}

function closeModal() {
  emit('close');
}

onMounted(() => {
  loadButtonConfig();
});
</script>

<style scoped>
</style>
