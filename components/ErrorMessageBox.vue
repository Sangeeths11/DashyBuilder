<template>
  <div v-if="visible" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mb-5 rounded relative w-full flex items-center" role="alert">
    <Icon name="ic:round-error" class="w-5 h-5" />
    <strong class="font-bold pl-2">
      Error:
    </strong>
    <span class="pl-2">{{ message }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  message: String
});

const visible = ref(false);


function hideMessage() {
  setTimeout(() => {
    visible.value = false;
  }, 2000);
}

watch(() => props.message, (newValue) => {
  if (newValue) {
    visible.value = true;
    hideMessage();
  }
});

onMounted(() => {
  if (props.message) {
    hideMessage();
  }
});
</script>
