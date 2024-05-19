class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.functions = {}
        self.classes = {}

    def interpret(self):
        for stmt in self.ast:
            self.execute(stmt)

    def execute(self, stmt):
        if stmt['type'] == 'IMPORT':
            self.import_module(stmt['module'])
        elif stmt['type'] == 'FUNCTION':
            self.define_function(stmt['name'], stmt['params'], stmt['body'])
        elif stmt['type'] == 'CLASS':
            self.define_class(stmt['name'], stmt['body'])
        elif stmt['type'] == 'IF':
            self.if_statement(stmt)
        elif stmt['type'] == 'FOR':
            self.for_statement(stmt)
        elif stmt['type'] == 'WHILE':
            self.while_statement(stmt)
        elif stmt['type'] == 'ELIF':
            self.elif_statement(stmt)
        elif stmt['type'] == 'EXPRESSION':
            self.evaluate(stmt['expression'])

    def import_module(self, module):
        exec(f"import {module}")

    def define_function(self, name, params, body):
        self.functions[name] = {'params': params, 'body': body}

    def define_class(self, name, body):
        self.classes[name] = body

    def if_statement(self, stmt):
        condition = self.evaluate(stmt['condition'])
        if condition:
            self.execute_block(stmt['body'])
        elif stmt['else_body'] is not None:
            self.execute_block(stmt['else_body'])

    def for_statement(self, stmt):
        iterable = self.evaluate(stmt['iterable'])
        for item in iterable:
            self.variables[stmt['variable']] = item
            self.execute_block(stmt['body'])

    def while_statement(self, stmt):
        while self.evaluate(stmt['condition']):
            self.execute_block(stmt['body'])

    def elif_statement(self, stmt):
        condition = self.evaluate(stmt['condition'])
        if condition:
            self.execute_block(stmt['body'])

    def evaluate(self, expr):
        if expr['type'] == 'IDENTIFIER':
            return self.variables.get(expr['value'])
        elif expr['type'] == 'NUMBER':
            return int(expr['value'])
        elif expr['type'] == 'STRING':
            return str(expr['value'])
        elif expr['type'] == 'BINARY_OP':
            left = self.evaluate(expr['left'])
            right = self.evaluate(expr['right'])
            op = expr['op']
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<':
                return left < right
            elif op == '>':
                return left > right
            elif op == '<=':
                return left <= right
            elif op == '>=':
                return left >= right

    def execute_block(self, stmts):
        for stmt in stmts:
            self.execute(stmt)
