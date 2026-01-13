# author https://github.com/MIrrox27/Axiom

class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class Statement(ASTNode):
    # Инструкция - действие, которое выполняется
    pass


class Expression(ASTNode):
    # Выражение - что-то, что вычисляется в значение
    pass


class Programm(ASTNode):
    # Вся программа - список инструкций
    def __init__(self, statements):
        self.statements = statements




class Literal(Expression):
    # Литерал - константное значение
    def __init__(self, value):
        self.value = value

class Identifier(Expression):
    # Идентификатор - имя переменной
    def __init__(self, name):
        self.name = name

class BinaryOp(Expression):
    # Бинарная операция: левый_операнд оператор правый_операнд
    def __init__(self,  left, operator, right):
        self. left = left
        self.operator = operator
        self.right = right
