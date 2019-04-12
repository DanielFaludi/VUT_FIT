#!/usr/bin/python3

from instruction import InstructionBase

class String(InstructionBase):

    def __init__(self):
        super().__init__()
    
    def unpack_symb_string(self, symb):
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
    
    def unpack_symb_int(self, symb):
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

class Concat(String, InstructionBase):

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        result = symbol1[0] + symbol2[0]

        self.frame_dict[self.frame].update(self.var_name, result, 'string')

        return 0        

    def initial_control(self):
        if not self.frame_dict[self.frame]:
            return 55
        elif self.var_name not in self.frame_dict[self.frame]:
            return 54

        symbol1 = self.unpack_symb_string(self.symb1)
        symbol2 = self.unpack_symb_string(self.symb2)

        if not isinstance(symbol1, tuple):
            return symbol1
        elif not isinstance(symbol2, tuple):
            return symbol2

        return (symbol1, symbol2)

class Strlen(String, InstructionBase):

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb = list(params.values())[1]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol = check
        result = len(symbol[0])

        self.frame_dict[self.frame].update(self.var_name, result, 'int')

        return 0

    def initial_control(self):
        if not self.frame_dict[self.frame]:
            return 55
        elif self.var_name not in self.frame_dict[self.frame]:
            return 54

        symbol1 = self.unpack_symb_string(self.symb)

        if not isinstance(symbol1, tuple):
            return symbol1

        return (symbol1)

class Getchar(String, InstructionBase):

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        symbol1, symbol2 = check
        pos = int(symbol2[0])
        
        if pos < 0:
            return 58

        try:
            result = symbol1[0][pos]
        except IndexError:
            return 58
        
        self.frame_dict[self.frame].update(self.var_name, result, 'string')

        return 0


    def initial_control(self):
        if not self.frame_dict[self.frame]:
            return 55
        elif self.var_name not in self.frame_dict[self.frame]:
            return 54

        symbol1 = self.unpack_symb_string(self.symb1)
        symbol2 = self.unpack_symb_int(self.symb2)

        if not isinstance(symbol1, tuple):
            return symbol1
        elif not isinstance(symbol2, tuple):
            return symbol2

        return (symbol1, symbol2)

class Setchar(String, InstructionBase):

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb1 = list(params.values())[1]
        self.symb2 = list(params.values())[2]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        check = self.initial_control()
        if not isinstance(check, tuple):
            return check

        value_pack = self.frame_dict[self.frame].get_val(self.var_name)
        var, var_type = value_pack
        if var_type != 'string':
            return 53

        symbol1, symbol2 = check
        pos = int(symbol1[0])
        modif = symbol2[0][0]

        result = list(var)

        if pos < 0:
            return 58

        try:
            result[pos] = modif
            result = ''.join(result)
        except IndexError:
            return 58

        self.frame_dict[self.frame].update(self.var_name, result, 'string')

        return 0

    def initial_control(self):
        if not self.frame_dict[self.frame]:
            return 55
        elif self.var_name not in self.frame_dict[self.frame]:
            return 54

        symbol1 = self.unpack_symb_int(self.symb1)
        symbol2 = self.unpack_symb_string(self.symb2)

        if not isinstance(symbol1, tuple):
            return symbol1
        elif not isinstance(symbol2, tuple):
            return symbol2

        return (symbol1, symbol2)