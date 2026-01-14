# author https://github.com/MIrrox27/Axiom
# AxiomParser.py

from AxiomASTNodes import *
from AxiomLexer import AxiomLexer
from  AxiomTokens import AxiomTokenType


class Parser:

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

# TESTd
if __name__ == '__main__':

    lexer = AxiomLexer("x + 5")
    parser = Parser(lexer)

    print(f"Текущий токен: {parser.current_token}")
    # Должно быть: Token(IDENTIFIER, 'x', line: 1)

    # Проверяем идентификатор
    parser.eat(AxiomTokenType.IDENTIFIER)
    print(f"{parser.current_token}")
    # Должно быть: Token(PLUS, line: 1)

    parser.eat(AxiomTokenType.PLUS)
    print(parser.current_token)
    # должно быть Token(AxiomTokenType.NUMBER, 5, line: 1)



# TODO:  -