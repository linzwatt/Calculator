import re


class OpCats:
    NUMBER, FUNCTION, EXP, MUL_DIV, ADD_SUB, BRACKET = range(6)


class Ops:
    COS, SIN, SQRT, EXP, MUL, DIV, ADD, SUB, LEFT_BRACKET, RIGHT_BRACKET, NUMBER = range(11)

str2op = {
    '+': Ops.ADD,
    '-': Ops.SUB,
    '*': Ops.MUL,
    '/': Ops.DIV,
    '^': Ops.EXP,
    '(': Ops.LEFT_BRACKET,
    ')': Ops.RIGHT_BRACKET,
    'cos': Ops.COS,
    'sin': Ops.SIN,
    'sqrt': Ops.SQRT
}

op2str = {v: k for k, v in str2op.items()}


class Op(object):
    def __init__(self, opType, value=None):
        self.type = opType
        self.value = value
        self.cat = -1
        if self.type == Ops.ADD or self.type == Ops.SUB:
            self.cat = OpCats.ADD_SUB
        elif self.type == Ops.MUL or self.type == Ops.DIV:
            self.cat = OpCats.MUL_DIV
        elif self.type == Ops.EXP:
            self.cat = OpCats.EXP
        elif self.type == Ops.LEFT_BRACKET or self.type == Ops.RIGHT_BRACKET:
            self.cat = OpCats.BRACKET
        elif self.type > 6:
            self.cat = OpCats.FUNCTION

    def __repr__(self):
        if self.type == Ops.NUMBER:
            return str(self.value)
        else:
            return op2str[self.type]


def formatCalc(c):
    s = ''
    for i in range(len(c)):
        end = ''
        if c[i].cat in [OpCats.ADD_SUB, OpCats.MUL_DIV]:
            end = ' '
        elif i < len(c) - 1 and c[i+1].cat in [OpCats.ADD_SUB, OpCats.MUL_DIV]:
                end = ' '
        s += str(c[i]) + end
    return s


def solve(c):

    numOps = len(c) // 2

    print(c)

    res = None
    for i in range(numOps):
        smallest = 1e99
        opIndex = -1
        for n in range(0, len(c)):
            if c[n].type < smallest and c[n].cat != c[opIndex].cat:
                smallest = c[n].type
                opIndex = n

        print(opIndex)
        if c[opIndex].type == Ops.NUMBER:
            res = c[opIndex].value
        if c[opIndex].type == Ops.ADD:
            res = c[opIndex-1].value + c[opIndex+1].value
        elif c[opIndex].type == Ops.SUB:
            res = c[opIndex - 1].value - c[opIndex + 1].value
        elif c[opIndex].type == Ops.MUL:
            res = c[opIndex - 1].value * c[opIndex + 1].value
        elif c[opIndex].type == Ops.DIV:
            res = float(c[opIndex - 1].value) / float(c[opIndex + 1].value)
        elif c[opIndex].type == Ops.EXP:
            res = float(c[opIndex - 1].value) ** float(c[opIndex + 1].value)

        res = Op(Ops.NUMBER, res)
        c[opIndex-1:opIndex+2] = [res]

    return res

calcString = ''#input('solve: ')
if calcString == '':
    calcString = '12+(( ((169 / 2^2) +17*12.5/2) -(18.5*(128 /8)+ 16.5)* 69.69+12.911 ) / 2)'

origCalcString = calcString
calcArray = []

i = 0
while i < len(calcString):
    funcSearch = re.search(r'[a-z]+', calcString[i:])
    numSearch = re.search(r'[\d\.]+', calcString[i:])

    if calcString[i] == ' ':
        calcString = calcString[i + 1:]
    elif calcString[i] in str2op:
        calcArray.append(Op(str2op[calcString[i]]))
        calcString = calcString[i + 1:]
    elif numSearch != None and numSearch.span()[0] == 0:
        num = numSearch.group()
        if '.' in num:
            num = float(num)
        else:
            num = int(num)
        calcArray.append(Op(Ops.NUMBER, num))
        calcString = calcString[i+len(str(num)):]
    elif funcSearch != None and funcSearch.span()[0] == 0:
        funcName = funcSearch.group()
        calcArray.append(Op(str2op[funcName]))
        calcString = calcString[i + len(funcName):]

print()
while len(calcArray) > 1:
    a = -1
    b = -1
    brackets = False

    for i in range(len(calcArray)):
        if calcArray[i].type == Ops.LEFT_BRACKET:
            a = i + 1
        elif calcArray[i].type == Ops.RIGHT_BRACKET:
            b = i
            brackets = True
            break

    if not brackets:
        a = 0
        b = len(calcArray)

    ans = solve(calcArray[a:b])

    if brackets:
        a -= 1
        b += 1

    print('=', formatCalc(calcArray))
    print('next:', formatCalc(calcArray[a:b]), '=', ans, '\n')#, '=', eval(formatCalc(calcArray[a:b])), '\n')

    calcArray[a:b] = [ans]

result = calcArray[0].value
check = eval(origCalcString.replace('^','**'))

print('=', calcArray[0])
print('\neval =', check)

if abs(result - check) < 1e-10:
    print('correct :D')
else:
    print('incorrect :(')
