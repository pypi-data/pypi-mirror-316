from abc import ABC, abstractmethod

class Value(ABC):
    @abstractmethod
    def out(self):
        pass

    @abstractmethod
    def sum(self):
        pass

    @abstractmethod
    def min(self):
        pass

    @abstractmethod
    def max(self):
        pass

    @abstractmethod
    def len(self):
        pass

    @abstractmethod
    def depth(self):
        pass

    @abstractmethod
    def __add__(self, numb):
        pass

    @abstractmethod
    def __sub__(self, numb):
        pass

    @abstractmethod
    def __mul__(self, numb):
        pass

    @abstractmethod
    def __truediv__(self, numb):
        pass

    @abstractmethod
    def replaceVar(self, string_old, string_new):
        pass


class Atom(Value):
    def __init__(self, value: str):
        self.value = value

    def out(self):

        print(self.value, end="")

    def sum(self):
        return self.value

    def min(self):
        return self.value

    def max(self):
        return self.value

    def len(self):
        return 1

    def depth(self):
        return 0

    def __add__(self, numb):
        return Atom(self.value + numb)

    def __sub__(self, numb):
        return Atom(self.value - numb)

    def __mul__(self, numb):
        return Atom(self.value * numb)

    def __truediv__(self, numb):
        return Atom(self.value / numb)

    def calc(self):
        return float(self.value)

    def replaceVar(self, string_old, string_new):
        if self.value == string_old:
            return Atom(string_new)
        return Atom(self.value)


class Pair(Value):
    def __init__(self, left: Value, right: Value):
        self.left = left
        self.right = right

    def out(self, flag: bool = False):

        if flag == True:
            print("Pair: [", end="")
        else:
            print("[", end="")
        # print("print left:", end=" ")
        self.left.out()
        print(", ", end="")
        # print("print right:", end=" ")
        self.right.out()
        print("]", end="")

    def sum(self):
        return self.left.sum() + self.right.sum()

    def min(self):
        return min(self.left.min(), self.right.min())

        # if self.left.min() < self.right.min():
        #     return self.left.min()
        #
        # return self.right.min()


    def max(self):
        return max(self.left.max(), self.right.max())

    def len(self):
        return self.left.len() + self.right.len()


    def depth(self):
        return max(self.left.depth(), self.right.depth()) + 1

    def __add__(self, numb):
        return Pair(self.left + numb, self.right + numb)

    def __sub__(self, numb):
        return Pair(self.left - numb, self.right - numb)

    def __mul__(self, numb):
        return Pair(self.left * numb, self.right * numb)

    def __truediv__(self, numb):
        return Pair(self.left / numb, self.right / numb)

    def calc(self):
        a = self.left
        p = self.right
        if a.value == '+':
            return p.left.calc() + p.right.calc()
        elif a.value == '-':
            return p.left.calc() - p.right.calc()
        elif a.value == '*':
            return p.left.calc() * p.right.calc()
        elif a.value == '/':
            if p.right.value == 0:
                raise ValueError("На 0 делить нельзя!!!")
            return p.left.calc() / p.right.calc()
        elif a.value == '**' or a.value == '^':
            return p.left.calc() ** p.right.calc()

    def replaceVar(self, string_old, string_new):
        return Pair(self.left.replaceVar(string_old, string_new), self.right.replaceVar(string_old, string_new))
