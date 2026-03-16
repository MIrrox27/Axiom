# author https://github.com/MIrrox27/Axiom
# AxiomParser.py


from axiom.AxiomASTNodes import *
from axiom.AxiomLexer import AxiomLexer
from  axiom.AxiomTokens import AxiomTokenType
import sys


class AxiomParser:

    def __init__(self, lexer, debug=False):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.debug = debug
        self.loop_for = False
        self.ERROR = Error("AxiomParser")

        self.builtin_functions = {
            AxiomTokenType.PRINT: "print",
            AxiomTokenType.INPUT: "input"
        }


    def log(self, message):
        if self.debug:
            print(f'[Parser DEBUG]: {message}, line: {self.lexer.line}, position: {self.lexer.position}, current char: "{self.lexer.current_char}"')


    def error(self, message, func):
        self.loop_for = False
        self.ERROR.error(message=f'{message}, line: {self.lexer.line}, position: {self.lexer.position}, current char: "{self.lexer.current_char}"', func=func)

    def eat(self, token_type): # Проверяет, что текущий токен имеет ожидаемый тип
        if self.current_token.type == token_type:
            self.log(f'[eat] received: [{token_type}]')
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Pending {token_type}, received {self.current_token.type}", 'eat') # self.current_token.type - тип токена который мы получили,
            # token_type - токен, который нам нужен


    def parse_primary(self):  # Парсит первичные выражения. Возвращает узел AST
        token = self.current_token


        # типы данных
        if token.type in (AxiomTokenType.INTEGER, AxiomTokenType.FLOAT): #
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxiomTokenType.STRING:
            self.eat(token.type)
            return Literal(token.value)

        elif token.type == AxiomTokenType.NILL:
            self.eat(token.type)
            return Literal(None)

        elif token.type == AxiomTokenType.BOOL:
            self.eat(token.type)
            return  Literal(token.value)

        elif token.type == AxiomTokenType.IDENTIFIER:
            self.eat(token.type)
            node = Identifier(token.value)

            if self.current_token.type == AxiomTokenType.LPAREN:
                return self.parse_call(node)

            return node


        elif token.type in self.builtin_functions: # встроенные функции
            self.eat(token.type)
            node = Identifier(self.builtin_functions[token.type])

            if self.current_token.type == AxiomTokenType.LPAREN:
                return self.parse_call(node)
            else:
                self.error(f"Expected '(' after {token.type.name}", 'parse_primary')


        # символы (скобки)
        elif token.type == AxiomTokenType.LPAREN:
            self.eat(AxiomTokenType.LPAREN) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RPAREN) #
            return node

        elif token.type == AxiomTokenType.LBRACE:
            self.eat(AxiomTokenType.LBRACE) #
            node = self.parse_expression()  # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RBRACE) #
            return node

        elif token.type == AxiomTokenType.LBRACKET:
            self.eat(AxiomTokenType.LBRACKET)  #
            node = self.parse_expression()     # Рекурсивно парсим выражение внутри
            self.eat(AxiomTokenType.RBRACKET)  #
            return node

        else:
            self.error(f"Received {token.type}", func='parse_primary')


    def parse_unary(self): # обработка унарных операторов, пока только not, потом добавлю ++ и --
        token = self.current_token

        if token.type == AxiomTokenType.NOT:
            self.eat(AxiomTokenType.NOT)
            expr = self.parse_unary()
            return UnaryOp(operator=token.type, expr=expr)
        else:
            return self.parse_primary()



    def parse_power(self): # парсит выражения с высшим приоритетом (допустим возведение в степень)
        node = self.parse_unary()

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
            AxiomTokenType.GREATER_EQUAL, # >=
            AxiomTokenType.LESS_EQUAL, # <=

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

    def parse_logical_and(self): # обработка логического and
        node = self.parse_comparison()
        while self.current_token.type == AxiomTokenType.AND:
            op = self.current_token.type
            self.eat(op)
            right = self.parse_comparison()

            node = BinaryOp(left=node, operator=op, right=right)
        return node


    def parse_logical_or(self): # обработка логического or
        node = self.parse_logical_and()
        while self.current_token.type == AxiomTokenType.OR:
            op = self.current_token.type
            self.eat(op)
            right = self.parse_logical_and()

            node = BinaryOp(left=node, operator=op, right=right)
        return node



    def parse_assignment(self): # парсинг присвоения
        func = 'parse_assignment'
        node = self.parse_logical_or()

        if self.current_token.type == AxiomTokenType.ASSIGN:
            if not isinstance(node, Identifier): # Потом добавим обработку присваивания массивам, спискам словарям и тп.
                self.error("Left side of assignment must be a variable", func)

            operator_token = self.current_token
            self.eat(AxiomTokenType.ASSIGN)

            right = self.parse_assignment()
            node = BinaryOp(left=node, operator=operator_token.type, right=right)
        return node


    def parse_expression(self): # главный модуль, сделан для начала парсинга
        return self.parse_assignment()



    def parse_block(self):
        func = 'parse_block'
        self.eat(AxiomTokenType.LBRACE)

        statements = []

        while self.current_token.type != AxiomTokenType.RBRACE:
            if self.current_token == AxiomTokenType.EOF:
                self.error("Block not closed, pending '}'", func)

            stmt = self.parse_statement()
            statements.append(stmt)

        self.eat(AxiomTokenType.RBRACE)
        return Block(statements=statements)


    def parse_var_declaration(self, loop:bool = False): # парсит объявление переменной
        func = 'parse_var_declaration'
        keyword_token = self.current_token
        self.eat(keyword_token.type)

        if self.current_token.type != AxiomTokenType.IDENTIFIER:    # получаем имя переменной
            self.error(f'After {keyword_token.type} pending main value', func=func)

        name = self.current_token.value
        self.eat(AxiomTokenType.IDENTIFIER)

        value = None
        if self.current_token.type == AxiomTokenType.ASSIGN: # проверяем наличие присваивания значения, если есть то парсим его
            self.eat(AxiomTokenType.ASSIGN)
            value = self.parse_expression()

        if keyword_token.type == AxiomTokenType.VAL and value is None:
            self.error(f"Const '{name}' must have a main value", func=func)

        if self.current_token.type == AxiomTokenType.SEMICOLON and not loop:
            self.eat(AxiomTokenType.SEMICOLON)

        return  VarDeclaration(keyword_token.type, name=name, value=value)


    def parse_if_statement(self): # парсинг if/elif/else
        self.eat(AxiomTokenType.IF) # съедаем if

        if self.current_token.type == AxiomTokenType.LPAREN: # если есть скобки парсим выражение внутри них
            self.eat(AxiomTokenType.LPAREN)
            condition = self.parse_expression()
            self.eat(AxiomTokenType.RPAREN)
        else:
            condition = self.parse_expression()

        than_branch = self.parse_block()

        elif_branches = []
        while self.current_token.type == AxiomTokenType.ELIF:
            self.eat(AxiomTokenType.ELIF)

            if self.current_token.type == AxiomTokenType.LPAREN:
                self.eat(AxiomTokenType.LPAREN)
                elif_condition = self.parse_expression()
                self.eat(AxiomTokenType.RPAREN)
            else:
                elif_condition = self.parse_expression()

            elif_block = self.parse_block()
            elif_branches.append(ElifClause(elif_condition, elif_block))

        else_branch = None
        if self.current_token.type == AxiomTokenType.ELSE:
            self.eat(AxiomTokenType.ELSE)
            else_branch = self.parse_block()

        return IFStmt(
            condition=condition,
            than_branch=than_branch,
            elif_branches=elif_branches,
            else_branch=else_branch
        )


    def parse_while_statement(self):
        func = 'parse_while_statement'
        self.eat(AxiomTokenType.WHILE)

        if self.current_token.type == AxiomTokenType.LPAREN:
            self.eat(AxiomTokenType.LPAREN)
            condition = self.parse_expression()
            self.eat(AxiomTokenType.RPAREN)
        else:
            self.error(f'where is "(" ?', func)

        body = self.parse_block()
        return WhileStmt(condition=condition, body=body)


    def parse_do_statement(self):
        func = 'parse_do_statement'
        self.eat(AxiomTokenType.DO)

        if self.current_token.type == AxiomTokenType.LPAREN:
            self.eat(AxiomTokenType.LPAREN)
            condition = self.parse_expression()
            self.eat(AxiomTokenType.RPAREN)
        else:
            self.error(f'where is "(" ?', func)

        body = self.parse_block()
        return DoStmt(condition=condition, body=body)


    def parse_for_statement(self):
        func = 'parse_for_statement'
        self.eat(AxiomTokenType.FOR)
        if self.current_token.type == AxiomTokenType.LPAREN:
            self.loop_for = True

            self.eat(AxiomTokenType.LPAREN) # тк у нас все условия цикла находятся в скобках

            # До первого ";"
            if self.current_token.type == AxiomTokenType.SEMICOLON:
                initializer = None
            elif self.current_token.type == AxiomTokenType.VAR:
                initializer = self.parse_var_declaration(loop=True)
            elif self.current_token.type == AxiomTokenType.VAL:
                return self.error("you can't use constants in loop", func)
            else:
                initializer = self.parse_expression()
            self.eat(AxiomTokenType.SEMICOLON)

                # После первого ";", до второго ";"
            if self.current_token.type == AxiomTokenType.SEMICOLON:
                condition = None
            else:
                condition = self.parse_expression()
            self.eat(AxiomTokenType.SEMICOLON)


                #
            if self.current_token.type == AxiomTokenType.RPAREN:
                increment = None
            else:
                increment = self.parse_expression()
            self.eat(AxiomTokenType.RPAREN)


            body  = self.parse_block()
            self.loop_for = False
            return ForStmt(initializer=initializer, condition=condition, increment=increment, body=body)

        else:
            return self.error("Where is '(' after 'for'?", func)


    def parse_foreach_statement(self):
        func = 'parse_foreach_statement'
        self.eat(AxiomTokenType.FOREACH)

        if self.current_token.type == AxiomTokenType.VAR:
            self.eat(AxiomTokenType.VAR)

        elif self.current_token.type == AxiomTokenType.VAL:
            self.error("you can't use 'val' in this loop", func)


        if self.current_token.type != AxiomTokenType.IDENTIFIER:
            self.error("After the loop a variable is expected", func)

        var_name = self.current_token.value
        self.eat(AxiomTokenType.IDENTIFIER)

        if self.current_token.type != AxiomTokenType.IN:
            self.error("After the variable expected 'in'", func)
        self.eat(AxiomTokenType.IN)

        iterable = self.parse_expression()

        body = self.parse_block()

        return ForeachStmt(Identifier(var_name), iterable=iterable, body=body)



    def parse_statement(self):
        token = self.current_token

        if token.type == AxiomTokenType.SEMICOLON:
            self.eat(AxiomTokenType.SEMICOLON)
            return EmtpyStmt

        elif token.type == AxiomTokenType.EOF:
            return EmtpyStmt

        elif token.type == AxiomTokenType.LBRACE:
            return self.parse_block() # функция, которая будет парсить блоки кода, у нас они находятся в {}

        elif token.type in (AxiomTokenType.VAL, AxiomTokenType.VAR):
            return self.parse_var_declaration()

        elif token.type == AxiomTokenType.IF:
            return self.parse_if_statement()

        elif token.type == AxiomTokenType.WHILE:
            return self.parse_while_statement()

        elif token.type == AxiomTokenType.FOR:
            return self.parse_for_statement()

        elif token.type == AxiomTokenType.FOREACH:
            return self.parse_foreach_statement()

        elif token.type == AxiomTokenType.DO:
            return self.parse_do_statement()

        # тут будут другие проверки действий
        else:
            expr = self.parse_expression()

            if self.current_token.type == AxiomTokenType.SEMICOLON:
                self.eat(AxiomTokenType.SEMICOLON)
            return ExpressionStmt(expr)



    def parse_call(self, callee): # парсинг вызова функций
        self.eat(AxiomTokenType.LPAREN)

        arguments = []

        if self.current_token.type != AxiomTokenType.RPAREN:
            while True:
                arg = self.parse_expression() # парсим выражение (аргумент)
                arguments.append(arg)

                if self.current_token.type == AxiomTokenType.COMMA: # если запятая (после аргумента), то продолжаем
                    self.eat(AxiomTokenType.COMMA)
                    continue

                elif self.current_token.type == AxiomTokenType.RPAREN:
                    break

                else:
                    self.error(message="Expected ',' or ')' after argument", func='parse_call')

        self.eat(AxiomTokenType.RPAREN)

        return CallExpr(callee, arguments)




# TEST
if __name__ == '__main__':

    tests = [

        'do (x < 1){var x = 1}',
        'while (x < 1 and x == 2){var x = 1}',
        ' val a = 1',
        ' 1 > 1'

    ]

    print("Тестирование")
    print("=" * 50)

    for code in tests:
        lexer = AxiomLexer(code)
        parser = AxiomParser(lexer)


        result = parser.parse_statement()

        if parser.current_token.type != AxiomTokenType.EOF:
            print(f"Внимание: не весь код разобран для '{code}'")

        print(f"{code:15s} → {result}")
    print("=" * 50)

