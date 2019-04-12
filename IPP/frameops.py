#!/usr/bin/python3

from instructionset import InstructionSet
from instruction import InstructionBase
from mem_model import GlobalFrame, TemporaryFrame, LocalFrame

class Defvar(InstructionBase):
    """DEFVAR instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        """Executes DEFVAR instruction"""

        if not self.frame_dict[self.frame]:
            return 55

        if self.var_name not in self.frame_dict[self.frame]:
            self.frame_dict[self.frame].append({self.var_name:{'value':{None:None}}})
        else:
            self.frame_dict[self.frame].redef(self.var_name)

        return 0

class Move(InstructionBase):
    """MOVE instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb = list(params.values())[1]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')
        for s_name, s_type in self.symb.items():
            self.symb_name, self.symb_type = s_name, s_type
        
    def execute(self):
        """Executes MOVE instruction"""

        if not self.frame_dict[self.frame]:
            return 55
        elif self.var_name not in self.frame_dict[self.frame]:
            return 54
        
        if self.symb_type['type'] == 'var':
            s_frame, s_name = self.symb_name.split('@')
            if not self.frame_dict[s_frame]:
                return 55
            elif s_name not in self.frame_dict[s_frame]:
                return 54
            else:
                value, value_t = self.frame_dict[s_frame].get_val(s_name)
        else:
            value, value_t = self.symb_name, self.symb_type['type']

        self.frame_dict[self.frame].update(self.var_name, value, value_t)
        return 0

class Createframe(InstructionBase):
    """CREATEFRAME instruction"""

    def __init__(self):
        super().__init__()
        self.ip_increment()

    def execute(self):
        """Executes CREATEFRAME instruction"""

        InstructionBase.temp_frame.init_frame()
        return 0

class Pushframe(InstructionBase):
    """PUSHFRAME instruction"""

    def __init__(self):
        super().__init__()
        self.ip_increment()

    def execute(self):
        """Execute PUSHFRAME instruction"""

        if self.temp_frame:
            self.local_frame.init_frame()
            self.local_frame.push(self.temp_frame.f_pop())
        else:
            return 55
        return 0

class Popframe(InstructionBase):
    """POPFRAME instruction"""

    def __init__(self):
        super().__init__()
        self.ip_increment()

    def execute(self):
        """Executes POPFRAME instruction"""

        if not self.local_frame:
            return 55
        
        self.temp_frame.push(self.local_frame.f_pop())
        return 0

class Call(InstructionBase):
    """CALL instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.label_list = InstructionSet().get_labels()
        self.label = list(params.values())[0]

    def execute(self):
        """Executes CALL instruction"""

        self.call_stack.append(self.ip_get())
        label_name = self.unpack_label()
        for item in self.label_list:
            for pos, name in item.items():
                if name == label_name:
                    self.ip_set(int(pos))
                    return 0

        return 52

    def unpack_label(self):
        for k, v in self.label.items():
            if v['type'] != 'label':
                return 53
            return k

class Return(InstructionBase):
    """RETURN instruction"""

    def __init__(self):
        super().__init__()
    
    def execute(self):
        """Execute RETURN instruction"""
        
        if len(self.call_stack) == 0:
            return 52

        self.ip_set(self.call_stack.pop())
        return 0
        