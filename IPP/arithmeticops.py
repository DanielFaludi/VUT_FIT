#!/usr/bin/python3

from instruction import InstructionBase

class Arithmetics(InstructionBase):
    """Base class for every arithmetical operation instruction"""

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
                    value_pack = self.frame_dict[s_frame].get_val(s_name)
                    s_name, s_type = value_pack
                    if s_type != 'int':
                        return 53
                    return value_pack
            elif s_type['type'] == 'int':
                return (s_val, s_type['type'])
            else:
                return 53

class Add(Arithmetics, InstructionBase):
    """ADD instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)
    
    def execute(self):
        """Executes ADD instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        result = int(symbol1[0]) + int(symbol2[0])

        self.frame_dict[self.frame].update(self.var_name, str(result), 'int')

        return 0

class Sub(Arithmetics, InstructionBase):
    """SUB instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)
    
    def execute(self):
        """Executes SUB instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        result = int(symbol1[0]) - int(symbol2[0])

        self.frame_dict[self.frame].update(self.var_name, str(result), 'int')

        return 0

class Mul(Arithmetics, InstructionBase):
    """MUL instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)
    
    def execute(self):
        """Executes MUL instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        result = int(symbol1[0]) * int(symbol2[0])

        self.frame_dict[self.frame].update(self.var_name, str(result), 'int')

        return 0

class Idiv(Arithmetics, InstructionBase):
    """IDIV instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)
    
    def execute(self):
        """Executes IDIV instruction"""
        
        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        try:
            result = int(symbol1[0]) // int(symbol2[0])
        except ZeroDivisionError:
            return 57

        self.frame_dict[self.frame].update(self.var_name, str(result), 'int')

        return 0