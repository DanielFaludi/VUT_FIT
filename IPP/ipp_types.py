#!/usr/bin/python3

from instruction import InstructionBase

class Type(InstructionBase):
    """TYPE instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.var = list(params.values())[0]
        self.symb = list(params.values())[1]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        """Executes TYPE instruction"""

        symbol = self.unpack_symb()
        
        if symbol[1] is not None:
            self.frame_dict[self.frame].update(self.var_name, symbol[1], 'string')
        else:
            self.frame_dict[self.frame].update(self.var_name, '', 'string')

        return 0

    def unpack_symb(self):
        for s_val, s_type in self.symb.items():
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