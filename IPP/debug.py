#!/usr/bin/python3

import sys

from instruction import InstructionBase

class Break(InstructionBase):
    """BREAK instruction"""

    def __init__(self):
        super().__init__()
        self.ip_increment()

    def execute(self):
        """Executes BREAK instruction"""

        sys.stderr.write("\n")
        sys.stderr.write("Instruction Pointer: {}\n".format(self.ip_get() - 1))
        sys.stderr.write("Number of executed instructions: {}\n".format(self.ic_get()))
        sys.stderr.write("Global Frame: \n{}\n".format(self.global_frame))
        sys.stderr.write("Temporary Frame: \n{}\n".format(self.temp_frame))
        sys.stderr.write("Local Frame: \n{}\n".format(self.local_frame))
        sys.exit(0)

class Dprint(InstructionBase):
    """DPRINT instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.symb = list(params.values())[0]
    
    def execute(self):
        """Executes DPRINT instruction"""
        
        for s_val, s_type in self.symb.items():
            if s_type['type'] == 'var':
                s_frame, s_name = s_val.split('@')
                if not self.frame_dict[s_frame]:
                    return 55
                elif s_name not in self.frame_dict[s_frame]:
                    return 54
                else:
                    value_pack = self.frame_dict[s_frame].get_val(s_name)
                    value = value_pack[0]
                    sys.stderr.write(str(value) + "\n")
            else:
                sys.stderr.write(str(s_val) + "\n")
        
        return 0