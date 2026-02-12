# author https://github.com/MIrrox27/Axiom
# AxiomASTNodes.py


class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def accept(self, visitor):
        # Метод для реализации Visitor pattern
        method_name = f'visit_{self.__class__.__name__}'.lower()
        visitor_method = getattr(visitor, method_name, None)
        if visitor_method:
            return visitor_method(self)


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



class Statement(ASTNode):
    # базовый класс для всех инструкций, которые не возвращают значения
    pass

class ExpressionStmt(Statement): # инструкция выражения
    def __init__(self, expression):
        self.expression = expression


class VarDeclaration(Statement): # объявление переменных и констант
    # тк структура этого класса выглядит так: var/val name = value, имена переменных соответствующие
    def __init__(self, keyword, name, value):
        self.keyword = keyword # слово которым я объявляю переменную (var/val)
        self.name = name # имя переменной
        self.value = value # значение переменной


class Block(Statement): # блок кода
    def __init__(self, statements):
        self.statements = statements

class EmtpyStmt(Statement): # пустая инструкция
    pass

class IFStmt(Statement):  # узел AST для оператора IF
    def __init__(self, condition, than_branch, elif_branches=None, else_branch=None):
        self.condition = condition # условие (выражение)
        self.than_branch = than_branch # сам блок if
        self.elif_branches = elif_branches if elif_branches else [] # список блоков elif (может быть равен 0)
        self.else_branch = else_branch # блок else (может отсутствовать)

class ElifClause:  # вспомогательный класс для ветки elif
    def __init__(self, condition, block):
        self.condition = condition # условие
        self.block = block # блок

    def __repr__(self): # строковое представление объекта
        return f"ElifClause({self.condition}, {self.block})"














# TEST
if __name__ == "__main__":
    number_literal = Literal(42)
    string_literal = Literal("hello")
    variable_x = Identifier("x")

    print(number_literal)  # Literal({'value': 42})
    print(variable_x)  # Variable({'name': 'x'})