<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <div class="bg-white p-6 rounded shadow-lg w-full max-w-lg text-center">
      <SucessMessageBox :message="successMessage" />
      <h1 class="text-2xl font-bold mb-4">Manage projects</h1>
      <input
        type="text"
        placeholder="Search project..."
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
            <button @click="openEditProjectModal(project)" class="text-green-500 hover:text-green-700">
              <Icon name="mdi:pencil" class="text-lg" />
            </button>
            <button @click="deleteProject(project.id)" class="text-red-500 hover:text-red-700">
              <Icon name="mdi:trash-can" class="text-lg" />
            </button>
          </div>
        </div>
      </div>
      <div class="flex justify-center mt-4">
        <button @click="openCreateProjectModal = true" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Create new project
        </button>
      </div>
    </div>

    <!-- Modal zum Erstellen eines neuen Projekts -->
    <div v-if="openCreateProjectModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 z-50 flex justify-center items-center">
      <div class="modal-container">
        <ErrorMessageBox :message="errorMessage" />
        <h3 class="text-lg font-semibold mb-4">Create new project</h3>
        <input type="text" v-model="newProjectName" placeholder="Projectname" class="mb-4 p-2 w-full border rounded">
        <div class="flex flex-col mb-4">
          <div class="flex justify-between items-center mb-2">
            <label for="cols" class="text-sm text-gray-600 w-1/2 text-center">Columns</label>
            <label for="rows" class="text-sm text-gray-600 w-1/2 text-center">Rows</label>
          </div>
          <div class="flex space-x-2">
            <input id="cols" type="number" v-model.number="newProjectCols" placeholder="Cols" class="p-2 border rounded w-1/2 text-center" min="1" max="18">
            <input id="rows" type="number" v-model.number="newProjectRows" placeholder="Rows" class="p-2 border rounded w-1/2 text-center" min="1" max="18">
          </div>
        </div>
        <textarea v-model="researchQuestion" placeholder="Enter your research question..." class="mb-4 p-2 w-full border rounded h-32 resize-none"></textarea>
        <div class="flex justify-end space-x-4">
          <button @click="closeCreateModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Cancel</button>
          <button @click="createProject" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">Create</button>
        </div>
      </div>
    </div>

    <!-- Modal zum Bearbeiten eines Projekts -->
    <div v-if="openEditProjectModalState" class="fixed inset-0 bg-gray-600 bg-opacity-50 z-50 flex justify-center items-center">
      <div class="modal-container">
        <ErrorMessageBox :message="errorMessage" />
        <h3 class="text-lg font-semibold mb-4">Modify Project</h3>
        <input type="text" v-model="editProjectName" placeholder="Projectname" class="mb-4 p-2 w-full border rounded">
            <textarea v-model="editResearchQuestion" placeholder="Enter your research question..." class="mb-4 p-2 w-full border rounded h-32 resize-none bg-gray-100 text-gray-500 border-gray-300 cursor-not-allowed" disabled></textarea>          <div class="flex justify-end space-x-4">
          <button @click="closeEditModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Cancel</button>
          <button @click="updateProject" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">Modify</button>
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
const newProjectCols = ref(1)
const newProjectRows = ref(1)
const researchQuestion = ref('')
const openCreateProjectModal = ref(false)
const openEditProjectModalState = ref(false)
const editProjectName = ref('')
const editResearchQuestion = ref('')
const editProjectId = ref(null)
const errorMessage = ref('')
const successMessage = ref('')

const filteredProjects = computed(() => {
  if (!projectStore.projects || projectStore.projects.length === 0) {
    return [];
  }
  return projectStore.projects.filter(project =>
    project.projectName.toLowerCase().includes(search.value.toLowerCase())
  );
});

async function createProject() {
    if(newProjectCols.value < 1 || newProjectCols.value > 18 || newProjectRows.value < 1 || newProjectRows.value > 18)
    {
        errorMessage.value = 'Please fill out all fields correctly (Grid size max 18x18).';
          setTimeout(() => {
              errorMessage.value = '';
          }, 3000);
          return;
    }
    if (!newProjectName.value || !researchQuestion.value) {
              errorMessage.value = 'Please fill out all fields.';
              setTimeout(() => {
                  errorMessage.value = '';
              }, 3000);
              return;
    } else if (projectStore.projects.some(project => project.projectName === newProjectName.value)) {
        errorMessage.value = 'A project with this name already exists.';
        setTimeout(() => {
            errorMessage.value = '';
        }, 3000);
        return;
    }
    const gridSize = `${newProjectCols.value}x${newProjectRows.value}`;
    await projectStore.createProject(newProjectName.value, gridSize, researchQuestion.value);
    newProjectName.value = '';
    newProjectCols.value = 1;
    newProjectRows.value = 1;
    researchQuestion.value = '';
    openCreateProjectModal.value = false;
    await projectStore.fetchProjects();
    successMessage.value = 'Project created successfully.';
    setTimeout(() => {
        successMessage.value = '';
    }, 3000);
}

async function openEditProjectModal(project) {
    editProjectName.value = project.projectName;
    editResearchQuestion.value = project.researchQuestion;
    editProjectId.value = project.id;
    openEditProjectModalState.value = true;
}

async function updateProject() {
    if (!editProjectName.value) {
        errorMessage.value = 'Please enter a project name.';
        setTimeout(() => {
            errorMessage.value = '';
        }, 3000);
        return;
    }
    await projectStore.updateProject(editProjectId.value, { projectName: editProjectName.value });
    openEditProjectModalState.value = false;
    await projectStore.fetchProjects();
    successMessage.value = 'Project updated successfully.';
    setTimeout(() => {
        successMessage.value = '';
    }, 3000);
}

function deleteProject(projectId) {
    projectStore.deleteProject(projectId);
    successMessage.value = 'Project deleted successfully.';
    setTimeout(() => {
        successMessage.value = '';
    }, 3000);
}

function closeCreateModal() {
    newProjectName.value = '';
    newProjectCols.value = 1;
    newProjectRows.value = 1;
    researchQuestion.value = '';
    openCreateProjectModal.value = false;
}

function closeEditModal() {
    editProjectName.value = '';
    openEditProjectModalState.value = false;
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

/* Gemeinsame Klasse für Modals */
.modal-container {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}
</style>
