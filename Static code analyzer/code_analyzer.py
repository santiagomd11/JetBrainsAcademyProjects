# write your code here
import os
import re
import sys
import ast


class StaticCodeAnalyzer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.errors = {"S001": "Too long",
                       "S002": "Indentation is not a multiple of four",
                       "S003": "Unnecessary semicolon after a statement",
                       "S004": "Less than two spaces before inline comments",
                       "S005": "TODO found ",
                       "S006": "More than two blank lines preceding a code line",
                       "S007": "Too many spaces after construction_name",
                       "S008": "Class name class_name should be written in CamelCase",
                       "S009": "Function name function_name should be written in snake_case",
                       "S010": "Argument name arg_name should be written in snake_case",
                       "S011": "Variable var_name should be written in snake_case",
                       "S012": "The default argument value is mutable"}
        self.lines = None
        self.blank_lines = 0
        self.func_list = []

    def get_func_list(self, path):
        with open(path, "r") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.func_list.append(node)

    def s001(self, line, line_number, path):
        if len(line) > 79:
            print(f'{path}: Line {line_number}: S001 {self.errors["S001"]}')

    def s002(self, line, line_number, path):
        if line:
            counter = 0
            for element in line:
                if element == ' ':
                    counter += 1
                else:
                    break
            if counter % 4 != 0:
                print(f'{path}: Line {line_number}: S002 {self.errors["S002"]}')

    def s003(self, line, line_number, path):
        if line:
            if re.search("(;  #|; #|\);  #|\);)", line):
                print(f'{path}: Line {line_number}: S003 {self.errors["S003"]}')

    def s004(self, line, line_number, path):
        try:
            comment_index = line.index("#")
            if comment_index != 0:
                if line[comment_index - 2: comment_index].count(" ") != 2:
                    print(f'{path}: Line {line_number}: S004 {self.errors["S004"]}')
        except ValueError:
            pass

    def s005(self, line, line_number, path):
        if "# todo" in line.lower():
            print(f'{path}: Line {line_number}: S005 {self.errors["S005"]}')

    def s006(self, line, line_number, path):
        if not line:
            self.blank_lines += 1
        else:
            if self.blank_lines > 2:
                print(f'{path}: Line {line_number}: S006 {self.errors["S006"]}')
                self.blank_lines = 0
            else:
                self.blank_lines = 0

    def s007(self, line, line_number, path):
        template = r"(class|def)\s{2,}.*"
        if re.search(template, line):
            print(f'{path}: Line {line_number}: S007 {self.errors["S007"]}')
            
    def s008(self, line, line_number, path):
        template = r".*class\s{1,}[A-Z]{1}\w*[A-Z]{0,}\w*"
        if not re.match(template, line):
            print(f'{path}: Line {line_number}: S008 {self.errors["S008"]}')

    def s009(self, line, line_number, path):
        template = r".*def\s{1,}_*[a-z]{1,}_?\w*"
        if not re.match(template, line):
            print(f'{path}: Line {line_number}: S009 {self.errors["S009"]}')

    def s010(self, path):
        template = r"_?^[a-z]+_?[a-z]*_?[a-z]*_?[a-z]*"
        for func in self.func_list:
            for a in func.args.args:
                if not re.match(template, a.arg):
                    print(f'{path}: Line {a.lineno}: S010 {self.errors["S010"].replace("arg_name", a.arg)}')

    def s011(self, path):
        template = r"_?^[a-z]+_?[a-z]*_?[a-z]*_?[a-z]*"
        for func in self.func_list:
            for v in func.body:
                if isinstance(v, ast.Assign):
                    try:
                        var_name = v.targets[0].value.id
                        if not re.match(template, var_name):
                            print(f'{path}: Line {v.lineno}: S011 {self.errors["S011"].replace("var_name", var_name)}')
                    except (AttributeError, ValueError):
                        pass
                    try:
                        var_name = v.targets[0].id
                        if not re.match(template, var_name):
                            print(f'{path}: Line {v.lineno}: S011 {self.errors["S011"].replace("var_name", var_name)}')
                    except (AttributeError, ValueError):
                        pass

    def s012(self, path):
        for func in self.func_list:
            for default in func.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    print(f'{path}: Line {default.lineno}: S012 {self.errors["S012"]}')
                    break

    def analyze_code_file(self, path):
        with open(path, 'r') as f:
            self.lines = f.readlines()
            for line_number, line in enumerate(self.lines, start=1):
                line = line.strip("\n")
                self.s001(line, line_number, path)
                self.s002(line, line_number, path)
                self.s003(line, line_number, path)
                self.s004(line, line_number, path)
                self.s005(line, line_number, path)
                self.s006(line, line_number, path)
                if "class" in line or "def" in line:
                    self.s007(line, line_number, path)
                if "class" in line:
                    self.s008(line, line_number, path)
                if "def" in line:
                    self.s009(line, line_number, path)
        try:
            self.get_func_list(path)
            self.s010(path)
            self.s011(path)
            self.s012(path)
        except Exception as e:
            pass

        self.func_list = []

    def analyze_code_dir(self):
        for root, dirs, files in os.walk(self.input_path, True):
            if dirs:
                for d in dirs:
                    for file in files:
                        if re.search(r".py$", file):
                            try:
                                self.analyze_code_file(os.path.join(root, d, file))
                            except FileNotFoundError:
                                pass
            else:
                files.sort()
                for file in files:
                    if re.search(r".py$", file):
                        self.analyze_code_file(os.path.join(root, file))

    def main(self):
        if re.search(r".py$", self.input_path):
            self.analyze_code_file(self.input_path)
        else:
            self.analyze_code_dir()


if __name__ == '__main__':
    argv = sys.argv
    file_path = argv[1]
    sca = StaticCodeAnalyzer(file_path)
    sca.main()
