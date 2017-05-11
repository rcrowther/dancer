#!/usr/bin/python3


import os.path
import os
import argparse
import sys

from Position import Position, NoPosition


class Parser:
    '''
    '''
    V_INSTRUCTIONSEQ = 1
    V_FUNCTION = 2
    
    def __init__(self, it, reporter):
        self.it = it
        self.reporter = reporter
        self.prevLineNo = 1
        self.prevIndent = 0
        self.indent = 0
        self.line = ''
   
        self.currentVarName = ''
        self.stashLines = False
        self.lineStash = []
        
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
        pos = Position(self.it.src, self.prevLineNo, 0) if withPosition else NoPosition 
        self.reporter.error(rule + ': ' + msg, pos)
        #? Might introduce some finness by allowing recovery sometimes?
        sys.exit(1)

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
        n = self.it.__next__()
        self.indent, self.line = n
        if (self.stashLines):
          self.lineStash.append(n)
          
    def indentIncreased(self):
        #print('indentIncreased :' + str(self.prevIndent) + '-' + str(self.indent) )
        return self.indent > self.prevIndent
        
    def indentHeld(self):
        #print('indentHeld :' + str(self.prevIndent) + '-' + str(self.indent) )
        return self.indent >= self.prevIndent



    ## Callbacks ##

    def commentCB(self, text):
      #print('comment...')
      #print('"' + text + '"')
      pass

    def namedParameterCB(self, name, value):
      #print('namedParameter...')
      #print(name + ':' +value)
      pass

    def functionNameCB(self, name):
      #print('function name...')
      #print(name)
      pass

    def functionCloseCB(self):
      #print('    functionCloseCB...')
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
            
    def functionBodyOpenCB(self):
      #print('  functionBody open...')
      pass      

    def functionBodyCloseCB(self):
      #print('  functionBody close...')
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


    def simultaneousInstructions(self):
      commit = (self.line[0] == '<' and self.line[1] == '<')
      if (commit):
        self.simultaneousInstructionsOpenCB()
        self._next()
        while(True):
          #! some form of body (accepts functions)
          #? but not simultaneousInstructions
          if(not(
            self.function()
            or self.comment()
            or self.plainInstruction()
          )):
            self.error('simultaneousInstructions', 'Code line not recognised as a function, plain instruction, or a comment', True)

          if(not self.indentHeld()):
            break
        self.simultaneousInstructionsCloseCB()
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
      baseIndent = self.indent
      commit = ((baseIndent > 0) and self.plainInstruction())
      while((self.indent >= baseIndent) and self.plainInstruction()):
        pass
      return commit

    def functionBody(self):
      if (self.indentIncreased()):
        self.functionBodyOpenCB()
        # ...in case indents further,
        # cache start indent             
        baseIndent = self.indent
        while (True):
          if(not(
          self.simultaneousInstructions()
          or self.function()
          or self.comment()
          or self.plainInstruction()
          )):
            self.error('functionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)

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
              
              #? need test?
              if (self.line[0] == ':'):
                  self.namedParameters()
                  
              #print('function2...' + str(self.indentIncreased()))
              self.functionBody()
              self.functionCloseCB()     
        return commit


    def variable(self):
      commit = (self.line[0] == '=')
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.error('variable', 'Expected name to assign to?', True)
        self.variableOpenCB(p[1])
        self.currentVarName = p[1]
        self.lineStash = []
        self.stashLines = True
        self._next()
        #! now, e.g. parameters, ins, etc?
        if (not (
          self.function()
          #or self.simultaneousInstructions()
          #or self.comment()
          #! also, block of these useful
          or self.plainInstructionSeq()
        )):
          self.error('variable', 'Variable must contain an understandable unit of code, currently one of a function, plain instruction, simultaneous instructions, or a comment', True)
        self.stashLines = False
        self.lineStash.pop()
      return commit
            
            
    def rootSeq(self):
        while(
          self.comment()
          or self.function()
          # this last. Has only alphabetic test, reacts to most lines
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



