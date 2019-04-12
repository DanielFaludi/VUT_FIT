#!/usr/bin/python3

from instruction import InstructionBase

class Relationals(InstructionBase):
    """Base class for every relational operation instruction"""

    def __init__(self, var, symb1, symb2):
        super().__init__()
        self.var = var
        self.symb1 = symb1
        self.symb2 = symb2
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
    
    def initial_control(self):
        if not self.frame_dict[self.frame]:
            return 55
        
        if self.var_name not in self.frame_dict[self.frame]:
            return 54
        
        symbol1 = self.unpack_symb(self.symb1)
        symbol2 = self.unpack_symb(self.symb2)

        if not isinstance(symbol1, tuple):
            return symbol1
        elif not isinstance(symbol2, tuple):
            return symbol2
        
        return (symbol1, symbol2)

    def unpack_symb(self, symb):
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

class Lt(Relationals, InstructionBase):
    """LT instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)

    def execute(self):
        """Executes LT instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        if symbol1[1] == symbol2[1]:
            s_type = symbol1[1]
        else:
            return 53

        if s_type == 'label' or s_type == 'nil':
            return 53
        
        if s_type == 'int':
            if int(symbol1[0]) < int(symbol2[0]):
                result = 'true'
            else:
                result = 'false'

        if s_type == 'bool':
            if symbol1[0] < symbol2[0]:
                result = 'true'
            else:
                result = 'false'
        
        if s_type == 'string':
            ord_s1 = 0
            ord_s2 = 0
            for s1_char in symbol1[0]:
                ord_s1 += ord(s1_char)
            for s2_char in symbol2[0]:
                ord_s2 += ord(s2_char)
            if ord_s1 < ord_s2:
                result = 'true'
            else:
                result = 'false'

        self.frame_dict[self.frame].update(self.var_name, result, 'bool')

        return 0

class Gt(Relationals, InstructionBase):
    """GT instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)

    def execute(self):
        """Executes GT instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        if symbol1[1] == symbol2[1]:
            s_type = symbol1[1]
        else:
            return 53

        if s_type == 'label' or s_type == 'nil':
            return 53
        
        if s_type == 'int':
            if int(symbol1[0]) > int(symbol2[0]):
                result = 'true'
            else:
                result = 'false'

        if s_type == 'bool':
            if symbol1[0] > symbol2[0]:
                result = 'true'
            else:
                result = 'false'
        
        if s_type == 'string':
            ord_s1 = 0
            ord_s2 = 0
            for s1_char in symbol1[0]:
                ord_s1 += ord(s1_char)
            for s2_char in symbol2[0]:
                ord_s2 += ord(s2_char)
            if ord_s1 > ord_s2:
                result = 'true'
            else:
                result = 'false'
                
        self.frame_dict[self.frame].update(self.var_name, result, 'bool')

        return 0

class Eq(Relationals, InstructionBase):
    """EQ instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)

    def execute(self):
        """Executes EQ instruction"""
        
        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        if symbol1[1] == symbol2[1]:
            s_type = symbol1[1]
        else:
            return 53

        if s_type == 'label' or s_type == 'nil':
            return 53
        
        if s_type == 'int':
            if int(symbol1[0]) == int(symbol2[0]):
                result = 'true'
            else:
                result = 'false'

        if s_type == 'bool':
            if symbol1[0] == symbol2[0]:
                result = 'true'
            else:
                result = 'false'
        
        if s_type == 'string':
            ord_s1 = 0
            ord_s2 = 0
            for s1_char in symbol1[0]:
                ord_s1 += ord(s1_char)
            for s2_char in symbol2[0]:
                ord_s2 += ord(s2_char)
            if ord_s1 == ord_s2:
                result = 'true'
            else:
                result = 'false'
                
        self.frame_dict[self.frame].update(self.var_name, result, 'bool')

        return 0