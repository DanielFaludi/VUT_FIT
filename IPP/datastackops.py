#!/usr/bin/python3

from instruction import InstructionBase

class DataStack(object):
    """Base class for data stack instructions"""

    data_stack = []

    def __init__(self):
        super().__init__()

    def __len__(self):
        """Returns number of items in data stack"""

        return len(self.data_stack)
    
    def __contains__(self, item):
        """Method that allows the use of 'in' operator call on this class"""

        if item in self.data_stack:
            return True
        return False

    def append(self, item):
        """Appends item to data stack"""

        self.data_stack.append(item)

    def s_pop(self):
        """Pops item from data stack"""

        return self.data_stack.pop()

class Pushs(InstructionBase):
    """PUSHS instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.data_stack = DataStack()
        self.symb = list(params.values())[0]
    
    def execute(self):
        """Executes PUSHS instruction"""

        for s_name, s_type in self.symb.items():
            if s_type['type'] == 'var':
                var_frame, var_name = s_name.split('@')
                if not self.frame_dict[var_frame]:
                    return 55
                elif var_name not in self.frame_dict[var_frame]:
                    return 54
                else:
                    value_pack = self.frame_dict[var_frame].get_val(var_name)
                    s_name, s_type = value_pack
                    self.data_stack.append({s_name:s_type})
            else:
                self.data_stack.append({s_name:s_type['type']})

        return 0

class Pops(InstructionBase):
    """POPS instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.data_stack = DataStack()
        self.var = list(params.values())[0]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
    
    def execute(self):
        """Executes POPS instruction"""
        
        if len(self.data_stack) == 0:
            return 56
        
        if not self.frame_dict[self.frame]:
            return 55
        if self.var_name not in self.frame_dict[self.frame]:
            return 54
        
        value_pack = self.data_stack.s_pop()
        for k, v in value_pack.items():
            self.frame_dict[self.frame].update(self.var_name, k, v)

        return 0