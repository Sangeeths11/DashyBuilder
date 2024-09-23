import ast
import re
from collections import defaultdict

class DashAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.components = defaultdict(list)
        self.layout_defined = False
        self.callbacks = []
        self.variables = set()
        self.shortcuts = []
        self.errors = []
        self.user_controls = []
        self.data_inputs = []
        self.try_except_blocks = []
        self.component_count = 0
        self.callback_inputs = []
        self.callback_outputs = []
        self.global_variables = set()
        self.function_defs = {}
        self.assignments = {}
        self.figures = {}
        self.figure_issues = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
                self.assignments[target.id] = node.value
                if self.is_figure(node.value):
                    self.figures[target.id] = node.value
            elif isinstance(target, ast.Attribute):
                if (isinstance(target.value, ast.Name) and target.value.id == 'app') and target.attr == 'layout':
                    self.layout_defined = True
        self.generic_visit(node)

    def is_figure(self, node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                module_name = ''
                if isinstance(node.func.value, ast.Name):
                    module_name = node.func.value.id
                elif isinstance(node.func.value, ast.Attribute):
                    module_name = self.get_full_attribute_name(node.func.value)
                if module_name.split('.')[0] in ['px', 'go']:
                    return True
        return False

    def get_full_attribute_name(self, node):
        names = []
        while isinstance(node, ast.Attribute):
            names.insert(0, node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            names.insert(0, node.id)
        return '.'.join(names)

    def visit_FunctionDef(self, node):
        decorators = [dec for dec in node.decorator_list if isinstance(dec, (ast.Call, ast.Attribute))]
        for dec in decorators:
            if isinstance(dec, ast.Call):
                if hasattr(dec.func, 'id') and dec.func.id == 'app':
                    self.callbacks.append(node.name)
                    self.function_defs[node.name] = node
                    for keyword in dec.keywords:
                        if keyword.arg == 'Input':
                            self.callback_inputs.extend(self.extract_component_ids(keyword.value))
                        elif keyword.arg == 'Output':
                            self.callback_outputs.extend(self.extract_component_ids(keyword.value))
            elif isinstance(dec, ast.Attribute):
                if isinstance(dec.value, ast.Name) and dec.value.id == 'app' and dec.attr == 'callback':
                    self.callbacks.append(node.name)
                    self.function_defs[node.name] = node
        self.generic_visit(node)

    def extract_component_ids(self, node):
        ids = []
        if isinstance(node, ast.Call):
            for arg in node.args:
                if isinstance(arg, ast.Str):
                    ids.append(arg.s)
            for keyword in node.keywords:
                ids.extend(self.extract_component_ids(keyword.value))
        elif isinstance(node, ast.List):
            for elt in node.elts:
                ids.extend(self.extract_component_ids(elt))
        return ids

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            module_name = ''
            if isinstance(node.func.value, ast.Name):
                module_name = node.func.value.id
            elif isinstance(node.func.value, ast.Attribute):
                module_name = self.get_full_attribute_name(node.func.value)
            func_name = node.func.attr
            if module_name.split('.')[0] in ['html', 'dcc', 'dbc']:
                self.components[func_name].append(node)
                self.component_count += 1
                if func_name in ['Button', 'Input', 'Slider', 'Dropdown', 'DatePickerRange']:
                    self.user_controls.append(func_name)
                if func_name in ['Upload', 'Input', 'Textarea']:
                    self.data_inputs.append(func_name)
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id in self.figures:
                    method_name = node.func.attr
                    if method_name in ['update_layout', 'update_xaxes', 'update_yaxes']:
                        self.analyze_figure_layout(node, self.figures[node.func.value.id], method_name)
        self.generic_visit(node)

    def analyze_figure_layout(self, node, figure_node, method_name):
        issues = []
        layout_args = {}
        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Dict):
                for k, v in zip(keyword.value.keys, keyword.value.values):
                    if isinstance(k, ast.Str):
                        layout_args[k.s] = v
            else:
                if isinstance(keyword.arg, str):
                    layout_args[keyword.arg] = keyword.value
        if method_name == 'update_layout':
            if 'title' not in layout_args:
                issues.append("Figure is missing a title.")
            else:
                title_arg = layout_args['title']
                title_text = ''
                if isinstance(title_arg, ast.Str):
                    title_text = title_arg.s
                elif isinstance(title_arg, ast.Dict):
                    for k, v in zip(title_arg.keys, title_arg.values):
                        if isinstance(k, ast.Str) and k.s == 'text':
                            if isinstance(v, ast.Str):
                                title_text = v.s
                if not title_text.strip():
                    issues.append("Figure has an empty title.")
                elif len(title_text.strip()) < 3:
                    issues.append(f"Figure title '{title_text}' may not be descriptive.")
            if 'xaxis_title' not in layout_args and 'xaxis' not in layout_args:
                issues.append("Figure is missing x-axis label.")
            if 'yaxis_title' not in layout_args and 'yaxis' not in layout_args:
                issues.append("Figure is missing y-axis label.")
        if method_name == 'update_xaxes':
            if 'title_text' not in layout_args:
                issues.append("Figure is missing x-axis label.")
        if method_name == 'update_yaxes':
            if 'title_text' not in layout_args:
                issues.append("Figure is missing y-axis label.")
        if issues:
            self.figure_issues.extend(issues)

    def visit_Try(self, node):
        self.try_except_blocks.append(node)
        self.generic_visit(node)

    def visit_Global(self, node):
        self.global_variables.update(node.names)
        self.generic_visit(node)

def analyze_code(code):
    analyzer = DashAnalyzer()
    tree = ast.parse(code)
    analyzer.visit(tree)
    feedback = []
    if not analyzer.layout_defined:
        feedback.append("Rule 1 (Consistency): The app layout is not properly defined. Ensure that 'app.layout' is set.")
    component_types = set(analyzer.components.keys())
    if len(component_types) > 0:
        feedback.append(f"Rule 1 (Consistency): The app uses the following components: {', '.join(component_types)}.")
    else:
        feedback.append("Rule 1 (Consistency): No standard components found. Ensure you're using Dash components properly.")
    if re.search(r'KeyBinding|key', code):
        feedback.append("Rule 2 (Shortcuts): Keyboard shortcuts detected, which is good for frequent users.")
    else:
        feedback.append("Rule 2 (Shortcuts): No keyboard shortcuts detected. Consider adding shortcuts for frequent users.")
    if not analyzer.callbacks:
        feedback.append("Rule 3 (Feedback): No callbacks are defined. Consider adding interactivity for better user feedback.")
    else:
        feedback.append(f"Rule 3 (Feedback): {len(analyzer.callbacks)} callbacks defined, providing user feedback through interactivity.")
    if not analyzer.callback_outputs:
        feedback.append("Rule 3 (Feedback): Callbacks do not produce outputs. Ensure outputs are defined for user feedback.")
    else:
        feedback.append(f"Rule 3 (Feedback): Callbacks produce outputs for components: {', '.join(analyzer.callback_outputs)}.")
    if analyzer.user_controls and analyzer.callback_outputs:
        feedback.append("Rule 4 (Closure): User actions lead to visible results, providing a sense of closure.")
    else:
        feedback.append("Rule 4 (Closure): Consider designing interactions that provide closure after user actions.")
    if analyzer.try_except_blocks:
        feedback.append("Rule 5 (Error Handling): Try-except blocks found, indicating error handling is implemented.")
    else:
        feedback.append("Rule 5 (Error Handling): No error handling detected. Implement try-except blocks in callbacks to handle errors gracefully.")
    if 'Reset' in code or 'clear' in code:
        feedback.append("Rule 6 (Reversal): Reset functionality detected, allowing users to reverse actions.")
    else:
        feedback.append("Rule 6 (Reversal): No reversal actions detected. Consider adding a reset button or undo functionality.")
    if analyzer.user_controls:
        feedback.append("Rule 7 (Control): User controls are present, supporting the user's internal locus of control.")
    else:
        feedback.append("Rule 7 (Control): No user controls detected. Add interactive components to give users control.")
    if len(component_types) > 10:
        feedback.append("Rule 8 (Memory Load): Too many components on the screen. Consider simplifying the layout to reduce cognitive load.")
    else:
        feedback.append("Rule 8 (Memory Load): The number of components is manageable, which helps reduce memory load.")
    if analyzer.figure_issues:
        for issue in analyzer.figure_issues:
            feedback.append(f"Chart Issue: {issue}")
    else:
        feedback.append("All charts have proper titles and layouts.")
    return feedback
