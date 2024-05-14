from enum import Enum, auto
import re

class TokenType(Enum):
    FLOAT = auto()
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    ILLEGAL = auto()

class ArithmeticLexer:
    def __init__(self):
        self.rules = [
            (r'[ \t]+', None),  # Ignore whitespace
            (r'\d+\.\d+', TokenType.FLOAT),
            (r'\d+', TokenType.INTEGER),
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MUL),
            (r'/', TokenType.DIV),
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
        ]
        self.rules = [(re.compile(pattern), token_type) for (pattern, token_type) in self.rules]

    def tokenize(self, text):
        pos = 0
        while pos < len(text):
            match = None
            for pattern, token_type in self.rules:
                regex_match = pattern.match(text, pos)
                if regex_match:
                    match = regex_match
                    if token_type:  # Ignore tokens like whitespace
                        yield (token_type, regex_match.group(0))
                    break
            if not match:
                yield (TokenType.ILLEGAL, text[pos])
                pos += 1
            else:
                pos = match.end(0)

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"BinaryOperation({self.left}, {self.operator}, {self.right})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.expression()

    def expression(self):
        node = self.term()
        while self.current_token() in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token()
            self.eat(token)
            node = BinaryOperation(node, token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token() in (TokenType.MUL, TokenType.DIV):
            token = self.current_token()
            self.eat(token)
            node = BinaryOperation(node, token, self.factor())
        return node

    def factor(self):
        token = self.current_token()
        if token == TokenType.INTEGER:
            value = int(self.current_value())
            self.eat(TokenType.INTEGER)
            return Number(value)
        elif token == TokenType.FLOAT:
            value = float(self.current_value())
            self.eat(TokenType.FLOAT)
            return Number(value)
        elif token == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise ValueError(f"Unexpected token: {token}")

    def eat(self, token_type):
        if self.current_token() == token_type:
            self.pos += 1
        else:
            raise Exception(f"Unexpected token: {self.current_token()}")

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None

    def current_value(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][1]
        return None

def validate_expression(tokens):
    paren_stack = []
    last_token_type = None

    for token in tokens:
        token_type, token_value = token

        # Check for illegal tokens
        if token_type == TokenType.ILLEGAL:
            return False, f"Illegal character found: {token_value}"

        # Check for balanced parentheses
        if token_type == TokenType.LPAREN:
            paren_stack.append(token_value)
        elif token_type == TokenType.RPAREN:
            if not paren_stack:
                return False, "Unbalanced parentheses"
            paren_stack.pop()

        # Check for valid sequences
        if last_token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV]:
            if token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.RPAREN]:
                return False, "Invalid operator usage"
        if last_token_type == TokenType.LPAREN and token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.RPAREN]:
            return False, "Invalid expression after '('"
        if last_token_type in [TokenType.INTEGER, TokenType.FLOAT, TokenType.RPAREN] and token_type == TokenType.LPAREN:
            return False, "Invalid expression before '('"

        last_token_type = token_type

    if paren_stack:
        return False, "Unbalanced parentheses"

    return True, "Valid expression"

# Example usage
lexer = ArithmeticLexer()
expression = '(3.14 + 2 * (1 - 5))'
tokens = list(lexer.tokenize(expression))

# Validate the tokens before parsing
is_valid, message = validate_expression(tokens)
if not is_valid:
    print(f"Validation: {message}")
else:
    # Parse the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}")
