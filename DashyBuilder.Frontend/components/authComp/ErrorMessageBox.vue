<template>
  <div v-if="message" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mb-5 rounded relative w-full" role="alert">
    <strong class="font-bold">
      <Icon name="ic:round-error" class="w-5 h-5 inline-block" />
    </strong>
    <span class="block sm:inline pl-2">{{ message }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps({
  message: String
});
</script>
