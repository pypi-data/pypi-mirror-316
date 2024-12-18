import unittest
from MyLabLibraryTAM.Value import Atom, Pair

class TestAtom(unittest.TestCase):

    def test_init(self):
        atom = Atom("5")
        self.assertEqual(atom.value, "5")

    def test_out(self):
        atom = Atom("5")
        with self.assertLogs() as captured:
            atom.out()
        self.assertIn("5", captured.output[0])

    def test_sum(self):
        atom = Atom("5")
        self.assertEqual(atom.sum(), "5")

    def test_min(self):
        atom = Atom("5")
        self.assertEqual(atom.min(), "5")

    def test_max(self):
        atom = Atom("5")
        self.assertEqual(atom.max(), "5")

    def test_len(self):
        atom = Atom("5")
        self.assertEqual(atom.len(), 1)

    def test_depth(self):
        atom = Atom("5")
        self.assertEqual(atom.depth(), 0)

    def test_arithmetic(self):
        atom1 = Atom("3")
        atom2 = Atom("7")
        self.assertEqual((atom1 + 2).value, "32")

    def test_replaceVar(self):
        atom = Atom("x")
        replaced = atom.replaceVar("x", "10")
        self.assertEqual(replaced.value, "10")

class TestPair(unittest.TestCase):

    def test_init(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual(pair.left, left)
        self.assertEqual(pair.right, right)

    def test_out(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        with self.assertLogs() as captured:
            pair.out()
        self.assertIn("[3, 5]", captured.output[0])

    def test_sum(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual(pair.sum(), "35")

    def test_min(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual(pair.min(), "3")

    def test_max(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual(pair.max(), "5")

    def test_len(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual(pair.len(), 2)

    def test_depth(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual(pair.depth(), 1)

    def test_arithmetic(self):
        left = Atom("3")
        right = Atom("5")
        pair = Pair(left, right)
        self.assertEqual((pair + 2).left.value, "32")
        self.assertEqual((pair + 2).right.value, "52")

    def test_replaceVar(self):
        left = Atom("x")
        right = Atom("y")
        pair = Pair(left, right)
        replaced = pair.replaceVar("x", "10")
        self.assertEqual(replaced.left.value, "10")
        self.assertEqual(replaced.right.value, "y")

if __name__ == "__main__":
    unittest.main()
