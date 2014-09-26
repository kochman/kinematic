#!/usr/bin/env python3

import argparse
import sympy
import sys
from sympy import Symbol as Sym


class DuoSymbol:

	def __init__(self, name, value):
		self.name = name
		self.value = float(value)

	def __repr__(self):
		return "DuoSymbol('{}', {})".format(self.name, self.value)


class KinematicEquation:

	def __init__(self, func, variables):
		self.func = func
		self.variables = variables

	def solve(self, symbols, for_var):
		solved = sympy.solve(self.func, for_var)
		vals = [(sym.name, sym.value) for sym in symbols]
		return [eq.subs(vals) for eq in solved]

	def __str__(self):
		return str(self.func)


def solve(symbols, looking_for):
	def find_suitable_equation(variables):
		for equation in equations:
			if equation.variables <= variables:
				return equation

	variables = {sym.name for sym in symbols}
	variables.add(looking_for)

	eq = find_suitable_equation(variables)
	if eq:
		return eq.solve(symbols, looking_for)
	raise ValueError

equations = set()
equations.add(KinematicEquation(
	0.5 * Sym('a') * (Sym('t') ** 2) + (Sym('Vi') * Sym('t')) - Sym('Dx'),
	set(['a', 't', 'Vi', 'Dx'])))
equations.add(KinematicEquation(
	0.5 * (Sym('Vf') + Sym('Vi')) * Sym('t') - Sym('Dx'),
	set(['Vf', 'Vi', 'Dx', 't'])))
equations.add(KinematicEquation(
	Sym('Vi') + Sym('a') * Sym('t') - Sym('Vf'),
	set(['Vf', 'Vi', 'a', 't'])))
equations.add(KinematicEquation(
	Sym('Vi') ** 2 + 2 * Sym('a') * Sym('Dx') - Sym('Vf') ** 2,
	set(['Vi', 'Dx', 'a', 'Vf'])))

parser = argparse.ArgumentParser()
parser.add_argument('variables', nargs='+', help='t=3.2')
parser.add_argument('find', help='a')
args = parser.parse_args()

symbols = set()
for var in args.variables:
	name, value = var.split('=')
	symbol = DuoSymbol(name, value)
	symbols.add(symbol)

try:
	result = solve(symbols, args.find)
except ValueError:
	print('Not possible with given values')
	sys.exit(1)
for eq in result:
	print(eq)
