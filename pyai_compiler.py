class Compiler:
    def __init__(self, ast):
        self.ast = ast
        self.python_code = ""

    def compile(self):
        self.python_code = ""
        for stmt in self.ast:
            self.python_code += self.compile_statement(stmt) + "\n"
        return self.python_code

    def compile_statement(self, stmt):
        if stmt['type'] == 'IMPORT':
            return f"import {stmt['module']}"
        elif stmt['type'] == 'FUNCTION':
            return self.compile_function(stmt)
        elif stmt['type'] == 'CLASS':
            return self.compile_class(stmt)
        elif stmt['type'] == 'IF':
            return self.compile_if(stmt)
        elif stmt['type'] == 'FOR':
            return self.compile_for(stmt)
        elif stmt['type'] == 'WHILE':
            return self.compile_while(stmt)
        elif stmt['type'] == 'EXPRESSION':
            return self.compile_expression(stmt['expression'])

    def compile_function(self, stmt):
        params = ", ".join(stmt['params'])
        body = "\n".join([self.compile_statement(s) for s in stmt['body']])
        return f"def {stmt['name']}({params}):\n    {body.replace('\n', '\n    ')}"

    def compile_class(self, stmt):
        body = "\n".join([self.compile_statement(s) for s in stmt['body']])
        return f"class {stmt['name']}:\n    {body.replace('\n', '\n    ')}"

    def compile_if(self, stmt):
        condition = self.compile_expression(stmt['condition'])
        body = "\n".join([self.compile_statement(s) for s in stmt['body']])
        code = f"if {condition}:\n    {body.replace('\n', '\n    ')}"
        if stmt.get('else_body'):
            else_body = "\n".join([self.compile_statement(s) for s in stmt['else_body']])
            code += f"\nelse:\n    {else_body.replace('\n', '\n    ')}"
        return code

    def compile_for(self, stmt):
        variable = stmt['variable']
        iterable = self.compile_expression(stmt['iterable'])
        body = "\n".join([self.compile_statement(s) for s in stmt['body']])
        return f"for {variable} in {iterable}:\n    {body.replace('\n', '\n    ')}"

    def compile_while(self, stmt):
        condition = self.compile_expression(stmt['condition'])
        body = "\n".join([self.compile_statement(s) for s in stmt['body']])
        return f"while {condition}:\n    {body.replace('\n', '\n    ')}"

    def compile_expression(self, expr):
        if expr['type'] == 'IDENTIFIER':
            return expr['value']
        elif expr['type'] == 'NUMBER':
            return str(expr['value'])
        elif expr['type'] == 'STRING':
            return f'"{expr['value']}"'
        elif expr['type'] == 'BINARY_OP':
            left = self.compile_expression(expr['left'])
            right = self.compile_expression(expr['right'])
            op = expr['op']
            return f"{left} {op} {right}"
