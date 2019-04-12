#!/usr/bin/python3

# Author: Daniel Faludi
# IPP Project 2 - interpret.py

import sys
import logging
import argparse
import xml.etree.ElementTree as ElementTree

from codexec import Execute
from analyze import Analyzer
from formatter import XMLFormatter
from instructionset import InstructionSet

def main():
    """
    Main function of interpreter, loads arguments, calls syntax and lexical
    analysis and code executer
    """

    parser = argparse.ArgumentParser() # Argument loading and processing
    parser.add_argument('--source', help='Specify source XML file')
    parser.add_argument('--input', help='Specify input file')
    
    args = parser.parse_args()

    if not (args.source or args.input):
        parser.error("Atleast one argument is required")
        sys.exit(31)

    if args.source:
        xml_arg = args.source
    else:
        xml_arg = sys.stdin

    if args.input:
        input_arg = args.input
    else:
        input_arg = sys.stdin

    try:
        root = ElementTree.parse(xml_arg).getroot() # Load XML file
    except ElementTree.ParseError:
        sys.exit(31)
    except FileNotFoundError:
        sys.exit(31)

    format_xml = XMLFormatter(root) # Check if XML is in correct format
    instr_set = format_xml.run()

    if(isinstance(instr_set, int)):
        sys.exit(instr_set)

    analyzer = Analyzer(instr_set) # Check if code represented by XML is lexically and syntactically correct
    analyzed_xml = analyzer.run()

    if(analyzed_xml != 0):
        sys.exit(analyzed_xml)

    i_set = InstructionSet() # Create instruction set from XML
    i_set.instr_set = instr_set

    retval = Execute(i_set, input_arg).run() # Run code
    if(retval > 51):
        sys.exit(retval)

    return retval
    
if __name__ == '__main__':
    main()
