<template>
  <div class="relative h-screen w-screen color" >
    <canvas ref="canvas" class="w-full h-full"></canvas>
    <div class="absolute inset-0 flex flex-col items-center justify-center text-black">
      <div class="text-center">
        <h1 class="text-6xl font-bold">
          Welcome to CulinaPlan
        </h1>
        <p class="mt-4 text-xl max-w-lg mx-auto">
          CulinaPlan is an innovative web application that aims to revolutionize the everyday cooking experience...
        </p>
        <StartExploringButton/>
      </div>
    </div>
  </div>
</template>


<script lang="ts">

interface Node {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

export default defineComponent({
  setup() {
    const canvas: Ref<HTMLCanvasElement | null> = ref(null);
    const nodes: Node[] = [];
    let nodeCount: number;
    let maxDistance: number;
    let maxDistanceSquared: int;
    let intensityCutoff: int;
    let nodeRadius: int;
    let edgeTranparanency: number;
    let intensityCutoffFactor: number;

    const resizeCanvas = () => {
      if (canvas.value) {
        canvas.value.width = window.innerWidth;
        canvas.value.height = window.innerHeight;
        nodeRadius = 5;

        let windowRealEstate = (window.innerHeight * window.innerWidth) / Math.pow(nodeRadius*2, 2);
        nodeCount = Math.floor(windowRealEstate * 0.005); // make 0.75% of window space node
        maxDistance = Math.max(window.innerHeight, window.innerWidth) * 0.1;
        maxDistanceSquared = maxDistance * maxDistance;
        intensityCutoff = maxDistanceSquared * 0.7;
        edgeTranparanency = 0.2;
        intensityCutoffFactor = 0.2 * (1/(maxDistanceSquared - intensityCutoff));
        console.log(`realEstate: ${windowRealEstate}, nodeCount: ${nodeCount}, maxDistance: ${maxDistance}, maxDistance^2: ${maxDistanceSquared}, intensityCutoff: ${intensityCutoff}`);
        initializeNodes();
      }
    };

    const initializeNodes = () => {
      nodes.splice(0, nodes.length);
      for (let i = 0; i < nodeCount; i++) {
        nodes.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
        });
      }
    };


    const distSquared = (self: Node, other: Node): number => {
      let xDiff = self.x - other.x;
      let yDiff = self.y - other.y;
      return xDiff * xDiff + yDiff * yDiff;
    }

    const drawNodes = () => {
      if (canvas.value) {
        const ctx = canvas.value.getContext('2d');
        if (ctx) {
          ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);

          // Linien
          ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';

          let nodeCount = nodes.length;
          for (let i = 0; i < nodeCount - 1; i++) {
            for (let j = i+1; j < nodeCount; j++) {
              const node = nodes[i];
              const other = nodes[j];
             // console.log(`draw from ${i} to ${j}, ${nodeCount} nodes total, self: ${node}, other: ${other}`);
              const distance = distSquared(node, other);
              if (distance < maxDistanceSquared) {
                const intensity = 0.2 - (Math.min(0, distance - intensityCutoff)*intensityCutoffFactor)
                ctx.strokeStyle = `rgba(0,0,0, ${intensity})`
                ctx.beginPath();
                ctx.moveTo(node.x, node.y);
                ctx.lineTo(other.x, other.y);
                ctx.stroke();
              }
            }
          }

          // Kreise
          ctx.fillStyle = 'rgba(0, 230, 255, 0.5)';

          nodes.forEach(node => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI);
            ctx.fill();
          });
        }
      }
    };

    const updateNodePositions = () => {
      nodes.forEach(node => {
        node.x += node.vx;
        node.y += node.vy;

        if (node.x <= 0 || node.x >= window.innerWidth) node.vx *= -1;
        if (node.y <= 0 || node.y >= window.innerHeight) node.vy *= -1;
      });
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
</style>
