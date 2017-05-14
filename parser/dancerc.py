#!/usr/bin/python3


import os.path
import os
import argparse
import sys

import SourceIterators
import ExpandIterator
import MetaAssertIterator

from ConsoleStreamReporter import ConsoleStreamReporter
from JSON import JSONPrintGenerator
from Python import PythonParser

#? No warnings?
#? use reporter?
def printMessage(msg):
    print(msg)

def printInfo(msg):
    print('[info] {0}'.format(msg))

def printError(msg):
    print('[error] {0}'.format(msg))    



def parse(srcAsLines, args):
    r = ConsoleStreamReporter()
    sit = SourceIterators.StringIterator(args.infile, srcAsLines)
    #it = MetaAssertIterator.MetaAssertIterator(sit, r)
    it = ExpandIterator.ExpandIterator(sit, r)
    #Parser(it, r)
    parseType = args.parser
    if (parseType ==  'JSON'):
      p = JSONPrintGenerator(it, r)
      p.parse()
      print('output:')
      print(''.join(p.result())) 

    if (parseType ==  'Bytecode'):
      print('Not enabled. Help!') 
      
    print(r.summaryString())

def writeOutputFile(args):
    with open(args.outfile, 'w', encoding=args.codec) as f:
        f.write()
    printInfo("written final 'dnc' file: {0}".format(args.outfile))
   
def openOutputFile(args):
  pass

def writeLine(args):
  pass  

def closeOutputFile(args):
  pass
         
def main(argv):
    parser = argparse.ArgumentParser(
        prog='dancerc'
        #epilog= "NB: keynames in the internal 'stanza' variable must be adjusted to match input files"
        )


    parser.add_argument("-c", "--codec",
        default='UTF-8',
        help="encoding of source file."
        )

    parser.add_argument("-e", "--expand-repeats", 
        default='all',
        help="Expand all repeated code, including code marked for visual repeats only."
        )

    parser.add_argument("-i", "--interlace-dancers", 
        default='all',
        help="Add marks for the dancer, reconstucting the instructions by beat"
        )
        
    parser.add_argument('-p', '--parser', 
        default='JSON',
        #type=string, 
        choices=('JSON', 'Bytecode')
        )
       
    parser.add_argument("-s", "--solo", 
        default='all',
        help="Generate code for one dancer only, by index or name."
        )

    parser.add_argument("-t", "--tween", 
        help="Generate a limited set of tween frames for instructions marked as animated.",
        action="store_true"
        )
                
    parser.add_argument("-o", "--outfile", 
        default='',
        help="File path for output"
        )
        
    parser.add_argument( "--comments", 
        help="Pass comments through to output",
        action="store_true"
        )
        
    parser.add_argument("infile", 
        default='in.dn',
        help="File for input"
        )
                
    args = parser.parse_args()

    # assert infile as absolute path
    args.infile = os.path.abspath(args.infile)

    f = args.infile
    if (not os.path.exists(f)):
        printError('Path not exists path: {0}'.format(f))
        return 1
        
    if (os.path.isdir(f)):
        printError('Path is dir path: {0}'.format(f))
        return 1

    # set output directory to inFile directory            
    (args.workingDir, name) = os.path.split(args.infile)
    
    # baseName is everything to the dot separator for extension, if it exists
    idx = name.find('.')
    args.baseName = name if(idx == -1) else name[0:idx]
 


    # if no outfile, invent one
    if (not args.outfile):
        args.outfile = os.path.join(args.workingDir, '{0}.dnc'.format(args.baseName))

    print ('infile:' + str(args.infile))
    print ('workingDir:' + str(args.workingDir))
    print ('baseName:' + str(args.baseName))
    print ('codec:' + str(args.codec))
    print ('parser:' + str(args.parser))
    print ('outfile:' + str(args.outfile))
    print ('comments:' + str(args.comments))

    print ('\n')
    
    
    
    #try:


    # do something
    with open(args.infile, 'r', encoding=args.codec) as f:
        srcAsLines = f.readlines()


    parse(srcAsLines, args)



    #except Exception as e:
     #   print('Error: most errors are caused by wrong format for source. Other errors from malformed files?\n{0}'.format(e))
        
        
if __name__ == "__main__":
        main(sys.argv[1:])
