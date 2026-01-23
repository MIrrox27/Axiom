# author https://github.com/MIrrox27/Axiom
# AxiomLexer.py

from AxiomTokens import AxiomTokenType, AxiomToken


class AxiomLexer:



    def __init__(self, text: str):
        self.text = text  # сам код который мы передаем в наш интерпритатор
        self.position = 0  # позиция "курсора" в тексте порядковый номер символа
        self.line = 1  # линия (строка в которой мы находимся) (по типу координаты Y)
        self.current_char = self.text[
            0] if self.text else None  # символ, который мы сейчас обрабатываем. Т. е если символ text не равен None то мы присваиваем self.current_char значение этого символа, иначе self.current_char = None
        self.KEYWORDS = {  # ключевые слова
            'fun': AxiomTokenType.FUN,
            'if': AxiomTokenType.IF,
            'elif': AxiomTokenType.ELIF,
            'else': AxiomTokenType.ELSE,
            'while': AxiomTokenType.WHILE,
            'for': AxiomTokenType.FOR,
            'foreach': AxiomTokenType.FOREACH,
            'var': AxiomTokenType.VAR,
            'val': AxiomTokenType.VAL,
            'print': AxiomTokenType.PRINT,
            'true': AxiomTokenType.BOOL,
            'false': AxiomTokenType.BOOL,
            'class': AxiomTokenType.CLASS,
            'import': AxiomTokenType.IMPORT,
            'enum': AxiomTokenType.ENUM,
            'script': AxiomTokenType.SCRIPT,
            'config': AxiomTokenType.CONFIG,
            'return': AxiomTokenType.RETURN
        }


    def error(self, message: str):
        raise Exception(f'[Lexer Error] in {self.line}: {message}')

    def advance(self):  # функция, которая двигает вперед наш курсор
        if self.current_char == "\n":
            self.line += 1  # если current_char равен символу перехода строки, то мы опускаемся вниз
        self.position += 1  # так как мы прошли символ перехода строки, надо переместиться на новый символ

        if self.position >= len(self.text):  # если наша позиция в тексе выходит за его рамки (текста)
            self.current_char = None  # то символ который мы обрабатываем равен None
        else:
            self.current_char = self.text[self.position]  # иначе self.символ_для_обработки = self.код[позиция_в_коде]

    def peekPosition(self, lookhead: int = 1):
        peek_position = self.position + lookhead
        if peek_position >= len(self.text):
            return None
        return self.text[peek_position]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():  # пока символ который мы проверяем НЕ равен None и это же символ равен пробелу
            self.advance()  # то мы двигаемся вперед

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':  # пока символ который мы проверяем НЕ равен None и находится на той же строке+
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def read_string(self):
        self.advance() # пропускаем первую кавычку (пример -> "строка")
        result = ''

        while self.current_char is not None and self.current_char != '"': # цикл идет пока проверяемый символ != None и != '"'
            result += self.current_char
            self.advance() # двигаемся вперед

        if self.current_char != '"': # проверяем, что строка закрыта
            self.error("second quotation mark not found")

        self.advance() # пропускаем закрывающую кавычку
        return AxiomTokenType.STRING, result

    def read_identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'): # первый символ - буква или подчеркивание
            result += self.current_char
            self.advance()
        return result




    def read_number(self):
        result = ''
        has_dot = False

        if self.current_char == '.':
            # Проверяем следующий символ - если цифра, то это float
            if self.peekPosition() and self.peekPosition().isdigit():
                has_dot = True
                result = '0.'  # Добавляем ведущий ноль
                #print(result)
                self.advance()  # Пропускаем точку

        while self.current_char is not None:

            if self.current_char == '.': #
                if has_dot == True: #
                    self.error("Two dots in number!") # если точка встречается повторно, выводим ошибку
                has_dot = True
                result += '.'

            elif self.current_char.isdigit(): # если символ число
                result += self.current_char # добавляем его к нашему результату (возвращаемому значению)

            else:
                break # если проверяемый символ не точка и не число, то выходим

            self.advance() # двигаемся вперед

        # Проверяем, что число не состоит из одной точки
        if result == '' or result == '0.':
            self.error("Неверный формат числа")

        if has_dot:
            return AxiomTokenType.FLOAT, float(result) # если точка есть, возвращаем float
        else:
            return AxiomTokenType.NUMBER, int(result) # если точки нет, возвращаем int

    def get_next_token(self, debug: bool= False):
        while self.current_char is not None:  # пока символ который мы проверяем не равен None
            if debug == True:
                print(f"DEBUG: current_char={repr(self.current_char)}, pos={self.position}")
            if self.current_char.isspace():  # если символ который мы проверяем равен пробелу
                self.skip_whitespace()  # то мы пропускаем пробелы

            if self.current_char is not None and (self.current_char.isdigit() or
                    (self.current_char == '.' and self.peekPosition() and self.peekPosition().isdigit())):
                token_type, value = self.read_number()
                return AxiomToken(token_type, value, self.line)

            # -- операторы и разделители --

            if self.current_char == '+':
                self.advance()
                return AxiomToken(AxiomTokenType.PLUS, line=self.line)

            if self.current_char == '-':
                self.advance()
                return AxiomToken(AxiomTokenType.MINUS, line=self.line)

            if self.current_char == '*':
                self.advance()

                if self.current_char == '*':
                    return AxiomToken(AxiomTokenType.POWER, line=self.line)
                else:
                    return AxiomToken(AxiomTokenType.MULTIPLY, line=self.line)

            if self.current_char == '/':
                self.advance()
                return AxiomToken(AxiomTokenType.DIVIDE, line=self.line)

            if self.current_char == '%':
                self.advance()
                return  AxiomToken(AxiomTokenType.MOD, line=self.line)

            if self.current_char == '=':
                self.advance()

                if self.current_char == '=':
                    return AxiomToken(AxiomTokenType.EQUALS, line=self.line)

                else:
                    return AxiomToken(AxiomTokenType.ASSIGN, line=self.line)

            if self.current_char == '!':
                self.advance()

                if self.current_char == '=':
                    return AxiomToken(AxiomTokenType.NOT_EQUALS)
                else:
                    self.error("WHERE IS '=' AFTER '!' ???")

            if self.current_char == '<':
                self.advance()
                return AxiomToken(AxiomTokenType.LESS, line=self.line)

            if self.current_char == '>':
                self.advance()
                return AxiomToken(AxiomTokenType.GREATER, line=self.line)

            if self.current_char == '(':
                self.advance()
                return AxiomToken(AxiomTokenType.LPAREN, line=self.line)

            if self.current_char == ')':
                self.advance()
                return AxiomToken(AxiomTokenType.RPAREN, line=self.line)

            if self.current_char == '{':
                self.advance()
                return AxiomToken(AxiomTokenType.LBRACE, line=self.line)

            if self.current_char == '}':
                self.advance()
                return AxiomToken(AxiomTokenType.RBRACE, line=self.line)

            if self.current_char == '[':
                self.advance()
                return AxiomToken(AxiomTokenType.RBRACKET, line=self.line)

            if self.current_char == ']':
                self.advance()
                return AxiomToken(AxiomTokenType.LBRACKET, line=self.line)

            if self.current_char == ';':
                self.advance()
                return AxiomToken(AxiomTokenType.SEMICOLON, line=self.line)

            if self.current_char == ',':
                self.advance()
                return AxiomToken(AxiomTokenType.COMMA, line=self.line)

            if self.current_char == '"': #
                token_type, value = self.read_string()
                return AxiomToken(token_type, value, self.line)

            if self.current_char == "#":  # если символ который мы проверяем равен символу комментария ( я сделал 2 символа комментариев)
                self.skip_comment()  # то мы вызываем функцию для пропуска коммментов
                continue  # continue начинает цикл заново с нового символа. Это гарантирует, что после пропуска пробелов/комментариев мы обработаем следующий значимый символ

            if self.current_char == '/':
                self.advance()
                if self.current_char == '/':  # Комментарий //
                    self.skip_comment()
                    continue

            if self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
                identifier = self.read_identifier()

                if identifier in self.KEYWORDS: # ищем ключевое слово
                    token_type = self.KEYWORDS[identifier]

                    # Для булевых значений возвращаем их значение
                    if token_type == AxiomTokenType.BOOL:
                        return AxiomToken(token_type, identifier == 'true', self.line)
                    return AxiomToken(token_type, identifier, self.line)

                # Обычный идентификатор (если ничего не нашли возвращаем их название)
                return AxiomToken(AxiomTokenType.IDENTIFIER, identifier, self.line)

        return AxiomToken(AxiomTokenType.EOF, line=self.line)


if __name__ == "__main__":
    test_code = "cg x = 2 ** 3; print x % 3; [sdfsdfsdfs] {} ()"
    lexer = AxiomLexer(test_code)
    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type == AxiomTokenType.EOF:
            break

        # TODO: 09.01.2026 - добавить обработку чисел с плавающей точкой СДЕЛАНО
        # TODO: 09.01.2026 - сделать базовую обработку строк СДЕЛАНО
        # TODO: 09.01.2026 - сделать небольшое описание + часть доки + цели
        # TODO: 11.01.2026 - сделать обработку ключевых слов СДЕЛАНО
        # TODO: 11.01.2026 - сделать обработку операторов (+, - и т.д) СДЕЛАНО
        # TODO: 11.01.2026 - доделать лексер и провести финальные тесты СДЕЛАНО