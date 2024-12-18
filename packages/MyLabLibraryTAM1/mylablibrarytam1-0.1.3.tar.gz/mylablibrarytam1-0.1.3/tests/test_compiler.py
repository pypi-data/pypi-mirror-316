import unittest
from MyLabLibraryTAM.Compiler import Compiler, Scope
from MyLabLibraryTAM.Struck import Atom, Pair


class TestCompiler(unittest.TestCase):

    def setUp(self):
        self.compiler = Compiler()

    def test_add_var(self):
        var_definition = Pair(Atom("x"), Pair(Atom("int"), Atom("10")))
        self.compiler.add_var(var_definition)
        variable = self.compiler.find_var("x")
        self.assertIsNotNone(variable)
        self.assertEqual(variable.value, "10")


if __name__ == "__main__":
    unittest.main()
