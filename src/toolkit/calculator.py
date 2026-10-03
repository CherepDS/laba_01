import re
from .errors import *
from .utils import save_calc
from decimal import Decimal, ROUND_HALF_UP

operations = {
    "+": {"precedence": 1},
    "-": {"precedence": 1},
    "*": {"precedence": 2},
    "/": {"precedence": 2},
    "//": {"precedence": 2},
    "%": {"precedence": 3},
}

# Получение последнего элемента списка
def get_token(expr):
    if expr:
        return expr[0]
    return ""

# Проверка, является ли данная строка допустимым операндом
def is_operand(token):
    int_operand = r"(?<![\d)])[+-]{0,1}\d+"
    float_operand = r"(?<![\d)])[+-]{0,1}\d+\.\d+"
    reg = f"{int_operand}|{float_operand}"
    if re.fullmatch(reg, token):
        return True
    else:
        return False

# Разбиение входной строки на токены
# 1. унарный знак(необяз.) целый операнд
# 2. унарный знак(необяз.) дробный операнд
# 3. скобки
# 4. знаки операций (некоторые экранированы)
def tokenization(expr):
    expr = expr.replace(" ","")
    tokens = []
    int_operand = r"(?<![\d)])[+-]{0,1}\d+"
    float_operand = r"(?<![\d)])[+-]{0,1}\d+\.\d+"
    bracket = r"[()]"
    operation = r"//|[+\-\/*%]"
    reg = f"{float_operand}|{int_operand}|{operation}|{bracket}"
    for token in re.finditer(reg, expr):
        tokens.append(token.group())
    if len("".join(tokens)) == len(expr):
        return tokens
    else:
        raise InvalidOperand()


# Представление токенов в обратной польской записи
# За основу принят алгоритм сортировочной станции (Эдсгер Дейкстра)
def rpn_covert(tokens):
    result = []
    stack = []
    expect = ("operand",)

    for token in tokens:
        if is_operand(token) and "operand" in expect:
            result.append(token)
            expect = ("operation", "close_bracket")
        elif token == '(' and "open_bracket" in expect:
            stack.append(token)
            expect = ("operand", "open_bracket")
        elif token == ')' and "close_bracket" in expect:
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            if stack:
                stack.pop()
                expect = ("operation", "close_bracket")
            else:
                raise InvalidBracket()
        elif token in operations and "operation" in expect:
            while (stack and stack[-1] in operations and operations[stack[-1]]["precedence"] >= operations[token]["precedence"]):
                result.append(stack.pop())
            stack.append(token)
            expect = ("operand", "open_bracket")
        else:
            raise InvalidOrder()
    while stack:
        result.append(stack.pop())
    return result

# Вычисление выражения с помощью обратной польской записи
def rpn_calc(expr):
    stack = []
    while tok := get_token(expr):
        if is_operand(tok):
            stack.append(Decimal(tok))
        elif tok in operations:
            if len(stack)>1:
                op1 = stack.pop()
                op2 = stack.pop()
            else:
                raise CalcExpression()

            match tok:
                case '+':
                    res = op2 + op1
                case '-':
                    res = op2 - op1
                case '*':
                    res = op2 * op1
                case '/':
                    if op1 == 0:
                        raise DivisionByZero()
                    res = op2 / op1
                case "//":
                    if op1 == 0:
                        raise DivisionByZero()
                    res = op2 // op1
                case "%":
                    res = op2 % op1
                case _:
                    raise CalcExpression()
            stack.append(res)
        else:
            raise CalcExpression()

        expr = expr[1:]

    if stack:
        return stack.pop().quantize(Decimal("1.000"), rounding=ROUND_HALF_UP).normalize()
    else:
        raise CalcExpression()

def calculate(expr):
    tokens = tokenization(expr)
    rpn_expr = rpn_covert(tokens)
    res = rpn_calc(rpn_expr)
    save_calc(expr, str(res))
    return res
