export const useProjectStore = defineStore('projectStore', () => {
  const client = useSupabaseClient();
  const user = useSupabaseUser();

  const projects = ref([]);

  const errorMessages = ref([]);

  const fetchProjects = async () => {
    const { data, error } = await client
      .from('projects')
      .select(`
        id,
        user_id,
        projectName,
        gridSize,
        researchQuestion
      `);

    if (error) {
      errorMessages.value.push('Error fetching projects: ' + error.message);
      projects.value = [];
      console.error('Error fetching projects:', error);
    } else {
      projects.value = data || [];
      console.log('Projects data:', data);
    }
  };

  async function fetchProjectNameById(id) {
    const { data, error } = await client.from('projects').select('projectName').eq('id', id).single();
    if (error) 
    {
      console.error('Error fetching project name:', error);
      return null;
    }
    else {
      return data.projectName;
    }
  }

  async function fetchProjectGridSizeById(id) {
    const { data, error } = await client.from('projects').select('gridSize').eq('id', id).single();
    if (error) {
      console.error('Error fetching project grid size:', error);
      return null;
    } else {
      return data.gridSize;
    }
  }

  async function fetchProjectGridSize(id) {
    const { data, error } = await client.from('projects').select('gridSize').eq('id', id).single();
    if (error) {
      console.error('Error fetching project grid size:', error);
      return null;
    } else {
      return data.gridSize;
    }
  }

  async function fetchProjectFilePath(id) {
    const { data, error } = await client.from('projects').select('filePath').eq('id', id).single();
    if (error) {
      console.error('Error fetching project grid size:', error);
      return null;
    } else {
      return data.filePath;
    }
  }

  async function fetchProjectResearchQuestionById(id) {
    const { data, error } = await client.from('projects').select('researchQuestion').eq('id', id).single();
    if (error) {
      console.error('Error fetching project grid size:', error);
      return null;
    } else {
      return data.researchQuestion;
    }
  }

  const createProject = async (projectName, gridSize, researchQuestion) => {
    if (!user.value) {
      errorMessages.value.push('User must be logged in to create a project.');
      return;
    }

    const { data: projectData, error: projectError } = await client
      .from('projects')
      .insert({
        user_id: user.value.id,
        projectName,
        gridSize,
        researchQuestion
      })
      .select();

    console.log('projectData:', projectData);
    if (projectError) {
      errorMessages.value.push('Error creating project: ' + projectError.message);
      console.error('Error creating project:', projectError);
    } else {
      console.log('Project created:', projectData.value);
      fetchProjects();
    }
  };

  const deleteProject = async (projectId) => {
    const { data, error } = await client
      .from('projects')
      .delete()
      .match({ id: projectId });

    if (error) {
      errorMessages.value.push('Error deleting project: ' + error.message);
      console.error('Error deleting project:', error);
    } else {
      console.log('Project deleted:', data);
      projects.value = projects.value.filter(project => project.id !== projectId);
      fetchProjects();
    }
  };

  const updateProject = async (projectId, updatedData) => {
    const { data, error } = await client
      .from('projects')
      .update(updatedData)
      .match({ id: projectId });

    if (error) {
      errorMessages.value.push('Error updating project: ' + error.message);
      console.error('Error updating project:', error);
    } else {
      console.log('Project updated:', data);
      // Optional: die Liste der Projekte neu laden
      fetchProjects();
    }
  };
  
  const getFileName = async (projectId) => {
    const { data, error } = await client
      .from('projects')
      .select('filePath')
      .eq('id', projectId)
      .single();

    if (error) {
      errorMessages.value.push('Error fetching file name: ' + error.message);
      console.error('Error fetching file name:', error);
    } else {
      return data.filePath;
    }
  }

  return {
    projects,
    fetchProjectNameById,
    fetchProjectGridSizeById,
    fetchProjectResearchQuestionById,
    fetchProjectGridSize,
    fetchProjectFilePath,
    fetchProjects,
    errorMessages,
    createProject,
    deleteProject,
    updateProject,
    getFileName
  };
});
