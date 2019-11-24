#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/11/24 

from projectq import MainEngine
from projectq.ops import H, Measure

def randb(engine):
  q = engine.allocate_qubit()
  H | q
  Measure | q
  engine.flush()
  return int(q)

if __name__ == "__main__":
  ITER = 1000
  OK = 0

  engine = MainEngine()
  for _ in range(ITER):
    if randb(engine): OK += 1
  
  print('Prob: %f' % (OK / ITER))