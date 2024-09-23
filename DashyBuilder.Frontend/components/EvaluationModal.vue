<template>
    <div
      v-if="show"
      class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50"
    >
      <div class="bg-white rounded-lg overflow-hidden shadow-xl w-11/12 md:w-3/4 lg:w-1/2 max-h-screen overflow-y-auto">
        <div class="px-6 py-4">
          <div class="flex justify-between items-center">
            <h3 class="text-2xl font-semibold">Dashboard Evaluation</h3>
            <button @click="$emit('close')" class="text-gray-700 hover:text-gray-900">
              <Icon name="mdi:close" class="text-2xl" />
            </button>
          </div>
          <div class="mt-6 space-y-4">
            <div
              v-for="(feedback, index) in structuredFeedback"
              :key="index"
              class="p-4 rounded-lg shadow flex items-start"
              :class="feedback.isPositive ? 'bg-green-50' : 'bg-red-50'"
            >
              <div class="flex-shrink-0">
                <Icon
                  :name="feedback.isPositive ? 'mdi:check-circle' : 'mdi:alert-circle'"
                  :class="feedback.isPositive ? 'text-green-500' : 'text-red-500'"
                  class="text-3xl"
                />
              </div>
              <div class="ml-4">
                <h4 class="text-lg font-semibold" :class="feedback.isPositive ? 'text-green-700' : 'text-red-700'">
                  {{ feedback.ruleTitle }}
                </h4>
                <p class="text-gray-700 mt-1">{{ feedback.message }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-100 text-right">
          <button
            @click="$emit('close')"
            class="bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    show: Boolean,
    evaluationResults: Array,
  });
  
  // Process the evaluationResults to structure them
  const structuredFeedback = computed(() => {
    return props.evaluationResults.map((feedback) => {
      // Extract the rule number and title
      const ruleMatch = feedback.match(/^Rule (\d) \(([^)]+)\): (.+)$/);
      if (ruleMatch) {
        const [, ruleNumber, ruleTitle, message] = ruleMatch;
        const isPositive = !message.toLowerCase().includes('no') && !message.toLowerCase().includes('not');
        return {
          ruleNumber,
          ruleTitle: `Rule ${ruleNumber}: ${ruleTitle}`,
          message,
          isPositive,
        };
      } else {
        return {
          ruleNumber: null,
          ruleTitle: 'General Feedback',
          message: feedback,
          isPositive: true,
        };
      }
    });
  });
  </script>
  
  <style scoped>
  /* Optional: Add any custom styles if needed */
  </style>
  