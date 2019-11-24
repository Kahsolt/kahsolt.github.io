#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/11/17 

# Deutsch算法
#
# |0>-----|H|-|    |-|H|-|M|--
#             | Uf |
# |0>-|X|-|H|-|    |----------   // 辅助比特
#
# (*Uf包装了输入函数)
#

from projectq import MainEngine
from projectq.ops import *

def deutsch(fn):
  engine = MainEngine()
  qs = engine.allocate_qureg(2)
  
  def wrapper():
    # pre op
    X | qs[1]
    All(H) | qs
  
    # the quantum black box `Uf`/`Ox`
    # conventional definition: `Uf|xy>=|x,y^f(y)>`
    fn(qs)
    
    # post op
    H | qs[0]
    All(Measure) | qs
    
    engine.flush()
    print('r = %d' % bool(qs[0]))
  return wrapper

@deutsch
def ZERO(qs):
  # 即输入为函数`f(x) = 0`
  # 要使得 Uf|xy> = |x,y^0> = |x,y> = |xy>
  # 因有 I|xy> = |xy>
  # 所以取Uf为I⊗I
  pass
  
@deutsch
def ONE(qs):
  # 即输入为函数`f(x) = 1`
  # 要使得 Uf|xy> = |x,y^1> = |x,~y>
  # 因有 X|y> = |~y>
  # 所以取Uf为I⊗X
  X | qs[1]

@deutsch
def ID(qs):
  # 即输入为函数`f(x) = x`
  # 要使得 Uf|xy> = |x,y^f(x)> = |x,y^x>
  # 因有 CNOT|xy> = |x,x^y>
  # 所以取Uf为CNOT
  CNOT | (qs[0], qs[1])
  
@deutsch
def NOT(qs):
  # 即输入为函数`f(x) = ~x`
  # 要使得 Uf|xy> = |x,y^f(x)> = |x,y^(~x)> = |x,~y^x>
  # 因有 CNOT|xy> = |x,x^y>
  # 所以取Uf为CNOT(I⊗X)
  CNOT | (qs[0], qs[1])
  X | qs[1]


if __name__ == '__main__':
  print("ZERO and ONE are constant:")
  ZERO()
  ONE()
  print("ID and NOT are balanced:")
  ID()
  NOT()
