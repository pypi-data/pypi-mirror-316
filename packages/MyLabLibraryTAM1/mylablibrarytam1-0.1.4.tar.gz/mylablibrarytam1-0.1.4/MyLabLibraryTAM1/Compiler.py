from .Struck import *


class Scope:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent if parent else None

    def add_variable(self, name, var_type, value):
        new_var = Var(name, var_type, value)
        self.vars[name] = new_var

def parse_args(args):
    result = []
    while isinstance(args, Pair) and args.left != "null":
        result.append(args.left)
        args = args.right
    return result

class Compiler:
    def __init__(self):
        self.vars = {}
        self.funcs = {}
        self.current_scope = Scope()

    def add_var(self, var):
        name = var.left.value
        var_type = var.right.left.value
        value = var.right.right.value

        # new_var = Var(name, var_type, value)

        self.current_scope.add_variable(name, var_type, value)

    def find_var(self, name):
        if self.current_scope and name in self.current_scope.vars:
            return self.current_scope.vars[name]
        else:
            return self.vars.get(name)


    def enter_scope(self):
        self.current_scope = Scope(self.current_scope)

    def leave_scope(self):
        self.current_scope = self.current_scope.parent

    def out(self, val):
        val.out()

    def add_func(self, val):
        pair = val
        left_pair = pair.left
        right_pair = pair.right


        name = left_pair.left.value
        func_type = left_pair.right.value


        args_pair = right_pair.left

        args_list = []
        if not(isinstance(args_pair, Atom)):
            while isinstance(args_pair, Pair):
                args_list.append(args_pair.left.value)
                args_pair = args_pair.right

        args_count = len(args_list)


        body = right_pair.right

        new_func = Func(name, func_type, args_count, args_list, body)
        self.funcs[name] = new_func

    def find_func(self, name):
        return self.funcs.get(name)

    def run(self, programm: Value):

        if isinstance(programm, Atom):

            return

        if isinstance(programm, Pair):
            p = Pair(programm.left, programm.right)
        else:
            raise ValueError("Invalid program format. Expected Pair.")

        if isinstance(programm, Pair):
            p = Pair(programm.left, programm.right)

            L = p.left

            R = p.right





            if L.value == "out":

                if R.value.startswith('"') and R.value.endswith('"'):

                    varx = self.find_var(R.value[1:-1])

                    print(varx.value)

                    return

                else:


                    self.out(R)
                    print()

                    return


            elif L.value == "+":
                if R.right.value.startswith('"') and R.right.value.endswith('"') and R.left.value.startswith('"') and R.left.value.endswith('"'):

                    x = self.find_var(R.left.value[1:-1])
                    y = self.find_var(R.right.value[1:-1])

                    if not isinstance(x.value, int):
                        if x.value.startswith('"'):
                            x.value = x.value[1:-1]
                        # print("pppppppppp")
                        # print(x.value)
                        x.value = int(x.value)

                    if not isinstance(y.value, int):
                        if y.value.startswith('"'):
                            y.value = y.value[1:-1]
                        y.value = int(y.value)


                    x.value = str(x.value + y.value)

                    return

                else:

                    x = self.find_var(R.left.value[1:-1])
                    y = R.right

                    x.value = str(int(x.value) + int(y.value))



                    print("НЕДОПИСАНО")

                    return

            elif L.value == "=":
                if R.right.value.startswith('"') and R.value.right.endswith('"') and R.left.value.startswith('"') and R.left.right.endswith('"'):

                    x = self.find_var(R.right.value[1:-1])
                    y = self.find_var(R.left.value[1:-1])
                    x.value = y.value

                    return

                else:

                    print("НЕДОПИСАНО")


            elif L.value == "var":
                self.add_var(R)
                return
            elif L.value == "block":

                if isinstance(R.right, Atom):
                    self.run(R.left)
                    return

                nex = R

                while isinstance(nex, Pair):
                    self.run(nex.left)
                    nex = nex.right
                return


            elif L.value == "def":



                self.add_func(R)



            elif L.value == "for":



                loop_var = R

                # R.out()
                # print()


                if not isinstance(loop_var, Pair):
                    raise ValueError("Invalid loop structure. Expected a Pair for loop variable.")



                loop_var, loop_range = R.left, R.left.left


                var_name, var_type, start, end = loop_var.left.value, loop_var.right.left.value, loop_var.right.right.left.value, loop_var.right.right.right.value

                # print("************")
                # print(var_name, var_type, start, end)
                # print("************")


                if start.startswith('"') and start.endswith('"'):

                    start = self.find_var(start[1:-1]).value

                if end.startswith('"') and end.endswith('"'):

                    end = self.find_var(end[1:-1]).value

                    # print(end)


                self.add_var(Pair(Atom(var_name), Pair(Atom(var_type), Atom(start))))


                loop_body = R.right



                if not isinstance(end, int):

                    # print(type(end))
                    end = int(end)

                for i in range(int(start), end):
                    self.current_scope.vars[var_name].value = str(i)

                    self.run(loop_body)



                del self.current_scope.vars[var_name]





            elif self.find_func(L.value):

                func = self.find_func(L.value)

                args = parse_args(R)


                if len(args) != func.args_count:
                    raise ValueError(
                        f"Incorrect number of arguments for function '{func.name}'. Expected {func.args_count}, got {len(args)}.")

                self.enter_scope()

                for i, arg in enumerate(func.args):
                    arg_type, arg_name = arg.split(':')
                    # print('------------')
                    # print(arg_type, arg_name, args[i].value)
                    # print('------------')
                    self.add_var(Pair(Atom(arg_name), Pair(Atom(arg_type), Atom(args[i].value))))

                self.run(func.body)


                self.leave_scope()