#!/usr/bin/python3

class InstructionSet(object):
    """
    Creates instruction set
    """

    instr_set = dict()
    labels = list()

    def get_set(self):
        """
        Returns instruction set
        
        :rtype dictionary: dictionary representation of instruction set
        """

        return self.instr_set

    def find_labels(self):
        """
        Finds labels and saves their position
        """

        for order, instr in self.instr_set.items():
            for opcode, args in instr.items():
                if opcode == 'LABEL':
                    arg = list(args.values())[0]
                    for l_name, l_type in arg.items():
                        if l_type['type'] == 'label':
                            self.labels.append({order:l_name})
        
        return 0
    
    def get_labels(self):
        return self.labels