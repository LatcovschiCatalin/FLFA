import re


class ArithmeticLexer:
    def __init__(self):
        # Rules for the arithmetic expressions
        self.rules = [
            (r'[ \t]+', None),  # Ignore whitespace
            (r'\d+\.\d+', 'FLOAT'),
            (r'\d+', 'INTEGER'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MUL'),
            (r'/', 'DIV'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
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
                # Yield an 'ILLEGAL' token type for further processing instead of raising an error
                yield ('ILLEGAL', text[pos])
                pos += 1
            else:
                pos = match.end(0)


def validate_expression(tokens):
    paren_stack = []
    last_token_type = None

    for token in tokens:
        token_type, token_value = token

        # Check for illegal tokens
        if token_type == 'ILLEGAL':
            return False, f"Illegal character found: {token_value}"

        # Check for balanced parentheses
        if token_type == 'LPAREN':
            paren_stack.append(token_value)
        elif token_type == 'RPAREN':
            if not paren_stack:
                return False, "Unbalanced parentheses"
            paren_stack.pop()

        # Check for valid sequences
        if last_token_type in ['PLUS', 'MINUS', 'MUL', 'DIV']:
            if token_type in ['PLUS', 'MINUS', 'MUL', 'DIV', 'RPAREN']:
                return False, "Invalid operator usage"
        if last_token_type == 'LPAREN' and token_type in ['PLUS', 'MINUS', 'MUL', 'DIV', 'RPAREN']:
            return False, "Invalid expression after '('"
        if last_token_type in ['INTEGER', 'FLOAT', 'RPAREN'] and token_type == 'LPAREN':
            return False, "Invalid expression before '('"

        last_token_type = token_type

    if paren_stack:
        return False, "Unbalanced parentheses"

    return True, "Valid expression"


# Example usage
lexer = ArithmeticLexer()
expression = '(3.14 + 2 * (1 - 5))'
tokens = list(lexer.tokenize(expression))
is_valid, message = validate_expression(tokens)
print(f"Expression: {expression}")
print(f"Tokens: {tokens}")
print(f"Validation: {message}")
