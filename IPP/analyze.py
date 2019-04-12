#!/usr/bin/python3

# This wasn't tested at all, it's possible that this has many issues

import re

class Analyzer(object):
    """
    Analyzes dictionary created from source XML and throws appropriate errors in case 
    of lexical or syntactic error
    """

    def __init__(self, xml_dict):
        self.xml_dict = xml_dict

    def run(self):
        """
        Main function of Analyzer
        """

        for instr in self.xml_dict.values():
            for opcode, arg in instr.items():
                if not self.opcode_switch(opcode, arg):
                    return 32 

        return 0
                
    def opcode_switch(self, opcode, arg):
        """
        Uses dictionary as a switch statement, calls methods for syntactic and lexical analysis

        :param opcode: opcode in XML source file
        :param arg: arguments of opcode
        :rtype: bool
        """

        opcode_switch_dict = {
            'MOVE' : self.var_symb_syntax,
            'STRLEN' : self.var_symb_syntax,
            'TYPE' : self.var_symb_syntax,
            'INT2CHAR' : self.var_symb_syntax,
            'NOT' : self.var_symb_syntax,
            'DEFVAR' : self.one_var_syntax,
            'POPS' : self.one_var_syntax,
            'PUSHS' : self.one_symb_syntax,
            'WRITE' : self.one_symb_syntax,
            'DPRINT' : self.one_symb_syntax,
            'EXIT' : self.one_symb_syntax,
            'ADD' : self.var_symb_symb_syntax,
            'SUB' : self.var_symb_symb_syntax,
            'MUL' : self.var_symb_symb_syntax,
            'IDIV' : self.var_symb_symb_syntax,
            'LT' : self.var_symb_symb_syntax,
            'GT' : self.var_symb_symb_syntax,
            'EQ' : self.var_symb_symb_syntax,
            'AND' : self.var_symb_symb_syntax,
            'OR' : self.var_symb_symb_syntax,
            'CONCAT' : self.var_symb_symb_syntax,
            'GETCHAR' : self.var_symb_symb_syntax,
            'SETCHAR' : self.var_symb_symb_syntax,
            'STRI2INT' : self.var_symb_symb_syntax,
            'CALL' : self.label_instr_syntax,
            'LABEL' : self.label_instr_syntax,
            'JUMP' : self.label_instr_syntax,
            'CREATEFRAME' : self.no_arg_instr_syntax,
            'PUSHFRAME' : self.no_arg_instr_syntax,
            'POPFRAME' : self.no_arg_instr_syntax,
            'RETURN' : self.no_arg_instr_syntax,
            'BREAK' : self.no_arg_instr_syntax,
            'JUMPIFEQ' : self.cond_jump_syntax,
            'JUMPIFNEQ' : self.cond_jump_syntax,
            'READ' : self.read_syntax
        }

        if opcode not in opcode_switch_dict.keys():
            return False

        result = opcode_switch_dict[opcode](arg)
        if not result:
            return False

        return True

    def known_type(self, arg_type):
        """
        Checks if given argument type is lexically valid (or is an existing type)

        :param arg_type: argument type
        :rtype: bool
        """

        type_list = [
            'string',
            'bool',
            'nil',
            'int',
            'var',
            'label'
        ]

        if arg_type not in type_list:
            return False
        return True

    def correct_string(self, argument):
        """
        Checks if given string argument is lexically valid

        :param argument: string to check
        :rtype: bool
        """

        argument = re.sub(r'(\\[0-9]{3})', '', argument) # Remove special chars
        check = re.search(r'(\\)|(#)|(\s+)', argument)

        if check is not None:
            return False
        return True

    def correct_int(self, argument):
        """
        Checks if given string argument is lexically valid

        :param argument: string to check
        :rtype: bool
        """

        check = re.match(r"^(\+?|\-?)[0-9]+$", argument)

        if check is None:
            return False
        return True

    def correct_bool(self, argument):
        """
        Checks if given ipp_bool argument is lexically valid

        :param argument: ipp_bool to check
        :rtype: bool
        """

        check = re.match(r"^(true)|(false)$", argument)

        if check is None:
            return False
        return True

    def correct_var(self, argument):
        """
        Checks if given variable argument is lexically valid

        :param argument: var to check
        :rtype: bool
        """

        check = re.match(r"^((?:GF|LF|TF))(@)((?![0-9])[a-zA-Z0-9\!\_\-\$\%\&\*\?]+)$", argument)

        if check is None:
            return False
        return True

    def correct_label(self, argument):
        """
        Checks if given label argument is lexically valid

        :param argument: label to check
        :rtype: bool
        """

        check = re.match(r"^(?![0-9])([a-zA-Z0-9\_\!\$\%\&\*\?]+)$", argument)

        if check is None:
            return False
        return True

    def correct_nil(self, argument):
        """
        Checks if given nil argument is lexically valid

        :param argument: nil to check
        :rtype: bool
        """

        check = re.match(r"^(nil@nil)$", argument)

        if check is None:
            return False
        return True

    def correct_type(self, argument):
        """
        Checks if given type argument is lexically valid

        :param argument: type to check
        :rtype: bool
        """

        check = re.match(r"^(string)|(int)|(bool)$", argument)

        if check is None:
            return False
        return True

    def one_symb_syntax(self, arg):
        """
        Check if instruction with one <symb> argument is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 1:
            return False

        symb = list(arg.values())[0]

        type_check = {
            'var' : self.correct_var,
            'int' : self.correct_int,
            'bool' : self.correct_bool,
            'string' : self.correct_string,
            'nil' : self.correct_nil,
            'label' : self.correct_label,
        }

        for symb_name, symb_type in symb.items():
            if symb_type['type'] == 'label':
                return False
            elif not type_check[symb_type['type']](symb_name): 
                return False

        return True

    def one_var_syntax(self, arg):
        if len(arg) != 1:
            return False

        var = list(arg.values())[0]

        for var_name, var_type in var.items():
            if var_type['type'] != 'var':
                return False
            elif not self.correct_var(var_name):
                return False

        return True

    def cond_jump_syntax(self, arg):
        """
        Check if conditional jump instruction is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 3:
            return False

        label = list(arg.values())[0]
        symb1 = list(arg.values())[1]
        symb2 = list(arg.values())[2]

        for a, a_type in label.items():
            label, label_type = a, a_type['type']
        
        for a, a_type in symb1.items():
            symb1, symb1_type = a, a_type['type']
        
        for a, a_type in symb2.items():
            symb2, symb2_type = a, a_type['type']

        type_check = {
            'var' : self.correct_var,
            'int' : self.correct_int,
            'bool' : self.correct_int,
            'string' : self.correct_string,
            'nil' : self.correct_nil,
            'label' : self.correct_label,
        }

        if label_type != 'label':
            return False
        else:
            if not type_check[label_type](label):
                return False

        if symb1_type == 'label':
            return False
        else:
            if not type_check[symb1_type](symb1):
                return False
        
        if symb2_type == 'label':
            return False
        else:
            if not type_check[symb2_type](symb2):
                return False

        return True


    def var_symb_syntax(self, arg):
        """
        Check if instruction with one <symb> and one <var> argument is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 2:
            return False

        var = list(arg.values())[0]
        symb = list(arg.values())[1]

        for a, a_type in var.items():
            var, var_type = a, a_type['type']
        
        for a, a_type in symb.items():
            symb, symb_type = a, a_type['type']
        

        type_check = {
            'var' : self.correct_var,
            'int' : self.correct_int,
            'bool' : self.correct_bool,
            'string' : self.correct_string,
            'nil' : self.correct_nil,
            'label' : self.correct_label,
        }

        if var_type != 'var':
            return False
        else:
            if not type_check[var_type](var):
                return False

        if symb_type == 'label':
            return False
        else:
            if not type_check[symb_type](symb):
                return False

        return True
                
    def var_symb_symb_syntax(self, arg):
        """
        Check if instruction with two <symb> and one <var> arguments is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 3:
            return False

        var = list(arg.values())[0]
        symb1 = list(arg.values())[1]
        symb2 = list(arg.values())[2]

        for a, a_type in var.items():
            var, var_type = a, a_type['type']
        
        for a, a_type in symb1.items():
            symb1, symb1_type = a, a_type['type']
        
        for a, a_type in symb2.items():
            symb2, symb2_type = a, a_type['type']

        type_check = {
            'var' : self.correct_var,
            'int' : self.correct_int,
            'bool' : self.correct_bool,
            'string' : self.correct_string,
            'nil' : self.correct_nil,
            'label' : self.correct_label,
        }

        if var_type != 'var':
            return False
        else:
            if not type_check[var_type](var):
                return False

        if symb1_type == 'label':
            return False
        else:
            if not type_check[symb1_type](symb1):
                return False
        
        if symb2_type == 'label':
            return False
        else:
            if not type_check[symb2_type](symb2):
                return False

        return True

    def label_instr_syntax(self, arg):
        """
        Check if label instruction is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 1:
            return False

        label = list(arg.values())[0]

        for label_name, label_type in label.items():
            if label_type['type'] != 'label':
                return False
            elif not self.correct_label(label_name):
                return False
        
        return True

    def no_arg_instr_syntax(self, arg):
        """
        Check if instruction with no arguments is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 0:
            return False

        return True
    
    def read_syntax(self, arg):
        """
        Check if read instruction is syntactically valid

        :param arg: arguments to check (list)
        :rtype: bool
        """

        if len(arg) != 2:
            return False

        var = list(arg.values())[0]
        t_type = list(arg.values())[1]

        for a, a_type in var.items():
            var, var_type = a, a_type['type']
        
        for a, a_type in t_type.items():
            t_type, t_type_type = a, a_type['type']
        
        if var_type != 'var':
            return False
        else:
            if not self.correct_var(var):
                return False
        
        if t_type_type == 'type':
            if not self.correct_type(t_type):
                return False
        else:
            return False

        return True