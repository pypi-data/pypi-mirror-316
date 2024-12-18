
from .Value import *


def parse(line: str):

    line = line.replace(" ", "")


    if line.isdigit() or (line.count('.') < 2 and "(" not in line and ")" not in line and "," not in line):  # поддержка float

        return Atom(line)

    balance = 0
    global_balance_min = 1
    for i, char in enumerate(line):
        if char == '(':
            balance += 1

        elif char == ')':
            balance -= 1

        elif char == ',' and balance == 0:
            left = line[:i]
            right = line[i + 1:]
            return Pair(parse(left), parse(right))

        global_balance_min = min(global_balance_min, balance)



    if global_balance_min >= 0 and line[0] == "(" and line[-1] == ')':

        return parse(line[1:-1])


def parseFormula(line: str):

    operations = ['+', '-', '*', '/']
    id = -1
    op_id = -1
    while (id == -1 and op_id<3):
        op_id += 1
        for s in range(len(line)):
            if line[s] == operations[op_id]:
                id = s

    if id == -1:
        return Atom(line)

    return Pair(Atom(operations[op_id]), Pair(parseFormula(line[0:id]), parseFormula(line[id+1:])))