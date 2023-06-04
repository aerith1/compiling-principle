class OperatorPrecedenceParser:
    def __init__(self):
        self.operators = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2, '(': -1, ')': -1}

    def has_higher_precedence(self, op1, op2):
        return self.operators[op1] >= self.operators[op2]

    def parse_expression(self, expression):
        stack = []
        output = []

        for token in expression:
            if token.isdigit():
                output.append(token)
            elif token in self.operators:
                if token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    if stack and stack[-1] == '(':
                        stack.pop()
                else:
                    while stack and stack[-1] != '(' and self.has_higher_precedence(stack[-1], token):
                        output.append(stack.pop())
                    stack.append(token)

        while stack:
            output.append(stack.pop())

        return output

    def evaluate_expression(self, expression):
        stack = []

        for token in expression:
            if token.isdigit():
                stack.append(int(token))
            elif token in self.operators:
                if token == '^':
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    result = operand1 ** operand2
                else:
                    operand2 = stack.pop()
                    operand1 = stack.pop()

                    if token == '+':
                        result = operand1 + operand2
                    elif token == '-':
                        result = operand1 - operand2
                    elif token == '*':
                        result = operand1 * operand2
                    elif token == '/':
                        result = operand1 / operand2

                stack.append(result)

        return stack.pop()


# 测试示例
parser = OperatorPrecedenceParser()

expression = '3+4*2/(1-5)^2'
parsed_expression = parser.parse_expression(expression)
print("Parsed expression:", parsed_expression)

result = parser.evaluate_expression(parsed_expression)
print("Result:", result)
