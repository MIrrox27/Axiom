# author https://github.com/MIrrox27/Axiom
# AxiomParser.py

from AxiomASTNodes import *
from AxiomLexer import AxiomLexer
from  AxiomTokens import AxiomTokenType


class AxiomParser:

    def __init__(self, lexer, debug=False):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.debug = debug

    def log(self, message):
        if self.debug:
            print(f'[Parser DEBUG]: {message}, line: {lexer.line}, position: {lexer.position}, current char: {lexer.current_char}')


    def error(self, message):
        raise Exception(f'[Parser Error]: {message}')

    def eat(self, token_type): # Проверяет, что текущий токен имеет ожидаемый тип
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Pending {token_type}, received {self.current_token.type}") # self.current_token.type - тип токена который мы получили,
            # token_type - токен, который нам нужен



    def parse_power(self): # парсит выражения с высшим приорететом (допустим возведение в степень)

        node = self.parse_primary()

        while self.current_token.type == AxiomTokenType.POWER:
            operator_token = self.current_token
            self.eat(AxiomTokenType.POWER)
            right = self.parse_power()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node

    def parse_mul_div_mod(self):
        node = self.parse_power()
         #
        while self.current_token.type in (AxiomTokenType.MULTIPLY, AxiomTokenType.DIVIDE, AxiomTokenType.MOD):
            operator_token = self.current_token
            self.eat(operator_token.type)

            right = self.parse_power()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )
        return node



    def parse_primary(self):  # Парсит первичные выражения. Возвращает узел AST
        token = self.current_token

        if token.type in (AxiomTokenType.NUMBER, AxiomTokenType.FLOAT): #
            self.log(f'received: [{token.type}]')
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxiomTokenType.STRING:
            self.log(f'received: [{token.type}]')
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxiomTokenType.BOOL:
            self.log(f'received: [{token.type}]', )
            self.eat(token.type)
            return  Literal(token.value)

        elif token.type == AxiomTokenType.IDENTIFIER:
            self.log(f'received: [{token.type}]')
            self.eat(token.type)
            return Identifier(token.value)


        elif token.type == AxiomTokenType.LPAREN:
            self.log(f'received: [{token.type}]')
            self.eat(AxiomTokenType.LPAREN) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RPAREN) #
            return node

        elif token.type == AxiomTokenType.LBRACE:
            self.log(f'received: [{token.type}]')
            self.eat(AxiomTokenType.LBRACE) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RBRACE) #
            return node

        elif token.type == AxiomTokenType.LBRACKET:
            self.log(f'received: [{token.type}]')
            self.eat(AxiomTokenType.LBRACKET)  #
            node = self.parse_expression()     # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RBRACKET)  #
            return node

        else:
            self.error(f"Received {token.type}")

    def parse_add_sub(self): # парсит сложение и вычитание
        self.log(f"Start parse_add_sub(), token: {self.current_token}")

        node = self.parse_mul_div_mod()
        self.log(f"Parse 1st parse_term(), node: {node}, token: {self.current_token}")

        while self.current_token.type in (AxiomTokenType.PLUS, AxiomTokenType.MINUS):
            operator_token = self.current_token
            self.log(f"Operator {operator_token.type}, parse further")

            self.eat(operator_token.type)
            right = self.parse_mul_div_mod()

            self.log(f"Create BinaryOp: {node} {operator_token.type} {right}")
            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right
            )

        self.log(f"End parse_expression(), return: {node}")
        return node

    def parse_comparison(self): # парсинг выражений равенства
        node = self.parse_add_sub()

        comparison_operators = (
            #AxiomTokenType.GREATER_EQUAL, # >=
            #AxiomTokenType.LESS_EQUAL, # <=

            AxiomTokenType.EQUALS, # ==
            AxiomTokenType.NOT_EQUALS, # !=
            AxiomTokenType.LESS, # <
            AxiomTokenType.GREATER # >
        )
        while self.current_token.type in comparison_operators:
            operator_token = self.current_token
            self.eat(operator_token.type)

            right = self.parse_add_sub()

            node = BinaryOp(
                left=node,
                operator=operator_token.type,
                right=right

            )
        return node


    def parse_expression(self): # главный модуль, сделан для начала распределения парсинга
        return self.parse_comparison()



# TEST
if __name__ == '__main__':

    tests = [
        'if __name__ == 1: ',
        'negr == 1 + 1',
        ' 1 < 1',
        ' 1 != 1',
        ' 1 > 1'
        #'(1 + 1) = (1 ** 1 != 1 + 1) != cos (123 + 1 ** 2 >= 1+ 1) + 2 + 1 + (1*1) <= 1 +1 ** [nig ** 2 ** 2] + {333+1==1}'
    ]

    print("Тестирование")
    print("=" * 50)

    for code in tests:
        lexer = AxiomLexer(code)
        parser = AxiomParser(lexer)


        result = parser.parse_expression()

        if parser.current_token.type != AxiomTokenType.EOF:
            print(f"Внимание: не весь код разобран для '{code}'")

        print(f"{code:15s} → {result}")
    print("=" * 50)

  #TODO: -