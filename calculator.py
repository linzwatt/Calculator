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

    def getValue(self):
        return self.value

    def __str__(self):
        return str(self.getValue())


class Var(Number):
    def __init__(self, _id, value=0.0):
        super().__init__(0)
        self.id = _id
        if _id not in varTable:
            varTable[_id] = float(value)

    def getValue(self):
        return varTable[self.id]


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


def tokenise(string):
    str2tok = {
        '+': add, '-': sub, '*': mul, '/': div, '^': idx, '(': lb, ')': rb
    }

    token_list = []
    i = 0
    while i < len(string):
        numSearch = re.search(r'[\d\.]+', string[i:])
        varSearch = re.search(r'[a-zA-Z]+', string[i:])

        if string[i] == ' ':
            string = string[i + 1:]
        elif string[i] in str2tok:
            token_list.append(str2tok[string[i]])
            string = string[i + 1:]
        elif varSearch is not None and varSearch.span()[0] == 0:
            var = varSearch.group()
            token_list.append(Var(var))
            string = string[i + len(var):]
        elif numSearch is not None and numSearch.span()[0] == 0:
            num = numSearch.group()
            l = len(num)
            token_list.append(Number(float(num)))
            string = string[i + l:]

    return token_list


def ShuntingYard(token_list):
    # Shunting-yard Algorithm
    operator_stack = []
    output_queue = queue.Queue()
    while len(token_list) > 0:
        tok = token_list.pop(0)
        if tok.type == Types.Number:
            output_queue.put(tok)
        elif tok.type == Types.Operator:
            if len(operator_stack) > 0:
                while (operator_stack[-1].precedence > tok.precedence) or \
                        ((operator_stack[-1].precedence == tok.precedence) and operator_stack[-1].lassoc) and \
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


def solveRPN(rpn_list):
    stack = []
    for token in rpn_list:
        if token.type == Types.Operator:
            op2 = stack.pop()
            op1 = stack.pop()
            res = 0
            if token.symbol == '^':
                res = Number(op1.getValue() ** op2.getValue())
            elif token.symbol == '*':
                res = Number(op1.getValue() * op2.getValue())
            elif token.symbol == '/':
                res = Number(op1.getValue() / op2.getValue())
            elif token.symbol == '+':
                res = Number(op1.getValue() + op2.getValue())
            elif token.symbol == '-':
                res = Number(op1.getValue() - op2.getValue())
            stack.append(res)
        elif token.type == Types.Number:
            stack.append(token)
    return stack[0].getValue()


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

varTable = {
    'ans': 0.0,
    'num': 169.0,
    'A': 2
}

if __name__ == '__main__':
    # input string
    input_string = '12+(( ((num / 2^2) +17*12.5/2) +(18.5*(128 /8)+ 16.5)* 69.69+12.911 ) / A)'
    eval_string = input_string
    for k, v in varTable.items():
        eval_string = eval_string.replace(k, str(v))
    eval_ans = eval(eval_string.replace('^', '**'))

    # tokenise and get formatted string
    tokens = tokenise(input_string)
    formatted = tokens2str(tokens)

    # Convert infix notation to Reverse Polish Notation (RPN)
    #   using Dijkstra's Shunting-yard Algorithm
    rpn = ShuntingYard(tokens)

    for t in rpn:
        print(t, end=' ')
    print()

    # solve RPN
    ans = solveRPN(rpn)

    print(formatted, '=', ans)

    assert ((ans - eval_ans) < float(1e-16)), "Answer does not match eval()"
