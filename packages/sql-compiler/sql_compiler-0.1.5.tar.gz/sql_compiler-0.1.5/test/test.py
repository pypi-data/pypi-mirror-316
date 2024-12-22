from rply import LexerGenerator, ParserGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Define tokens with improved regex patterns
        self.lexer.add('PRINT', r'print')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('DIV', r'/')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('RPAREN', r'\)')
        self.lexer.add('LPAREN', r'\(')
        # Support for floating point numbers
        self.lexer.add('NUMBER', r'\d*\.\d+|\d+\.?')
        self.lexer.add('ID', r'[a-zA-Z_][a-zA-Z0-9_]*')
        # Improved whitespace handling
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

    def tokenize(self, text):
        """Tokenize input text and return list of tokens"""
        lexer = self.get_lexer()
        return list(lexer.lex(text))

class AST:
    class Number:
        def __init__(self, value):
            self.value = float(value)
        
        def eval(self):
            return self.value

    class BinaryOp:
        def __init__(self, left, right):
            self.left = left
            self.right = right

    class Add(BinaryOp):
        def eval(self):
            return self.left.eval() + self.right.eval()

    class Subtract(BinaryOp):
        def eval(self):
            return self.left.eval() - self.right.eval()

    class Multiply(BinaryOp):
        def eval(self):
            return self.left.eval() * self.right.eval()

    class Divide(BinaryOp):
        def eval(self):
            right_val = self.right.eval()
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return self.left.eval() / right_val()

    class Print:
        def __init__(self, expression):
            self.expression = expression
        
        def eval(self):
            result = self.expression.eval()
            print(result)
            return result

class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            ['PRINT', 'NUMBER', 'PLUS', 'DIV', 'SUB', 'MUL', 
             'LPAREN', 'RPAREN', 'ID'],
        )
        self._define_grammar()

    def _define_grammar(self):
        @self.pg.production('program : PRINT LPAREN expression RPAREN')
        def program(p):
            return AST.Print(p[2])

        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression(p):
            left, op, right = p[0], p[1], p[2]
            
            if op.gettokentype() == 'PLUS':
                return AST.Add(left, right)
            elif op.gettokentype() == 'SUB':
                return AST.Subtract(left, right)
            elif op.gettokentype() == 'MUL':
                return AST.Multiply(left, right)
            elif op.gettokentype() == 'DIV':
                return AST.Divide(left, right)

        @self.pg.production('expression : NUMBER')
        def number(p):
            return AST.Number(p[0].value)

        @self.pg.production('expression : LPAREN expression RPAREN')
        def paren_expr(p):
            return p[1]

        @self.pg.error
        def error(token):
            raise ValueError(f"Syntax error at token: {token}")

    def get_parser(self):
        return self.pg.build()

class Interpreter:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self._parser = self.parser.get_parser()

    def evaluate(self, text):
        try:
            # Tokenize
            tokens = self.lexer.tokenize(text)
            
            # Parse
            ast = self._parser.parse(iter(tokens))
            
            # Evaluate
            return ast.eval()
        except Exception as e:
            return f"Error: {str(e)}"

interpreter = Interpreter()
    
    # Test cases
test_inputs = [
        "print(3 + 4 * 2)",
        "print((3 + 4) * 2)",
        "print(3.14 * 2)",
        "print(1 / 0)",  # Error handling
        "print(10 - 5 + 3)"
    ]
    
for test in test_inputs:
        print(f"\nInput: {test}")
        result = interpreter.evaluate(test)
        print(f"Result: {result}")