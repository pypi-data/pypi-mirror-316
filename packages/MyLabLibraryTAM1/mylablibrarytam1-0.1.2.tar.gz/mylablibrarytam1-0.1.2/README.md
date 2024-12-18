# My Library

Это чисто моя демонстрация навыков работы с выгрузкой библиотек для питона. Представленная библиотека является прототипом атомарного компилятора, который мало что умеет, но при переводе в библиотеку рабочких функций не потерял. Для проверки работы предлагаю проверить работу следующей программы

```
from MyLabLibraryTAM1 import Compiler, Atom, Pair

# Пример работы с библиотекой
compiler = Compiler()

# Тест: создание атомов и пар
atom1 = Atom("42")
atom2 = Atom("24")
pair = Pair(atom1, atom2)

print("Atom1:", atom1.value)
print("Atom2:", atom2.value)

print("Pair sum:", pair.sum())
print("Pair depth:", pair.depth())

# Тест: выполнение программы с компилятором
program = Pair(Atom("var"), Pair(Atom("x"), Pair(Atom("int"), Atom("10"))))


compiler.run(program)

# Проверка значения переменной
var = compiler.find_var("x")
print("Variable x:", var.value)
```

## Installation

Install it using pip:
```bash
pip install MyLabLibraryTAM