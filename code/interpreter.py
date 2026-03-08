class Environment:
    def __init__(self):
        self.variables = {}

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        raise Exception(f'Undefined variable: {name}')



