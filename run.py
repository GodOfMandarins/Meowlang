from pathlib import Path
import sys
from lark import Lark
from interpreter import MeowLangInterpreter

def main():
    filename = Path("program.meow")
    grammar = Path("syntax.lark").read_text()

    code = filename.read_text()
    #LALR - Look-Ahead LR parsing algoritmas. Skaito kaire -> desine
    #geras mazom kalbom
    parser = Lark(grammar, parser="lalr")
    #lark gerai, nes mazose kalbose paduoda node vaika vietoj 
    # papildomo reference jei jis vienas
    #pvz statement(give(x=10)) duoda give(x=10)
    tree = parser.parse(code)

    interpreter = MeowLangInterpreter()
    interpreter.transform(tree)


if __name__ == "__main__":
    main()