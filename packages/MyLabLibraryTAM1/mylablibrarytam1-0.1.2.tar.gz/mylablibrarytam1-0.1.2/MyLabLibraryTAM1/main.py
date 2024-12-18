from .Compiler import *
from .Parser import parse, parseFormula



file_name = 'prog.txt'

# Открываем файл для чтения
with open(file_name, 'r', encoding='utf-8') as file:
    contents = file.read()
    contents = contents[0:-1]





comp = Compiler()
program = parse(contents)


program.out()
print()

comp.run(program)