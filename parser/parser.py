#!/usr/bin/python3


import os.path
import os
import argparse
import sys

from Position import Position, NoPosition

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



    def simultaneousInstructions(self):
      commit = (self.line[0] == '<')
      if (commit):
        #print('simultaneousInstructions ' + str(self._prevLineNo))
        self.simultaneousInstructionsOpenCB()
        self._next()
        
        while(self.line[0] != '>'):
          #! some form of body (accepts functions)
          #? but not simultaneousInstructions
          if(not(
            self.functionCall()
            or self.comment()
            or self.plainInstruction()
          )):
            self.error('simultaneousInstructions', 'Code line not recognised as a function, plain instruction, or a comment', True)


        self.simultaneousInstructionsCloseCB()
        self._next()
      return commit
      
    def plainInstruction(self):
      commit = self.line[0].isalpha()
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.instructionCB(p[0], [])
        else:
          self.instructionCB(p[0], p[1:])
        self._next()
      return commit

    def plainInstructionSeq(self):
      commit = self.plainInstruction()
      while (self.plainInstruction()):
        pass
      return commit

    def functionBody(self):
      commit = (self.line[0] == '{')
      if (commit):
        self.functionBodyOpenCB()
        self._next()
        
        while (True):
          if(not(
          self.simultaneousInstructions()
          or self.functionCall()
          or self.comment()
          or self.plainInstruction()
          )):
            self.error('functionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)
          if (self.line[0] == '}'):
            break

        self.functionBodyCloseCB()             
        self._next()
      return commit
        
        
    def functionCall(self):
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

            self.functionBody()
            
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
          self.functionBody()
        )):
          self.error('variable', 'Variable must contain an understandable unit of code, currently anything allowed in a function body', True)
        self._stashVarLines = False
        self.varLineStash.pop()
      return commit
            
            
    def rootSeq(self):
        while(True):
            if(not(
            self.comment()
            or self.functionCall()
            # this last. Has only alphabetic test, reacts to most lines
            or self.variable()          
          )):
            self.error('root sequence', 'Must contain an understandable unit of code, currently a comment, variable, or function call', True)

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


# Test
#from SourceIterators import StringIterator
#from ConsoleStreamReporter import ConsoleStreamReporter

#with open('../test/test', 'r') as f:
    #srcAsLines = f.readlines()
    
#sit = StringIterator(srcAsLines)
#r = ConsoleStreamReporter()
#p = Parser(sit, r)

#p.parse()
