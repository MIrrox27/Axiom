class Environment:
    def __init__(self):
        self.variables = {}

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        raise Exception(f'Undefined variable: {name}')



class Interpreter:
    def __init__(self):
        self.env = Environment() # класс с глобальным окружением

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_error)
        return method(node)

    def visit_error(self, node):
        raise Exception(f'No visit method for {type(node).__name__}')

    def visit_Literal(self, node):
        return node.value

    def visit_Identifier(self, node):
        return self.env.get(node.name)










