import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from lark import Lark
from interpreter import MeowLangInterpreter


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = (ROOT / "syntax.lark").read_text(encoding="utf-8")
PARSER = Lark(GRAMMAR, parser="lalr")


def run_meow(source):
    output = io.StringIO()
    with redirect_stdout(output):
        MeowLangInterpreter().visit(PARSER.parse(source))
    return output.getvalue()


def run_python(source):
    output = io.StringIO()
    with redirect_stdout(output):
        exec(source)
    return output.getvalue()


class BasicTests(unittest.TestCase):
    def compare_programs(self, meow_code, python_code):
        meow_output = run_meow(meow_code)
        python_output = run_python(python_code)

        print(f"\n  Meowlang: {meow_code!r} prints {meow_output!r}", file=sys.stderr)
        print(f"  Python:   {python_code!r} prints {python_output!r}", file=sys.stderr)

        self.assertEqual(meow_output, python_output)

    def test_text_output(self):
        self.compare_programs('scream "Hello"', 'print("Hello")')

    def test_arithmetic_and_priority(self):
        self.compare_programs("scream 2 + 3 * 4", "print(2 + 3 * 4)")

    def test_variable(self):
        self.compare_programs(
            "x = 10\nscream x - 4",
            "x = 10\nprint(x - 4)",
        )
        
    def test_division_and_decimals(self):
        self.compare_programs(
            "scream 7 / 2\nscream 1.5 + 2.25",
            "print(7 / 2)\nprint(1.5 + 2.25)",
        )

    def test_ifpet_branches(self):
        self.compare_programs(
            'ifpet purr { scream "yes" } bite { scream "no" }',
            'if True:\n    print("yes")\nelse:\n    print("no")',
        )
        self.compare_programs(
            'ifpet hiss { scream "yes" } bite { scream "no" }',
            'if False:\n    print("yes")\nelse:\n    print("no")',
        )
    def test_elsebite_branch(self):
        self.compare_programs(
            'ifpet hiss { scream "first" } '
            'elsebite purr { scream "second" } '
            'bite { scream "third" }',
            'if False:\n    print("first")\n'
            'elif True:\n    print("second")\n'
            'else:\n    print("third")',
        )

    def test_zoomies_loop(self):
        self.compare_programs(
            "zoomies i in territory(3) { scream i }",
            "for i in range(3):\n    print(i)",
        )

    def test_function_and_return(self):
        self.compare_programs(
            "cattrick add(a, b) { cough a + b }\nscream add(2, 3)",
            "def add(a, b):\n    return a + b\nprint(add(2, 3))",
        )

    def test_lists(self):
        self.compare_programs(
            'scream ["Luna", "Milo"]',
            'print(["Luna", "Milo"])',
        )
        self.compare_programs(
            'scream cuddlepile("Luna", "Milo")',
            'print(["Luna", "Milo"])',
        )

    def test_empty_list(self):
        self.compare_programs("scream []", "print([])")

    def test_function_without_parameters(self):
        self.compare_programs(
            "cattrick answer() { cough 42 }\nscream answer()",
            "def answer():\n    return 42\nprint(answer())",
        )
    def test_boolean_and_null_values(self):
        self.compare_programs(
            "scream purr\nscream hiss",
            "print(True)\nprint(False)",
        )
        self.compare_programs(
            "scream schrodinger",
            "print(None)",
        )
    def test_comparisons(self):
        self.compare_programs(
            "scream 2 == 2\n"
            "scream 2 != 2\n"
            "scream 2 < 3\n"
            "scream 2 > 3\n"
            "scream 3 >= 3\n"
            "scream 3 <= 2",
            "print(2 == 2)\n"
            "print(2 != 2)\n"
            "print(2 < 3)\n"
            "print(2 > 3)\n"
            "print(3 >= 3)\n"
            "print(3 <= 2)",
        )

    def test_text_functions(self):
        self.compare_programs(
            'scream meow("Hello")\nscream flea("M")',
            'print("Hello")\nprint("M")',
        )