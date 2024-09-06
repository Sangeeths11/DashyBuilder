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

  return {
    createWidgetTable,
    createChart,
  };
});