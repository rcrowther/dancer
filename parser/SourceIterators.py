#!/usr/bin/python3



class SourceIterator():
  '''
  Iterate a source.
  Multiple newlines must be reduced to one newline.
  Must lstrip() all limes.
  Must raise StopIteration at end of iteration.
  Carries self._srcName description.
  Carries self._lineCount, starting at 0.
  '''
  def __init__(self, srcName):
    self._srcName = srcName
    self._lineCount = 0

  
#! Need a IteratorFile
class StringIterator(SourceIterator):
    '''
    Creates an iterator from a collection of lines.
    
    #Removes empty lines (so guarantees next()[0])
    Raises StopIteration at end of iteration
    
    @srcLines As returned by Python readlines()
    '''
    def __init__(self, srcName, srcLines):
      SourceIterator.__init__(self, srcName)
      #self._srcName = srcName
      self.src = srcLines
      self.i = 0
      self.size = len(srcLines)
      #self._lineCount = 0
      self.inEmpty = False
        
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
            if (l or not(self.inEmpty)):
              self.inEmpty = not(l)
              break
          return l         
        except IndexError:
            raise StopIteration

#p = '../test/test.dn'
#with open(p, 'r') as f:
    #srcAsLines = f.readlines()
#it = StringIterator(p, srcAsLines)

#print(it.srcName + ':')
#for l in it:
  #print(str(it.lineCount) + ' ' + l)

