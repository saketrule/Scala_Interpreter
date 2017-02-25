## Driver program
## Written by Saket

import sys

from lexer import *
from parser import *

def usage():
    sys.stderr.write('Provide scala filename as argument\n')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    tokens = scala_lex(text)
    print("Tokens found: \n")
    for x in tokens:
        print(x)