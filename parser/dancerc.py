#!/usr/bin/python3


import os.path
import os
import argparse
import sys

import SourceIterators
import EventIterators
import ExpandIterator

from ConsoleStreamReporter import ConsoleStreamReporter
import chains

from contexts import GlobalContext



#from JSON import JSONPrintGenerator
#from Python import PythonBuilder
from parser import Parser
#from Phases import *

#? No warnings?
#? use reporter?
def printMessage(msg):
    print(msg)

def printInfo(msg):
    print('[info] {0}'.format(msg))

def printError(msg):
    print('[error] {0}'.format(msg))    



def getContextData(args, reporter):
  inPath = args.infile
  if (inPath.endswith('.dnc')):
    #assuming a compiled event file
    ctx = GlobalContext()
    it = EventIterators.EventIteratorFile(args.infile)
    ctx.prepareForEventSteamData(it)
    return ctx
    
  elif (inPath.endswith('.dn')):
    # assuming a parsable Dancer file
    with open(inPath, 'r', encoding=args.codec) as f:
      srcAsLines = f.readlines()
    #! Needs a concept and so tidy-up. this is no good.
    #? maybe better with SourceIteratorFile
    #? build ExpandIterator in? To parser? 
    sit = SourceIterators.StringIterator(args.infile, srcAsLines)
    it = ExpandIterator.ExpandIterator(sit, reporter)
    #? Parser not here, it's irrelevant. Build into GlobalContext?
    p = Parser(it, reporter)
    p.parse()
    ctx = p.ast()
    ctx.prepareAsParsedData(inPath)
    return ctx

  else:
    printError("file has no dancer extension ('.dnc', '.dn'): {0}".format(infile))


def doSomething(args):
    r = ConsoleStreamReporter()
    ctx = getContextData(args, r)
    
    if (args.print):
      ctx.setChainAs(chains.EventsToConsole)
      ctx.runProcessChain()
    else:
      form = args.format
      
      if (form == 'events'):
        args.outfile = args.outfile + '.dnc'
        ctx.mergeProperty('outfile', args.outfile)
        ctx.setChainAs(chains.EventsToFile)
        ctx.runProcessChain()
  
      if (form == 'json'):
        args.outfile = args.outfile + '.json'
        #p = JSONPrintGenerator(it, r)
        #p.parse()
        #print('output:')
        #print(''.join(p.result())) 
        print('JSON Not enabled. Help!') 
  
      if (form == 'bytecode'):
        args.outfile = args.outfile + '.dnbc'
        print('bytecode Not enabled. Help!') 

      if (form == 'pdf'):
        #ctx.prepareDispatchers()

        print('pdf Not enabled. Help!') 
        
      printInfo('written: {0}'.format(args.outfile))
    print(r.summaryString())



         
def main(argv):
    parser = argparse.ArgumentParser(
        prog='dancerc'
        #epilog= "NB: keynames in the internal 'stanza' variable must be adjusted to match input files"
        )

    parser.add_argument("-b", "--beat-assert", 
        help="Reconstucting the events for every beat.",
        action="store_true"
        )
        
    parser.add_argument("-c", "--codec",
        default='UTF-8',
        help="encoding of source file."
        )

    parser.add_argument("-e", "--expand-repeats", 
        help="Expand all repeated code, including code marked for visual repeats only.",
        action="store_true"
        )
        
    parser.add_argument('-f', '--format', 
        help="Output format. 'events' is the default, a compiled input.",
        default='events',
        choices=('events', 'json', 'bytecode', 'pdf')
        )

    parser.add_argument('-p', '--print',
        help="Print the event queue to the console. Overrides -f.",
        action="store_true"
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
        args.outfile = os.path.join(args.workingDir, '{0}'.format(args.baseName))

    print ('infile:' + str(args.infile))
    print ('workingDir:' + str(args.workingDir))
    print ('baseName:' + str(args.baseName))
    print ('codec:' + str(args.codec))
    print ('format:' + str(args.format))
    print ('print:' + str(args.print))
    print ('outfile:' + str(args.outfile))
    print ('comments:' + str(args.comments))

    print ('\n')
    
    
    
    #try:


    # do something

    doSomething(args)



    #except Exception as e:
     #   print('Error: most errors are caused by wrong format for source. Other errors from malformed files?\n{0}'.format(e))
        
        
if __name__ == "__main__":
        main(sys.argv[1:])
