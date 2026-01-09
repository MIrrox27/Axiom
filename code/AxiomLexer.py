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

    def read_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return AxiomTokenType.NUMBER, int(result)

    def get_next_token(self):
        while self.current_char is not None:  # пока символ который мы проверяем не равен None
            if self.current_char.isspace():  # если символ который мы проверяем равен пробелу
                self.skip_whitespace()  # то мы пропускаем пробелы

            if self.current_char == "$" or self.current_char == "#":  # если символ который мы проверяем равен символу комментария ( я сделал 2 символа комментариев)
                self.skip_comment()  # то мы вызываем функцию для пропуска коммментов
                continue  # continue начинает цикл заново с нового символа. Это гарантирует, что после пропуска пробелов/комментариев мы обработаем следующий значимый символ

            if self.current_char.isdigit():
                token_type, velue = self.read_number()
                return AxiomToken(token_type, velue, self.line)

            return AxiomToken(AxiomToken.EOF, line=self.line)


if __name__ == "__main__":
    lexer = AxiomLexer("10 20 30 ")
    tokens = []
    for _ in range(4):  # 3 числа + EOF
        token = lexer.get_next_token()
        tokens.append(token)
        print(token)

        # TODO: 09.01.2026 добавить обработку чисел с плавающей точкой