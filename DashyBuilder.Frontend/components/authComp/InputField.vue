<template>
  <div class="mb-4 w-full">
    <label :for="id" class="block text-gray-700 text-sm font-bold mb-2">
      {{ label }}
    </label>
    <div class="flex items-center relative">
      <Icon :name="iconName" class="absolute left-3 w-5 h-5 text-gray-400" />
      <input 
        :id="id"
        :type="type"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="shadow appearance-none border rounded w-full py-2 pl-10 pr-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  label: String,
  id: String,
  type: String,
  placeholder: String,
  iconName: String,
  modelValue: [String, Number]
});
</script>
