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
        gridSize
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

  const createProject = async (projectName, gridSize) => {
    if (!user.value) {
      errorMessages.value.push('User must be logged in to create a project.');
      return;
    }

    const { data: projectData, error: projectError } = await client
      .from('projects')
      .insert({
        user_id: user.value.id,
        projectName,
        gridSize
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

  return {
    projects,
    fetchProjectNameById,
    fetchProjectGridSizeById,
    fetchProjectGridSize,
    fetchProjects,
    errorMessages,
    createProject,
    deleteProject
  };
});
