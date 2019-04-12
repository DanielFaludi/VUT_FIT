#!/usr/bin/python3

import sys

from instruction import InstructionBase
from instructionset import InstructionSet

class Flowcontrol(InstructionBase):
    """Base class for all flowcontrol (jump) instructions"""

    def __init__(self):
        super().__init__()

    def initial_control(self, symb1, symb2):
        """Check if both parameters are the same type"""

        symbol1 = self.unpack_symb(symb1)
        symbol2 = self.unpack_symb(symb2)

        if symbol1[1] != symbol2[1]:
            return 53

        return (symbol1, symbol2)

    def jump(self, label, label_list):
        """Perform jump to a label"""

        label_name = self.unpack_label(label)
        for item in label_list:
            for pos, name in item.items():
                if name == label_name:
                    self.ip_set(int(pos))
                    return 0

        return 52

    def unpack_label(self, label):
        """Unpack label parameter, check if it's type is label"""

        for k, v in label.items():
            if v['type'] != 'label':
                return 53
            return k

    def unpack_symb(self, symb):
        """Unpack <symb> parameter"""

        for s_val, s_type in symb.items():
            if s_type['type'] == 'var':
                s_frame, s_name = s_val.split('@')
                if not self.frame_dict[s_frame]:
                    return 55
                elif s_name not in self.frame_dict[s_frame]:
                    return 54
                else:
                    return self.frame_dict[s_frame].get_val(s_name)
            else:
                return (s_val, s_type['type'])

class Label(Flowcontrol, InstructionBase):
    """LABEL instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()

    def execute(self):
        return 0

class Jump(Flowcontrol, InstructionBase):
    """JUMP instruction"""

    def __init__(self, params):
        super().__init__()
        self.label = list(params.values())[0]
        self.label_list = InstructionSet().get_labels()
    
    def execute(self):
        """Execute JUMP instruction"""

        self.jump(self.label, self.label_list)
        return 0

class Jumpifeq(Flowcontrol, InstructionBase):
    """JUMPIFEQ instruction"""

    def __init__(self, params):
        super().__init__()
        self.label = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        self.label_list = InstructionSet().get_labels()
    
    def execute(self):
        """Execute JUMPIFEQ instruction"""

        check = self.initial_control(self.symb1, self.symb2)
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        if symbol1[1] == 'int':
            if int(symbol1[0]) == int(symbol2[0]):
                return self.jump(self.label, self.label_list)
        elif symbol1[1] == 'string':
            ord_s1 = 0
            ord_s2 = 0
            for s1_char in symbol1[0]:
                ord_s1 += ord(s1_char)
            for s2_char in symbol2[0]:
                ord_s2 += ord(s2_char)
            if ord_s1 == ord_s2:
                return self.jump(self.label, self.label_list)
        else:
            if symbol1[0] == symbol2[0]:
                return self.jump(self.label, self.label_list)
        
        self.ip_increment()
        return 0

class Jumpifneq(Flowcontrol, InstructionBase):
    """JUMPIFNEQ instruction"""

    def __init__(self, params):
        super().__init__()
        self.label = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        self.label_list = InstructionSet().get_labels()
    
    def execute(self):
        """executes JUMPIFNEQ instruction"""

        check = self.initial_control(self.symb1, self.symb2)
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        if symbol1[1] == 'int':
            if int(symbol1[0]) != int(symbol2[0]):
                return self.jump(self.label, self.label_list)
        elif symbol1[1] == 'string':
            ord_s1 = 0
            ord_s2 = 0
            for s1_char in symbol1[0]:
                ord_s1 += ord(s1_char)
            for s2_char in symbol2[0]:
                ord_s2 += ord(s2_char)
            if ord_s1 != ord_s2:
                return self.jump(self.label, self.label_list)
        else:
            if symbol1[0] != symbol2[0]:
                return self.jump(self.label, self.label_list)
        
        self.ip_increment()
        return 0   

class Exit(Flowcontrol, InstructionBase):
    """EXIT instruction"""

    def __init__(self, params):
        super().__init__()
        self.symb = list(params.values())[0]

    def execute(self):
        """Executes EXIT instruction"""
        
        symbol = self.unpack_symb(self.symb)
        if not isinstance(symbol, tuple):
            return symbol

        if symbol[1] != 'int':
            return 53
        elif int(symbol[0]) not in range(0, 50):
            return 57
        else:
            sys.exit(int(symbol[0]))
        