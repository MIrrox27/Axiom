# author https://github.com/MIrrox27/Axiom
# repl.py

from axiom.AxiomTokens import *
from axiom.AxiomLexer import *
from axiom.AxiomParser import *
from axiom.AxiomASTNodes import *
from axiom.AxiomInterpreter import *
from axiom import __version__


def repl():
    interpreter = AxiomInterpreter
    print("Axiom REPL (type 'exit' to quit)")
    print(f"Version {__version__}")

    __all__ = [
        'AxiomLexer',
        'AxiomParser',
        'AxiomInterpreter',
        'AxiomTokenType',
        '__version__',
    ]