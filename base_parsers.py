class Literal:
    def __init__(self,val):
        self.val = val
        
    def eval(self,env):
        return self.val
    
class IntLit(Literal):        
    def __repr__(self):
        return 'IntLit(%d) ' % self.val
        
class BoolLit(Literal):
    def __repr__(self):
        return 'BoolLit(%d) ' % self.val
        
class CharLit(Literal):
    def __repr__(self):
        return 'CharLit(%c) ' % self.val
        
class StringLit(Literal):
    def __repr__(self):
        return 'StringLit(%s) ' % self.val
        
class FloatLit(Literal):
    def __repr__(self):
        return 'FloatLit(%f) ' % self.val
        

class BinOp():
    def __init__(self,left,op,right):
        self.op = op
        self.left = left
        self.right = right

class InfixNumOp(BinOp):
    def __repr__(self):
        return 'Infixnumop(%s, %s, %s)' % (self.left, self.op, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value
        
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

class StringOp(BinOp):
    def __repr__(self):
        return 'StringOp(%s, %s, %s)' % (self.left, self.op, self.right)
        
    def eval(self,env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if(self.op == '+'):
            value = left_value + right_value
        else:
            raise RuntimeError('Invalid operation on Strings :%s'%self.op)
        return value
        
class RelBinOp(BinOp):
    def __init__(self,l,op,r):
        print("called binop",l,op,r)
        self.left = l
        self.op = op
        self.right = r
        
    def __repr__(self):
        return 'RelBinOp(%s, %s, %s)' % (self.left, self.op, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value
        
class BoolBinOp(BinOp):
    def __repr__(self):
        return 'BoolBinaryOp(%s, %s, %s)' % (self.left,self.op,self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if(self.op =='|'):
            return left_value or right_value
        elif(self.op =='&'):
            return left_value and right_value
        elif(self.op =='^'):
            return left_value ^ right_value
        else:
            raise RuntimeError("Unknown operation : "+self.op)
            
bool_precedence_levels = [
    ['^'],
    ['&'],
    ['|'],
]
        
class Val:
    def __init__(self,name,type,val =None):
        self.name = name
        self.val = val
        self.type = type
        
    def __repr__(self):
        return 'DeclareVal(%s, %s, %s) ' % (self.name,self.type,self.val)
        
    def eval(self,env):
        val = self.val.eval(env)
        if(self.type =='String'):
            try:
                env[self.name] = String(val)
                return String(val)
            except ValueError:
                print("Type Error: Cannot convert value to String ")
        elif(self.type == 'Int'):
            try:
                env[self.name] = int(val)
                return int(val)
            except ValueError:
                print("Type Error: Cannot convert value to Float ")
        elif(self.type =='Float'):
            try:
                env[self.name] = float(val)
                return float(val)
            except ValueError:
                print("Type Error: Cannot convert value to Float ")
        else:
            env[self.name] = val
            return val
        
class ObjectRef:
    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return 'ObjectRef(%s) ' % (self.name)
        
    def eval(self,env):
        try:
            return env[self.name]
        except KeyError:
            print("Error: Object %s not found " %self.name )
        

class CompoundStatement():
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        return ("%s,%s"%(self.first.eval(env),self.second.eval(env)))