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

    def error(self, message: str):
        raise Exception(f'Error in {self.line}: {message}')

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

        #
        while self.current_char is not None and self.current_char != '"': # цикл идет пока проверяемый символ != None и != '"'
            result += self.current_char
            self.advance() # двигаемся вперед

        if self.current_char != '"': # проверяем, что строка закрыта
            self.error("second quotation mark not found")

        self.advance() # пропускаем закрывающую кавычку
        return AxiomTokenType.STRING, result


    def read_number(self):
        result = ''
        has_dot = False

        if self.current_char == '.':
            # Проверяем следующий символ - если цифра, то это float
            if self.peekPosition() and self.peekPosition().isdigit():
                has_dot = True
                result = '0.'  # Добавляем ведущий ноль
                print(result)
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

    def get_next_token(self):
        while self.current_char is not None:  # пока символ который мы проверяем не равен None
            if self.current_char.isspace():  # если символ который мы проверяем равен пробелу
                self.skip_whitespace()  # то мы пропускаем пробелы

            if self.current_char == '"': #
                token_type, value = self.read_string()
                return AxiomToken(token_type, value, self.line)

            if self.current_char == "$" or self.current_char == "#":  # если символ который мы проверяем равен символу комментария ( я сделал 2 символа комментариев)
                self.skip_comment()  # то мы вызываем функцию для пропуска коммментов
                continue  # continue начинает цикл заново с нового символа. Это гарантирует, что после пропуска пробелов/комментариев мы обработаем следующий значимый символ

            if (self.current_char.isdigit() or
                    (self.current_char == '.' and self.peekPosition() and self.peekPosition().isdigit())):
                token_type, velue = self.read_number()
                return AxiomToken(token_type, velue, self.line)

            return AxiomToken(AxiomToken.EOF, line=self.line)


if __name__ == "__main__":
    lexer = AxiomLexer('"hello"')
    print(lexer.get_next_token())

        # TODO: 09.01.2026 - добавить обработку чисел с плавающей точкой СДЕЛАНО
        # TODO: 09.01.2026 - сделать базовую обработку строк СДЕЛАНО
        # TODO: 09.01.2026 - сделать небольшое описание + часть доки + цели