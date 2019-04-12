# Implementační dokumentace k 2. úloze do IPP 2018/2019<br> Jméno a přijímení : Daniel Faludi<br> Login: xfalud00

## `interpret.py`
This is a main module of an IPP interpreter, it loads and processes arguments and a XML representation of IPP code. This module calls `formatter` module to check if given XML is in correct format and after determining that it is, it calls `analyze` module to check if the code represented by the XML is lexically and syntactically valid. If an XML file passes both of these controls, the code inside is then executed by the `codexec` module.

## `formatter.py`
Checks if given XML file is in correct format, meaning, it checks if the instruction tags are valid and if their arguments are valid. If the instructions in XML file are not in correct order, it sorts them in an ascending order.

## `analyze.py`
Checks if code represented by an XML file is lexically and syntactically valid. It relies on heavy use of regular expressions.

## `codexec.py`
This module executes each instruction in an XML representation of IPPCode19. It is implemented by a while loop that is iterated by an instruction pointer. 
> Instruction pointer is implemented in `instruction.py`

Every instruction is implemented as a class which extends the base instruction class implemented in `instruction.py`. This way every instruction has access to instruction pointer and memory model.

## Instructions

Since the instruction set is a complex dictionary and accessing it's keys and values is not very simple, each instruction is implemented as a class with main method *execute()* and methods for unpacking arguments from the dictionary and performing necessary semantic checks. Some groups of instructions also extend their specific base class (for example *arithmeticops*). This way each child object shares these auxiliary methods which are implemented in the parent object. This was done to prevent a duplication of code.

## Memory Model

Each frame is implemented as a class which extends the `Frame` base class. The logic behind implementation of memory model is very similar to the one behind implementation of instruction classes. The main difference here is the heavy use of *double underscore* methods. These methods allow/modify the behavior of some keyword functions/operations used on these objects. For example by implementing a method `__contains__()` in `Frame` class, it is now possible to call the `in` operator on objects of type `Frame`. This greatly improves the ease of use of these objects, and further simplifies the code.
