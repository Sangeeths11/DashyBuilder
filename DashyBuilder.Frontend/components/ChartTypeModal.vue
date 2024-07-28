<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300">
      <div class="bg-white p-6 rounded-lg shadow-lg w-11/12 md:w-1/3 transition-transform transform scale-95 hover:scale-100 duration-300">
        <h2 class="text-2xl font-bold mb-4 text-center">Select Chart Type</h2>
        <div>
          <h3 class="text-xl font-semibold mb-2 text-center">Basic Charts</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <button @click="selectChartType('Bar')" class="chart-button">Bar Chart <i class="mdi mdi-chart-bar"></i></button>
            <button @click="selectChartType('Line')" class="chart-button">Line Chart <i class="mdi mdi-chart-line"></i></button>
            <button @click="selectChartType('Pie')" class="chart-button">Pie Chart <i class="mdi mdi-chart-pie"></i></button>
            <button @click="selectChartType('Scatter')" class="chart-button">Scatter Chart <i class="mdi mdi-chart-scatter-plot"></i></button>
          </div>
          <h3 class="text-xl font-semibold mb-2 text-center">Statistical Charts</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <button @click="selectChartType('Histogram')" class="chart-button">Histogram <i class="mdi mdi-chart-histogram"></i></button>
            <button @click="selectChartType('Box')" class="chart-button">Box Plot <i class="mdi mdi-chart-box"></i></button>
            <button @click="selectChartType('Violin')" class="chart-button">Violin Plot <i class="mdi mdi-chart-bell-curve"></i></button>
            <button @click="selectChartType('Density')" class="chart-button">Density Plot <i class="mdi mdi-chart-density"></i></button>
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="$emit('close')" class="close-button">Close</button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    props: {
      isOpen: {
        type: Boolean,
        required: true
      },
      widget: {
        type: Object,
        required: true
      }
    },
    methods: {
      selectChartType(type: string) {
        this.$emit('save', type);
        this.$emit('close');
      }
    }
  });
  </script>
  
  <style scoped>
  /* Optional: Add any additional styling here */
  
  .chart-button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    background-color: #e0f7fa;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
  }
  
  .chart-button i {
    margin-left: 0.5rem;
  }
  
  .chart-button:hover {
    background-color: #b2ebf2;
    transform: translateY(-2px);
  }
  
  .close-button {
    background-color: #007bff;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
  }
  
  .close-button:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
  }
  
  </style>
  