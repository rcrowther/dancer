#!/usr/bin/python3


import ExpandIterator


class MetaAssertIterator():
    '''
    Normalise the stream from header data.
    Currently adds initialising beatPerBar and tempo info as stream
    instructions.
    '''
    #? may do more?
    def __init__(self, srcIt, reporter):
      self.reporter = reporter
      self.it = ExpandIterator.ExpandIterator(srcIt, reporter)
      self.tempo = ''
      self.beatsPerBar = ''
      self.stash = []
      
      
    def lineCount():
      return self.it.lineCount
      
    def __iter__(self):
      return self
        
    def __next__(self):
      r = self.stash.pop() if (len(self.stash) > 0) else self.it.__next__()

      if r.startswith(':beatsPerBar'):
        self.beatsPerBar = r[12:].lstrip()  
        if (not self.beatsPerBar):
          self.reporter.warning(':beatsPerBar in \init not given a parameter')
      if r.startswith(':tempo'):
        self.tempo = r[6:].lstrip()  
        if (not self.tempo):
          self.reporter.warning(':tempo  in \init not given a parameter')
        
      if r.startswith('\\staff'):
        self.stash = []
        #self.stash.append(r)
        a = None
        while True:
          a = self.it.__next__()
          if a[0] != '{':
            self.stash.append(a)
          else:
            break
        # now at body beginning
        # append that too
        self.stash.append(a)
        
        # now append exta instructions
        if (not self.beatsPerBar):
          self.reporter.warning(':beatsPerBar not set in \init, default to 4')
          self.beatsPerBar = '4'
        if (not self.tempo):
          self.reporter.warning(':tempo not set in \init, default to 60')
          self.tempo = '60'
          
        self.stash.append('\\beatsPerBar '  + self.beatsPerBar)
        self.stash.append('\\tempo ' + self.tempo)
        self.stash = list(reversed(self.stash))
      return r
      
      
import SourceIterators

from ConsoleStreamReporter import ConsoleStreamReporter

with open('../test/test', 'r') as f:
    srcAsLines = f.readlines()
    
r = ConsoleStreamReporter()
sit = SourceIterators.StringIterator(srcAsLines)
it = MetaAssertIterator(sit, r)

for l in it:
  print(l)
