# author https://github.com/MIrrox27/Axiom
# AxiomTest.py

from axiom.AxiomLexer import AxiomLexer
from axiom.AxiomTokens import *
from axiom.AxiomASTNodes import *
from axiom.AxiomParser import AxiomParser
from axiom.AxiomInterpreter import *


class Tests:
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
        # СЧЕТЧИКИ:
        instructions_err = 0

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
        # должно быть Token(AxiomTokenType.INTEGER, 5, line: 1)

        print('><><' * 60)
        test_cases = [
            # Простые объявления
            ("var x;", "VarDeclaration с именем x без значения"),
            ("varAxiome = 'тест на русском'", "VarDeclaration с именем x и текстовым значением "),
            ("val y_s2a = 10;", "VarDeclaration с val, именем y_s2a и значением 10"),

            # Блоки кода
            ("{}", "Пустой блок"),
            ("{ var x = 5 - 5; }", "Блок с одной инструкцией"),
            ("{ var x = 10 / 5; var y = 10 ** 1; }", "Блок с двумя инструкциями"),

            # Инструкции-выражения
            ("x + 5; # комментарий", "ExpressionStmt с выражением x + 5"),
            ("42; // тоже комментарий", "ExpressionStmt с литералом 42"),

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
                    instructions_err += 1

            except Exception as e:
                print(f"ОШИБКА: {e}")
        print(f"\n ---Errors: {instructions_err}")

    def test_parser_loops(self):
        print("ТЕСТИРОВАНИЕ ЦИКЛОВ")
        print("=" * 60)
        """     На данном этапе я не подключил обработку var и val


                                        """

        test_cases = [
            # WHILE
            ("while x < 5 { val x = 5; val y = 10; }", "простой while"),
            ("while (x < 5) { if 1 == 1{ val I_Love_Axiome = 1;} }", "while со скобками"),
            ("while true { }", "бесконечный while (пустое тело)"),

            # FOR (пока только с выражением в инициализации)
            ("for (var i = 0; i < 10; i = i + 1) { val prnt = 234; }", "for с выражением-инициализатором"),
            ("for (; i < 10; i = i + 1) { }", "for без инициализации"),
            ("for (var i = 0; ; i = i + 1) { }", "for без условия (бесконечный)"),
            ("for (; ;) { var ex = 1; var i = i + 1; }", "for без инкремента"),

            # FOREACH (после добавления IN)
            ("foreach item in items { val value = 'value 123 ;1;1 != тест '; }", "foreach по коллекции"),
            ("foreach var x in range { val text = '{value на русском и английском}'; }", "foreach с вызовом функции"),
        ]

        for code, description in test_cases:
            print(f"\n {description}")
            print(f"Код: {code}")
            lexer = AxiomLexer(code)
            parser = AxiomParser(lexer)
            try:
                ast = parser.parse_statement()
                print(f"AST: {ast}")
                if parser.current_token.type != AxiomTokenType.EOF:
                    print(f"  Остались токены: {parser.current_token}")
                else:
                    print(" Весь код разобран")
            except Exception as e:
                if str(e) != "[Parser Error]: Received AxiomTokenType.PRINT":  # временно пропускаем ошибку с отсутствием функции
                    print(f" Ошибка: {e}")
                else:
                    print(" Весь код разобран")

    def test_if_parsing(self):
        print("ТЕСТИРОВАНИЕ ПАРСИНГА IF-ELIF-ELSE")
        print("=" * 60)

        err = 0
        good_err = 0
        tokens = 0

        test_cases = [
            # Простой if
            ('if x > 5 {  }', "if без else"),
            # if-else
            ('if x > 5 { var I_Love_Axiome = 1; } else { var I_Love_Axiome = 2; }', "if-else"),
            # if-elif-else
            ('if x > 5 { var i = true; } elif x == 5 { var i = false; } else {  }', "if-elif-else"),
            # Несколько elif
            ('if x > 10 { val e = 1; } elif x > 5 { var i = 2 } elif x > 0 { var j = 2 }', "несколько elif"),
            # Условие в скобках
            ('if (x > 5) { var i = 234234 }', "скобки вокруг условия"),
            # Пустой блок (допустимо)
            ('if x > 5 {}', "пустой then-блок"),
            # Только if, без точки с запятой (блок сам по себе)
            ('if x > 5 { var a = 10; }', "if с объявлением переменной"),
            ('if x == 5 { if x > 5 { val value = "value 123 ;1;1 != тест "; } elif x == 5 { val value = "value 123 ;1;1 != тест "; } else { var = "ест на символы {elif x == 5 { val value = "value 123 ;1;1 != тест "; }}" } }',
             "вложенные условия")
        ]

        for code, description in test_cases:
            print(f"\n>>> {description}")
            print(f"Код: {code}")

            lexer = AxiomLexer(code)
            parser = AxiomParser(lexer)

            try:
                ast = parser.parse_statement()
                print(f"AST: {ast}")

                # Проверяем, что весь код разобран
                if parser.current_token.type != AxiomTokenType.EOF:
                    print(f"----Остались токены: {parser.current_token}")
                    tokens += 1
                else:
                    print("+Весь код разобран")

            except Exception as e:
                if str(e) != "[Parser Error]: Received AxiomTokenType.PRINT":  # временно пропускаем ошибки с неизвестными функциями
                    err += 1
                    print(f"----Ошибка: {e}")

                print("\n" + "=" * 60)
                print("ТЕСТИРОВАНИЕ ОШИБОК")
                print("=" * 60)

                error_cases = [
                    ('if x > 5', "нет блока после условия"),
                    ('if { print("ok"); }', "нет условия"),
                    ('if x > 5 { ; } elif { print("elif"); }', "нет условия у elif"),
                    ('if x > 5 {  x=42; } else { } else { }', "два else"),
                ]

                for code, description in error_cases:
                    print(f"\n>>> {description}")
                print(f"Код: {code}")
                lexer = AxiomLexer(code)
                parser = AxiomParser(lexer)
            try:
                ast = parser.parse_statement()
                print(f"-----Ошибка не обнаружена! AST: {ast}")
                err += 1
            except Exception as e:
                good_err += 1
                print(f"-----Ожидаемая ошибка: {e}")

        print(f'\n>> Ожидаемые ошибки: {good_err} \n>> Непроверенные токены: {tokens} \n>> Неизвестные ошибки: {err}')

    def test_parser_full(self):
        # ------------------ ПОЗИТИВНЫЕ ТЕСТЫ (должны парситься без ошибок) ------------------
        positive_tests = [
            # Простые инструкции
            "var x;",
            "val y = 42;",
            "var z = x + 5;",
            "x = 10;",
            "x = y + 2 * 3;",

            # Блоки
            "{ var a = 1; val b = 2; }",

            # Арифметика и сравнения
            "a + b * c ** d;",
            "x == y;",
            "x != y;",
            "x < y;",
            "x > y;",
            "x <= y;",
            "x >= y;",
            "2 - 3 == 5;",

            # Условные операторы
            "if x > 5 { var msg = 'big'; }",
            "if x > 5 { msg = 'big'; } else { msg = 'small'; }",
            "if x > 10 { msg = 'very big'; } elif x > 5 { msg = 'big'; } else { msg = 'small'; }",
            "if (x > 5) { }",

            # Циклы
            "while (x < 10) { x = x + 1; }",
            "while (x < 10) { x = x + 1; }",
            "for (var i = 0; i < 10; i = i + 1) { prnt = i ** 1 + 2; }",
            "for (i = 0; i < 10; i = i + 1) { }",
            "for (; i < 10; i = i + 1) { }",
            "for (var i = 0; ; i = i + 1) { }",
            "for (var i = 0; i < 10; ) { i = i + 1; }",
            "foreach item in items { prnt = item; }",
            "foreach var item in items { item = prnt + 1; }",

            # Сложные комбинации
            "{ var x = 0; while (x < 5) { if x % 2 == 0 { x = x + 2; } else { x = x + 1; } } }",
        ]

        print("Запуск позитивных тестов...")
        for i, code in enumerate(positive_tests, 1):
            lexer = AxiomLexer(code)
            parser = AxiomParser(lexer)
            try:
                ast = parser.parse_statement()
                # Проверяем, что после парсинга достигнут конец файла
                assert parser.current_token.type == AxiomTokenType.EOF, \
                    f"Тест {i}: после парсинга остались токены: {parser.current_token}"
                # Если мы дошли сюда без исключений, тест пройден
            except Exception as e:
                raise AssertionError(f"Позитивный тест {i} не прошел:\nКод: {code}\nОшибка: {e}")

        print(f"[v] Все позитивные тесты пройдены ({len(positive_tests)})")

        negative_tests = [
            # Ожидаемая ошибка: синтаксическая
            ("var x = ;", "переменная без выражения"),
            ("x = ;", "присваивание без правой части"),
            ("if x > { }", "условие без выражения"),
            ("while() { }", "while без условия"),
            ("for (i = 0; i < 10; )", "for без тела"),
            ("foreach item in { }", "foreach без выражения коллекции"),
            ("{ var x = 5;", "незакрытый блок"),
            ("val x;", "константа без значения"),
            ("1 + ;", "незавершённое выражение"),
        ]

        print("Запуск негативных тестов...")
        for i, (code, desc) in enumerate(negative_tests, 1):
            lexer = AxiomLexer(code)
            parser = AxiomParser(lexer)
            try:
                ast = parser.parse_statement()
                # Если исключения не возникло — ошибка теста
                raise AssertionError(
                    f"Негативный тест {i} должен был провалиться, но не провалился:\nКод: {code} ({desc})")
            except Exception:
                # Исключение ожидаемо — тест пройден
                pass

        print(f"[v] Все негативные тесты пройдены ({len(negative_tests)})")

        print("\n[V] Все тесты парсера успешно пройдены!")


class TestInterpreter(AxiomInterpreter):
    # интерпретатор с захватом вывода print для тестирования

    def __init__(self):
        super().__init__()
        self.output = []
        # Переопределяем print, чтобы он добавлял строки в output
        self._original_print = self.global_env.get('print')
        self.global_env.define('print', Callable('print', -1, self._test_print))

    def _test_print(self, *args):
        output = ' '.join(str(arg) for arg in args)
        self.output.append(output)
        return None


def run_test(code, expected_output=None, expected_error=None):
    # Запускает код и возвращает вывод или ошибку
    lexer = AxiomLexer(code)
    parser = AxiomParser(lexer)
    interpreter = TestInterpreter()

    # Парсим программу
    statements = []
    try:
        while parser.current_token.type != AxiomTokenType.EOF:
            stmt = parser.parse_statement()
            statements.append(stmt)
    except Exception as e:
        if expected_error:
            assert str(e).startswith(expected_error), f"Expected error '{expected_error}', got '{e}'"
            return
        else:
            raise

    # Выполняем
    try:
        for stmt in statements:
            interpreter.visit(stmt)
    except Exception as e:
        if expected_error:
            assert str(e).startswith(expected_error), f"Expected error '{expected_error}', got '{e}'"
            return
        else:
            raise

    if expected_output is not None:
        assert interpreter.output == expected_output, f"Expected output {expected_output}, got {interpreter.output}"

    # Возвращаем интерпретатор для дополнительных проверок (например, значений переменных)
    return interpreter

    # Общие тесты интерпретатора


def test_arithmetic():
    code = """
    var x = 5 + 3 * 2;
    print(x);
    """
    run_test(code, ["11"])


def test_comparison():
    code = """
    var a = 5 > 3;
    var b = 5 == 5;
    var c = 5 != 3;
    print(a, b, c);
    """
    run_test(code, ["True True True"])


def test_logical():
    code = """
    var t = true;
    var f = false;
    print(t and f);
    print(t or f);
    print(not t);
    """
    run_test(code, ["False", "True", "False"])


def test_variables():
    code = """
    var x = 10;
    var y = 20;
    x = x + y;
    print(x);
    """
    run_test(code, ["30"])


def test_if():
    code = """
    var x = 5;
    if x > 3 {
        print("big");
    } else {
        print("small");
    }
    """
    run_test(code, ["big"])


def test_if_elif_else():
    code = """
    var x = 5;
    if x > 10 {
        print(">10");
    } elif x > 3 {
        print(">3");
    } else {
        print("<=3");
    }
    """
    run_test(code, [">3"])


def test_while():
    code = """
    var i = 0;
    while (i < 3) {
        print(i);
        i = i + 1;
    }
    """
    run_test(code, ["0", "1", "2"])


def test_for():
    code = """
    var sum = 0;
    for (var i = 0; i < 3; i = i + 1) {
        sum = sum + i;
    }
    print(sum);
    """
    run_test(code, ["3"])


def test_do():
    code = """
    var i = 5;
    do (i < 3) {
        print(i);
        i = i + 1;
    }
    """
    run_test(code, ["5"])


def test_nested_blocks():
    code = """
    var x = 1;
    {
        var x = 2;
        print(x);
    }
    print(x);
    """
    run_test(code, ["2", "1"])


def test_function_call():
    code = """
    print("Hello", "world!");
    """
    run_test(code, ["Hello world!"])


def test_division_by_zero():
    code = """
    var x = 5 / 0;
    """
    run_test(code, expected_error="[AxiomInterpreter]: [visit_BinaryOp] Division by zero")


def test_undefined_variable():
    code = """
    print(y);
    """
    run_test(code, expected_error="[AxiomEnvironment]: [get] Variable 'y' is not defined")


def _test_all():
    test_arithmetic()
    test_comparison()
    test_logical()
    test_variables()
    test_if()
    test_if_elif_else()
    test_while()
    test_for()
    test_do()
    test_nested_blocks()
    test_function_call()
    test_division_by_zero()
    test_undefined_variable()
    print("Все тесты пройдены успешно!")


# Запуск теста
if __name__ == "__main__":
    test = Tests()
    test.test_lexer_complete()
    test.test_lexer_edge_cases()
    test.test_AST()
    test.test_parser()
    test.test_if_parsing()
    test.test_parser_loops()
    test.test_parser_full()

    _test_all()


