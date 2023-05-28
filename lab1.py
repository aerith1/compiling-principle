class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_index = 0
        self.token_buffer = []

    def get_next_char(self):
        if self.current_index < len(self.source_code):
            char = self.source_code[self.current_index]
            self.current_index += 1
            return char
        else:
            return None
    
    def analyze_tokens(self):
        keyword_table = {
            'BEGIN': 'BEGIN',
            'DO': 'DO',
            'ELSE': 'ELSE',
            'END': 'END',
            'IF': 'IF',
            'THEN': 'THEN',
            'VAR': 'VAR',
            'WHILE': 'WHILE'
        }

        delimiter_table = {
            ',': ',',
            ';': ';',
            '.': '.',
            ':': ':',
            '=': '=', 
            '(': '(',
            ')': ')'
        }

        def add_token(token_type, token_value):
            self.token_buffer.append((token_type, token_value))

        def is_keyword(token):
            return token in keyword_table

        char = self.get_next_char()

        while char is not None:
            if char.isalpha():
                # 处理标识符或关键字
                identifier = char
                char = self.get_next_char()

                while char is not None and (char.isalpha() or char.isdigit()):
                    identifier += char
                    char = self.get_next_char()

                if is_keyword(identifier):
                    add_token('KEYWORD', keyword_table[identifier])
                else:
                    add_token('IDENTIFIER', identifier)

            elif char.isdigit():
                # 处理常数
                constant = char
                char = self.get_next_char()

                while char is not None and char.isdigit():
                    constant += char
                    char = self.get_next_char()

                add_token('CONSTANT', constant)
            
            elif char == ':':
                # operator
                next_char = self.get_next_char()

                if next_char == '=':
                    add_token('OPERATOR', ':=')
                    char = self.get_next_char()
                else:
                    # delimiter
                    add_token('DELIMITER', ':')
                    char = next_char

            elif char in delimiter_table:
                # 处理分界符
                add_token('DELIMITER', delimiter_table[char])
                char = self.get_next_char()

            elif char in ['+', '-', '*', '/', '。', '<', '=', '>']:
                # 处理运算符
                operator = char
                char = self.get_next_char()

                # 检查是否是双字符运算符
                if char is not None and char == '=' and operator in ['<', '>', ':']:
                    operator += char
                    char = self.get_next_char()
                
                add_token('OPERATOR', operator)
            else:
                # 处理错误或未识别的字符
                add_token('ERROR', char)
                char = self.get_next_char()
    def get_tokens(self):
        return self.token_buffer

file_path = "input.txt"
file = open(file_path, "r")

file_content = file.read()

file.close()

source_code = file_content
lexer = Lexer(source_code)

# 执行词法分析
lexer.analyze_tokens()

tokens = lexer.get_tokens()

# 输出
for token_type, token_value in tokens:
    print(token_type, token_value)
