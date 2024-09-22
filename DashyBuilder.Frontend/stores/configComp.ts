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

  const updateChart = async (chartConfig_id, chartConfig) => {
    try {
      const { data, error } = await client
        .from('chartConfig')
        .update({
          xAxis: chartConfig.x,
          yAxis: chartConfig.y,
          size: chartConfig.size,
          color: chartConfig.color,
          labels: chartConfig.labels,
          values: chartConfig.values,
        })
        .eq('id', chartConfig_id);

      if (error) {
        errorMessages.value.push('Error updating chart config: ' + error.message);
        console.error('Error updating chart config:', error);
        return;
      }
      console.log('Chart config successfully updated:', data);
    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
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

  const createTable = async (widgetId, columns) => {
    try {
      const { data: tableConfigData, error: tableConfigError } = await client
        .from('tableConfig')
        .insert([
          { columns: columns }
        ])
        .select();

      if (tableConfigError) {
        errorMessages.value.push('Error creating table config: ' + tableConfigError.message);
        console.error('Error creating table config:', tableConfigError);
        return;
      }

      const tableConfigId = tableConfigData[0].id;
      const { data: widgetUpdateData, error: widgetUpdateError } = await client
        .from('widgets')
        .update({
          tableConfig_id: tableConfigId
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
  }

  const fetchTableConfig = async (widgetId) => {
    const { data, error } = await client
      .from('widgets')
      .select('columns:tableConfig_id (columns), tableConfig_id')
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error fetching widget text: ' + error.message);
      console.error('Error fetching widget text:', error);
      return null;
    }
    return data[0];
  }

  const updateTable = async (tableConfig_id, columns) => {
    try {
      const { data, error } = await client
        .from('tableConfig')
        .update({ columns: columns })
        .eq('id', tableConfig_id);

      if (error) {
        errorMessages.value.push('Error updating table config: ' + error.message);
        console.error('Error updating table config:', error);
        return;
      }
      console.log('Table config successfully updated:', data);
    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
  }

  const createFilter = async (widgetId, filterConfig) => {
    try {
      const { data: filterConfigData, error: filterConfigError } = await client
        .from('filterConfig')
        .insert([
          { column: filterConfig.column,
            step: filterConfig.step,
            startDate: filterConfig.startDate,
            endDate: filterConfig.endDate,
           }
        ])
        .select();

      if (filterConfigError) {
        errorMessages.value.push('Error creating filter config: ' + filterConfigError.message);
        console.error('Error creating filter config:', filterConfigError);
        return;
      }

      const filterConfigId = filterConfigData[0].id;
      const { data: widgetUpdateData, error: widgetUpdateError } = await client
        .from('widgets')
        .update({
          filterConfig_id: filterConfigId
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
  }

  const fetchFilterConfig = async (widgetId) => {
    const { data, error } = await client
      .from('widgets')
      .select('column:filterConfig_id (column),step:filterConfig_id (step),startDate:filterConfig_id (startDate),endDate:filterConfig_id (endDate), filterConfig_id')
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error fetching widget text: ' + error.message);
      console.error('Error fetching widget text:', error);
      return null;
    }
    return data[0];
  }

  const updateFilter = async (filterConfig_id, filterConfig) => {
    try {
      const { data, error } = await client
        .from('filterConfig')
        .update({
          column: filterConfig.column,
          step: filterConfig.step,
          startDate: filterConfig.startDate,
          endDate: filterConfig.endDate,
        })
        .eq('id', filterConfig_id);

      if (error) {
        errorMessages.value.push('Error updating filter config: ' + error.message);
        console.error('Error updating filter config:', error);
        return;
      }
      console.log('Filter config successfully updated:', data);
    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
  }

  const createButton = async (widgetId, buttonConfig) => {
    try {
      const { data: buttonConfigData, error: buttonConfigError } = await client
        .from('buttonConfig')
        .insert([
          { buttonText: buttonConfig.buttonText,
            buttonColor: buttonConfig.buttonColor,
            buttonSize: buttonConfig.buttonSize,
           }
        ])
        .select();

      if (buttonConfigError) {
        errorMessages.value.push('Error creating button config: ' + buttonConfigError.message);
        console.error('Error creating button config:', buttonConfigError);
        return;
      }

      const buttonConfigId = buttonConfigData[0].id;
      const { data: widgetUpdateData, error: widgetUpdateError } = await client
        .from('widgets')
        .update({
          buttonConfig_id: buttonConfigId
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
  }

  const fetchButtonConfig = async (widgetId) => {
    const { data, error } = await client
      .from('widgets')
      .select('buttonText:buttonConfig_id (buttonText),buttonColor:buttonConfig_id (buttonColor),buttonSize:buttonConfig_id (buttonSize), buttonConfig_id')
      .eq('id', widgetId);

    if (error) {
      errorMessages.value.push('Error fetching widget text: ' + error.message);
      console.error('Error fetching widget text:', error);
      return null;
    }
    return data[0];
  }

  const updateButton = async (buttonConfig_id, buttonConfig) => {
    try {
      const { data, error } = await client
        .from('buttonConfig')
        .update({
          buttonText: buttonConfig.text,
          buttonColor: buttonConfig.color,
          buttonSize: buttonConfig.size,
        })
        .eq('id', buttonConfig_id);

      if (error) {
        errorMessages.value.push('Error updating button config: ' + error.message);
        console.error('Error updating button config:', error);
        return;
      }
      console.log('Button config successfully updated:', data);
    } catch (err) {
      errorMessages.value.push('An unexpected error occurred: ' + err.message);
      console.error('Unexpected error:', err);
    }
  }

  return {
    createWidgetTable,
    createChart,
    createTable,
    fetchWidgetText,
    updateWidgetTable,
    fetchChartConfig,
    updateChart,
    fetchTableConfig,
    updateTable,
    createFilter,
    fetchFilterConfig,
    updateFilter,
    createButton,
    fetchButtonConfig,
    updateButton,
  };
});
