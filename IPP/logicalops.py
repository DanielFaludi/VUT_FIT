#!/usr/bin/python3

from instruction import InstructionBase

class Logic(InstructionBase):
    """Base class for every logical operation instruction"""

    def __init__(self, *args):
        super().__init__()
        if len(args) == 3:
            self.var = args[0]
            self.symb1 = args[1]
            self.symb2 = args[2]
        else:
            self.var = args[0]
            self.symb1 = args[1]

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

    def initial_control_not(self):
        if not self.frame_dict[self.frame]:
            return 55
        
        if self.var_name not in self.frame_dict[self.frame]:
            return 54
        
        symbol = self.unpack_symb(self.symb1)

        if not isinstance(symbol, tuple):
            return symbol

        return symbol

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
                    if s_type != 'bool':
                        return 53
                    return value_pack
            elif s_type['type'] == 'bool':
                return (s_val, s_type['type'])
            else:
                return 53

class And(Logic, InstructionBase):
    """AND instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)
    
    def execute(self):
        """Executes AND instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        
        if symbol1[0] == 'false' or symbol2[0] == 'false':
            result = 'false'
        else:
            result = 'true'

        self.frame_dict[self.frame].update(self.var_name, result, 'bool')

        return 0

class Or(Logic, InstructionBase):
    """OR instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb1, self.symb2)
    
    def execute(self):
        """Executes OR instruction"""

        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        
        if symbol1[0] == 'true' or symbol2[0] == 'true':
            result = 'true'
        else:
            result = 'false'

        self.frame_dict[self.frame].update(self.var_name, result, 'bool')

        return 0

class Not(Logic, InstructionBase):
    """NOT instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb = list(params.values())[1]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var, self.symb)
    
    def execute(self):
        """Execute NOT instruction"""
        
        check = self.initial_control_not()
        if not isinstance(check, tuple):
            return check

        symbol = check
        
        if symbol[0] == 'true':
            result = 'false'
        elif symbol[0] == 'false':
            result = 'true'
        
        self.frame_dict[self.frame].update(self.var_name, result, 'bool')

        return 0