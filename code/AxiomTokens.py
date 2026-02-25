# author https://github.com/MIrrox27/Axiom
# AxiomTokens.py

from enum import Enum


# Перечисление всех типов токенов в нашем языке программирования
class AxiomTokenType(Enum):
    # ЛИТЕРАЛЫ (константные значения)
    INTEGER = 'INTEGER'  # Целое число: 42, 100, -5
    STRING = 'STRING'  # Строка в кавычках: "привет", "мир"
    FLOAT = 'FLOAT'  # Десятичное число: 3.14, 2.5, 0.5
    BOOL = 'BOOL'  # Логическое значение: true, false
    FUNCTION = 'FUNCTION' # Особый тип данных для использования в словарях и списках
    ALL = 'ALL' # Специальный тип данных для использования в словарях и списках, показывает что можно использовать любой тип данных указанных выше


    # КЛЮЧЕВЫЕ СЛОВА (зарезервированные слова языка)
    FUN = 'FUN'  # Объявление функции: fun(value){}
    CONFIG = 'CONFIG' # Объявление конфига: config{} (для использования в линуксе)
    SCRIPT = 'SCRIPT' # Объявление начала скрипта: script{} (для использования в линуксе)
    CLASS = 'CLASS'  # Объявление класса: class{}
    ENUM = 'ENUM'  # Объявление перечисления: enum{}
    IMPORT = 'IMPORT'  # Импорт модулей: import <module>
    VAR = 'VAR'  # Объявление изменяемой переменной var __name__ = value <- not const
    VAL = 'VAL' # Объявление неизменяемой переменной val __name__ = value <- const
    IF = 'IF'  # Условный оператор: if(parameters){}
    ELIF = 'ELIF' # Условный оператор: elif(parameters){}
    ELSE = 'ELSE'  # Условный оператор: else{}
    WHILE = 'WHILE'  # Цикл while: while
    FOR = "FOR"  # Цикл for: for
    FOREACH = "FOREACH" # Цикл foreach: foreach(variable in collection)
    PRINT = 'PRINT'  # Вывод на печать: print(value)
    BLOCK = 'BLOCK' # Ключевое слово для обозначения исполнения блока кода на другом языке block __lang__{code}
    #AXIOM = "AXIOM" # Еще не придумал
    RETURN = 'RETURN' # Возврат значения: return
    IS = 'IS' # is
    IN = 'IN' # in


    # ОПЕРАТОРЫ (математические и логические операции)
    PLUS = 'PLUS'  # Сложение: +
    MINUS = 'MINUS'  # Вычитание: -
    MULTIPLY = 'MULTIPLY'  # Умножение: *
    DIVIDE = 'DIVIDE'  # Деление: /
    ASSIGN = 'ASSIGN'  # Присваивание: =
    EQUALS = 'EQUALS'  # Равенство: ==
    NOT_EQUALS = 'NOT_EQUALS'  # Неравенство: !=
    LESS = 'LESS'  # Меньше: <
    GREATER = 'GREATER'  # Больше: >
    MOD = 'MOD' # %
    POWER = 'POWER' # степень числа: **
    LESS_EQUAL = 'LESS_EQUAL' # <=
    GREATER_EQUAL = 'GREATER_EQUAL' # >=

    # РАЗДЕЛИТЕЛИ (пунктуация и скобки)
    LPAREN = 'LPAREN'  # Левая круглая скобка: (
    RPAREN = 'RPAREN'  # Правая круглая скобка: )
    LBRACE = 'LBRACE'  # Левая фигурная скобка: {
    RBRACE = 'RBRACE'  # Правая фигурная скобка: }
    LBRACKET = 'LBRACKET' # Левая квадратная скобка: [
    RBRACKET = 'RBRACKET' # Правая квадратная скобка: ]
    SEMICOLON = 'SEMICOLON'  # Точка с запятой: ;
    COLON = 'COLON' # Двоеточие: :
    COMMA = 'COMMA'  # Запятая: ,

    # СПЕЦИАЛЬНЫЕ ТОКЕНЫ
    EOF = 'EOF'  # Конец файла (End Of File)
    IDENTIFIER = 'IDENTIFIER'  # Идентификатор (имя переменной/функции)


# Класс для представления отдельного токена
class AxiomToken:
    def __init__(self, type: AxiomTokenType, value: any = None, line: int = 1):
        self.type = type  # Тип токена из перечисления TokenType
        self.value = value  # Значение токена (для чисел, строк, идентификаторов)
        self.line = line  # Номер строки, где найден токен (для отладки ошибок)

    def __str__(self):
        # Красивое строковое представление токена для отладки
        if self.value is not None:
            return f"Token({self.type}, {repr(self.value)}, line: {self.line})"
        return f"Token({self.type}, line: {self.line})"

    def __repr__(self):
        # Техническое строковое представление
        return self.__str__()