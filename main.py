## Driver program
## Written by Saket

import sys

from lexer import *
from parsers import *

def usage():
    sys.stderr.write('Provide scala filename as argument\n')
    sys.exit(1)
    
def evaluate(result,env):
    print(result.eval(env))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    tokens = scala_lex(text)
    print("Tokens found: \n")
    for x in tokens:
        print(x)
    ast = program()(tokens,0)
    print("\nStatements parsed in ast: \n")
    print(ast.value)
    print("\n\nEvaluated values are: \n")
    evaluate(ast.value,{})