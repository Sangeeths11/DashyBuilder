<template>
  <div ref="grid" class="grid-stack">
    <div
      v-for="item in layout"
      :key="item.id"
      class="grid-stack-item"
      :gs-x="item.x"
      :gs-y="item.y"
      :gs-width="item.width"
      :gs-height="item.height"
    >
      <div class="grid-stack-item-content">
        Widget {{ item.id }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import 'gridstack/dist/gridstack.min.css'
import { GridStack } from 'gridstack'

const grid = ref(null)

const layout = ref([
  { id: 1, x: 0, y: 0, width: 2, height: 2 },
  { id: 2, x: 2, y: 0, width: 2, height: 2 },
  { id: 3, x: 4, y: 0, width: 2, height: 2 },
])

onMounted(() => {
  const gridstack = GridStack.init({
    float: true,
  }, grid.value)

  gridstack.on('change', (event, items) => {
    items.forEach(item => {
      const layoutItem = layout.value.find(l => l.id === parseInt(item.id))
      if (layoutItem) {
        layoutItem.x = item.x
        layoutItem.y = item.y
        layoutItem.width = item.width
        layoutItem.height = item.height
      }
    })
  })
})
</script>

<style scoped>
.grid-stack-item-content {
  background-color: #4caf50;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>
