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
        condition = self.visit(tree.children[0]) #jei if praeina
        then_body = tree.children[1].children    # sukuria body
        else_body = tree.children[2].children if len(tree.children) > 2 else [] #sukurto body else'as

        for statement in then_body if condition else else_body: #issirenka viena
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

        raise NameError(f"Unknown function: '{function_name}'")

    def string(self, tree):
        return str(tree.children[0])[1:-1]

    def boolean(self, tree):
        return self.visit(tree.children[0])

    def true(self, _):
        return True

    def false(self, _):
        return False
