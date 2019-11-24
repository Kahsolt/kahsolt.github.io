#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/11/24
 
import math

from projectq import MainEngine
from projectq.ops import H, Z, X, Measure, All
from projectq.meta import Loop, Compute, Uncompute, Control


def run_grover(eng, n, Ox):
  # start in uniform superposition
  x = eng.allocate_qureg(n)
  All(H) | x

  # the auxiliary indicator qbit, prepare it as '|->'
  y = eng.allocate_qubit()
  X | y
  H | y

  # number of iterations we have to run:
  ITER = int(math.pi / 4.0 * math.sqrt(1 << n))
  with Loop(eng, ITER):
    # oracle adds a (-1)-phase to the solution(s)
    Ox(eng, x, y)

    # reflection across uniform superposition
    with Compute(eng):
      All(H) | x
      All(X) | x

    with Control(eng, x[:-1]):  # Z == H-CNOT(x[-1])-H ??
      Z | x[-1]

    Uncompute(eng)

  All(Measure) | x
  Measure | y

  eng.flush()
  return ''.join([str(int(q)) for q in x])

def Ox_alter_bits(eng, x, y):
  with Compute(eng):
    All(X) | x[1::2]
  with Control(eng, x):
    X | y
  Uncompute(eng)

def Ox_half(eng, x, y):
  with Compute(eng):
    All(X) | x[0:len(x)//2]
  with Control(eng, x):
    X | y
  Uncompute(eng)

if __name__ == '__main__':
  eng = MainEngine()
  print(run_grover(eng, 7, Ox_alter_bits))
  print(run_grover(eng, 7, Ox_half))