import queue
import re


# CLASSES

class Types:
    Number = 0
    Operator = 1
    LeftBracket = 2
    RightBracket = 3


class Token(object):
    def __init__(self, _type, precedence=0, lassoc=False, symbol=''):
        self.type = _type
        self.precedence = precedence
        self.lassoc = lassoc
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Number(Token):
    def __init__(self, value):
        super().__init__(Types.Number)
        self.value = float(value)

    def __str__(self):
        return str(self.value)


# FUNCTIONS

def tokens2str(c):
    s = ''
    for i in range(len(c)):
        end = ''
        if c[i].type == Types.Operator and not c[i].symbol == '^':
            end = ' '
        elif i < len(c) - 1 and c[i + 1].type == Types.Operator and not c[
                    i + 1].symbol == '^':
            end = ' '
        s += str(c[i]) + end
    return s


def tokenise(input_string):
    str2tok = {
        '+': add, '-': sub, '*': mul, '/': div, '^': idx, '(': lb, ')': rb
    }

    tokens = []
    i = 0
    while i < len(input_string):
        numSearch = re.search(r'[\d\.]+', input_string[i:])

        if input_string[i] == ' ':
            input_string = input_string[i + 1:]
        elif input_string[i] in str2tok:
            tokens.append(str2tok[input_string[i]])
            input_string = input_string[i + 1:]
        elif numSearch != None and numSearch.span()[0] == 0:
            num = numSearch.group()
            l = len(num)
            tokens.append(Number(float(num)))
            input_string = input_string[i + l:]

    return tokens


def ShuntingYard(tokens):
    # Shunting-yard Algorithm
    operator_stack = []
    output_queue = queue.Queue()
    while len(tokens) > 0:
        tok = tokens.pop(0)
        if tok.type == Types.Number:
            output_queue.put(tok)
        elif tok.type == Types.Operator:
            if len(operator_stack) > 0:
                while (operator_stack[-1].precedence > tok.precedence) or \
                                ((operator_stack[
                                      -1].precedence == tok.precedence) and
                                     operator_stack[-1].lassoc) and \
                                (operator_stack[-1].type != Types.LeftBracket):
                    output_queue.put(operator_stack.pop())
                    if len(operator_stack) == 0:
                        break
            operator_stack.append(tok)
        elif tok.type == Types.LeftBracket:
            operator_stack.append(tok)
        elif tok.type == Types.RightBracket:
            missing_lb = (len(operator_stack) == 0)
            if not missing_lb:
                while operator_stack[-1].type != Types.LeftBracket:
                    output_queue.put(operator_stack.pop())
                    if len(operator_stack) == 0:
                        missing_lb = True
                        break
                if not missing_lb:
                    operator_stack.pop()
            if missing_lb:
                print('missing (')

    while len(operator_stack) > 0:
        op = operator_stack.pop()
        if op.type == Types.LeftBracket or op.type == Types.RightBracket:
            print('mismatched brackets')
        output_queue.put(op)

    rpn = []
    while not output_queue.empty():
        rpn.append(output_queue.get())
    return rpn


def solveRPN(rpn):
    stack = []
    for token in rpn:
        if token.type == Types.Operator:
            op2 = stack.pop()
            op1 = stack.pop()
            if token.symbol == '^':
                res = Number(op1.value ** op2.value)
            elif token.symbol == '*':
                res = Number(op1.value * op2.value)
            elif token.symbol == '/':
                res = Number(op1.value / op2.value)
            elif token.symbol == '+':
                res = Number(op1.value + op2.value)
            elif token.symbol == '-':
                res = Number(op1.value - op2.value)
            stack.append(res)
        elif token.type == Types.Number:
            stack.append(token)
    return (stack[0].value)


def solveString(string):
    return solveRPN(ShuntingYard(tokenise(string)))


# VARIABLES

lb = Token(Types.LeftBracket, symbol='(')
rb = Token(Types.RightBracket, symbol=')')

idx = Token(Types.Operator, 4, False, '^')
mul = Token(Types.Operator, 3, True, '*')
div = Token(Types.Operator, 3, True, '/')
add = Token(Types.Operator, 2, True, '+')
sub = Token(Types.Operator, 2, True, '-')

if __name__ == '__main__':
    # input string
    string = '12+(( ((169 / 2^2) +17*12.5/2) +(18.5*(128 /8)+ 16.5)* 69.69+12.911 ) / 2)'

    # tokenise and get formatted string
    tokens = tokenise(string)
    formatted = tokens2str(tokens)

    # Convert infix notation to Reverse Polish Notation (RPN)
    #   using Dijkstra's Shunting-yard Algorithm
    rpn = ShuntingYard(tokens)

    # solve RPN
    ans = solveRPN(rpn)

    print(formatted, '=', ans)
