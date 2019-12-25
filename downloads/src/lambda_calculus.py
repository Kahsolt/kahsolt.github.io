#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/10/12 
#
# 参考:
#  [神奇的λ演算](https://www.jianshu.com/p/e7db2f50b012/)
#  [《计算的本质》/ Tom Stuart. Understanding Computation: From Simple Machine to Impossible Programs](https://www.jb51.net/books/409637.html)
#

## Lambda Expression
class L:
  
  def __init__(self, expr:str):
    self.expr = expr
    self.expr_h = expr.replace(':', '').replace('lambda ', 'λ.')
    self.proc = eval(expr)
  
  def __str__(self):
    return self.expr
  
  def __repr__(self):
    return self.expr_h
  
  def __call__(self, x):  # .apply()
    return L('((%s)(%s))' % (self, x))
  
  def to_string(self):
    return eval('lambda s: s()')(self.proc)
  
  def to_bool(self):
    return eval('lambda b: b(True)(False)')(self.proc)
  
  def to_number(self):
    return eval('lambda n: n(lambda x: x + 1)(0)')(self.proc)
  
  def to_tuple(self, vtype='N'):
    VTYPES = {
      'N': 'to_number',
      'B': 'to_bool',
      'S': 'to_string',
    }
    return [getattr(op(self), VTYPES.get(vtype))() for op in [FIRST, SECOND]]


## Literal Type
S = lambda s: L('lambda : %r' % str(s))


## Logical Type - true / false
B = lambda b: L('lambda x: lambda y: %s' % (b and 'x' or 'y')) 
TRUE, FALSE = B(True), B(False)

IF = L('lambda b: lambda x: lambda y: b(x)(y)')
NOT = L('lambda b: b(%s)(%s)' % (FALSE, TRUE))
NOT2 = L('lambda b: lambda x: lambda y: b(y)(x)') # UNLESS == NOT IF
AND = L('lambda x: lambda y: x(y)(%s)' % FALSE)
OR = L('lambda x: lambda y: x(%s)(y)' % TRUE)
XOR = L('lambda x: lambda y: (%s)((%s)((%s)(x))(y))((%s)(x)((%s)(y)))' % (OR, AND, NOT, AND, NOT))
IMPL = L('lambda x: lambda y: (%s)((%s)(x))(y)' % (OR, NOT))


## Number Type - natural numbers
N = lambda n: L('lambda f: lambda x: ' + 'f(' * n + 'x' + ')' * n)
ZERO, ONE, TWO, THREE = N(0), N(1), N(2), N(3)

SUCC = L('lambda n: lambda f: lambda x: f(n(f)(x))')
SUCC2 = L('lambda n: lambda f: lambda x: n(f)(f(x))')
IS_ZERO = L('lambda n: n(lambda x: %s)(%s)' % (FALSE, TRUE))
ADD = L('lambda n: lambda m: lambda f: lambda x: n(f)(m(f)(x))')
MULT = L('lambda n: lambda m: lambda f: lambda x: n(m(f))(x)')
POWER = L('lambda n: lambda m: lambda f: m(n)(f)')


## List Types - tuple/triple/../n-tuple
P = lambda x, y: L('lambda f: f(%s)(%s)' % (x, y))
FIRST = L('lambda p: p(%s)' % TRUE)
SECOND = L('lambda p: p(%s)' % FALSE)
TP = lambda *args: L('lambda f: f' + ('(%s)' * len(args)) % args)
NTH = lambda i, n: L('lambda p: p' 
                     + ''.join(['(lambda x%d: ' % (i + 1) for i in range(n)])
                     + 'x%d' % i + ')' * n)
# helper func: make [N, M] => [N + 1, N]
PHI = L('lambda p: %s' % P('(%s)((%s)(p))' % (SUCC, FIRST), '((%s)(p))' % (FIRST)))
PRED = L('lambda n: (%s)(n(%s)(%s))' % (SECOND, PHI, P(ZERO, ZERO)))
SUB = L('lambda x: lambda y: y(%s)(x)' % PRED)

LEQ = L('lambda x: lambda y: (%s)((%s)(x)(y))' % (IS_ZERO, SUB))
GT = L('lambda x: lambda y: (%s)((%s)(x)(y))' % (NOT, LEQ))
GEQ = L('lambda x: lambda y: (%s)((%s)(y)(x))' % (IS_ZERO, SUB))
LT = L('lambda x: lambda y: (%s)((%s)(x)(y))' % (NOT, GEQ))
EQ = L('lambda x: lambda y: (%s)((%s)(x)(y))((%s)(x)(y))' % (AND, GEQ, LEQ))

MOD = L('lambda x: lambda y: (%s)(x(lambda p: (%s)((%s)((%s)(p))((%s)(p)))(%s)(p))(%s))' % (
        FIRST, IF, GEQ, FIRST, SECOND, 
        P('(%s)((%s)(p))((%s)(p))' % (SUB, FIRST, SECOND), 'y'),
        P('x', 'y')))


## Recursive Functions - find the fixpoint F for f, then f = <FPC> F
# Turing’s fixpoint combinator
FPC_TA = L('lambda x: lambda y: y(x(x)(y))')
FPC_T = L('(%s)(%s)' % (FPC_TA, FPC_TA))
# Church’s fixpoint combinator
FPC_YA = L('lambda x: f(x(x))')
FPC_Y = L('lambda f: (%s)(%s)' % (FPC_YA, FPC_YA))

# however, Python's eager evaluation tatic raises RecursionError
# thus recursivity seems not implementable?
# F = L('lambda f: lambda n: (%s)((%s)(n))(%s)((%s)(n)(f((%s)(n))))' % (IF, IS_ZERO, ONE, MULT, PRED))
# FACT = L('(%s)(%s)' % (FPC_T, F))


## simple test programs
def foobar(x, echo=False):
  X = N(x)
  SIX, TWO, THREE = N(6), N(2), N(3)
  prog = IF(IS_ZERO(MOD(X)(SIX)))(S('foobar'))(
            IF(IS_ZERO(MOD(X)(TWO)))(S('foo'))(
               IF(IS_ZERO(MOD(X)(THREE)))(S('bar'))(
                  S(x))))
  if echo: print(repr(prog))
  return prog.to_string()


def timer(fn):
  def wrapper(*args, **kwargs):
    import time
    s = time.time()
    ret = fn(*args, **kwargs)
    t = time.time()
    print('[Timer] %r done in %.4f seconds' % (fn.__name__, t - s))
    return ret
  return wrapper

@timer
def unittest():
  # logical
  print(r'\\ testing logical')
  assert NOT(TRUE).to_bool() == FALSE.to_bool()
  assert NOT2(FALSE).to_bool() == TRUE.to_bool()
  assert AND(TRUE)(TRUE).to_bool() == TRUE.to_bool()
  assert AND(FALSE)(TRUE).to_bool() == FALSE.to_bool()
  assert OR(TRUE)(TRUE).to_bool() == TRUE.to_bool()
  assert OR(FALSE)(FALSE).to_bool() == FALSE.to_bool()
  assert XOR(TRUE)(FALSE).to_bool() == TRUE.to_bool()
  assert XOR(FALSE)(FALSE).to_bool() == FALSE.to_bool()
  assert IMPL(TRUE)(FALSE).to_bool() == FALSE.to_bool()
  assert IMPL(FALSE)(TRUE).to_bool() == TRUE.to_bool()
  print('// passed')
  
  # numerical
  print(r'\\ testing numerical')
  assert SUCC(ZERO).to_number() == ONE.to_number()
  assert SUCC(N(10)).to_number() == N(11).to_number()
  assert SUCC(THREE).to_number() == SUCC2(THREE).to_number()
  assert PRED(ONE).to_number() == ZERO.to_number()
  assert PRED(ZERO).to_number() == ZERO.to_number()
  assert IS_ZERO(ZERO).to_bool() == TRUE.to_bool()
  assert IS_ZERO(TWO).to_bool() == FALSE.to_bool()
  
  assert LEQ(TWO)(THREE).to_bool() == TRUE.to_bool()
  assert GT(TWO)(THREE).to_bool() == FALSE.to_bool()
  assert GEQ(TWO)(TWO).to_bool() == TRUE.to_bool()
  assert LT(TWO)(TWO).to_bool() == FALSE.to_bool()
  assert EQ(TWO)(THREE).to_bool() == FALSE.to_bool()
  assert EQ(TWO)(TWO).to_bool() == TRUE.to_bool()
  
  assert ADD(N(2))(N(3)).to_number() == N(5).to_number()
  assert SUB(N(10))(N(7)).to_number() == N(3).to_number()
  assert MULT(N(3))(N(7)).to_number() == N(21).to_number()
  assert POWER(N(2))(N(3)).to_number() == N(8).to_number()
  print('// passed')
  
  # tuple
  print(r'\\ test tuple')
  assert FIRST(P(ONE, TWO)).to_number() == ONE.to_number()
  assert SECOND(P(ONE, TWO)).to_number() == TWO.to_number()
  
  assert NTH(1, 3)(TP(ZERO, ONE, TWO)).to_number() == ZERO.to_number()
  assert NTH(2, 3)(TP(ZERO, ONE, TWO)).to_number() == ONE.to_number()
  assert NTH(3, 3)(TP(ZERO, ONE, TWO)).to_number() == TWO.to_number()
  
  assert PHI(P(N(5), N(2))).to_tuple() == P(N(6), N(5)).to_tuple()
  print('// passed')

  # simple programs
  print(r'\\ test foobar')
  assert foobar(3) == 'bar'
  assert foobar(4) == 'foo'
  assert foobar(6) == 'foobar'
  assert foobar(7) == '7'
  print('// passed')


if __name__ == '__main__':
  unittest()
