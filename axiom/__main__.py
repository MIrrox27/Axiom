# author https://github.com/MIrrox27/Axiom
# __main__.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiom.AxiomTokens import *
from axiom.AxiomLexer import *
from axiom.AxiomParser import *
    # from axiom.AxiomASTNodes import *
from axiom.AxiomInterpreter import *

from axiom.repl import repl



def run_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()

    except FileExistsError:
        print(f'Error: File "{filename}" not found')
        sys.exit(1)

    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


    lexer = AxiomLexer(code)
    parser = AxiomParser(lexer)
    interpreter = AxiomInterpreter()

    try:
        while parser.current_token.type != AxiomTokenType.EOF:
            #print(f"DEBUG: Current token before parse: {parser.current_token}")
            stmt = parser.parse_statement()
            interpreter.visit(stmt)

        if parser.current_token.type != AxiomTokenType.EOF:
            raise Exception("Parsing did not consume all tokens")

    except Exception as e:

        print(f'Runtime error: {e}')
        sys.exit(1)




def main():

    if len(sys.argv) > 1:
        run_file(sys.argv[1])

    else:
        repl()


if __name__ == "__main__":
    main()


















