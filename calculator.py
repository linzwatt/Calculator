import re

# 12 + ((((169/ 2.5)+17* 3.8/2)-(18.5 *(128/8) +16.5) * 69.69 + 12.911) / 2)


class Ops:
    NUMBER, ADD, SUB, MUL, DIV, LEFT_BRACKET, RIGHT_BRACKET = range(7)

strings = ['num', '+', '-', '*', '/', '(', ')']
opsDict = {'+': Ops.ADD, '-': Ops.SUB, '*': Ops.MUL, '/': Ops.DIV, '(':Ops.LEFT_BRACKET, ')': Ops.RIGHT_BRACKET}


class Op(object):
    def __init__(self, opType, value=None):
        self.type = opType
        self.value = value

    def __repr__(self):
        if self.type == Ops.NUMBER:
            return str(self.value)
        else:
            return strings[self.type]


def disp(c):
    for i in range(len(c)):
        end = ''
        if 1 <= c[i].type <= 4:
            end = ' '
        if i < len(c) - 1:
            if 1 <= c[i+1].type <= 4
                end = ' '
        print(c[i], end=end)
    print()


def solve(c):

    numOps = len(c) // 2

    res = None
    for i in range(numOps):
        for n in range(len(c)):
            if c[n].type != Ops.NUMBER:
                break

        if c[n].type == Ops.ADD:
            res = c[n-1].value + c[n+1].value
        elif c[n].type == Ops.SUB:
            res = c[n - 1].value - c[n + 1].value
        elif c[n].type == Ops.MUL:
            res = c[n - 1].value * c[n + 1].value
        elif c[n].type == Ops.DIV:
            res = float(c[n - 1].value) / float(c[n + 1].value)

        res = Op(Ops.NUMBER, res)
        c[0:3] = [res]

    return res

calcString = input('solve: ')
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

    disp(calcArray)
    print('ans =', ans, '\n')

    calcArray[a:b] = [ans]

result = calcArray[0].value
check = eval(origCalcString)

print('result =', calcArray[0])
print('check =', check)

if abs(result - check) < 1e-10:
    print('correct')
else:
    print('incorrect')
