<template>
    <div class="flex flex-col items-center justify-center min-h-screen">
        <div class="bg-white p-6 rounded shadow-lg w-full max-w-lg">
            <h1 class="text-2xl font-bold mb-4">Projekte verwalten</h1>
            <input
                type="text"
                placeholder="Projekt suchen..."
                v-model="search"
                class="mb-4 p-2 w-full border rounded"
            />
            <div class="grid gap-4 md:grid-cols-2">
                <div v-for="project in filteredProjects" :key="project.id" class="bg-gray-100 rounded-lg p-4 shadow">
                    <h2 class="text-lg font-semibold">{{ project.name }}</h2>
                    <p class="text-sm text-gray-600">Grid-System: {{ project.grid }}</p>
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
                    <option>3x3</option>
                    <option>4x4</option>
                </select>
                <div class="flex justify-end space-x-4">
                    <button @click="openCreateProjectModal = false" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Abbrechen</button>
                    <button @click="createProject" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">Erstellen</button>
                </div>
            </div>
        </div>
    </div>
</template>


  
<script setup>
    definePageMeta({
        title: 'DashyBuilder - Projekte',
        middleware: ['auth-index'],
    })

    const search = ref('')
    const projects = ref([
        { id: 1, name: 'Projekt 1', grid: '3x3' },
        { id: 2, name: 'Projekt 2', grid: '4x4' }
    ])
    const newProjectName = ref('')
    const newProjectGrid = ref('')
    const openCreateProjectModal = ref(false)
    const router = useRouter()

    const filteredProjects = computed(() => {
        return projects.value.filter(project => project.name.toLowerCase().includes(search.value.toLowerCase()))
    })

    function createProject() {
        if (!newProjectName.value || !newProjectGrid.value) {
            alert("Bitte alle Felder ausfüllen")
            return
        }
        const newProjectId = Date.now()
        projects.value.push({
            id: newProjectId,
            name: newProjectName.value,
            grid: newProjectGrid.value
        })
        newProjectName.value = ''
        newProjectGrid.value = ''
        openCreateProjectModal.value = false
        router.push(`/overview/${newProjectId}`)
    }

    function deleteProject(projectId) {
        projects.value = projects.value.filter(project => project.id !== projectId)
    }
</script>

  
<style scoped>
</style>
  