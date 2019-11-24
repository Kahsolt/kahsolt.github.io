#!/usr/bin/env python3
# Author: Armit
# Create Time: 2019/11/24 

from projectq import MainEngine
from projectq.ops import All, CNOT, H, Measure, Rz, X, Z
from projectq.meta import Dagger, Control

def teleport(eng, init_phi_fn):
  # make bell-state pair
  b1, b2 = eng.allocate_qubit(), eng.allocate_qubit()
  H | b1
  CNOT | (b1, b2)

  # Alice creates a nice state to send
  print("Alice is creating her state from scratch, i.e. |0>.")
  psi = eng.allocate_qubit()
  init_phi_fn(eng, psi)

  # entangle it with Alice's b1
  print("Alice entangled her qubit with her share of the Bell-pair.")
  CNOT | (psi, b1)

  # measure two values (once in Hadamard basis) and send the bits to Bob
  H | psi
  All(Measure) | [psi, b1]
  msg_to_bob = [int(psi), int(b1)]  # classical
  print("Alice is sending the message {} to Bob.".format(msg_to_bob))

  # Bob may have to apply up to two operation depending on the message sent by Alice:
  with Control(eng, b1):    # if int(b1) == 1: ...
    X | b2
  with Control(eng, psi):
    Z | b2

  #########################################
  # TELEPORTATION HAS BEEN DONE TILL HERE #
  #########################################
  
  # try to uncompute the psi state
  print("Bob is trying to uncompute the state.")
  with Dagger(eng):
    init_phi_fn(eng, b2)

  # check whether the uncompute was successful. The simulator only allows to
  # delete qubits which are in a computational basis state.
  del b2
  eng.flush()

  print("Bob successfully arrived at |0>")


if __name__ == "__main__":
  eng = MainEngine()

  # define our state-creation routine, which transforms a |0> to the state
  # we would like to send. Bob can then try to uncompute it and, if he
  # arrives back at |0>, we know that the teleportation worked.
  def init_phi(eng, q):
    H | q
    Rz(1.21) | q

  teleport(eng, init_phi)