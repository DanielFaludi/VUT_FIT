#!/usr/bin/python3

from mem_model import GlobalFrame, LocalFrame, TemporaryFrame

class InstructionBase(object):
    """Base class for every instruction"""

    global_frame = GlobalFrame()
    local_frame = LocalFrame()
    temp_frame = TemporaryFrame()

    instr_counter = -1 # -1 to prevent increment to 1 on first initialization
    instr_pointer = 1 # start with first instruction

    call_stack = []

    def __init__(self):
        InstructionBase.instr_counter += 1
        self.frame_dict = {
            'GF' : InstructionBase.global_frame,
            'LF' : InstructionBase.local_frame,
            'TF' : InstructionBase.temp_frame,
        }

    def ip_increment(self):
        """Increments instruction pointer"""

        InstructionBase.instr_pointer += 1

    def ip_set(self, value):
        """Sets instruction pointer"""

        InstructionBase.instr_pointer = value

    def ip_get(self):
        """Get value of instruction pointer"""

        return InstructionBase.instr_pointer

    def ic_get(self):
        """Get value of instruction counter"""
        
        return InstructionBase.instr_counter