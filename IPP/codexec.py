#!/usr/bin/python3

import sys
import ipp_types
import debug
import strings
import frameops
import logicalops
import conversions
import inputoutput
import flowcontrol
import datastackops
import arithmeticops
import relationalops

from instruction import InstructionBase
from instructionset import InstructionSet

class Execute(object):
    """Executes code represented in source xml file"""

    def __init__(self, i_set, input_arg):
        self.i_set = i_set
        self.input_arg = input_arg
        self.instr_set = i_set.get_set()
        self.i_set.find_labels()
        self.ip = InstructionBase()

    def run(self):
        """
        While loop iterated by instruction pointer which handles the execution of code

        :rtype int: return error code if some instruction failed or 0 if everything went correctly
        """

        while not self.ip.ip_get() > len(self.instr_set):
            for opcode, params in self.instr_set[str(self.ip.instr_pointer)].items():
                result = self.execute_instr(opcode, params)
                if result > 49:
                    return result
        
        return result


    def execute_instr(self, opcode, params):
        """ Dictionary used as a switch for instruction execution """
        
        opcode_switch = {
            'DEFVAR' :      (lambda params: frameops.Defvar(params).execute()),
            'MOVE' :        (lambda params: frameops.Move(params).execute()),
            'CREATEFRAME' : (lambda params: frameops.Createframe().execute()),
            'PUSHFRAME' :   (lambda params: frameops.Pushframe().execute()),
            'POPFRAME' :    (lambda params: frameops.Popframe().execute()),
            'CALL' :        (lambda params: frameops.Call(params).execute()),
            'RETURN' :      (lambda params: frameops.Return().execute()),
            'PUSHS' :       (lambda params: datastackops.Pushs(params).execute()),
            'POPS' :        (lambda params: datastackops.Pops(params).execute()),
            'ADD' :         (lambda params: arithmeticops.Add(params).execute()),
            'SUB' :         (lambda params: arithmeticops.Sub(params).execute()),
            'MUL' :         (lambda params: arithmeticops.Mul(params).execute()),
            'IDIV' :        (lambda params: arithmeticops.Idiv(params).execute()),
            'LT' :          (lambda params: relationalops.Lt(params).execute()),
            'GT' :          (lambda params: relationalops.Gt(params).execute()),
            'EQ' :          (lambda params: relationalops.Eq(params).execute()),
            'AND' :         (lambda params: logicalops.And(params).execute()),
            'OR' :          (lambda params: logicalops.Or(params).execute()),
            'NOT' :         (lambda params: logicalops.Not(params).execute()),
            'INT2CHAR' :    (lambda params: conversions.IntToChar(params).execute()),
            'STRI2INT' :    (lambda params: conversions.StrToInt(params).execute()),
            'LABEL' :       (lambda params: flowcontrol.Label(params).execute()),
            'JUMP' :        (lambda params: flowcontrol.Jump(params).execute()),
            'JUMPIFEQ' :    (lambda params: flowcontrol.Jumpifeq(params).execute()),
            'JUMPIFNEQ' :   (lambda params: flowcontrol.Jumpifneq(params).execute()),
            'EXIT' :        (lambda params: flowcontrol.Exit(params).execute()),
            'BREAK' :       (lambda params: debug.Break().execute()),
            'DPRINT' :      (lambda params: debug.Dprint(params).execute()),
            'CONCAT' :      (lambda params: strings.Concat(params).execute()),
            'STRLEN' :      (lambda params: strings.Strlen(params).execute()),
            'GETCHAR' :     (lambda params: strings.Getchar(params).execute()),
            'SETCHAR' :     (lambda params: strings.Setchar(params).execute()),
            'READ' :        (lambda params: inputoutput.Read(params, self.input_arg).execute()),
            'WRITE' :       (lambda params: inputoutput.Write(params).execute()),
            'TYPE' :        (lambda params: ipp_types.Type(params).execute()),
        }

        return opcode_switch[opcode](params) # Call dictionary value (instruction) with given parameters