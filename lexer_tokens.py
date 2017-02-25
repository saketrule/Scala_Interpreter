RESERVED = 'RESERVED'
LITERAL = 'LITERAL'
INT      = 'INT'
ID       = 'ID'
FLOAT    = 'FLOAT'
STRING   = 'STRING'
DATATYPE = 'DATATYPE'
SEMI     = 'SEMI'
PAREN    = 'PAREN'
COMPARE  = 'COMPARE'
COMMENT  = 'COMMENT'
OPCHAR   = 'OPCHAR'
QUALID   = 'QUALID'

tokens = [
    (r'and',                    RESERVED),
    (r'or',                     RESERVED),
    (r'not',                    RESERVED),
    (r'if',                     RESERVED),
    (r'else',                   RESERVED),
    (r'while ',                 RESERVED),
    (r'do',                     RESERVED),    
    (r'val',                    RESERVED),
    (r'var',                    RESERVED),
    
    (r'String',                 DATATYPE),           ## May remove once implement classes
    (r'Int',                    DATATYPE),
    (r'Float',                  DATATYPE),
    (r'Unit',                   DATATYPE),
    (r'Double',                 DATATYPE),
    
    (r'[\(\){}\[\]]',           PAREN),
    (r'\/\/[^\n]*\n*',          COMMENT),
    (r'/\*[^(\*/)]*?\*/',       COMMENT),           ##Can't figure out how to match /,.. ## no nested comments :<
    
    (r'object ',                RESERVED),
    (r'def ',                   RESERVED),
    (r'main',                   RESERVED),
    (r'import',                 RESERVED),          
    (r'\'.\'',                  LITERAL),           ## Check what . matches
    (r'\".*?\"',                LITERAL),
    (r'-?[0-9]+',               LITERAL),
    (r'[0-9]*\.[0-9]+',         LITERAL),
    (r'(true|false)',           LITERAL),
    (r'[A-Za-z][A-Za-z0-9_]*',  ID),
    (r'<-',                     OPCHAR),
    (r'=>',                     OPCHAR),            ##Not sure belongs to opchar, for anonymous functions
    (r'<=|<|==|>|>=|!=',        COMPARE),
    (r'[\+\-\*/^\?]',           OPCHAR),
    (r'=',                      RESERVED),
    (r'.',                      QUALID),            ## hAVEN'T added ,
    (r';',                      SEMI    ),
    (r'\n+',                    SEMI    ),
    (r'[ \n\t]+',               None   ),
]