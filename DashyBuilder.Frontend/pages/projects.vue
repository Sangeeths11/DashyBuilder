<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
        <div class="bg-white p-6 rounded shadow-lg w-full max-w-lg text-center">
            <h1 class="text-2xl font-bold mb-4">Projekte verwalten</h1>
            <input
                type="text"
                placeholder="Projekt suchen..."
                v-model="search"
                class="mb-4 p-2 w-full border rounded"
            />
            <div class="grid gap-4 md:grid-cols-3">
                <div v-for="project in filteredProjects" :key="project.id" class="bg-gray-100 rounded-lg p-4 shadow">
                    <h2 class="text-lg font-semibold">{{ project.projectName }}</h2>
                    <p class="text-sm text-gray-600">Grid-System: {{ project.gridSize }}</p>
                    <div class="flex justify-between items-center mt-2">
                        <NuxtLink :to="`/overview/${project.id}`" class="text-blue-500 hover:text-blue-700">
                            <Icon name="mdi:eye" class="text-lg" />
                        </NuxtLink>
                        <button @click="deleteProject(project.id)" class="text-red-500 hover:text-red-700">
                            <Icon name="mdi:trash-can" class="text-lg" />
                        </button>
                    </div>
                </div>
            </div>
            <div class="flex justify-center mt-4">
                <button @click="openCreateProjectModal = true" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Neues Projekt erstellen
                </button>
            </div>
        </div>
        
        <div v-if="openCreateProjectModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 z-50 flex justify-center items-center">
            <div class="bg-white p-5 rounded-lg shadow-lg">
                <h3 class="text-lg font-semibold mb-4">Neues Projekt erstellen</h3>
                <input type="text" v-model="newProjectName" placeholder="Projektname" class="mb-4 p-2 w-full border rounded">
                <select v-model="newProjectGrid" class="mb-4 p-2 w-full border rounded">
                    <option disabled value="">Wähle ein Grid-System</option>
                    <option>4x4</option>
                    <option>5x5</option>
                    <option>6x6</option>
                    <option>12x12</option>
                </select>
                <div class="flex justify-end space-x-4">
                    <button @click="closeCreateModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Abbrechen</button>
                    <button @click="createProject" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">Erstellen</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
  title: 'DashyBuilder - Projekte',
  layout: 'main',
  middleware: ['auth-index'],
});

const search = ref('')
const projectStore = useProjectStore()
const newProjectName = ref('')
const newProjectGrid = ref('')
const openCreateProjectModal = ref(false)

const filteredProjects = computed(() => {
  if (!projectStore.projects || projectStore.projects.length === 0) {
    return [];
  }
  return projectStore.projects.filter(project =>
    project.projectName.toLowerCase().includes(search.value.toLowerCase())
  );
});

async function createProject() {
    if (!newProjectName.value || !newProjectGrid.value) {
        alert("Bitte alle Felder ausfüllen");
        return;
    }
    await projectStore.createProject(newProjectName.value, newProjectGrid.value);
    newProjectName.value = '';
    newProjectGrid.value = '';
    openCreateProjectModal.value = false;
    await projectStore.fetchProjects();
}

function deleteProject(projectId) {
    projectStore.deleteProject(projectId);
}

function closeCreateModal() {
    newProjectName.value = '';
    newProjectGrid.value = '';
    openCreateProjectModal.value = false;
}

onMounted(async () => {
  await projectStore.fetchProjects();
});
</script>

<style scoped>
html, body {
  overflow: hidden;
}

.min-h-screen {
  min-height: calc(100vh - 7rem); /* Adjust this value if your header height changes */
}
</style>