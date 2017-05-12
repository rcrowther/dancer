#!/usr/bin/python3


import ExpandIterator


class MetaAssertIterator():
    '''
     Raises error on end of iteration
     Requires an unprimed parser.
    '''
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

      if r[1].startswith(':beatsPerBar'):
        self.beatsPerBar = r[1][12:].lstrip()  
        if (not self.beatsPerBar):
          self.reporter.warning(':beatsPerBar in \init not given a parameter')
      if r[1].startswith(':tempo'):
        self.tempo = r[1][6:].lstrip()  
        if (not self.tempo):
          self.reporter.warning(':tempo  in \init not given a parameter')
        
      if r[1].startswith('\\staff'):
        self.stash = []
        #self.stash.append(r)
        a = None
        while True:
          a = self.it.__next__()
          if a[1][0] == ':':
            self.stash.append(a)
          else:
            break
        if (not self.beatsPerBar):
          self.reporter.warning(':beatsPerBar in \init not set, set to 4')
          self.beatsPerBar = '4'
        if (not self.tempo):
          self.reporter.warning(':tempo in \init not set, set to 60')
          self.tempo = '60'
        indent = r[0] + 1
        self.stash.append((indent, '\\beatsPerBar '))
        self.stash.append((indent + 1, ':' + self.beatsPerBar))
        self.stash.append((indent, '\\tempo '))
        self.stash.append((indent + 1, ':' + self.tempo))
        self.stash.append(a)
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
