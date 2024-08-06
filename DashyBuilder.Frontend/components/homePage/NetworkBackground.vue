<template>
  <div class="relative h-screen w-screen color">
    <canvas ref="canvas" class="w-full h-full"></canvas>
    <div class="absolute inset-0 flex flex-col items-center justify-center text-black">
      <div class="text-center">
        <h1 class="text-6xl font-bold">
          Welcome to DashyBuilder
        </h1>
        <p class="mt-4 text-xl max-w-lg mx-auto">
          DashyBuilder is a cutting-edge web application designed to empower you with easy and intuitive dashboard creation. Customize your data visualization effortlessly and export it directly to Plotly Dash with just a few clicks.
        </p>
        <HomePageStartExploringButton/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, ref } from 'vue';

interface Node {
  x: number;
  y: number;
  vx: number;
  vy: number;
  type: string;
  data: number[];
  colors: string[];
}

export default defineComponent({
  setup() {
    const canvas = ref<HTMLCanvasElement | null>(null);
    const nodes: Node[] = [];

    const resizeCanvas = () => {
      if (canvas.value) {
        canvas.value.width = window.innerWidth;
        canvas.value.height = window.innerHeight;
        initializeNodes();
      }
    };

    const initializeNodes = () => {
      nodes.splice(0, nodes.length);
      const area = window.innerWidth * window.innerHeight;
      const desiredDensity = 0.00005;
      const numberOfNodes = Math.max(10, Math.floor(area * desiredDensity));

      const chartTypes = ['pie', 'bar', 'line'];
      for (let i = 0; i < numberOfNodes; i++) {
        const data = Array.from({ length: 5 }, () => Math.random() * 100);
        nodes.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          type: chartTypes[Math.floor(Math.random() * chartTypes.length)],
          data,
          colors: ['hsl(210, 100%, 50%)', 'hsl(210, 100%, 60%)', 'hsl(210, 100%, 70%)', 'hsl(210, 100%, 80%)', 'hsl(210, 100%, 90%)']
        });
      }
    };

    const drawNode = (ctx: CanvasRenderingContext2D, node: Node) => {
      switch(node.type) {
        case 'bar':
          drawBarChart(ctx, node);
          break;
        case 'pie':
          drawPieChart(ctx, node, 15);
          break;
        case 'line':
          drawLineChart(ctx, node);
          break;
      }
    };

    const drawBarChart = (ctx: CanvasRenderingContext2D, node: Node) => {
      const barWidth = 50 / node.data.length;
      ctx.fillStyle = 'rgb(100, 149, 237)';
      node.data.forEach((val, i) => {
        const barHeight = val / 100 * 50;
        ctx.fillRect(node.x + i * barWidth - 25, node.y - barHeight, barWidth * 0.9, barHeight);
      });
    };

    const drawPieChart = (ctx: CanvasRenderingContext2D, node: Node, radius: number) => {
      let total = node.data.reduce((acc, val) => acc + val, 0);
      let startAngle = 0;
      node.data.forEach((val, i) => {
        const endAngle = startAngle + (val / total) * 2 * Math.PI;
        ctx.beginPath();
        ctx.moveTo(node.x, node.y);
        ctx.arc(node.x, node.y, radius, startAngle, endAngle);
        ctx.fillStyle = node.colors[i];
        ctx.fill();
        startAngle = endAngle;
      });
    };

    const drawLineChart = (ctx: CanvasRenderingContext2D, node: Node) => {
      ctx.beginPath();
      ctx.moveTo(node.x, node.y - (node.data[0] / 100 * 50));
      node.data.forEach((val, i) => {
        ctx.lineTo(node.x + i * (50 / node.data.length), node.y - (val / 100 * 50));
      });
      ctx.strokeStyle = 'rgb(255, 0, 0)';
      ctx.stroke();
    };

    const drawConnections = (ctx: CanvasRenderingContext2D) => {
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
      nodes.forEach((node, index) => {
        nodes.slice(index + 1).forEach(otherNode => {
          if (Math.hypot(node.x - otherNode.x, node.y - otherNode.y) < 300) {
            ctx.beginPath();
            ctx.moveTo(node.x, node.y);
            ctx.lineTo(otherNode.x, otherNode.y);
            ctx.stroke();
          }
        });
      });
    };

    const updateNodePositions = () => {
      nodes.forEach(node => {
        node.x += node.vx;
        node.y += node.vy;

        if (node.x <= 50 || node.x >= window.innerWidth - 50) node.vx = -node.vx;
        if (node.y <= 50 || node.y >= window.innerHeight - 50) node.vy = -node.vy;
      });
    };

    const drawNodes = () => {
      const ctx = canvas.value?.getContext('2d');
      if (ctx) {
        ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
        drawConnections(ctx);
        nodes.forEach(node => drawNode(ctx, node));
      }
    };

    const animate = () => {
      updateNodePositions();
      drawNodes();
      requestAnimationFrame(animate);
    };

    onMounted(() => {
      resizeCanvas();
      animate();
      window.addEventListener('resize', resizeCanvas);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', resizeCanvas);
    });

    return { canvas };
  },
});
</script>

<style scoped>
  .color {
    background-color: white;
  }

  h1 {
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
  }

  p {
    text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.2);
  }
</style>
