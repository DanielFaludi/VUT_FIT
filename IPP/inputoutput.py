#!/usr/bin/python3

import re
import sys

from instruction import InstructionBase

class Read(InstructionBase):
    """READ instruction"""

    pos = 0 # Position in the input file (if specified)

    def __init__(self, params, input_f):
        super().__init__()
        self.ip_increment()
        self.input_f = input_f
        self.var = list(params.values())[0]
        self.a_type = list(params.values())[1]
        for variable in self.var.keys():
            self.frame, self.var_name = variable.split('@')

    def execute(self):
        """Executes READ instruction"""

        self.a_type = self.unpack_type()
        if isinstance(self.input_f, str):
            try:
                with open(self.input_f) as f:
                    f.seek(Read.pos)
                    x = f.readline().strip()
                    Read.pos = f.tell()
            except FileNotFoundError:
                return 32
        else:
            x = input('Enter value: ')
        
        if self.a_type == 'int':
            try:
                result = int(x)
            except ValueError:
                result = 0
        elif self.a_type == 'string':
            try:
                result = str(x)
            except ValueError:
                result = '0'
        else:
            if x.lower() == 'true':
                result = 'true'
            else:
                result = 'false'
        
        self.frame_dict[self.frame].update(self.var_name, result, self.a_type)

        return 0

    def unpack_type(self):
        for a_type in self.a_type.keys():
            return a_type

class Write(InstructionBase):
    """WRITE instruction"""

    def __init__(self, params):
        super().__init__()
        self.ip_increment()
        self.symb = list(params.values())[0]

    def execute(self):
        """Executes WRITE instruction"""

        symbol = self.unpack_symb()
        
        if symbol[1] == 'string':
            result = self.format_string(symbol[0])
            print(result, end='')
        else:
            print(symbol[0], end='')

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

    def format_string(self, string):
        """
        Converts special charatecters in a string to their real format

        :param string: string with special characters
        :rtype string: string with converted special characters
        """
        
        special_chars = []
        p = re.compile(r'(\\[0-9]{3})')
        for m in p.finditer(string):
            special_chars.append(m.group())
        
        for i, char in enumerate(special_chars):
            special_chars[i] = re.sub(r'(^\\0*)', '', char)
            
        for char in special_chars:
            replacement = chr(int(char))
            string = re.sub(r'(\\[0-9]{3})', replacement, string, 1)

        return string