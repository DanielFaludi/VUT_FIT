#!/usr/bin/python3

class Frame(object):
    """Base class for every frame"""

    def __init__(self):
        self.frame = []

    def __contains__(self, searched_item):
        """Allows a call of 'in' operator on this object"""

        if len(self.frame) == 0:
            return False

        for item_dict in self.frame:
            for item_name in item_dict.keys():
                if searched_item == item_name:
                    return True
        return False

    def __len__(self):
        """Allows a call of 'len()' on this object"""

        return len(self.frame)

    def __bool__(self):
        if self.frame is None:
            return False
        return True

    def __str__(self):
        """Printable representation of this object"""

        content = []
        for item in self.frame:
            for var, var_t in item.items():
                for value in var_t.values():
                    for val, val_t in value.items():
                        content.append("{} -> value: {} type: {}".format(var, val, val_t).encode('unicode_escape').decode('utf-8'))
        
        return str.join('\n', content)

    def print_dict(self):
        """Prints a dictionary of items in a frame"""

        for item in self.frame:
            print(item)

    def append(self, item):
        """Append item to a frame"""

        self.frame.append(item)

    def redef(self, searched_var):
        """Redefine a variable"""

        for item in self.frame:
            for var in item.keys():
                if var == searched_var:
                    item[var] = {'value':{None:None}}
    
    def update(self, searched_var, value, value_t):
        """Update the value and/or type of a variable in frame"""

        for item in self.frame:
            for var in item.keys():
                if var == searched_var:
                    item[var] = {'value':{value:value_t}}

    def get_val(self, searched_var):
        """Get value of a variable in frame"""

        for item in self.frame:
            for var in item.keys():
                if var == searched_var:
                    for v in item[var].values():
                        for val, val_t in v.items():
                            return (val, val_t)


class GlobalFrame(Frame):

    def __init__(self):
        super().__init__()

class TemporaryFrame(Frame):

    def __init__(self):
        super().__init__()
        self.frame = None

    def __str__(self):
        if self.frame is None:
            return ''
        
        content = []
        for item in self.frame:
            for var, var_t in item.items():
                for value in var_t.values():
                    for val, val_t in value.items():
                        content.append("{} -> value: {} type: {}".format(var, val, val_t))
        
        return str.join('\n', content)

    def init_frame(self):
        self.frame = []
    
    def f_pop(self):
        """Pops the whole temporary frame"""

        retval = self.frame
        self.frame = None
        return retval
    
    def push(self, item):
        """Appends item to the end of temporary frame"""

        if self.frame is None:
            self.init_frame()
        self.frame = []
        for i in item:
            self.frame.append(i)

class LocalFrame(Frame):

    def __init__(self):
        super().__init__()
        self.frame = None

    def __contains__(self, searched_item):
        if len(self.frame) == 0:
            return False

        for item_dict in self.frame[-1]:
            for item_name in item_dict.keys():
                if searched_item == item_name:
                    return True
        return False

    def __str__(self):
        if self.frame is None:
            return ''

        content = []
        for top_item in self.frame:
            for item in top_item:
                for var, var_t in item.items():
                    for value in var_t.values():
                        for val, val_t in value.items():
                            content.append("{} -> value: {} type: {}".format(var, val, val_t))
        
        return str.join('\n', content)

    def init_frame(self):
        self.frame = []

    def push(self, item):
        """Appends item to a local frame"""

        if isinstance(item, list):
            self.frame.append(item)
        else:
            print('Cannot push non-list objects')
    
    def f_pop(self):
        """Pops from top of a local frame"""

        retval = self.frame.pop(-1)
        if not self.frame:
            self.frame = None
        
        return retval

    def update(self, searched_var, value, value_t):
        """Updates a variable in a local frame"""

        for item in self.frame[-1]:
            for var in item.keys():
                    if var == searched_var:
                        item[var] = {'value':{value:value_t}}
    
    def get_val(self, searched_var):
        """Get value and type of a variable in a local frame"""

        for item in self.frame[-1]:
            for var in item.keys():
                if var == searched_var:
                    for v in item[var].values():
                        for val, val_t in v.items():
                            return (val, val_t)
            