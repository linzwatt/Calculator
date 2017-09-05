import re


class OpCats:
    NUMBER, MUL_DIV, ADD_SUB, BRACKET = range(4)


class Ops:
    NUMBER, MUL, DIV, ADD, SUB, LEFT_BRACKET, RIGHT_BRACKET = range(7)

strings = ['num', '*', '/', '+', '-', '(', ')']
opsDict = {'+': Ops.ADD, '-': Ops.SUB, '*': Ops.MUL, '/': Ops.DIV, '(':Ops.LEFT_BRACKET, ')': Ops.RIGHT_BRACKET}


class Op(object):
    def __init__(self, opType, value=None):
        self.type = opType
        self.value = value
        self.cat = -1
        if self.type == Ops.ADD or self.type == Ops.SUB:
            self.cat = OpCats.ADD_SUB
        elif self.type == Ops.MUL or self.type == Ops.DIV:
            self.cat = OpCats.MUL_DIV

    def __repr__(self):
        if self.type == Ops.NUMBER:
            return str(self.value)
        else:
            return strings[self.type]


def formatCalc(c):
    s = ''
    for i in range(len(c)):
        end = ''
        if 1 <= c[i].type <= 4:
            end = ' '
        elif i < len(c) - 1 and 1 <= c[i+1].type <= 4:
                end = ' '
        s += str(c[i]) + end
    return s


def solve(c):

    numOps = len(c) // 2

    res = None
    for i in range(numOps):
        smallest = 1e99
        opIndex = -1
        for n in range(1, len(c), 2):
            if c[n].type < smallest and c[n].cat != c[opIndex].cat:
                smallest = c[n].type
                opIndex = n

        if c[opIndex].type == Ops.ADD:
            res = c[opIndex-1].value + c[opIndex+1].value
        elif c[opIndex].type == Ops.SUB:
            res = c[opIndex - 1].value - c[opIndex + 1].value
        elif c[opIndex].type == Ops.MUL:
            res = c[opIndex - 1].value * c[opIndex + 1].value
        elif c[opIndex].type == Ops.DIV:
            res = float(c[opIndex - 1].value) / float(c[opIndex + 1].value)

        res = Op(Ops.NUMBER, res)
        c[opIndex-1:opIndex+2] = [res]

    return res

calcString = input('solve: ')
if calcString == '':
    calcString = '12+(( ((169 / 2) +17*12.5/2) -(18.5*(128 /8)+ 16.5)* 69.69+12.911 ) / 2)'

origCalcString = calcString
calcArray = []

i = 0
while i < len(calcString):
    if calcString[i] == ' ':
        calcString = calcString[i + 1:]
    elif calcString[i] in opsDict:
        calcArray.append(Op(opsDict[calcString[i]]))
        calcString = calcString[i + 1:]
    else:
        num = re.search(r'[\d\.]+', calcString[i:]).group()
        if '.' in num:
            num = float(num)
        else:
            num = int(num)
        calcArray.append(Op(Ops.NUMBER, num))
        calcString = calcString[i+len(str(num)):]

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
check = eval(origCalcString)

print('=', calcArray[0])
print('eval =', check)

if abs(result - check) < 1e-10:
    print('\ncorrect')
else:
    print('\nincorrect')
