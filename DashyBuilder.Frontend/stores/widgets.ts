export const useWidgetStore = defineStore('widgetStore', () => {
  const client = useSupabaseClient();
  const widgets = ref([]);
  const errorMessages = ref([]);

  const fetchWidgetsByProjectId = async (projectId) => {
    const { data, error } = await client
      .from('widgets')
      .select('*')
      .eq('project_id', projectId);

    if (error) {
      errorMessages.value.push('Error fetching widgets: ' + error.message);
      console.error('Error fetching widgets:', error);
    } else {
      widgets.value = data || [];
    }
  };

  const createWidget = async (type, name, gridPosition, projectId) => {
    const { data, error } = await client
      .from('widgets')
      .insert([
        { type, name, gridPosition, project_id: projectId }
      ]);

    if (error) {
      errorMessages.value.push('Error creating widget: ' + error.message);
      console.error('Error creating widget:', error);
    } else {
      widgets.value.push(data[0]);
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

  const updateWidget = async (widgetId, updates) => {
    const { data, error } = await client
      .from('widgets')
      .update(updates)
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error updating widget: ' + error.message);
      console.error('Error updating widget:', error);
    } else {
      const index = widgets.value.findIndex(widget => widget.id === widgetId);
      if (index !== -1) {
        widgets.value[index] = { ...widgets.value[index], ...updates };
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
