# author https://github.com/MIrrox27/Axiom
# AxiomInterpreter.py

from AxiomASTNodes import *
from AxiomTokens import *

class Error:
    def __init__(self, module):
        self.module = module


    def raise_error(self, message, func):
        raise Exception(f'[{self.module}]: [{func}] {message}')



class AxiomEnvironment: #
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
        self.error = Error(module='AxiomEnvironment')


    def env_error(self, message, func):
       self.error.error(message=message, func=func)

    def define(self, name, value): # определение новой переменной в текущем окружении или перезаписывает текущую
        self.variables[name] = value


    def get(self, name): # возвращает значение переменной
        if name in self.variables:
            return self.variables[name]

        if self.parent is not None:
            return self.parent.get(name)
        # raise Exception(f"Variable '{name}' is not defined")
        self.env_error(message="Variable '{name}' is not defined", func='set')


    def set(self, name, value): # Изменение значения переменной, не работает с необъявленными переменными
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return

        #raise Exception(f"Variable '{name}' is not defined")
        self.env_error(message="Variable '{name}' is not defined", func='set')



class AxiomInterpreter: # класс интерпретатора
    def __init__(self):
        self.error = Error(module='AxiomEnvironment')
        self.env = AxiomEnvironment() # класс с глобальным окружением


    def visit(self, node): # основной метод создания
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_error)
        return method(node)


    def visit_error(self, node): # метод ошибки
        self.error.raise_error(func='visit_error', message=f'No visit method for {type(node).__name__}')
        #raise Exception(f'No visit method for {type(node).__name__}')


    def visit_Literal(self, node): #
        return node.value


    def visit_Identifier(self, node): #
        return self.env.get(node.name)




    def visit_VarDeclaration(self, node):
        value = None
        if node.value is not None:
            value = self.visit(node.value)

        self.env.define(node.name, value)
        return None


    def visit_Block(self, node):
        previous_env = self.env # создаем новое окружение для бока
        self.env = AxiomEnvironment(previous_env)

        try:
            for stmt in node.statements:
                self.visit(stmt)

        finally:
            self.env = previous_env # восстанавливаем окружение

        return None

    def visit_ExpressionStmt(self, node): # временно делаем
        self.visit(node.expression) # Вычисляем выражение, результат отбрасываем
        return None


    def visit_BinaryOp(self, node): # выполняет бинарную операцию
        left_val = self.visit(node.left)

        if node.operator == AxiomTokenType.AND: # если левый операнд ложный, результат - False, правый нет смысла вычислять
            if not self.is_truthy(left_val):
                return False

            right_val = self.visit(node.right)
            return self.is_truthy(right_val)

        elif node.operator == AxiomTokenType.OR:  # если левый операнд истинный, результат - True, правый нет смысла вычислять
            if self.is_truthy(left_val):
                return True

            right_val = self.visit(node.right)
            return self.is_truthy(right_val)

        elif node.operator == AxiomTokenType.ASSIGN:
            if not isinstance(node.left, Identifier):
                self.error.raise_error("Left side of assignment must be a variable", func='visit_BinaryOp')

            right_val = self.visit(node.right) # вычисляем значение переменной
            self.env.set(node.left.name, right_val) # сохраняем переменную

            return right_val # присваивание возвращает присвоенное значение

        right_val = self.visit(node.right)

        # Арифметические операторы (возвращают результат)
        if node.operator == AxiomTokenType.PLUS:
            self._check_numeric_or_string(left_val, right_val, node.operator)
            return left_val + right_val

        elif node.operator == AxiomTokenType.MINUS:
            self._check_numeric(right_val, left_val, node.operator)
            return left_val - right_val

        elif node.operator == AxiomTokenType.MULTIPLY:
            self._check_numeric(left_val, right_val, node.operator)
            return left_val * right_val

        elif node.operator == AxiomTokenType.DIVIDE:
            self._check_numeric(left_val, right_val, node.operator)

            if right_val == 0:
                self.error.raise_error(f"Division by zero", func='visit_BinaryOp')
            return left_val / right_val

        elif node.operator == AxiomTokenType.MOD:
            self._check_numeric(left_val, right_val, node.operator)

            if right_val == 0:
                self.error.raise_error(f"Division by zero", func='visit_BinaryOp')

            return left_val % right_val

        elif node.operator == AxiomTokenType.POWER:
            self._check_numeric(left_val, right_val, node.operator)
            return left_val ** right_val

        # Операторы сравнения (возвращают true / false)

        elif node.operator == AxiomTokenType.EQUALS:
            return left_val == right_val

        elif node.operator == AxiomTokenType.NOT_EQUALS:
            return left_val != right_val

        elif node.operator == AxiomTokenType.LESS:
            return  left_val < right_val

        elif node.operator == AxiomTokenType.GREATER:
            return left_val > right_val

        elif node.operator == AxiomTokenType.LESS_EQUAL:
            return left_val <= right_val

        elif node.operator == AxiomTokenType.GREATER_EQUAL:
            return left_val >= right_val

        else:
            self.error.raise_error(f"Unknown binary operator: {node.operator}", func='visit_BinaryOp')



        # Вспомогательные функции для проверки типов
    def is_truthy(self, value): # смотрит, является ли значение истинным
        # в Axiom false, 0 и nill считаются ложными, все остальное истинными
        if value is False or value is None:
            return False

        if isinstance(value, bool): # true
            return True

        if isinstance(value, (int, float)):
            return value != 0

        if isinstance(value, str):
            return bool(value)

        # тут будут еще проверки

        return True


    def _check_numeric(self, left, right, op): # проверяет что оба операнда числа
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            self.error.raise_error(func='_check_numeric', message=f"Operator '{op}' requires numeric operands")


    def _check_numeric_or_string(self, left, right, op): # проверяет что оба операнда числа либо строки
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return

        if isinstance(left, str) and isinstance(left, str):
            return

        self.error.raise_error(func='_check_numeric', message=f'Operator {op} requires both numbers or both string')


    def _check_comparable(self, left, right, op): # проверяет что операнды можно сравнивать

        if type(left) != type(right):
            self.error.raise_error(func='_check_comparable', message=f"Operator {op} requires operands of the same type")

        if not isinstance(left, (int, float, str)):
            self.error.raise_error(func='_check_comparable', message=f"Operator {op} not supported for {type(left).__name__}")





if __name__ == '__main__':

    var_decl = VarDeclaration(AxiomTokenType.VAR, 'x', Literal(5))
    print(var_decl)
    add_op = BinaryOp(Identifier('x'), AxiomTokenType.PLUS, Literal(2))
    print(add_op)
    assign = BinaryOp(Identifier('x'), AxiomTokenType.ASSIGN, add_op)
    print(assign)

    assign_stmt = ExpressionStmt(assign)
    program = [var_decl, assign_stmt]

    # Интерпретируем
    interp = AxiomInterpreter()
    for stmt in program:
        interp.visit(stmt)

    # Проверим значение x
    print(interp.env.get('x'))  # должно быть 7









