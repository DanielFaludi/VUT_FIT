#!/usr/bin/python3

from instruction import InstructionBase

class Conversion(InstructionBase):
    """Conversion instruction base class"""

    def __init__(self, var):
        super().__init__()
        self.var = var
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def initial_control(self):
        """Check if variables in accessed frames are existing"""

        if not self.frame_dict[self.frame]:
            return 55
        
        if self.var_name not in self.frame_dict[self.frame]:
            return 54
        
        return 0
    
    def unpack_symb_int(self, symb):
        """Unpack <symb> parameter and extract integer parameter"""

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

    def unpack_symb_str(self, symb):
        """Unpack <symb> parameter and extract string parameter"""

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
                    if s_type != 'string':
                        return 53
                    return value_pack
            elif s_type['type'] == 'string':
                return (s_val, s_type['type'])
            else:
                return 53

class IntToChar(Conversion, InstructionBase):
    """INT2CHAR instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb = list(params.values())[1]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var)
    
    def execute(self):
        """Executes instruction"""

        check = self.initial_control()
        if check != 0:
            return check

        symbol = self.unpack_symb_int(self.symb)
        if not isinstance(symbol, tuple):
            return symbol

        try:
            result = chr(int(symbol[0]))
        except ValueError:
            return 58

        self.frame_dict[self.frame].update(self.var_name, result, 'string')

        return 0
    

class StrToInt(Conversion, InstructionBase):
    """STR2INT instruction"""

    def __init__(self, params):
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        super().__init__(self.var)
    
    def execute(self):
        check = self.initial_control()
        if check != 0:
            return check

        symbol1 = self.unpack_symb_str(self.symb1)
        symbol2 = self.unpack_symb_int(self.symb2)

        if not isinstance(symbol1, tuple):
            return symbol1
        
        if not isinstance(symbol2, tuple):
            return symbol2

        try:
            char = symbol1[0][int(symbol2[0])]
        except IndexError:
            return 58
        
        try:
            result = ord(char)
        except ValueError:
            return 58

        self.frame_dict[self.frame].update(self.var_name, result, 'int')

        return 0