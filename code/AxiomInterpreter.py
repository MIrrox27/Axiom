# author https://github.com/MIrrox27/Axiom
# AxiomInterpreter.py

from AxiomASTNodes import *



class AxiomEnvironment: #
    def __init__(self):
        self.variables = {}

    def define(self, name, value): # определение новой переменной в текущем окружении или перезаписывает текущую
        self.variables[name] = value

    def get(self, name): # возвращает значение переменной
        if name in self.variables:
            return self.variables[name]
        raise Exception(f'Undefined variable: {name}')



class AxiomInterpreter: # класс интерпретатора
    def __init__(self):
        self.env = AxiomEnvironment() # класс с глобальным окружением

    def visit(self, node): # основной метод создания
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_error)
        return method(node)

    def visit_error(self, node): # метод ошибки
        raise Exception(f'No visit method for {type(node).__name__}')

    def visit_Literal(self, node): #
        return node.value

    def visit_Identifier(self, node): #
        return self.env.get(node.name)



if __name__ == '__main__':
    ast = Identifier('x')
    interp = AxiomInterpreter()
    interp.env.define('x', 42)
    result = interp.visit(ast)
    print(result)  # Должно вывести 42









