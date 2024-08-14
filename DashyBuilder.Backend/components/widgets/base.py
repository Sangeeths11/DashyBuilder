class Widget:
    def __init__(self, widget_info, cols):
        self.name = widget_info.get('name', f'Widget{widget_info.get("id", "")}')
        self.grid_position = widget_info['gridPosition']['gridPosition']
        self.min_row, self.min_col, self.row_span, self.col_span = self.parse_grid_positions(self.grid_position, cols)

    def parse_grid_positions(self, grid_position_str, cols):
        positions = list(map(int, grid_position_str.split(',')))

        row_positions = [(pos - 1) // cols + 1 for pos in positions]
        col_positions = [(pos - 1) % cols + 1 for pos in positions]

        min_row, max_row = min(row_positions), max(row_positions)
        min_col, max_col = min(col_positions), max(col_positions)

        row_span = max_row - min_row + 1
        col_span = max_col - min_col + 1

        return min_row, min_col, row_span, col_span

    def generate_code(self):
        raise NotImplementedError("Subclasses should implement this method")