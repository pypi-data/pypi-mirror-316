import ply.lex as lex
import ply.yacc as yacc
from typing import List, Tuple, Union, Any

# --- Lexer ---
reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

tokens = [
    'IDENTIFIER', 'STRING', 'NUMBER',
    'EQUALS', 'GREATER', 'LESS', 'GREATER_EQUALS', 'LESS_EQUALS', 'NOT_EQUALS',
    'LPAREN', 'RPAREN', 'SEMICOLON', 'COMMA', 'ASTERISK'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUALS = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATER_EQUALS = r'>='
t_LESS_EQUALS = r'<='
t_NOT_EQUALS = r'!=|<>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_ASTERISK = r'\*'

# Ignored characters
t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Check for reserved words
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\'[^\']*\'|"[^"]*"'
    # Strip quotes and handle escape sequences
    t.value = t.value[1:-1].replace('\\"', '"').replace("\\'", "'")
    return t

def t_NUMBER(t):
    r'-?\d*\.?\d+'
    # Handle both integers and floating point numbers
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, position {t.lexpos}")

# --- Parser ---
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQUALS', 'NOT_EQUALS', 'GREATER', 'LESS', 'GREATER_EQUALS', 'LESS_EQUALS'),
)

class SQLQuery:
    def __init__(self, columns: List[str], table: str, condition: Any = None):
        self.columns = columns
        self.table = table
        self.condition = condition

    def __str__(self) -> str:
        columns_str = ', '.join(self.columns)
        query = f"SELECT {columns_str} FROM {self.table}"
        if self.condition:
            query += f" WHERE {self.condition}"
        return query + ";"

def p_query(p):
    '''query : SELECT select_columns FROM table where_clause SEMICOLON'''
    p[0] = SQLQuery(columns=p[2], table=p[4], condition=p[5])

def p_select_columns(p):
    '''select_columns : ASTERISK
                     | column_list'''
    p[0] = ['*'] if p[1] == '*' else p[1]

def p_column_list(p):
    '''column_list : IDENTIFIER
                  | column_list COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_table(p):
    'table : IDENTIFIER'
    p[0] = p[1]

def p_where_clause(p):
    '''where_clause : WHERE condition
                   | empty'''
    p[0] = p[2] if p[1] else None

def p_condition(p):
    '''condition : condition AND condition
                | condition OR condition
                | NOT condition
                | LPAREN condition RPAREN
                | comparison'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ('NOT', p[2])
    else:
        p[0] = p[1]

def p_comparison(p):
    '''comparison : IDENTIFIER compare_op value'''
    p[0] = (p[2], p[1], p[3])

def p_compare_op(p):
    '''compare_op : EQUALS
                 | NOT_EQUALS
                 | GREATER
                 | LESS
                 | GREATER_EQUALS
                 | LESS_EQUALS'''
    p[0] = p[1]

def p_value(p):
    '''value : STRING
             | NUMBER
             | IDENTIFIER'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' (line {p.lineno}, position {p.lexpos})")
    else:
        raise SyntaxError("Syntax error at EOF")

# --- Query Executor ---
class SQLExecutor:
    def __init__(self):
        self.lexer = lex.lex()
        self.parser = yacc.yacc()
        
    def parse(self, query: str) -> SQLQuery:
        """Parse a SQL query string into a SQLQuery object."""
        return self.parser.parse(query)
    
    def execute(self, query: str) -> None:
        """Execute a SQL query and print the execution plan."""
        try:
            parsed_query = self.parse(query)
            print("Execution Plan:")
            print(f"Operation: SELECT")
            print(f"Columns: {', '.join(parsed_query.columns)}")
            print(f"From Table: {parsed_query.table}")
            if parsed_query.condition:
                print(f"Where Condition: {self._format_condition(parsed_query.condition)}")
            return parsed_query
        except (SyntaxError, ValueError) as e:
            print(f"Error executing query: {str(e)}")
            return None
    
    def _format_condition(self, condition: Tuple) -> str:
        """Format a condition tuple into a readable string."""
        if isinstance(condition, tuple):
            if len(condition) == 3:
                if condition[0] in ('AND', 'OR'):
                    left = self._format_condition(condition[1])
                    right = self._format_condition(condition[2])
                    return f"({left} {condition[0]} {right})"
                else:
                    return f"{condition[1]} {condition[0]} {condition[2]}"
            elif len(condition) == 2 and condition[0] == 'NOT':
                return f"NOT ({self._format_condition(condition[1])})"
        return str(condition)

def main():
    executor = SQLExecutor()
    
    # Example queries
    test_queries = [
        'SELECT * FROM users WHERE age >= 25 AND (name = "John" OR city = "New York");',
        'SELECT id, name, age FROM employees WHERE salary > 50000;',
        'SELECT department, count FROM statistics WHERE value != 0;'
    ]
    
    print("Testing SQL Parser with example queries:\n")
    for query in test_queries:
        print(f"Query: {query}")
        result = executor.execute(query)
        if result:
            print(f"Parsed successfully: {result}")
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()