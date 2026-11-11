from lark.visitors import Interpreter


class MeowLangInterpreter(Interpreter):
    def __init__(self):
        self.variables = {}

    def start(self, tree):
        return self.visit_children(tree)

    def assign_stmt(self, tree):
        var_name = str(tree.children[0])
        value = self.visit(tree.children[1])
        self.variables[var_name] = value
        return value

    def print_stmt(self, tree):
        value = self.visit(tree.children[-1])
        print(value)
        return value

    def for_stmt(self, tree):
        var_name = str(tree.children[0])
        iterable = self.visit(tree.children[1])
        body = tree.children[2:]

        for value in iterable:
            self.variables[var_name] = value
            for statement in body:
                self.visit(statement)

    def if_stmt(self, tree):
        if self.visit(tree.children[0]):
            self._execute_block(tree.children[1])
            return

        index = 2
        while index + 1 < len(tree.children):
            if self.visit(tree.children[index]):
                self._execute_block(tree.children[index + 1])
                return
            index += 2

        if index < len(tree.children):
            self._execute_block(tree.children[index])

    def _execute_block(self, block):
        for statement in block.children:
            self.visit(statement)

    def add(self, tree):
        left, right = tree.children
        return self.visit(left) + self.visit(right)

    def sub(self, tree):
        left, right = tree.children
        return self.visit(left) - self.visit(right)

    def mul(self, tree):
        left, right = tree.children
        return self.visit(left) * self.visit(right)

    def div(self, tree):
        left, right = tree.children
        return self.visit(left) / self.visit(right)

    def number(self, tree):
        value = str(tree.children[0])
        return float(value) if "." in value else int(value)

    def var(self, tree):
        var_name = str(tree.children[0])
        if var_name not in self.variables:
            raise NameError(f"Unknown variable: '{var_name}'")
        return self.variables[var_name]

    def args(self, tree):
        return [self.visit(argument) for argument in tree.children]

    def call(self, tree):
        function_name = str(tree.children[0])
        arguments = self.visit(tree.children[1]) if len(tree.children) > 1 else []

        if function_name == "territory":
            if len(arguments) != 1:
                raise TypeError("territory expects exactly one argument")
            return range(arguments[0])

        if function_name == "flea":
            if len(arguments) != 1 or not isinstance(arguments[0], str):
                raise TypeError("flea expects exactly one string argument")
            if len(arguments[0]) != 1:
                raise ValueError("flea expects a single character")
            return arguments[0]

        if function_name == "meow":
            if len(arguments) != 1 or not isinstance(arguments[0], str):
                raise TypeError("meow expects exactly one string argument")
            return arguments[0]

        raise NameError(f"Unknown function: '{function_name}'")

    def string(self, tree):
        return str(tree.children[0])[1:-1]

    def boolean(self, tree):
        return self.visit(tree.children[0])

    def true(self, _):
        return True

    def false(self, _):
        return False

    def null(self, _):
        return None

    def equal(self, tree):
        return self.visit(tree.children[0]) == self.visit(tree.children[1])

    def not_equal(self, tree):
        return self.visit(tree.children[0]) != self.visit(tree.children[1])

    def greater(self, tree):
        return self.visit(tree.children[0]) > self.visit(tree.children[1])

    def less(self, tree):
        return self.visit(tree.children[0]) < self.visit(tree.children[1])

    def greater_equal(self, tree):
        return self.visit(tree.children[0]) >= self.visit(tree.children[1])

    def less_equal(self, tree):
        return self.visit(tree.children[0]) <= self.visit(tree.children[1])
