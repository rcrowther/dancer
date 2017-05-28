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

   


   
def functionHandlerCreateSubcontext(context, name, posParams, namedParams):
  print('new context for' + context.name)
  newCtx = None
  if (name == 'score'):
    newCtx = ScoreContext()
  if (name == 'dancerGroup'):
    newCtx = DancerContext()
  elif (name == 'dancer'):
    newCtx = DancerContext()
  context.appendChild(newCtx)
  return newCtx

# DO NOT REMOVE
# Unuse, but here so you know I tried it R.C.
#class AcceptedFunctionsDummy():
  #'''
  #Pretends to be an acceptedFunction dictionary.
  #Every call returns the same handler.
  #Every hander entry does nothing. The handler returns None (no body)
  #or, if the function needs a body, a DnummyContext. 
  #'''  
  #DUMMY_CONTEXT = DummyContext()
  ## Should be kept up-to-date.
  ## ...the nasty part of this.
  #funcsWithBody = [
    #"score", "dancer", "dancerGroup", "repeat", "seenRepeat", "alternative"
    #]
    
  #def dummyFunctionHandler(self, context, name, posParams, namedParams):
    #r = None 
    #if (name in AcceptedFunctionsDummy.funcsWithBody):
      #r = AcceptedFunctionsDummy.DUMMY_CONTEXT
    #return r
    
  #def get(self, k):
   #return self.dummyFunctionHandler
   
#acceptedFunctionsDummy = AcceptedFunctionsDummy()


 

#! not parsing all positional parameters
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
        self.globalExp = GlobalContext(reporter)

       
        self.acceptedFunctionsGlobal = {
          "init" : self.functionHandlerSetContextProperties,
          "about" : self.functionHandlerSetContextProperties,
          "score" : self.functionHandlerCreateSubcontext
          } 
        
        self.acceptedFunctionsSimultaneous = {
          #"score" : functionHandlerCreateSubcontext,
          "dancer" : self.functionHandlerCreateSubcontext,
          #? for now
          "dancerGroup" : self.functionHandlerCreateSubcontext
          } 
        
        self.acceptedFunctionsInstructions = {
          "beatsPerBar" : self.functionHandlerBeatsPerBarEvent,
          "tempo" : self.functionHandlerTempoEvent,
          "repeat" : self.functionHandlerRepeat,
          "seenRepeat" : self.functionHandlerDummy,
          "alternative" : self.functionHandlerAlternative,
          "bar" : self.functionHandlerBarline,
          "skip" : self.functionHandlerDummy
          } 





    ################ Utility handlers ##################

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
      
      
    def strToInt(self, s):
      assert(isinstance(s, str))
      v = None
      try:
          v = int(s)
      except ValueError:
        self.error('', 'Value not parsable as an integer', True)
      return v
    
    def strToIntWithDefault(self, s, default):
      assert(isinstance(s, str))
      assert(isinstance(default, int))
      return self.strToInt(s) if v else default
      
    def getParam(self, lst, idx):
      assert(isinstance(lst, list))
      assert(isinstance(idx, int))
      if (not (idx < len(lst))):
        self.error('', 'Expected a parameter : atPosition: {0}'.format(idx), True)
      return lst[idx]
      
      


      
    ################ Function handlers ##################

    def functionHandlerDummy(self, context, name, posParams, namedParams):
      print('dummy function handler: ' + name)
      return None

   
    def functionHandlerCreateSubcontext(self, context, name, posParams, namedParams):
      print('new context for' + context.name)
      newCtx = None
      if (name == 'score'):
        newCtx = ScoreContext(self.reporter)
      if (name == 'dancerGroup'):
        newCtx = DancerContext(self.reporter)
      elif (name == 'dancer'):
        newCtx = DancerContext(self.reporter)
      context.appendChild(newCtx)
      return newCtx
      
    def functionHandlerSetContextProperties(self, context, name, posParams, namedParams):
      for k, v in namedParams:
        context.properties[k] = v
      return None
  
    def functionHandlerTempoEvent(self, context, name, posParams, namedParams):
      #print('merge property function handler: ' + name)
      p = self.getParam(posParams, 0)
      v = self.strToInt(p)
      context.appendChild(TempoChangeEvent(context.uid, v))
      return None
    
    def functionHandlerBeatsPerBarEvent(self, context, name, posParams, namedParams):
      #print('merge property function handler: ' + name)
      p = self.getParam(posParams, 0)
      v = self.strToInt(p)
      context.appendChild(BeatsPerBarChangeEvent(context.uid, v))
      return None  

        
    def functionHandlerRepeat(self, context, name, posParams, namedParams):
      print('unimplemented handler for Repeat')
      # Stash, just stash until see alternatives?
      return context
    
    def functionHandlerAlternative(self, context, name, posParams, namedParams):
      print('unimplemented handler for Repeat Alternative')
      return context

    def functionHandlerBarline(self, context, name, posParams, namedParams):
      p = self.getParam(posParams, 0)
      print('barline function handler: ' + str(p))
      context.appendChild(BarlineEvent(context.uid, p))
      print('ctx:' + str(context))
      return None



    ################# Parsing #########################

    #! do by auto?
    def parse(self):
        # ...prime
        self._next()
        # let's go
        self.root()
        
    def result(self):
      return self.globalExp
    
    #! dont do this here. just call this and ast
    #! resultExp()
    #def toEvents(self):
      #b = []
      #b.extend(self.globalExp.toCreateEvents())
      #b.append(MomentStart(0))
      ##? not sure trigger by dancer? This is a big clump of startup properties.
      ##? by iteration? here for now.
      #b.extend(self.globalExp.toPropertyEvents())
      #return b 



    def _next(self):
        #self._prevLineNo = self.it.lineCount
        n = self.it.__next__()
        self.line = n
        if (self._stashVarLines):
          self.varLineStash.append(n)

         
         
                  
    ## Rules ##

    #def barlineMark(self, context):
      #if (self.line[0] == '.'):
        #context.appendChild(BarlineEvent(context.uid, ''))
        ## if not empty, carry on with the line
        #self.line = self.line[1:].lstrip()
        ## If empty, move along
        #if (not  self.line):
          #self._next()

    def barlineMark(self, context):
      commit = (not self.line)
      if (commit):
        context.appendChild(BarlineEvent(context.uid, ''))
        self._next()
      return commit
      
    def emptyLine(self):
      '''
      Skip empty lines, where barlines are not used.
      Used within variable parsing and Flobal/Root contexts. 
      '''
      commit = (not self.line)
      if (commit):
        self._next()
      return commit

    def comment(self):
        # needs protection against empty lines
        commit = (self.line and self.line[0] == "#")
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
      # needs protection against trailing empty lines
      while(self.line and self.line[0] == ':'):
        p = self.line.split(maxsplit=1)
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
        buildingContext = BuildingContext(context.uid)  
        self._next()

          #? some form of body 
          # - accepts functions
          # - but not simultaneousInstructions
        while(
            self.comment()
            or self.emptyLine()
            or self.functionCall(buildingContext, self.acceptedFunctionsInstructions)
            or self.plainInstruction(buildingContext)
          ):
          pass
          
        if(self.line[0] != '>'):          
          self.error('simultaneousInstructions', 'Seems to be end of instructions, but no angle bracket close?', True)

        context.appendChild(SimultaneousEventsEvent(buildingContext.children))
        self._next()
      return commit
      
    def danceEvent(self, context, name, duration, params):
      s = None
      if (
      name == 'r'
      or name == 'repeat'
      or name == 'mergeProp'
      or name == 'deleteProp'
      or name == 'skip' 
      or name == 'bar' 
      ):
        #if (name == 'manymove'):
        #  s = ManyMoveStruct(structs)
        if (name == 'r'):
          s = RestEvent(context.uid, duration)
        if (name == 'repeat'):
          s = RepeatEvent(context.uid, duration, params)
        #if (name == 'mergeProp'):
        #  s = PropertyMergeStruct(context.uid, k, v)
        #if (name == 'deleteProp'):
        #  s = PropertyDeleteStruct(context.uid, k)
        if (name == 'skip'):
          s = NothingEvent(context.uid, params)
        if (name == 'bar'):
          s = BarlineEvent(context.uid, params)          
        ## dealt with from function callbacks
        #if (name == 'beatsPerBar'):
        #  s = BeatsPerBarChangeStruct(params)
        #if (name == 'tempo'):
        #  s = TempoChangeStruct(params)
      else:
        # Can't test for the zillions of move event names, so make a 
        # move. 
        #? any structural tests?
        #self.error('plainInstruction', 'Code line not recognised', True)
        s = MoveEvent(context.uid, name, duration, params)
      context.appendChild(s)       

      
            
    def plainInstruction(self, context):
      commit = self.line[0].isalpha()
      if (commit):
        p = self.line.split()
        name = p[0]      
          
        # split name and durations
        # durations may not be present (tempo changes, etc.)
        i = len(name) - 1
        while(i >= 0 and name[i].isdigit()):
          i -= 1
        if (i == -1):
          self.error('plainInstruction', 'An instruction name can not be all digits', True)
        i += 1
        
        #! protect
        durationStr = name[i:]
        duration = 1
        if (durationStr):
          duration = int(durationStr)
          
          
        name = name[:i]
        
        params = []
        if (len(p) > 1):
          params = p[1:]
          
        #context.appendChild(DanceEvent(context.uid, name, duration, params))
        e = self.danceEvent(context, name, duration, params)
        
        self._next()
      return commit


    # bodyMountPoint
    def functionBody(self, context):
      # needs protection against trailing empty lines
      commit = (self.line and self.line[0] == '{')
      if (commit):
        if(not context):
          self.error('functionBody', 'Not expecting a body?', True)
          
        self._next()
        
        while (
            self.comment()
            or self.barlineMark(context)
            or self.simultaneousInstructions(context)
            or self.functionCall(context, self.acceptedFunctionsInstructions)
            or self.plainInstruction(context)
          ):
          pass
        #  self.info('ow', True)
        #  print(self.line)
        if (self.line[0] != '}'):
            self.error('functionBody', 'Seems to be end of instructions allowed, but no curly bracket close?', True)
           
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
        
        while (
            self.comment()
            or self.emptyLine()
            or self.functionCall(context, self.acceptedFunctionsSimultaneous)
          ):
          pass
          
        if (not(
          len(self.line) > 1 
          and self.line[0] == '>' 
          and self.line[1] == '>'
        )):
          self.error('simultaneousFunctionBody', 'Seems to be end of instructions allowed, but no double angle bracket close?', True)
           
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
            for p in self.namedParamsStash:
              context.mergeProperty(p[0], p[1])

            bodyMountPoint = handler(context, name, posParams, self.namedParamsStash)
            
            # both optional
            # may need properties or children
            self.functionBody(bodyMountPoint)
            # will only need children
            self.simultaneousFunctionBody(bodyMountPoint)
            
        return commit


####################
    ## variable handling ##
    
    #  Sadly, we do need to modify this, or it will go hunting for 
    # specific acceptedFunction's.
    def variableFunctionBody(self, context):
      #self.info('ow', True)
      #print(self._next() )
      commit = (self.line and self.line[0] == '{')
      if (commit):
        
        self._next()
        
        while (
          #self.barlineMark(context)
          self.comment()
          or self.emptyLine()
          or self.simultaneousInstructions(context)
          or self.variableFunctionCall(context)
          or self.plainInstruction(context)
          ):
          pass
        if (self.line[0] != '}'):
          self.error('variableFunctionBody', 'Seems to be end of instructions allowed in a variable, but no bracket close?', True)
           
        self._next()
      return commit

    # Sadly, we do need to modify this, or it will 'handle' functions.
    # While the handling can be nullified by returning DummyContext
    # we need to kill name searching altogether (e.g. variable names 
    # are still present)
    def variableFunctionCall(self, context):
        commit = (self.line[0] == '\\')
        if(commit):
            parts = self.line[1:].split()
            if (len(parts) < 1):
              self.error('variableFunctionCall', 'Expected characters for a function name', True)
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
      # needs protection against empty lines
      commit = (self.line and self.line[0] == '=')
      if (commit):
        p = self.line.split()
        if (len(p) < 2):
          self.error('variable', 'Expected name to assign to?', True)
        self.currentVarName = p[1]
        
        #? try this instead,
        #buildingContext = BuildingContext(context.uid)  
        self.varLineStash = []
        self._stashVarLines = True
        
        self._next()
        if (not (
          #? this covers all we need and allow?
          self.variableFunctionBody(DummyContext(self.reporter))
        )):
          self.error('variable', 'Variable must contain an understandable unit of code, currently anything allowed in a function body', True)
          
        self._stashVarLines = False
        self.varLineStash.pop()
      return commit
           
#####################################

            
    def rootSeq(self, globalExp):
        while(True):
          if(not(
            #or self.barlineMark()
            self.comment()
            or self.emptyLine()
            or self.functionCall(globalExp, self.acceptedFunctionsGlobal)
            # this last. Has only alphabetic test, reacts to most lines
            #or self.variable()          
          )):
            self.error('root sequence', 'Must contain an understandable unit of code, currently a comment or function call', True)


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
#from ConsoleStreamReporter import ConsoleStreamReporter
##import ExpandIterator

#p = '../test/expanded_test.dn'
#with open(p, 'r') as f:
    #srcAsLines = f.readlines()
    
#r = ConsoleStreamReporter()
#sit = StringIterator(p, srcAsLines)
##it = ExpandIterator.ExpandIterator(sit, r)

#p = Parser(sit, r)

#p.parse()

#print(str(p.result()))

