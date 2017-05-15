#!/usr/bin/python3


import os.path
import os
import argparse
import sys

from Position import Position, NoPosition
from trees.Trees import *


#! not parsing positional parameters
#! need a resolverIterator to remove functions from instruction lists?
#! otheerwise they screw JSON representation, and maybe other bytecode?
#! scores cannot accept staffs as bodies. 
#! Positional, or named?
#! 
class Parser:
    '''
    '''
    V_INSTRUCTIONSEQ = 1
    V_FUNCTION = 2
    
    def __init__(self, it, reporter):
        self.it = it
        self.reporter = reporter
        
        self.tree = Root()

        #self._prevLineNo = 1
        self.line = ''
   
        # var data gathering
        self.currentVarName = ''
        self._stashVarLines = False
        self.varLineStash = []

        # namedParams gathering
        self.namedParamsStash = []
        
        # ...prime
        #self._next()
        # let's go
        #self.root()

    def parse(self):
        # ...prime
        self._next()
        # let's go
        self.root()
        
    def ast(self):
      return self.tree
      
    def error(self, rule, msg, withPosition):
        pos = Position(self.it.srcName, self.it.lineCount, 0) if withPosition else NoPosition 
        self.reporter.error(rule + ': ' + msg, pos)
        #? Might introduce some finness by allowing recovery sometimes?
        sys.exit(1)

    def warning(self, msg, withPosition):
        pos = Position(self.it.srcName, self.it.lineCount, 0) if withPosition else NoPosition 
        self.reporter.warning(msg, pos)

    def info(self, msg, withPosition):
        pos = Position(self.it.srcName, self.it.lineCount, 0) if withPosition else NoPosition 
        self.reporter.info(msg, pos)

    def expectedError(self, msg):
        self.error("Expected {0} but found '{1}'".format(msg, tokenToString[self.tok]), True)
      
    def _next(self):
        #self._prevLineNo = self.it.lineCount
        n = self.it.__next__()
        self.line = n
        if (self._stashVarLines):
          self.varLineStash.append(n)




    ## Callbacks ##

    def commentCB(self, text):
      #print('comment...')
      #print('"' + text + '"')
      pass

    # @posParams [param1, ...] @namedParams [[name, val],...]
    def functionCallOpenCB(self, name, posParams, namedParams):
      #print('functionCall...')
      #print(name + ':' + str(posParams) +str(namedParams))
      pass
      
    def functionCallCloseCB(self, name):
      #print('    functionCallCloseCB...')
      #print(name)
      pass

    def functionBodyOpenCB(self):
      #print('  functionBody open...')
      pass      

    def functionBodyCloseCB(self):
      #print('  functionBody close...')
      pass        

    def simultaneousFunctionBodyOpenCB(self):
      #print('  simultaneousFunctionBody open...')
      pass      

    def simultaneousFunctionBodyCloseCB(self):
      #print('  simultaneousFunctionBody close...')
      pass       
      
      
    def instructionCB(self, cmd, params):
      #print('ins...')
      #print(cmd)
      pass
      
    def simultaneousInstructionsOpenCB(self):
      #print('  simultaneousInstructions open...')
      pass      

    def simultaneousInstructionsCloseCB(self):
      #print('  simultaneousInstructions close...')
      pass  
            

    def variableOpenCB(self, name):
      #print('variable name...')
      #print(name)  
      pass    
            
    def variableCloseCB(self, tpe):
      #print('variable type...')
      #print(str(tpe))  
      pass 

         
         
         
                  
    ## Rules ##
    
    def comment(self):
        commit = (self.line[0] == "#")
        if(commit):
          txt = ''
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



    def namedParameters(self):
      self.namedParamsStash = []
      while(self.line[0] == ':'):
        p = self.line.split()
        name = p[0][1:]
        if (len(p) > 2):
            self.error('namedParameters', 'A parameter appears to have more than one value?', True)          
        if (len(p) < 2):
          self.namedParamsStash.append([name, ''])
        else:
          self.namedParamsStash.append([name, p[1]])
        self._next()



    def simultaneousInstructions(self, childList):
      commit = (self.line[0] == '<')
      if (commit):
        #print('simultaneousInstructions ' + str(self._prevLineNo))
        self.simultaneousInstructionsOpenCB()
        self._next()
        n = GenericSimultaneousInstruction()
        childList.append(n)
        while(self.line[0] != '>'):
          #! some form of body (accepts functions)
          #? but not simultaneousInstructions
          if(not(
            self.functionCall(n.children)
            or self.comment()
            or self.plainInstruction(n.children)
          )):
            self.error('simultaneousInstructions', 'Code line not recognised as a function, plain instruction, or a comment', True)


        self.simultaneousInstructionsCloseCB()
        self._next()
      return commit
      
    def plainInstruction(self, childList):
      commit = self.line[0].isalpha()
      if (commit):
        p = self.line.split()
        name = p[0]
        
        # split durations
        i = len(name) - 1
        while(i >= 0 and name[i].isdigit()):
          i -= 1
        if (i == -1):
          self.error('plainInstruction', 'An instruction name can not be all digits', True)
        i += 1
        
        # get name and duration values
        duration = name[i:]
        if (not duration):
          duration = 1
        name = name[:i]
        
        if (len(p) < 2):
          self.instructionCB(name, [])
          #print('ins' + p[0])
          childList.append(GenericInstruction(name, duration, []))
        else:
          self.instructionCB(p[0], p[1:])
          childList.append(GenericInstruction(name, duration, p[1:]))
        self._next()
      return commit


    def functionBody(self, childList):
      commit = (self.line[0] == '{')
      if (commit):
        #self.functionTreeNode()
        self.functionBodyOpenCB()
        self._next()
        
        #!? Why both instructions and instruction?
        while (True):
          if(not(
          self.simultaneousInstructions(childList)
          or self.functionCall(childList)
          or self.comment()
          or self.plainInstruction(childList)
          )):
            self.error('functionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)
          if (self.line[0] == '}'):
            break

        self.functionBodyCloseCB()             
        self._next()
      return commit
        
    def simultaneousFunctionBody(self, childList):
      commit = (
        len(self.line) > 1 
        and self.line[0] == '<' 
        and self.line[1] == '<'
      )
      
      if (commit):
        self.simultaneousFunctionBodyOpenCB()
        self._next()
        
        while (True):
          if(not(
            self.functionCall(childList)
            or self.comment()
          )):
            self.error('simultaneousFunctionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)
          if (
            len(self.line) > 1 
            and self.line[0] == '>' 
            and self.line[1] == '>'
          ):
            break

        self.simultaneousFunctionBodyCloseCB()             
        self._next()
      return commit
        
    #def functionCallTreeNode(self):
      #Dancer(name)
      #Repeat(isVisual, body, alternatives)
      #BeatsPerBar
      #Tempo
      
    def functionCall(self, childList):
        commit = (self.line[0] == '\\')
        if(commit):
            parts = self.line[1:].split()
            if (len(parts) < 1):
              self.error('functionCall', 'Expected characters for a function name', True)
            name = parts[0]            
            posParams = parts[1:]
            self._next()
            self.namedParameters()
            self.functionCallOpenCB(name, posParams, self.namedParamsStash)
            n = GenericFunction(name, posParams, self.namedParamsStash)
            childList.append(n)

            # both optional
            self.functionBody(n.children)
            self.simultaneousFunctionBody(n.children)
            
            self.functionCallCloseCB(name)     
        return commit


    def variable(self):
      commit = (self.line[0] == '=')
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.error('variable', 'Expected name to assign to?', True)
        self.variableOpenCB(p[1])
        self.currentVarName = p[1]
        self.varLineStash = []
        self._stashVarLines = True
        self._next()
        if (not (
          #? this covers all we need and allow?
          self.functionBody([])
        )):
          self.error('variable', 'Variable must contain an understandable unit of code, currently anything allowed in a function body', True)
        self._stashVarLines = False
        self.varLineStash.pop()
      return commit
            
            
    def rootSeq(self, childList):
        while(True):
          if(not(
            self.comment()
            or self.functionCall(childList)
            # this last. Has only alphabetic test, reacts to most lines
            or self.variable()          
          )):
            self.error('root sequence', 'Must contain an understandable unit of code, currently a comment, variable, or function call', True)


    def root(self):
        try:
            self.rootSeq(self.tree.children)
            # if we don't except on StopIteration...
            self.error('parser', 'Parsing did not complete, stopped here?', True)
        except StopIteration:
            # All ok
            pass


# Test
#from SourceIterators import StringIterator
#from ConsoleStreamReporter import ConsoleStreamReporter

#p = '../test/test'
#with open(p, 'r') as f:
    #srcAsLines = f.readlines()
    
#it = StringIterator(p, srcAsLines)
#r = ConsoleStreamReporter()
#p = Parser(it, r)

#p.parse()
