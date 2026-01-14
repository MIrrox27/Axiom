# author https://github.com/MIrrox27/Axiom
# AxiomTest.py

from AxiomLexer import AxiomLexer
from AxiomTokens import AxiomTokenType

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


    def test_edge_cases(self):
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





# Запуск теста
if __name__ == "__main__":

    test1 = Test()
    test1.test_lexer_complete()
    test1.test_edge_cases()