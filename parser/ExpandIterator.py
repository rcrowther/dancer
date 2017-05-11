#!/usr/bin/python3

import parser



class ExpandIterator():
    '''
     Raises error on end of iteration
     Requires an unprimed parser.
    '''
    def __init__(self, srcIt, reporter):
        self.it = srcIt
        self.reporter = reporter
        self.parser = parser.Parser(srcIt, reporter)
        self.varMap = {}
        # [[indent, line]...]
        self.expandingVars = []
        
    def lineCount():
      return self.it.lineCount
      
    def __iter__(self):
        return self
        


    def isVarToExpand(self, line):
        foundExpansion = False
        forTest = (line[1][0] == '\\')
        #print('**is var to expand**')
        if(forTest):
          name = line[1][1:].rstrip()
          #print('**var to expand**' + name)
          m = self.varMap.get(name)
          if (m):
            #print('**var to expand**' + name)
            # ...a reference copy, I hope
            self.expandingVars.extend(reversed(m))
            #print('**expanding**')
            foundExpansion = True
        return self.nextFromExpansion() if foundExpansion else line
                
    def nextFromExpansion(self):
      if (len(self.expandingVars) > 0):
        return self.expandingVars.pop()
      else:
        return None
        
    def nextFromIterator(self):
      self.parser._next()

      #? This is daft
      if (self.parser.variable()):
        ## The parse moves us on... never mind...
        #print('**found var**')
        self.varMap[self.parser.currentVarName] = self.parser.lineStash
        while(self.parser.variable()):
          #print('**found var**')
          self.varMap[self.parser.currentVarName] = self.parser.lineStash
      r = (self.parser.indent, self.parser.line)
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
