export const useConfigCompStore = defineStore('configComp', () => {
  const client = useSupabaseClient();
  const user = useSupabaseUser();
  
  const errorMessages = ref([]);

  const createWidgetTable = async (textValue, widgetId) => {
    try {
      const { data: textConfigData, error: textConfigError } = await client
        .from('textConfig')
        .insert([
          { text: textValue }
        ])
        .select();

      if (textConfigError) {
        errorMessages.value.push('Error creating text config: ' + textConfigError.message);
        console.error('Error creating text config:', textConfigError);
        return;
      }

      // Nehmen wir an, dass nur ein Datensatz eingefügt wurde, und wir die ID benötigen
      const textConfigId = textConfigData[0].id;
      console.log('Text config created:', textConfigId);

      const { data: widgetUpdateData, error: widgetUpdateError } = await client
        .from('widgets')
        .update({
          textConfig_id: textConfigId
        })
        .eq('id', widgetId);

      if (widgetUpdateError) {
        errorMessages.value.push('Error updating widget: ' + widgetUpdateError.message);
        console.error('Error updating widget:', widgetUpdateError);
        return;
      }
      console.log('Widget successfully updated:', widgetUpdateData);

    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
  };

  const createChart = async (chartConfig, widgetId) => {
    try {
      const { data: chartConfigData, error: chartConfigError } = await client
        .from('chartConfig')
        .insert([
          {
            xAxis: chartConfig.x,
            yAxis: chartConfig.y,
            size: chartConfig.size,
            color: chartConfig.color,
            labels: chartConfig.labels,
            values: chartConfig.values,
          }
        ])
        .select();

      if (chartConfigError) {
        errorMessages.value.push('Error creating chart config: ' + chartConfigError.message);
        console.error('Error creating chart config:', chartConfigError);
        return;
      }

      const chartConfigDataId = chartConfigData[0].id;
      const { data: widgetUpdateData, error: widgetUpdateError } = await client
        .from('widgets')
        .update({
          chartConfig_id: chartConfigDataId
        })
        .eq('id', widgetId);

      if (widgetUpdateError) {
        errorMessages.value.push('Error updating widget: ' + widgetUpdateError.message);
        console.error('Error updating widget:', widgetUpdateError);
        return;
      }
      console.log('Widget successfully updated:', widgetUpdateData);
    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
  };

  const fetchWidgetText = async (widgetId) => {
    const { data, error } = await client
      .from('widgets')
      .select('text:textConfig_id (text), textConfig_id')
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error fetching widget text: ' + error.message);
      console.error('Error fetching widget text:', error);
      return null;
    }
    return data[0];
  }

  const fetchChartConfig = async (widgetId) => {
    const { data, error } = await client
      .from('widgets')
      .select('xAxis:chartConfig_id (xAxis), yAxis:chartConfig_id (yAxis), size:chartConfig_id (size), color:chartConfig_id (color),labels:chartConfig_id (labels),values:chartConfig_id (values),chartConfig_id')
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error fetching widget text: ' + error.message);
      console.error('Error fetching widget text:', error);
      return null;
    }
    return data[0];
  }

  const updateWidgetTable = async (textConfig_id, textContent) => {
    try {
      const { data, error } = await client
        .from('textConfig')
        .update({ text: textContent })
        .eq('id', textConfig_id);

      if (error) {
        errorMessages.value.push('Error updating text config: ' + error.message);
        console.error('Error updating text config:', error);
        return;
      }
      console.log('Text config successfully updated:', data);
    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
  }

  return {
    createWidgetTable,
    createChart,
    fetchWidgetText,
    updateWidgetTable,
    fetchChartConfig,
  };
});
