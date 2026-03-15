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
       self.error.raise_error(message=message, func=func)

    def define(self, name, value): # определение новой переменной в текущем окружении или перезаписывает текущую
        self.variables[name] = value


    def get(self, name): # возвращает значение переменной
        if name in self.variables:
            return self.variables[name]

        if self.parent is not None:
            return self.parent.get(name)
        # raise Exception(f"Variable '{name}' is not defined")
        self.env_error(message=f"Variable '{name}' is not defined", func='set')


    def set(self, name, value): # Изменение значения переменной, не работает с необъявленными переменными
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return

        #raise Exception(f"Variable '{name}' is not defined")
        self.env_error(message="Variable '{name}' is not defined", func='set')




class Callable: # базовый класс для всех функций
    def __init__(self, name, arity, func):
        self.name = name
        self.arity = arity
        self.func = func
        self.error = Error('Callable')

    def call(self, args): # вызов функции с переданными аргументами
        if self.arity != -1 and len(args) != self.arity: # ошибка если функция не помечена как принимающая любое число аргументов и число аргументов не равно нужному
            self.error.raise_error(f"Function '{self.name}' expects {self.arity} arguments, got {len(args)}", func='call')

        return self.func(*args)






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

        # особые операторы
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



        # проверка операторов
    def visit_IfStmt(self, node): # Обработка if
        if self.is_truthy(self.visit(node.condition)):
            self.visit(node.than_branch)
            return None

        for elif_clause in node.elif_branches:
            if self.is_truthy(self.visit(elif_clause.condition)):
                self.visit(elif_clause.block)
                return None

        if node.else_branch is not None:
            self.visit(node.else_branch)



    def visit_WhileStmt(self, node): # обработка while
        while True:  # пока условие верное, выполняем действия
            condition_value = self.visit(node.condition) # если условие ложное - выходим
            if not self.is_truthy(condition_value):
                break
            self.visit(node.body)

        return None



    def visit_ForStmt(self, node):
        previos_env = self.env # создаем новое окружение
        self.env = AxiomEnvironment(previos_env)

        try:
            if node.initializer is not None:
                self.visit(node.initializer)

            while True:
                if node.condition is not None:
                    condition_value = self.visit(node.condition)

                    if not self.is_truthy(condition_value):
                        break

                self.visit(node.body)

                if node.increment is not None:
                    self.visit(node.increment)

        finally:
            self.env = previos_env

        return None



    def visit_DoStmt(self, node):
        while True:
            self.visit(node.body)

            condition_value = self.visit(node.condition)
            if not self.is_truthy(condition_value):
                break

        return None



    def visit_ForeachStmt(self, node):

        iterable = self.visit(node.iterable)

        if isinstance(iterable, str): # пока только работа со строками
            items = iterable

        else:
            self.error.raise_error( f"foreach: unsupported iterable type {type(iterable).__name__}", func='visit_ForeachStmt')

        previous_env = self.env # сохраняем текущее окружение
        try:
            for item in items:
                self.env = AxiomEnvironment(previous_env) # создаем новое окружение

                var_name = node.variable.name
                self.env.define(var_name, item)

                self.visit(node.body) # выполняем тело цикла

                self.env = previous_env # восстанавливаем окружение

        finally:
            self.env = previous_env # если была ошибка, то окружение восстановится

        return None



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

    # Создаём узлы
    # var x = 0
    var_x = VarDeclaration(AxiomTokenType.VAR, 'x', Literal(0))

    # for (var i = 0; i < 3; i = i + 1) { x = x + i; }
    # инициализатор: var i = 0
    init = VarDeclaration(AxiomTokenType.VAR, 'i', Literal(0))
    # условие: i < 3
    cond = BinaryOp(Identifier('i'), AxiomTokenType.LESS, Literal(3))
    # инкремент: i = i + 1
    inc = BinaryOp(Identifier('i'), AxiomTokenType.ASSIGN,
                   BinaryOp(Identifier('i'), AxiomTokenType.PLUS, Literal(1)))
    # тело: x = x + i (как выражение, но оно должно быть инструкцией-выражением)
    body_expr = BinaryOp(Identifier('x'), AxiomTokenType.ASSIGN,
                         BinaryOp(Identifier('x'), AxiomTokenType.PLUS, Identifier('i')))
    body_stmt = ExpressionStmt(body_expr)
    body_block = Block([body_stmt])

    # узел for
    for_stmt = ForStmt(init, cond, inc, body_block)

    # Программа
    program = [var_x, for_stmt]

    # Интерпретация
    interp = AxiomInterpreter()
    for stmt in program:
        interp.visit(stmt)

    print(interp.env.get('x'))  # должно быть 3
    print(interp.env.get('i'))  # ошибка: i не определена









