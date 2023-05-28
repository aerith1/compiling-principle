def ZC():
    while True:
        expression = input("请输入算术表达式（输入'q'退出）：")
        if expression.lower() == 'q':
            break
        result, _ = E(expression, 0)
        if result and _ == len(expression):
            print("算术表达式语法正确")
        else:
            print("算术表达式语法错误")

def E(expression, index):
    result, index = T(expression, index)
    while index < len(expression) and expression[index] in ('+', '-'):
        operator = expression[index]
        index += 1
        temp_result, index = T(expression, index)
        if temp_result is not None:
            result = result + operator + temp_result
        else:
            return None, index
    return result, index

def T(expression, index):
    result, index = F(expression, index)
    while index < len(expression) and expression[index] in ('*', '/'):
        operator = expression[index]
        index += 1
        temp_result, index = F(expression, index)
        if temp_result is not None:
            result = result + operator + temp_result
        else:
            return None, index
    return result, index

def F(expression, index):
    if index < len(expression):
        if expression[index].isdigit():
            number = expression[index]
            return number, index + 1
        elif expression[index] == '(':
            result, index = E(expression, index + 1)
            if index < len(expression) and expression[index] == ')':
                return '(' + result + ')', index + 1
    return None, index

ZC()
