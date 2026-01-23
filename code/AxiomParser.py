# author https://github.com/MIrrox27/Axiom
# AxiomParser.py

from AxiomASTNodes import *
from AxiomLexer import AxiomLexer
from  AxiomTokens import AxiomTokenType


class AxiomParser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(f'[Parser Error]: {message}')

    def eat(self, token_type): # Проверяет, что текущий токен имеет ожидаемый тип
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Pending {token_type}, received {self.current_token.type}") # self.current_token.type - тип токена который мы получили,
            # token_type - токен, который нам нужен

    def parse_factor(self):

        node = self.parse_primary()

        while self.current_token.type == AxiomTokenType.POWER:
            operator_token = self.current_token
            self.eat(AxiomTokenType.POWER)
            right = self.parse_factor()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node

    def parse_term(self):
        node = self.parse_factor()
         #
        while self.current_token.type in (AxiomTokenType.MULTIPLY, AxiomTokenType.DIVIDE, AxiomTokenType.MOD, AxiomTokenType.POWER):
            operator_token = self.current_token
            self.eat(operator_token.type)

            right = self.parse_factor()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node



    def parse_primary(self):  # Парсит первичные выражения. Возвращает узел AST
        token = self.current_token

        if token.type in (AxiomTokenType.NUMBER, AxiomTokenType.FLOAT): #
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxiomTokenType.STRING:
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxiomTokenType.BOOL:
            self.eat(token.type)
            return  Literal(token.value)

        elif token.type == AxiomTokenType.IDENTIFIER:
            self.eat(token.type)
            return Literal(token.value)


        elif token.type == AxiomTokenType.LPAREN:
            self.eat(AxiomTokenType.LPAREN) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RPAREN)  #
            return node

        elif token.type == AxiomTokenType.LBRACE:
            self.eat(AxiomTokenType.LBRACE) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RBRACE)  #
            return node

        elif token.type == AxiomTokenType.LBRACKET:
            self.eat(AxiomTokenType.LBRACKET)  #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RBRACKET)  #
            return node

        else:
            self.error(f"Received {token.type}")

    def parse_expression(self):
        node = self.parse_term()

        # парсим операторы + и -
        while self.current_token.type in (AxiomTokenType.PLUS, AxiomTokenType.MINUS):
            operator_token = self.current_token
            self.eat(operator_token.type) # обрабатываем оператор (сьедаем)

            right = self.parse_term() # парсим праавую часть

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node





# TEST
if __name__ == '__main__':




    # Тестируем приоритет операторов
    test_cases = [
        "(2 + 3) * 4",  # → (2 + 3) * 4
        "2 * (3 + 4)",  # → 2 * (3 + 4)
        "((2 + 3) * 4)", # → ((2 + 3) * 4)
        "1 ** 1"
    ]

    for code in test_cases:
        lexer = AxiomLexer(code)
        parser = AxiomParser(lexer)
        result = parser.parse_expression()
        print(f"{code:15s} → {result}")


  #TODO:  -