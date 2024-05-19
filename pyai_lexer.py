import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_token = ''
        self.current_char = ''
        self.position = -1
        self.advance()

    def advance(self):
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def add_token(self, type, value):
        self.tokens.append({'type': type, 'value': value})
        self.current_token = ''

    def tokenize(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif re.match(r'[a-zA-Z_]', self.current_char):
                self.identifier()
            elif self.current_char.isdigit():
                self.number()
            elif self.current_char == '"':
                self.string()
            elif self.current_char == '#':
                self.comment()
            else:
                self.symbol()
                self.advance()
        return self.tokens

    def identifier(self):
        while self.current_char is not None and re.match(r'[a-zA-Z0-9_]', self.current_char):
            self.current_token += self.current_char
            self.advance()
        self.add_token('IDENTIFIER', self.current_token)

    def number(self):
        while self.current_char is not None and self.current_char.isdigit():
            self.current_token += self.current_char
            self.advance()
        self.add_token('NUMBER', self.current_token)

    def string(self):
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            self.current_token += self.current_char
            self.advance()
        self.advance()
        self.add_token('STRING', self.current_token)

    def comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()

    def symbol(self):
        self.add_token('SYMBOL', self.current_char)
