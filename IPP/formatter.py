#!/usr/bin/python3

# Should be working correctly

from collections import OrderedDict, defaultdict

class XMLFormatter(object):
    """Analyzes XML file, in case of wrong format returns appropriate return value (error code)"""

    def __init__(self, root):
        self.root = root

    def run(self):
        """
        Main function of XMLFormatter, checks XML format, outputs dictionary representation

        :rtype: dictionary representation of XML source file
        """

        if self.root.tag != 'program':
            return 31
        
        for lang, value in self.root.attrib.items():
            if lang != 'language':
                return 31
            if value != 'IPPcode19':
                return 31

        order_check = []
        instructions = {}
        for child in self.root:
            arg_count = 0
            arg_dict = {}
            if not self.correct_child_node_format(child):
                return 31
            if int(child.attrib['order']) in order_check: # Check for duplicate instruction
                return 31
            order_check.append(int(child.attrib['order']))
            for arg in child:
                arg_count += 1
                if not self.correct_arg_node_format(arg):
                    return 31
                arg_dict[arg_count] = {arg.text:arg.attrib}
            instructions[child.attrib['order']] = {child.attrib['opcode']:arg_dict}

        instructions = OrderedDict(sorted(instructions.items(), key=lambda x: int(x[0])))
        order_list = list(instructions.keys())
        if not self.correct_sequence(order_list):
            return 31
        return instructions

    def correct_sequence(self, order_list):
        """
        Checks order sequence for missing indices

        :param order_list: Order sequence
        :rtype: bool
        """
        
        order_list = list(map(int, order_list)) # Convert list of strings to list of ints
        check = sum(range(order_list[0],order_list[-1]+1)) - sum(order_list) # Check for missing (or duplicate) number

        if(check == 0):
            return True
        return False
    
    def correct_child_node_format(self, child):
        """
        Checks if instruction node is in correct format

        :param child: instruction node
        :rtype: bool
        """

        if child.tag != 'instruction':
            return False

        for attrib_1, attrib_2 in child.items():
            if attrib_1 == 'order':
                try:
                    isinstance(int(attrib_2), int)
                except ValueError:
                    return False
            elif attrib_1 == 'opcode':
                try:
                    isinstance(attrib_2, str)
                except ValueError:
                    return False
            else:
                return False
        
        return True

    def correct_arg_node_format(self, arg):
        """
        Checks if argument node is in correct format

        :param child: argument node
        :rtype: bool
        """

        arg_strings = ['arg1', 'arg2', 'arg3']

        if arg.tag not in arg_strings:
            return False

        for a in arg.keys():
            if a != 'type':
                return False

        return True