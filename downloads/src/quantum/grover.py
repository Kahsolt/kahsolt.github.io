#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/11/13 

# Grover算法(N=4, M=1的例子)
#
# |0>-----|H|-|    |-|H|-|X|-----|CNOT|-----|X|-|H|-------
# |0>-----|H|-| Uf |-|H|-|X|-|H|-|CNOT|-|H|-|X|-|H|-------
# |0>-|X|-|H|-|    |---------------------------------|H|--
#
# <  初始化 > <标记> <          相位调整          > <收尾>
#             |        这两个部分重复多次↑        |

from projectq import MainEngine
from projectq.ops import *

def grover(fn):
  engine = MainEngine()
  qs = engine.allocate_qureg(3)
  
  def wrapper():
    # 初始化、打散
    X | qs[2]
    All(H) | qs

    # 黑箱变换Uf：|x> -> (-1)^f(x)|x>
    fn(qs)
    
    # 相位调整：|0> -> |0>, |x> -> -|x>（对|0^n>均匀打散的|U>进行反射）
    All(H) | [qs[0], qs[1]]
    All(X) | [qs[0], qs[1]]
    H | qs[1]
    CNOT   | (qs[0], qs[1])
    H | qs[1]
    All(X) | [qs[0], qs[1]]
    All(H) | [qs[0], qs[1]]
    
    # 还原、测量
    H | qs[2]
    All(Measure) | qs
    
    engine.flush()
    print('%d%d' % (bool(qs[0]), bool(qs[1])))
  return wrapper

@grover
def ALL_ONES(qs):
  # 输入函数为`f(x,y) = x&y`
  # 要使得Uf|xyz>=|x,z^(x&y)>
  # 所以取Uf为CCNOT
  '''
  H | qs[2]  
  CNOT | (qs[1], qs[2])
  Tdagger | qs[2]
  CNOT | (qs[0], qs[2])
  T | qs[2]
  
  CNOT | (qs[1], qs[2])
  Tdagger | qs[2]
  CNOT | (qs[0], qs[2])
  Tdagger | qs[1]
  T | qs[2]  

  CNOT | (qs[0], qs[1])
  H | qs[2]
  Tdagger | qs[1]
  CNOT | (qs[0], qs[1])
  T | qs[0]
  S | qs[1]
  '''
  # 标记目标元素（对|B>反射？）
  Toffoli | (qs[0], qs[1], qs[2])

@grover
def ALL_ZEROS(qs):
  # 输入函数为`f(x,y) = ~x&~y`
  # 要使得Uf|xyz>=|x,z^(~x&~y)>
  # 所以取Uf为(X⊗X⊗I)CCNOT(X⊗X⊗I)

  All(X) | [qs[0], qs[1]]
  Toffoli | (qs[0], qs[1], qs[2])
  All(X) | [qs[0], qs[1]]   # UNCOMPUTE!!

@grover
def ZERO_ONE(qs):
  # 输入函数为`f(x,y) = ~x&y`
  # 要使得Uf|xyz>=|x,z^(~x&y)>
  # 所以取Uf为(X⊗I⊗I)CCNOT(X⊗I⊗I)

  X | qs[0]
  Toffoli | (qs[0], qs[1], qs[2])
  X | qs[0]   # UNCOMPUTE!!

@grover
def ONE_ZERO(qs):
  # 输入函数为`f(x,y) = x&~y`
  # 要使得Uf|xyz>=|x,z^(x&~y)>
  # 所以取Uf为(I⊗X⊗I)CCNOT(I⊗X⊗I)

  X | qs[1]
  Toffoli | (qs[0], qs[1], qs[2])
  X | qs[1]   # UNCOMPUTE!!

if __name__ == '__main__':
  ALL_ZEROS()
  ZERO_ONE()
  ONE_ZERO()
  ALL_ONES()
