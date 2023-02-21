#!/usr/bin/python3

import itertools

# Representation of propositional formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (ATOM).
#
# The methods supported are:
#   vars(self)     Return variables occurring in a formula
#

# Both AND and OR will inherit __init__ and vars from NaryFormula
# NaryFormula means formulas with multiple subformulas.
# conjunction (AND) and disjunction (OR) are traditionally defined
# as binary connectives, that is, with two subformulas.
# Because of associativity, ie. A & (B & C) and (A & B) & C are equivalent,
# it is often more convenient to write A & B & C.

class NaryFormula:  # N-ary formulas with multiple subformulas
    def __init__(self, subformulas):
        self.subformulas = subformulas

    def vars(self):
        vs = [f.vars() for f in self.subformulas]
        return set.union(*vs)

# AND and OR are defined with multiple subformulas (phi1 & phi2 & ... & phiN)

class AND(NaryFormula):
    def __repr__(self):
        return "(and " + (' '.join([str(x) for x in self.subformulas])) + ")"

class OR(NaryFormula):
    def __repr__(self):
        return "(or " + (' '.join([str(x) for x in self.subformulas])) + ")"

class NOT:
    def __init__(self, subformula):
        self.subformula = subformula

    def __repr__(self):
        return "(not " + str(self.subformula) + ")"

    def vars(self):
        return self.subformula.vars()

class ATOM:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def vars(self):
        return {self.name}

# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1, f2):
    return OR([NOT(f1), f2])


# A <-> B is reduced to (-A V B) & (-B V A)

def EQVI(f1, f2):
    return AND([IMPL(f1, f2), IMPL(f2, f1)])
