class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.advance()

    def advance(self):
        self.position += self.position + 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def parse(self):
        return self.statements()

    def statements(self):
        stmts = []
        while self.current_token is not None:
            stmts.append(self.statement())
        return stmts

    def statement(self):
        if self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'import':
            return self.import_statement()
        elif self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'def':
            return self.function_statement()
        elif self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'class':
            return self.class_statement()
        elif self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'if':
            return self.if_statement()
        elif self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'for':
            return self.for_statement()
        elif self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'while':
            return self.while_statement()
        elif self.current_token['type'] == 'IDENTIFIER' and self.current_token['value'] == 'elif':
            return self.elif_statement()
        else:
            return self.expression_statement()

    def import_statement(self):
        self.advance()
        module_name = self.current_token['value']
        self.advance()
        return {'type': 'IMPORT', 'module': module_name}

    def function_statement(self):
        self.advance()
        func_name = self.current_token['value']
        self.advance()
        params = self.parameters()
        body = self.block()
        return {'type': 'FUNCTION', 'name': func_name, 'params': params, 'body': body}

    def class_statement(self):
        self.advance()
        class_name = self.current_token['value']
        self.advance()
        body = self.block()
        return {'type': 'CLASS', 'name': class_name, 'body': body}

    def if_statement(self):
        self.advance()
        condition = self.expression()
        body = self.block()
        else_body = None
        if self.current_token is not None and self.current_token['value'] == 'else':
            self.advance()
            else_body = self.block()
        return {'type': 'IF', 'condition': condition, 'body': body, 'else_body': else_body}

    def for_statement(self):
        self.advance()
        variable = self.current_token['value']
        self.advance()  # Skip 'in'
        self.advance()  # Skip 'in'
        iterable = self.expression()
        body = self.block()
        return {'type': 'FOR', 'variable': variable, 'iterable': iterable, 'body': body}

    def while_statement(self):
        self.advance()  # Skip 'while'
        condition = self.expression()
        body = self.block()
        return {'type': 'WHILE', 'condition': condition, 'body': body}

    def elif_statement(self):
        self.advance()  # Skip 'elif'
        condition = self.expression()
        body = self.block()
        return {'type': 'ELIF', 'condition': condition, 'body': body}

    def parameters(self):
        self.advance()  # Skip '('
        params = []
        while self.current_token is not None and self.current_token['value'] != ')':
            params.append(self.current_token['value'])
            self.advance()
            if self.current_token['value'] == ',':
                self.advance()
        self.advance()  # Skip ')'
        return params

    def block(self):
        self.advance()  # Skip '{'
        stmts = self.statements()
        self.advance()  # Skip '}'
        return stmts

    def expression_statement(self):
        expr = self.expression()
        self.advance()  # Skip ';'
        return {'type': 'EXPRESSION', 'expression': expr}

    def expression(self):
        if self.current_token['type'] == 'IDENTIFIER':
            return self.identifier_expression()
        elif self.current_token['type'] == 'NUMBER':
            return self.number_expression()
        elif self.current_token['type'] == 'STRING':
            return self.string_expression()
        elif self.current_token['type'] == 'SYMBOL' and self.current_token['value'] in ('+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>='):
            return self.binary_op_expression()

    def identifier_expression(self):
        identifier = self.current_token['value']
        self.advance()
        return {'type': 'IDENTIFIER', 'value': identifier}

    def number_expression(self):
        number = self.current_token['value']
        self.advance()
        return {'type': 'NUMBER', 'value': number}

    def string_expression(self):
        string = self.current_token['value']
        self.advance()
        return {'type': 'STRING', 'value': string}

    def binary_op_expression(self):
        left = self.expression()
        op = self.current_token['value']
        self.advance()
        right = self.expression()
        return {'type': 'BINARY_OP', 'left': left, 'op': op, 'right': right}
