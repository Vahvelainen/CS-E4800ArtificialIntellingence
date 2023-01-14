#!/usr/bin/python3

import itertools
#from itertools import chain, combinations

def powerset(iterable):
  "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
  s = list(iterable)
  return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def powersetAsList(l):
  return list( powerset(l) )

# Representation of propositional formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious equivalences.
# Separate classes represent each connective, atomic formulas, and
# the constants TRUE and FALSE.
#
# The methods supported are:
#   f.vars(self)          Set of all variables occurring in the formula f
#   f.truthValue(self,v)  Compute truth-value of f under valuation 'v'
#                         Returns True if v |= f and False otherwise
#
# Valuations are represented as sets/lists consisting of the names
# of those atomic formulas that are True. For example, the empty
# set/list corresponds to the valuation in which all atomic formulas
# are False. To test if the formula ATOM("a") is true in a valuation
# V, one tests if "a" is an element of the set/list V.

# Superclass to handle parts of AND and OR

class BinaryFormula:
  def __init__(self,subformula1,subformula2):
    self.subformula1 = subformula1
    self.subformula2 = subformula2
  def vars(self):
    return self.subformula1.vars().union(self.subformula2.vars())

# Both AND and OR will inherit __init__ and vars from BinaryFormula

# AND - conjunction

class AND(BinaryFormula):
  def __repr__(self):
    return "(" + str(self.subformula1) + " AND " + str(self.subformula2) + ")"
  def truthValue(self,v):
    return self.subformula1.truthValue(v) and self.subformula2.truthValue(v)
### IMPLEMENT THIS (~ 1 line)

# OR - disjunction

class OR(BinaryFormula):
  def __repr__(self):
    return "(" + str(self.subformula1) + " OR " + str(self.subformula2) + ")"
  def truthValue(self,v):
    return self.subformula1.truthValue(v) or self.subformula2.truthValue(v)
### IMPLEMENT THIS (~ 1 line)

# NOT - negation

class NOT:
  def __init__(self,subformula):
    self.subformula = subformula
  def __repr__(self):
    return "(NOT " + str(self.subformula) + ")"
  def vars(self):
    return self.subformula.vars()
  def truthValue(self,v):
    return not self.subformula.truthValue(v)
### IMPLEMENT THIS (~ 1 line)

# ATOM - atomic formulas

class ATOM:
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    return self.name
  def vars(self):
    return {self.name}
  def truthValue(self,v):
    # self is type of ATOM, str(self) = "A"
    # v 's type is a list of strings it seems
    # print ('asdf1self' + str(self)) #self = ATOM
    # print ('asdfv' + str(v)) #v =list
    # print ( str(self) in v)
    # maybe use vars and some python iteration functions instead of srt(self)
    # print(self.vars()) should propably use dis and not str()
    return all(i in v for i in self.vars()) #dis wrks, no idea should this be all or any but all sees to work
### IMPLEMENT THIS (~ 1 line)

# FALSE - the constant that represents the truth-value False

class FALSE:
  def __repr__(self):
    return "FALSE"
  def vars(self):
    return set()
  def truthValue(self,v):
    return False #I dont understand this meaning
### IMPLEMENT THIS (~ 1 line)

# TRUE - the constant that represents the truth-value True

class TRUE:
  def __repr__(self):
    return "TRUE"
  def vars(self):
    return set()
  def truthValue(self,v):
    return True #I dont understand this meaning
### IMPLEMENT THIS (~ 1 line)


# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return OR(NOT(f1),f2)

# A <-> B is reduced to (A -> B) & (B -> A)

def EQVI(f1,f2):
  return AND(IMPL(f1,f2),IMPL(f2,f1))

# Test for the satisfiability of a formula
# This function should return False if the formula is unsatisfiable,
# and otherwise it will return a valuation that satisfies the formula.
# The valuation is a list of names of true atomic formulas.

# A very simple implementation would first find the set of all
# variables occurring in a formula, and then generate all possible
# subsets of that set (or corresponding lists), which represent
# all possible valuations, and then test if the given formula is
# true in at least one of the valuations.

# 'satisfiable' returns False if the formula is NOT satisfiable,
# and it returns the valuation that makes the formula true otherwise.

def satisfiable(f):
  #return passing subset if found one and false if no
  subsets = powersetAsList(f.vars())
  for subset in subsets:
    if f.truthValue(subset):
      return subset #im 60% sure this should be a list of all the sets
  return False
### IMPLEMENT THIS (10 to 15 lines total)

##IDK what is valuation need to check homework
def satisfiableAll(f):
  #return passing subset if found one and false if no
  subsets = powersetAsList(f.vars())
  valuation = []
  for subset in subsets:
    if f.truthValue(subset):
      valuation.append(subset) #im 60% sure this should be a list of all the sets
  if len(valuation):
    return valuation
  return False

# Test logical consequence
# Returns True if f2 is a logical consequence of f1 (that is f1 |= f2)
# and returns False otherwise.

def logicalConsequence(f1,f2):
  # print(satisfiableAll(f1))
  # print(satisfiableAll(f2))
  return satisfiable(f1) == satisfiable(f2)
### IMPLEMENT THIS (~ 1 line)
