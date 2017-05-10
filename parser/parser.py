#!/usr/bin/python3


import os.path
import os
import re
import argparse
import sys
import subprocess

import SourceIterators

from ConsoleStreamReporter import ConsoleStreamReporter
from Position import Position, NoPosition

from tokens import *


#? Could use reporter anyway?
def printMessage(msg):
    print(msg)

def printInfo(msg):
    print('[info] {0}'.format(msg))

def printError(msg):
    print('[error] {0}'.format(msg))    




class Parser:
    '''
    '''
    def __init__(self, it, reporter):
        self.it = it
        self.reporter = reporter
        self.prevLineNo = 1
        self.prevIndent = 0
        self.indent = 0
        self.line = ''
        # store for split lines
        self.splitLine = []
        # ...prime
        self._next()
        # let's go
        self.root()


    def error(self, rule, msg, withPosition):
        pos = Position(self.it.src, self.prevLineNo, 0) if withPosition else NoPosition 
        self.reporter.error(rule + ':' + msg, pos)

    def warning(self, msg, withPosition):
        pos = Position(self.it.src, self.prevLineNo, 0) if withPosition else NoPosition 
        self.reporter.warning(msg, pos)

    def info(self, msg, withPosition):
        pos = Position(self.it.src, self.prevLineNo, 0) if withPosition else NoPosition 
        self.reporter.info(msg, pos)

    def expectedError(self, msg):
        self.error("Expected {0} but found '{1}'".format(msg, tokenToString[self.tok]), True)

    def _next(self):
        self.prevLineNo = self.it.lineCount
        self.prevIndent = self.indent
        self.indent, self.line = self.it.__next__()

    def indentIncreased(self):
        #print('indentIncreased :' + str(self.prevIndent) + '-' + str(self.indent) )
        return self.indent > self.prevIndent
        
    def indentHeld(self):
        print('indentHeld :' + str(self.prevIndent) + '-' + str(self.indent) )
        return self.indent >= self.prevIndent





    def commentCB(self, text):
        print('comment...')
        print('"' + text + '"')

    def comment(self):
        commit = (self.line[0] == "#")
        if(commit):
          if(len(self.line) > 1 and self.line[1] == "#"):
            #multiline
            txt = self.line[2:].lstrip()
            self._next()
            while(self.line[0] != '#'):
              txt += self.line
              self._next()
          else:
            # singleline
            txt = self.line[1:].strip()
          self.commentCB(txt)
          self._next()
        return commit 
        



    def unbracketedParam(self):
        print('unbracketedParam params...')
        #commit = (self.value())
        #return commit

    def namedParameterCB(self, name, value):
      print('namedParameter...')
      print(name + ':' +value)
            
    def functionNameCB(self, name):
      print('function name...')
      print(name)
      
    def namedParameter(self):
      p = self.line.split()
      name = p[0][1:]
      if (len(p) < 2):
        self.namedParameterCB(name, '')
      else:
        self.namedParameterCB(name, p[1])
      self._next()
      

    def namedParameters(self):
      while(self.line[0] == ':'):
        self.namedParameter()

    def instructionCB(self, cmd, params):
      print('ins...')
      print(cmd)
            
    #?
    def splitAndTest(self, ruleName, expectedItemCount):
      self.splitLine = self.line.split()
      if (len(self.splitLine) != expectedItemCount):
        self.error(ruleName, 'Expected different count of items : count: ' + str(expectedItemCount), True)
        
    #?  
    def assertSplitLineElement(self,  ruleName, idx, e):
      if(self.splitLine[idx] != e):
        #! sort offset
        self.error('{0} : Expected element: {1}'.format(ruleName, e), True)
        #! StopIteration
      
    def simultaneousInstructionsOpenCB(self):
      print('  simultaneousInstructions open...')
      pass      

    def simultaneousInstructionsCloseCB(self):
      print('  simultaneousInstructions close...')
      pass  
            
    def simultaneousInstructions(self):
      commit = (self.line[0] == '<' and self.line[1] == '<')
      if (commit):
        self.simultaneousInstructionsOpenCB()
        self._next()
        while(True):
          #! some form of body (accepts instructions)
          self.plainInstruction()
          if(not self.indentHeld()):
            break
        self.simultaneousInstructionsCloseCB()
      return commit
      
    def plainInstruction(self):
      commit = self.line[0].isalpha()
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.instructionCB(p, [])
        else:
          self.instructionCB(p, p[1:])
        self._next()
      return commit

    def functionBodyOpenCB(self):
      print('  functionBody open...')
      pass      

    def functionBodyCloseCB(self):
      print('  functionBody close...')
      pass        
      
    def functionBody(self):
      if (self.indentIncreased()):
        self.functionBodyOpenCB()             
        baseIndent = self.indent
        while (True):
          (
          self.simultaneousInstructions()
          or self.function()
          or self.comment()
          or self.plainInstruction()
          )
          if (self.indent < baseIndent):
            break
        self.functionBodyCloseCB()             


        
        
    def function(self):
        commit = (self.line[0] == '\\')
        if(commit):
            if (len(self.line) < 2):
              self.error('function', 'Expected characters', True)
            else:
              name = self.line[1:].rstrip()
              self.functionNameCB(name)
              
              self._next()
              
              if (self.line[0] == ':'):
                  self.namedParameters()
                  
              #print('function2...' + str(self.indentIncreased()))
              #! ah, but the parameters would have stepped on?
              self.functionBody()
            
        return commit

    def variableNameCB(self, name):
      print('variable name...')
      print(name)      
      
    def variable(self):
      commit = (self.line[0] == '=')
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.error('variable', 'Expected name to assign to?', True)
        self.variableNameCB(p[1])
        self._next()
        #! now, e.g. parameters, ins, etc?
        if (not (
          self.function()
          or self.simultaneousInstructions()
          or self.comment()
          #! but this accepts near anything?
          #! also, block of these useful
          or self.plainInstruction()
        )):
          self.error('variable', 'Variable must contain an understandable unit of code, currently one of a function, plain instruction, simultaneous instructions, or a comment', True)
      return commit
              
    def rootSeq(self):
        while(
          self.comment()
          or self.function()
          # this last. Has no intro chars, reacts to any line
          or self.variable()
          #or self.block()
        ):
          pass

    def root(self):
        try:
            self.rootSeq()
            #self.seqContents(self.treeRoot.body)
            # if we don't except on StopIteration...
            self.error('parser', 'Parsing did not complete, stopped here?', True)
        except StopIteration:
            # All ok
            pass




def parse(srcAsLines):
    #print(srcAsLines)
    r = ConsoleStreamReporter()
    it = SourceIterators.StringIterator(srcAsLines)
    Parser(it, r)



def main(argv):
    parser = argparse.ArgumentParser(
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
                
    parser.add_argument("-s", "--solo", 
        default='all',
        help="Generate code for one dancer only, by index or name."
        )

    parser.add_argument("-t", "--tween", 
        default=False,
        help="Generate a limited set of tween frames for instructions marked as animated."
        )
                
    parser.add_argument("-o", "--outfile", 
        default='',
        help="file path for output"
        )
        
    parser.add_argument("infile", 
        default='in.dn',
        help="file for input"
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
    print ('outfile:' + str(args.outfile))
    print ('\n')
    
    
    
    #try:


    # do something
    with open(args.infile, 'r', encoding=args.codec) as f:
        srcAsLines = f.readlines()


    parse(srcAsLines)

    printInfo("written final 'dnc' file: path: {0}".format(args.outfile))

    #with open(args.outfile, 'w', encoding=args.codec) as f:
        #f.write(parser.result())

    #except Exception as e:
     #   print('Error: most errors are caused by wrong format for source. Other errors from malformed files?\n{0}'.format(e))
        
        
if __name__ == "__main__":
        main(sys.argv[1:])
