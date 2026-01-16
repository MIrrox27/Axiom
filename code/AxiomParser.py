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
        while self.current_token.type in (AxiomTokenType.MULTIPLY, AxiomTokenType.DIVIDE, AxiomTokenType.MOD):
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
            self.error('временно не доступно')
            #self.eat(AxiomTokenType.LPAREN) #
            #node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            #self.eat(AxiomTokenType.RPAREN)  #
            #return node

        elif token.type == AxiomTokenType.LBRACE:
            self.error('временно не доступно')
            # self.eat(AxiomTokenType.LBRACE) #
            # node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            # self.eat(AxiomTokenType.RBRACE)  #
            # return node

        elif token.type == AxiomTokenType.LBRACKET:
            self.error('временно не доступно')
            # self.eat(AxiomTokenType.LBRACKET) #
            # node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            # self.eat(AxiomTokenType.RBRACKET)  #
            # return node

        else:
            self.error(f"Received {token.type}")






# TEST
if __name__ == '__main__':

    # Тест 1: Числа
    lexer = AxiomLexer("42")
    parser = AxiomParser(lexer)
    result = parser.parse_primary()
    print(f"Тест 1 (число 42): {result}")
    print(f"  Тип узла: {type(result).__name__}")
    print(f"  Значение: {result.value}")  # ← Используем .value для Literal

    # Тест 2: Идентификатор
    lexer = AxiomLexer("variable_name")
    parser = AxiomParser(lexer)
    result = parser.parse_primary()
    print(f"\nТест 2 (идентификатор): {result}")
    print(f"  Тип узла: {type(result).__name__}")
    if isinstance(result, Identifier):  # ← Проверяем тип перед доступом к .name
        print(f"  Имя переменной: {result.name}")
    else:
        print(f"  Узел не является идентификатором, это: {type(result).__name__}")


  #TODO:  -