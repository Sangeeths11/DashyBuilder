<template>
  <div>
    <header class="bg-blue-500 text-white p-4 text-lg flex items-center">
      <div class="flex items-center">
        <span class="text-3xl mr-1"><Icon name="mdi:chart-box-outline" color="white" /></span>
        <span class="font-bold">Dashybuilder</span>
      </div>
    </header>

    <main class="flex-grow p-4">
      <slot />
    </main>
  </div>
</template>

<script lang="ts" setup>
</script>

<style>
</style>
