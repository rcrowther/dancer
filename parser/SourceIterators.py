#!/usr/bin/python3



#! Need a IteratorFile
class StringIterator:
    '''
    Creates an iterator from a collection of lines.
    
    Removes empty lines (so guarantees next()[0])
    Raises StopIteration at end of iteration
    
    @srcLines As returned by Python readlines()
    '''
    def __init__(self, srcName, srcLines):
        self._srcName = srcName
        self.src = srcLines
        self.i = 0
        self.size = len(srcLines)
        self._lineCount = 0

    @property
    def srcName(self):
      return self._srcName
         
    @property
    def lineCount(self):
      return self._lineCount

    
    def __iter__(self):
        return self


    def __next__(self):
        try:
          while(True):
            l = self.src[self.i].lstrip()
            self.i += 1
            self._lineCount += 1
            if (l):
              break
          return l
        except IndexError:
            raise StopIteration

#p = '../test/test'
#with open(p, 'r') as f:
    #srcAsLines = f.readlines()
#it = StringIterator(p, srcAsLines)

#print(it.srcName + ':')
#for l in it:
  #print(str(it.lineCount) + ' ' + l)

