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
    FUNCTION_TYPE = 'FUNCTION_TYPE' # Особый тип данных для использования в словарях и списках (понадобится в будущем)
    ALL = 'ALL' # Специальный тип данных для использования в словарях и списках, показывает что можно использовать любой тип данных указанных выше (понадобится в будущем)


    # КЛЮЧЕВЫЕ СЛОВА (зарезервированные слова языка)
    FUN = 'FUN'  # Объявление функции: fun(value){}
    CONFIG = 'CONFIG' # Объявление конфига: config{} (для использования в линуксе)
    SCRIPT = 'SCRIPT' # Объявление начала скрипта: script{} (для использования в линуксе)
    CLASS = 'CLASS'  # Объявление класса: class(наследование){}
    ENUM = 'ENUM'  # Объявление перечисления: enum{}
    IMPORT = 'IMPORT'  # Импорт модулей: import module
    VAR = 'VAR'  # Объявление изменяемой переменной var __name__ = value <- not const
    VAL = 'VAL' # Объявление неизменяемой переменной val __name__ = value <- const
    IF = 'IF'  # Условный оператор: if(parameters){}
    ELIF = 'ELIF' # Условный оператор: elif(parameters){}
    ELSE = 'ELSE'  # Условный оператор: else{}
    WHILE = 'WHILE'  # Цикл while: while
    DO = 'DO' # Цикл do (образован от цикла do while), первый раз выполняется всегда, потом по условию
    FOR = "FOR"  # Цикл for: for
    FOREACH = "FOREACH" # Цикл foreach: foreach(variable in collection)
    PRINT = 'PRINT'  # Вывод на печать: print(value)
    INPUT = 'INPUT'
    BLOCK = 'BLOCK' # Ключевое слово для обозначения исполнения блока кода на другом языке block __lang__{axiom}
    PYTHON = 'PYTHON' # Ключевое слово для исполнения кода на питоне
    #AXIOM = "AXIOM" # Еще не придумал
    RETURN = 'RETURN' # Возврат значения: return
    IS = 'IS' # Ключевое слово is
    IN = 'IN' # Ключевое слово in
    AND = 'AND' # Ключевое слово and (&&)
    OR = 'OR' # Ключевое слово or (||)
    NONE = 'NONE' # Ключевое слово nill (мб, сделаем так, чтобы можно было заменить на ";;")
    NOT = 'NOT' # Ключевое слово not, так же может обозначаться знаком "!"



    # ОПЕРАТОРЫ (математические и логические операции)
    PLUS = 'PLUS'  # Сложение: +
    MINUS = 'MINUS'  # Вычитание: -
    INCREMENT = 'INCREMENT' # ++x
    DECREMENT = 'DECREMENT' # --x
    POST_INCREMENT = 'POST_INCREMENT'  # x++
    POST_DECREMENT = 'POST_DECREMENT'  # x--
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
    DOT = 'DOT' # точка .

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