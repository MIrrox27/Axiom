# author https://github.com/MIrrox27/Axiom
# AxiomInterpreter.py

from axiom.AxiomASTNodes import *
from axiom.AxiomTokens import *

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

    def define(self, name, value, constant=False): # определение новой переменной в текущем окружении или перезаписывает текущую
        self.variables[name] = {
            'value': value,
            'constant': constant
        }


    def get(self, name): # возвращает значение переменной
        if name in self.variables:
            return self.variables[name]['value']

        if self.parent is not None:
            return self.parent.get(name)
        self.env_error(message=f"Variable '{name}' is not defined", func='get')


    def set(self, name, value): # Изменение значения переменной, не работает с необъявленными переменными
        if name in self.variables:
            if self.variables[name]['constant']:
                self.error.raise_error(f"Cannot assign to constant '{name}' (declared with val)", 'set')
            self.variables[name]['value'] = value
            return

        if self.parent is not None:
            self.parent.set(name, value)
            return
        self.error.raise_error(f"Variable '{name}' is not defined", 'set')




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


    def __repr__(self):
        return f"<built-in function {self.name}>"




class Module:
    def __init__(self, name):
        self.name = name
        self.exports = {}
        self.error = Error(module="Module")


    def define(self, name, value):
        self.exports[name] = value


    def get(self, name):
        if name in self.exports:
            return self.exports[name]
        self.error.raise_error(f"Module '{self.name}' has no export '{name}'", func='get')

    def __repr__(self):
        return f"<module {self.name}>"




class UserFunction(Callable):
    def __init__(self, name, parameters, body, closure_env, interpreter):

        # Вызываем конструктор родителя (Callable) и проверяем количество аргументов сами
        super().__init__(name, -1, None)
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure_env = closure_env # окружение на момент объявления
        self.interpreter = interpreter # ссылка на интерпретатор


    def call(self, args):
        if len(args) != len(self.parameters):
            self.error.raise_error(
                f"Function '{self.name}' expects {len(self.parameters)} arguments, got {len(args)}",
                'call'
            )

        call_env = AxiomEnvironment(self.closure_env) # создаем новое окружение для вызова функции

        for param_name, arg_value in zip(self.parameters, args): # Связываем параметры с аргументами
            call_env.define(param_name, arg_value, constant=False)

        previous_env = self.interpreter.env # Сохраняем текущее окружение интерпретатора
        self.interpreter.env = call_env # Устанавливаем новое окружение в интерпретаторе


        try:
            self.interpreter.visit(self.body)
        except ReturnValue as ret:
            return ret.value

        finally:
            self.interpreter = previous_env

        return None




class AxiomInterpreter: # класс интерпретатора
    def __init__(self):
        self.error = Error(module='AxiomInterpreter')

        self.global_env = AxiomEnvironment() # глобальное окружение
        self.env = self.global_env

        self.modules = {}  # все модули

        self._register_builtins() # регистрируем все функции
        self._register_standard_modules() # регистрируем стандартные модули



            # --------ВСТРОЕННЫЕ ФУНКЦИИ--------

    def _register_builtins(self):

        def print_func(*args):  # print выводит значения через пробел
            output = ' '.join(str(arg) for arg in args)
            print(output)
            return None
        self.global_env.define('print', Callable('print', -1, print_func)) # регистрируем функцию


        def input_func(prompt=""): # принимает только 1 значение
            return input(str(prompt))
        self.global_env.define('input', Callable('input', 1, input_func)) # регистрируем функцию


        def int_func(*args):
            output = ' '.join(str(arg) for arg in args)
            return int(output)
        self.global_env.define('int', Callable('int', -1, int_func))


        def str_func(*args):
            output = ' '.join(str(arg) for arg in args)
            return str(output)
        self.global_env.define('str', Callable('str', -1, str_func))


        def is_int_func(expressions):
            if expressions % 1 == 0:
                return True

            else:
                return False
        self.global_env.define('is_int', Callable('is_int', 1, is_int_func))


        #def calculate(expressions):
           # expressions = list(expressions)


        # тут будут все остальные функции


    def visit_MemberAccess(self, node):  # Вычисляет доступ к члену объекта
        obj = self.visit(node.obj)

        if not isinstance(obj, Module):
            self.error.raise_error(f"Cannot access member of non-module object: {obj}", 'visit_MemberAccess')

        #print(f"DEBUG: Accessing {node.obj}.{node.member}")
        return obj.get(node.member)



    def visit_ImportStmt(self, node):  # Выполняет импорт модуля
        module_name = node.module_name

        if module_name not in self.modules:
            self.error.raise_error(f"Module '{module_name}' not found", func="visit_ImportStmt")

        module = self.modules[module_name]

        #print(f"DEBUG: Importing module {module_name}")
        #print(f"DEBUG: Module object: {module}")

        self.global_env.define(module_name, module, constant=False)
        return None



    def visit_ReturnStmt(self, node): # Выполняет оператор return.
        value = None
        if node.value is not None:
            value = self.visit(node.value)

        raise ReturnStmt(value) # Вычисляет значение и выбрасывает исключение ReturnValue.



    def visit_FunDeclaration(self, node): # Создаёт пользовательскую функцию и сохраняет её в окружении.
        func = UserFunction(node.name, node.parameters, node.body, self.env) # Создаём функцию, сохраняя текущее окружение
        self.env.define(node.name, func, constant=False) # Сохраняем функцию в текущем окружении

        return None




            # --------БИБЛИОТЕКИ (МОДУЛИ)--------

    def _register_standard_modules(self):
        math_module = Module('math')
        self._register_math_functions(math_module)
        self.modules['math'] = math_module



        # ---MATH---
    def _register_math_functions(self, module):
        import math as py_math

            # функции
        def sqrt_func(x): #
            return py_math.sqrt(x)
        module.define('sqrt', Callable('math.sqrt', 1, sqrt_func))

        def pow_func(x, y): # возведение в степень
            return x ** y
        module.define('pow', Callable('math.pow', 2, pow_func))

            # константы
        module.define('pi', py_math.pi)
        module.define('e', py_math.e)





    def visit_CallExpr(self, node): # выполняет вызов функции
        callee = self.visit(node.callee)

        if not isinstance(callee, Callable): # проверяем что это функция

            if isinstance(node.callee, MemberAccess):

                if isinstance(node.callee.obj):
                    obj_name = node.callee.obj.name
                else:
                    obj_name = str(node.callee.obj)
                callee_name = f"{obj_name}.{node.callee.member}"

            elif isinstance(node.callee, Identifier):
                callee_name = node.callee.name
            else:
                callee_name = str(node.callee)

            self.error.raise_error(f"'{callee_name}' is not a function (got {type(callee).__name__})", func='visit_CallExpr')



        args = []
        for arg_node in node.arguments:
            arg_value = self.visit(arg_node)
            args.append(arg_value)

        return callee.call(args)



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

        is_const = (node.keyword == AxiomTokenType.VAL)

        self.env.define(node.name, value, is_const)
        return None



    def visit_EmtpyStmt(self, node):
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
            self._check_numeric(left_val, right_val, node.operator)
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


    def visit_UnaryOp(self, node):
        if node.operator == AxiomTokenType.NOT:
            val = self.visit(node.expr)
            return not self.is_truthy(val)

        else:
            self.error.raise_error(f"Unknown unary operator: {node.operator}", 'visit_UnaryOp')


        # проверка операторов

    def visit_IFStmt(self, node):
        # Вычисляем условие if
        if self.is_truthy(self.visit(node.condition)):
            self.visit(node.than_branch)
            return None

        # Проверяем все elif
        for elif_clause in node.elif_branches:
            if self.is_truthy(self.visit(elif_clause.condition)):
                self.visit(elif_clause.block)
                return None

        # Если ничего не сработало и есть else
        if node.else_branch is not None:
            self.visit(node.else_branch)
        return None



    def visit_WhileStmt(self, node): # обработка while
        while True:  # пока условие верное, выполняем действия
            condition_value = self.visit(node.condition) # если условие ложное - выходим
            if not self.is_truthy(condition_value):
                break
            self.visit(node.body)

        return None



    def visit_ForStmt(self, node):
        previous_env = self.env # создаем новое окружение
        self.env = AxiomEnvironment(previous_env)

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
            self.env = previous_env

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

        if isinstance(left, str) and isinstance(right, str):
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









