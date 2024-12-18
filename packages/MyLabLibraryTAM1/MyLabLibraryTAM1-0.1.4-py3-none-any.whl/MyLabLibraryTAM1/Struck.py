from .Value import *

import weakref

class Var:
    def __init__(self, name, var_type, value):
        self.name = name
        self._type = var_type
        self.value = value


class Func:
    def __init__(self, name, func_type, args_count, args, body):
        self.name = name
        self._type = func_type
        self.args_count = args_count
        self.args = args
        self.body = body

