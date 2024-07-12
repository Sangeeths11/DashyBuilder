export const useWidgetStore = defineStore('widgetStore', () => {
  const client = useSupabaseClient();
  const widgets = ref([]);
  const errorMessages = ref([]);

  const fetchWidgetsByProjectId = async (projectId) => {
    widgets.value = [];
    const { data, error } = await client
      .from('widgets')
      .select('*')
      .eq('project_id', projectId);

    if (error) {
      errorMessages.value.push('Error fetching widgets: ' + error.message);
      console.error('Error fetching widgets:', error);
      widgets.value = [];
      console.log('Fetched widgets:', widgets.value);
    } else {
      widgets.value = data || [];
      console.log('Fetched widgets:', widgets.value);
    }
  };

  const createWidget = async (type, name, projectId) => {
    const { data, error } = await client
      .from('widgets')
      .insert([
        { type,
          name,
          project_id: projectId,
          gridPosition: '[]',
        }
      ])
      .select();
    if (error) {
      errorMessages.value.push('Error creating widget: ' + error.message);
      console.error('Error creating widget:', error);
    } else {
      fetchWidgetsByProjectId(projectId);
    }
  };

  const deleteWidget = async (widgetId) => {
    const { data, error } = await client
      .from('widgets')
      .delete()
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error deleting widget: ' + error.message);
      console.error('Error deleting widget:', error);
    } else {
      widgets.value = widgets.value.filter(widget => widget.id !== widgetId);
    }
  };

  const updateWidget = async (widgetId, gridPosition) => {
    const { error } = await client
      .from('widgets')
      .update({ gridPosition })
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error updating widget: ' + error.message);
      console.error('Error updating widget:', error);
    } else {
      const widget = widgets.value.find(w => w.id === widgetId);
      if (widget) {
        widget.grid_position = gridPosition;
        fetchWidgetsByProjectId(widget.project_id);
      }
    }
  };

  return {
    widgets,
    errorMessages,
    fetchWidgetsByProjectId,
    createWidget,
    deleteWidget,
    updateWidget,
  };
});
