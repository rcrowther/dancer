#!/usr/bin/python3

import parser



class ExpandIterator():
    '''
    Expands variables in the input stream.
    Requires an unprimed instance of the parser.
    '''
    def __init__(self, srcIt, reporter):
        self.it = srcIt
        self.reporter = reporter
        self.parser = parser.Parser(srcIt, reporter)
        self.varMap = {}
        # a stack of expanded material
        self.expandingVars = []

    def error(self, msg, withPosition):
        pos = Position(self.it.src, self.prevLineNo, 0) if withPosition else NoPosition 
        self.reporter.error(msg, pos)
        #? Might introduce some finness by allowing recovery sometimes?
        sys.exit(1)
        
    def lineCount():
      return self.it.lineCount
      
    def __iter__(self):
        return self
        


    def isVarToExpand(self, line):
        foundExpansion = False
        forTest = (line[0] == '\\')
        if(forTest):
          name = line[1:].rstrip()
          m = self.varMap.get(name)
          if (m):
            foundExpansion = True
            # ...a reference copy, I hope
            self.expandingVars.extend(reversed(m))
        return self.nextFromExpansion() if foundExpansion else line
                
    def nextFromExpansion(self):
      if (len(self.expandingVars) > 0):
        return self.expandingVars.pop()
      else:
        return None
        
    def nextFromIterator(self):
      self.parser._next()
      # A sucessful parse steps us on... that's where we want to be...
      while(self.parser.variable()):
        # linestash works round a function body,
        # so includes the surrounding curly brackets.
        # For an expansion, these have no meaning
        self.varMap[self.parser.currentVarName] = self.parser.lineStash[1:-1]
      r = self.parser.line
      return r
                
                 
    def __next__(self):
        r = self.nextFromExpansion()
        if (not r):
          r = self.nextFromIterator()
        return self.isVarToExpand(r)

            
            
#import SourceIterators

#from ConsoleStreamReporter import ConsoleStreamReporter

#with open('../test/test', 'r') as f:
    #srcAsLines = f.readlines()
    
#r = ConsoleStreamReporter()
#sit = SourceIterators.StringIterator(srcAsLines)
#eit = ExpandIterator(sit, r)

#for l in eit:
  #print(l)

#print('map:')
#print(eit.varMap)
