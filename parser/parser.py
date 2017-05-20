#!/usr/bin/python3


import os.path
import os
import argparse
import sys
from events import *
from contexts import *

from Position import Position, NoPosition


#! fix missimg functions
#! do something about counting and prepare marks
#! look at context nesting again
#! fix import loop with iterator
#! build in a timer
#! where are dancer names going?

## Specifics ##
# Return is the params a body should accept. 
# Score hierachy: a sub context 
# Most others: context properties or children 
# None : no body should be present

def functionHandlerDummy(context, name, posParams, namedParams):
  print('dummy function handler: ' + name)
  return None
  
def functionHandlerGlobalProperties(context, name, posParams, namedParams):
  for k, v in namedParams:
    context.properties[k] = v
  return None
   


   
def functionHandlerCreateSubcontext(context, name, posParams, namedParams):
  print('new context for' + context.name)
  newCtx = None
  if (name == 'score'):
    newCtx = ScoreContext()
  if (name == 'dancerGroup'):
    newCtx = DancerContext()
  elif (name == 'dancer'):
    newCtx = DancerContext()
  context.children.append(newCtx)
  return newCtx

class AcceptedFunctionsDummy():
  def dummyFunctionHandler(self, context, name, posParams, namedParams):
    return context
    
  def get(self, k):
   return self.dummyFunctionHandler
   
acceptedFunctionsGlobal = {
"init" : functionHandlerGlobalProperties,
"about" : functionHandlerGlobalProperties,
"score" : functionHandlerCreateSubcontext
} 

acceptedFunctionsSimultaneous = {
#"score" : functionHandlerCreateSubcontext,
"dancer" : functionHandlerCreateSubcontext,
#! for now
"dancerGroup" : functionHandlerCreateSubcontext
} 


def functionHandlerMergeProperty(context, name, posParams, namedParams):
  print('merge property function handler: ' + name)
  context.children.append(MergeProperty(context.uid, name, posParams[0]))
  return None

  
    
def functionHandlerRepeat(context, name, posParams, namedParams):
  #print('dummy function handler: ' + name)
  # Stash, just stash until see alternatives?
  return context

def functionHandlerAlternative(context, name, posParams, namedParams):
  #print('dummy function handler: ' + name)
  return context
  
acceptedFunctionsInstructions = {
"beatsPerBar" : functionHandlerMergeProperty,
"tempo" : functionHandlerMergeProperty,
"repeat" : functionHandlerRepeat,
"seenRepeat" : functionHandlerDummy,
"alternative" : functionHandlerAlternative,
"endBar" : functionHandlerDummy
} 

#! not parsing positional parameters
#! need a resolverIterator to remove functions from instruction lists?
#! otheerwise they screw JSON representation, and maybe other bytecode?
#! scores cannot accept staffs as bodies. 
#! Positional, or named?
#! 
class Parser:
    '''
   Generates a parser-based DanceEvent form,
   - MomentEvents are dummies to mark simutaneous operation.
   - *Property events may appear. Like the input language, these
   are associated with following events. Not marked as simultaneous.
   - DanceEvent is a step in time.
   No Finish and no end is marked to the DanceEvent chain. 
   - *Context does not appear at all.
   - Finish does not appear
   No premoment instructions exist.
    '''
    V_INSTRUCTIONSEQ = 1
    V_FUNCTION = 2
    
    def __init__(self, it, reporter):
        self.it = it
        self.reporter = reporter

        self.line = ''
   
        # var data gathering
        self.currentVarName = ''
        self._stashVarLines = False
        self.varLineStash = []

        # namedParams gathering
        self.namedParamsStash = []
        self.globalExp = GlobalContext()


    def parse(self):
        # ...prime
        self._next()
        # let's go
        self.root()
        
    def ast(self):
      return self.globalExp
    
    def toEvents(self):
      b = []
      b.extend(self.globalExp.toCreateEvents())
      b.append(MomentStart(0))
      #? not sure trigger by dancer? This is a big clump of startup properties.
      #? by iteration? here for now.
      b.extend(self.globalExp.toPropertyEvents())
      return b 
      
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



    def simultaneousInstructions(self, context):
      commit = (self.line[0] == '<')
      if (commit):
        #print('simultaneousInstructions ' + str(self._prevLineNo))
        context.children.append(MomentStart(-3))
        
        self._next()

        while(self.line[0] != '>'):
          #? some form of body 
          # - accepts functions
          # - but not simultaneousInstructions
          if(not(
            self.functionCall(context, acceptedFunctionsInstructions)
            or self.comment()
            or self.plainInstruction(context)
          )):
            self.error('simultaneousInstructions', 'Code line not recognised as a function, plain instruction, or a comment', True)

        context.children.append(MomentEnd())
        
        self._next()
      return commit
      
      
    def plainInstruction(self, context):
      commit = self.line[0].isalpha()
      if (commit):
        p = self.line.split()
        name = p[0]      
          
        # split name and durations
        i = len(name) - 1
        while(i >= 0 and name[i].isdigit()):
          i -= 1
        if (i == -1):
          self.error('plainInstruction', 'An instruction name can not be all digits', True)
        i += 1
        
        duration = name[i:]
        if (not duration):
          duration = 1
          
        name = name[:i]
        
        params = []
        if (len(p) > 1):
          params = p[1:]
          
        context.children.append(DanceEvent(context.uid, name, duration, params))
        
        self._next()
      return commit


    # bodyMountPoint
    def functionBody(self, context):
      commit = (self.line[0] == '{')
      if (commit):
        if(not context):
          self.error('functionBody', 'Not expecting a body?', True)
          
        self._next()
        
        while (True):
          if(not(
          self.simultaneousInstructions(context)
          or self.functionCall(context, acceptedFunctionsInstructions)
          or self.comment()
          or self.plainInstruction(context)
          )):
            self.error('functionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)
          if (self.line[0] == '}'):
            break
           
        self._next()
      return commit

        
    def simultaneousFunctionBody(self, context):
      commit = (
        len(self.line) > 1 
        and self.line[0] == '<' 
        and self.line[1] == '<'
      )
      
      if (commit):
        if(not context):
          self.error('simultaneousFunctionBody', 'Not expecting a body?', True)
        
        self._next()
        
        while (True):
          if(not(
            self.functionCall(context, acceptedFunctionsSimultaneous)
            or self.comment()
          )):
            self.error('simultaneousFunctionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)
          if (
            len(self.line) > 1 
            and self.line[0] == '>' 
            and self.line[1] == '>'
          ):
            break
            
        self._next()
      return commit
        

      
    def functionCall(self, context, acceptedFunctions):
        commit = (self.line[0] == '\\')
        if(commit):
            parts = self.line[1:].split()
            if (len(parts) < 1):
              self.error('functionCall', 'Expected characters for a function name', True)
            name = parts[0]    
            #print(name)
            handler = acceptedFunctions.get(name)
            if (not handler):
              self.error('functionCall', 'Function name not recognised (at this level?): level: "{0}", name: "{1}"'.format(context.name, name), True)
            posParams = parts[1:]
            self._next()
            self.namedParameters()

            bodyMountPoint = handler(context, name, posParams, self.namedParamsStash)
            
            # both optional
            # may need properties or children
            self.functionBody(bodyMountPoint)
            # will only need children
            self.simultaneousFunctionBody(bodyMountPoint)
            
        return commit


####################

    def variableFunctionBody(self, context):
      commit = (self.line[0] == '{')
      if (commit):
        
        self._next()
        
        while (True):
          if(not(
          self.simultaneousInstructions(context)
          or self.variableFunctionCall(context)
          or self.comment()
          or self.plainInstruction(context)
          )):
            self.error('functionBody', 'Code line not recognised as a function, plain instruction, simultaneousInstruction, or a comment', True)
          if (self.line[0] == '}'):
            break
           
        self._next()
      return commit

    def variableFunctionCall(self, context):
        commit = (self.line[0] == '\\')
        if(commit):
            parts = self.line[1:].split()
            if (len(parts) < 1):
              self.error('functionCall', 'Expected characters for a function name', True)
            name = parts[0]    
            #print(name)
            posParams = parts[1:]
            self._next()
            self.namedParameters()

            # both optional
            # may need properties or children
            self.variableFunctionBody(context)
            # will only need children
            self.simultaneousFunctionBody(context)
            
        return commit
        
    # Must drop level name-checking for functions,
    # ...we have no idea on the level of the functions 
    def variable(self):
      commit = (self.line[0] == '=')
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.error('variable', 'Expected name to assign to?', True)
        self.currentVarName = p[1]
        self.varLineStash = []
        self._stashVarLines = True
        self._next()
        if (not (
          #? this covers all we need and allow?
          self.variableFunctionBody(DummyContext())
        )):
          self.error('variable', 'Variable must contain an understandable unit of code, currently anything allowed in a function body', True)
        self._stashVarLines = False
        self.varLineStash.pop()
      return commit
           
#####################################

            
    def rootSeq(self, globalExp):
        while(True):
          if(not(
            self.comment()
            or self.functionCall(globalExp, acceptedFunctionsGlobal)
            # this last. Has only alphabetic test, reacts to most lines
            #or self.variable()          
          )):
            self.error('root sequence', 'Must contain an understandable unit of code, currently a comment, variable, or function call', True)


    def root(self):
        try:
            self.rootSeq(self.globalExp)
            # if we don't except on StopIteration...
            self.error('parser', 'Parsing did not complete, stopped here?', True)
        except StopIteration:
            # All ok
            self.info('done', False)
            pass


# Test
#from SourceIterators import StringIterator
##import ExpandIterator
#from ConsoleStreamReporter import ConsoleStreamReporter

#p = '../test/test.dn'
#with open(p, 'r') as f:
    #srcAsLines = f.readlines()
    
#r = ConsoleStreamReporter()
#sit = StringIterator(p, srcAsLines)
##it = ExpandIterator.ExpandIterator(sit, r)

#p = Parser(sit, r)

#p.parse()

#print(str(p.ast()))

#xe = p.toEvents()
#for e in xe:
  #print(str(e))
