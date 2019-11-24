#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/10/05 

# minimal generator set - brute force

import time
import numpy as np

NUMBERS = np.array([ # '0' ~ '9'
  0x3F, 0x06, 0x5B, 0x4F, 0x66, 
  0x6D, 0x7D, 0x07, 0x7F, 0x6F,
], dtype=np.uint8)
NOT = lambda x, y: ~x
AND = lambda x, y: x & y
OR  = lambda x, y: x | y
XOR = lambda x, y: x ^ y
OPS = [ NOT, AND, OR, XOR ]

to_bin = lambda x, w=8: bin(x)[2:].rjust(w, '0')

def timer(fn):
  def wrapper(*args, **kwargs):
    s = time.time()
    ret = fn(*args, **kwargs)
    t = time.time()
    print('[Timer] %.4fs' % (t - s))
    return ret
  return wrapper

@timer
def MGS_bf(N=NUMBERS, OP=OPS):
  target, solutions = set(N), [ ]
  nlen = len(N)
  for sel in range(2**nlen):
    sel_bin = to_bin(sel, nlen)
    partial = { N[i] for i in range(len(sel_bin)) if sel_bin[i] == '1' }
    partial_orig = partial.copy() # save orig for ans
    
    size = 0
    while size != len(partial): # search result extended
      size = len(partial)
      new_partial = { op(x, y) for op in OP for x in partial for y in partial }
      partial.update(new_partial)
      
      if partial.issuperset(target):
        solutions.append(partial_orig)
        break

  print('>> %d solutions found in total' % len(solutions))
  groups = { }
  for sol in solutions:
    sz = len(sol)
    if sz in groups: groups[sz].append(sol)
    else: groups[sz] = [ sol ]

  min_sols = groups.get(sorted(groups)[0])  # just need the shortest groups
  return [sorted([np.where(NUMBERS == g)[0][0] for g in sol]) for sol in min_sols]
  
if __name__ == '__main__':
  print('over {OR, AND, XOR, NOT}')
  for sol in MGS_bf():
    print(sol)
  print()

  print('over {OR, AND}')
  for sol in MGS_bf(NUMBERS, [OR, AND]):
    print(sol)
  print()
  
  print('over {OR, NOT}')
  for sol in MGS_bf(NUMBERS, [OR, NOT]):
    print(sol)
  print()
    
  print('over {AND, NOT}')
  for sol in MGS_bf(NUMBERS, [AND, NOT]):
    print(sol)
  print()
