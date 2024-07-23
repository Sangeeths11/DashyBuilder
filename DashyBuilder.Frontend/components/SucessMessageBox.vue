<template>
  <div v-if="visible" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 mb-5 rounded relative w-full flex items-center" role="alert">
    <Icon name="ic:round-check-circle" class="w-5 h-5" />
    <strong class="font-bold pl-2">
      Success:
    </strong>
    <span class="pl-2">{{ message }}</span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  message: String
});

const visible = ref(false);


function hideMessage() {
  setTimeout(() => {
    visible.value = false;
  }, 3000);
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
