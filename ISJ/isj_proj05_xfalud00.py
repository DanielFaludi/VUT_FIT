#!/usr/bin/env python3

import re, itertools

class Polynomial:

    # Initialize class with args, list or kwargs
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            if type(args[0]) == type([]):
                self.coeffs = args[0] # Assign list from tuple
            elif type(args[0]) == type(0):
                self.coeffs = list(args) # Convert tuple to list and assign to coeffs
        if len(kwargs) > 0:
            key_str = ''.join([k for k,v in sorted(kwargs.items())])
            match = re.findall(r"([a-z]+)([0-9]+)", key_str)
            if match:
                items = [int(x[1]) for x in match] # List of index numbers
                if len(items) == 1 and items[0] == 0:
                    self.coeffs = [v for k, v in sorted(kwargs.items())] # If there is only one index and that index is 0, assign
                elif len(items) == 1 and items[0] != 0:
                    list_len = items[0]
                    args_count = [x for x in range(0, list_len)]
                    for arg in args_count:
                        kwargs.update({'x{}'.format(arg): 0}) # Fill missing indexes when there is only one index and it is not 0
                    self.coeffs = [v for k, v in sorted(kwargs.items())]
                else:
                    if items[0] != 0:
                        for i in range(items[0]):
                            kwargs.update({'x{}'.format(i): 0}) # Fill missing indexes up to lowest entered index
                    args_list = [x for x in range(items[0], items[-1] + 1)]
                    missing_args = (list(set(items) ^ set(args_list))) # Find missing indexes
                    for i in range(len(missing_args)):
                        kwargs.update({'x{}'.format(missing_args[i]): 0}) # Update dict with missing indexes
                    self.coeffs = [v for k, v in sorted(kwargs.items())]

    # Function to convert input to human readable polynomial string
    def __repr__(self):

        # Dictinoary for sign assignment
        joiner = {
            (True, True): '-',
            (True, False): '',
            (False, True): ' - ',
            (False, False): ' + '
        }

        result = []
        for power, coeff in reversed(list(enumerate(self.coeffs))):
            j = joiner[not result, coeff < 0]
            coeff = abs(coeff)
            if coeff == 0: # If coefficient is zero, skip iteration
                continue
            if coeff == 1 and power != 0: # If coefficient is one, dont append 1 to x
                coeff = ''
            f = {0: '{}{}', 1: '{}{}x'}.get(power, '{}{}x^{}')
            result.append(f.format(j, coeff, power))
        return ''.join(result) or '0' # Return human readable string

    # Adds two polynomials
    def __add__(self, other):
        return Polynomial(*(x + y for x, y in itertools.zip_longest(self.coeffs, other.coeffs, fillvalue = 0)))

    # Compares two polynomials in human readable form
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    
    # Outputs power to the n'th of polynomial
    def __pow__(self, val):
        return Polynomial(*(self.__pow(self.coeffs, val)))

    # Outputs first derivative of polynomial
    def derivative(self):
        return Polynomial(*(self.__der()))

    # Outputs value of polynomial for specified x
    def at_value(self, *val):
        exp = (len(self.coeffs) - 1)
        if len(val) == 1:
            res = 0             
            for x in reversed(self.coeffs):
                res += (x*val[0]**exp)
                exp -= 1
            return res
        if len(val) == 2:
            res1 = 0
            res2 = 0
            for x in reversed(self.coeffs):
                res1 += (x*val[0]**exp)
                res2 += (x*val[1]**exp)
                exp -= 1
            return res2 - res1

    # Performs derivative of given polynomial
    def __der(self):
        res = []
        for i in range(1, len(self.coeffs)):
            res.append(i*self.coeffs[i])
        return res or [0] # If there is only one element, that means it's a constant therefore return 0

    # Multiplies two polynomials (needed for __pow__)    
    def __mul(self, a, b):
        res = [0]*(len(a) + len(b)-1)
        for i in range(len(a)):
            ai = a[i]
            for j in range(len(b)):
                res[i + j] += ai * b[j]
        return res

    # Performs power to the n'th of polynomial
    def __pow(self, a, n):
        res = [1]
        for i in range(n):
            res = self.__mul(res, a)
        return res    

# Assertions
def test():
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1)+Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1,x1=1)**1) == "x - 1"
    assert str(Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1,x1=1)
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2,x1=3,x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2,3,4,-5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
    pol5 = Polynomial([1,0,-2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1,3.6) == -23.92
    assert pol5.at_value(-1,3.6) == -23.92

if __name__ == '__main__':
    test()