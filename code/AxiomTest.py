# author https://github.com/MIrrox27/Axiom
# AxiomTest.py

from AxiomLexer import AxiomLexer
from AxiomTokens import AxiomTokenType
from AxiomASTNodes import *
from AxiomParser import AxiomParser

class Test:
    def __init__(self):
        self.test_code = '''
        # Объявление переменных
        var x = 42
        var pi = 3.14
        var name = "Василий"
        var active = true
        var inactive = false
        
        # Арифметические операции
        val sum = x + 10
        val power = 2 ** 3
        val remainder = 10 % 3
        
        # Условный оператор
        if x > 5 {
            print "x больше 5"
        } else {
            print "x меньше или равно 5"
        }
        
        # Цикл
        cg i = 0
        while i < 3 {
            print "Итерация: " + i
            i = i + 1
        }
        
        # Вызов функции (объявление)
        fun greet(person) {
            print "Привет, " + person
        }
        
        # Использование функции
        greet(name)
        
        '''


    def test_lexer_complete(self):
        print("=" * 60)
        print("Финальный Тест")
        print("=" * 60)

        lexer = AxiomLexer(self.test_code)
        tokens = []

        print("Исходный код:")
        print(self.test_code)
        print("\n" + "=" * 60)
        print("Распознанные токены:")
        print("=" * 60)

        while True:
            token = lexer.get_next_token()
            tokens.append(token)
            print(f"Строка {token.line:3d}: {token}")

            if token.type == AxiomTokenType.EOF:
                break

        print("=" * 60)
        print(f"Всего токенов: {len(tokens)}")

        # Группируем токены по типам для статистики
        token_counts = {}
        for token in tokens:
            token_type = token.type.value
            token_counts[token_type] = token_counts.get(token_type, 0) + 1

        print("\nСтатистика по типам токенов:")
        for token_type, count in sorted(token_counts.items()):
            print(f"  {token_type:15s}: {count:3d}")

        return tokens


    def test_lexer_edge_cases(self):
        print("\n" + "=" * 60)
        print("ТЕСТИРОВАНИЕ ПОГРАНИЧНЫХ СЛУЧАЕВ")
        print("=" * 60)

        edge_cases = [
            ("Пустая строка", ""),
            ("Только пробелы", "   \n  \t  "),
            ("Только комментарий", "# только комментарий"),
            ("Число с точкой в конце", "5."),
            ("Число с точкой в начале", ".5"),
            ("Сложное выражение", "x = (a + b) * c ** 2 % 3"),
            ("Вложенные строки", 'print "Строка с "'),
        ]

        for description, code in edge_cases:
            print(f"\n{description}:")
            print(f"Код: '{code}'")
            lexer = AxiomLexer(code)
            while True:
                token = lexer.get_next_token()
                print(f"  {token}")
                if token.type == AxiomTokenType.EOF:
                    break


    def test_AST(self):
        # TODO: сделать оформление

        print('\nAST TEST')
        print('=' * 60)
        number_literal = Literal(42)
        string_literal = Literal("hello")
        variable_x = Identifier("x")

        print(number_literal)
        print(variable_x)
        print(string_literal)

        print('=' * 60)

        multiply = BinaryOp(
            left=Literal(5),
            operator="*",
            right=Literal(3)
        )


        expression = BinaryOp(
            left=Identifier("x"),
            operator="+",
            right=multiply
        )

        print("AST дерево:")
        print(expression)
        print("\nРазберем по частям:")
        print(f"Весь узел: {expression}")
        print(f"Левый операнд: {expression.left}")
        print(f"Оператор: {expression.operator}")
        print(f"Правый операнд: {expression.right}")
        print(f"  → Левый операнд умножения: {expression.right.left}")
        print(f"  → Правый операнд умножения: {expression.right.right}")

        print('=' * 60)



    def test_parser(self):
        # TODO: сделать оформление
        lexer = AxiomLexer("x + 5")
        parser = AxiomParser(lexer)

        print(f"Текущий токен: {parser.current_token}")
        # Должно быть: Token(IDENTIFIER, 'x', line: 1)

        # Проверяем идентификатор
        parser.eat(AxiomTokenType.IDENTIFIER)
        print(f"{parser.current_token}")
        # Должно быть: Token(PLUS, line: 1)

        parser.eat(AxiomTokenType.PLUS)
        print(parser.current_token)
        # должно быть Token(AxiomTokenType.NUMBER, 5, line: 1)

        print('><><' * 60)
        test_cases = [
            # Простые объявления
            ("var x;", "VarDeclaration с именем x без значения"),
            ("var x = 5;", "VarDeclaration с именем x и значением 5"),
            ("val y = 10;", "VarDeclaration с val, именем y и значением 10"),

            # Блоки кода
            ("{}", "Пустой блок"),
            ("{ var x = 5; }", "Блок с одной инструкцией"),
            ("{ var x = 5; var y = 10; }", "Блок с двумя инструкциями"),

            # Инструкции-выражения
            ("x + 5;", "ExpressionStmt с выражением x + 5"),
            ("42;", "ExpressionStmt с литералом 42"),

            # Пустая инструкция
            (";", "EmptyStmt"),
        ]

        print("Тестирование парсинга инструкций:")
        print("=" * 60)

        for code, description in test_cases:
            print(f"\nТест: {description}")
            print(f"Код: {code}")

            lexer = AxiomLexer(code)
            parser = AxiomParser(lexer)

            try:
                result = parser.parse_statement()
                print(f"Результат: {result}")

                # Проверяем, что весь код разобран
                if parser.current_token.type != AxiomTokenType.EOF:
                    print(f"ВНИМАНИЕ: Не весь код разобран. Остался: {parser.current_token}")

            except Exception as e:
                print(f"ОШИБКА: {e}")


# Запуск теста
if __name__ == "__main__":

    test = Test()
    #test.test_lexer_complete()
    #test.test_lexer_edge_cases()
    #test.test_AST()
    test.test_parser()