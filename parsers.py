import sys
import re
from basic_parser_combinators import *
from base_parsers import *
from lexer_tokens import *

def program():
    #return bool_term() | stringExpr()
    return Phrase(expr() * separator() + Opt(Tag(SEMI)) ^ getres)
    
def getres(parsed):
    (res,_) = parsed
    return res

def separator():
    return Tag(SEMI) ^ (lambda x: lambda l,r: CompoundStatement(l,r))
     
def expr():
    return ifStmt() | Def() | simpleExpr()
    
def simpleExpr():
    return litExp() | Path()
    
def Path():
    return Tag(ID) ^ (lambda x: ObjectRef(x))

####################IF Statement################
def ifStmt():
    def condition():
        return Reserved('(',PAREN) + simpleExpr() + Reserved(')',PAREN) ^ process_group
    def block():
        return Reserved('{',PAREN) + Lazy(expr) + Reserved('}',PAREN) ^ process_group \
                | simpleExpr()
    def expr2():
        def get_block(parsed):
            (_,blk) = parsed
            return blk
        return Reserved('else',RESERVED) + block() ^ get_block
    def par_stmt(parsed):
        (((_,con),blk),e2) = parsed
        return IfStmt(con,blk,e2)
    return Reserved('if',RESERVED) + condition() + block() + Opt(expr2()) ^ par_stmt

#######################EXPRESSIONS##############

def litExp():
    ##add prefix expression
    ##add super postfix
    return boolExpr() | inFixNumExpr() | stringExpr()
    
#####Bool
def boolExpr():
    def bool_Bin_Op(op):
        return (lambda l,r: BoolBinOp(l,op,r))
    return precedence(bool_prefix(),bool_precedence_levels,bool_Bin_Op,BOOLOP)
    
    
def bool_prefix():
    def pre_op(parsed):
        (op,bexp) = parsed
        return PreOp(op,bexp)
    return Reserved('!',PREOPCHAR) + bool_term() ^ pre_op  \
           | bool_term()
    
def bool_term():
    return ((numLit() + Tag(COMPARE) + numLit()) ^ rel_Bin_Op) \
        | inFixNumExpr() + Tag(COMPARE) + inFixNumExpr() ^ rel_Bin_Op \
        | Path() \
        | Tag(BOOL) ^ getbool
        
def getbool(val):
    if val == 'true':
        return BoolLit(True)
    elif val == 'false':
        return BoolLit(False)
    else:
        raise RuntimeError("Invalid Boolean Literal: %s "%val)
def rel_Bin_Op(parsed):
    ((l,op),r) = parsed
    return RelBinOp(l,op,r)
   
#####String
def stringExpr():
    return (string_term() + Reserved('+',OPCHAR) + Lazy(stringExpr)) ^ stringadd \
            | string_term() 

def string_term():
    return (Tag(STRING) ^ getString) \
            | (Reserved('(',PAREN) + stringExpr + Reserved(')',PAREN) ^ process_group)  ##CHECK IS NEED LAZY()
            
def getString(parsed):
    res_str = re.search('\"(.*)\"',parsed);
    if(res_str):
        return StringLit(res_str.group(1))
    else:
        return StringLit(re.search("\'(.*)\'",parsed).group(1))
        
def stringadd(parsed):
    ((l,op),r) = parsed
    return StringOp(l,op,r)
####Numeric
    
def inFixNumExpr():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      infix_num_op, OPCHAR)
                      
def aexp_term():
    return numLit() | aexp_group()
    
def numLit():
    return intLit() | floatLit() | Path()
    
def intLit():
    return Tag(INT) ^ (lambda i: IntLit(int(i)))
    
def floatLit():
    return Tag(FLOAT) ^ (lambda i: FloatLit(float(i)))

def aexp_group():
    return Reserved('(',PAREN) + Lazy(litExp) + Reserved(')',PAREN) ^ process_group


def precedence(value_parser, precedence_levels, combine,key):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level,key) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser
    
def any_operator_in_list(ops,key):
    op_parsers = [Reserved(op,key) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser
    
def process_group(parsed):
    ((_, p), _) = parsed
    return p
    
def infix_num_op(op):
    return (lambda l,r : InfixNumOp(l,op,r))
    
#############################Pattern_Definition#############

def Def():
    return Reserved('val',RESERVED) + valDef() + Reserved('=',OPCHAR) + simpleExpr()  ^ decValCombine
    
def valDef():
    return Tag(ID) + Opt(Reserved(':',COLON) + Tag(DATATYPE))
    
def decValCombine(parsed):
    (((_, ((nm,tp))), _),vl) = parsed
    if(tp!=None):
        (_,tp) = tp
    return Val(nm,tp,vl)
    