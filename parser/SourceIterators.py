#!/usr/bin/python3




class StringIterator:
    '''
    Creates an iterator from a collection of lines.
    
    Removes empty lines (so guarantees next()[0])
    Raises StopIteration at end of iteration
    
    @srcLines As returned by Python readlines()
    '''
    def __init__(self, srcLines):
        self.src = srcLines
        self.i = 0
        self.size = len(srcLines)
        self.lineCount = 1


    def __iter__(self):
        return self


    def __next__(self):
        try:
          while(True):
            l = self.src[self.i].lstrip()
            self.i += 1
            self.lineCount += 1
            if (l):
              break
          return l
        except IndexError:
            raise StopIteration

# Test
#with open('../test/test', 'r') as f:
    #srcAsLines = f.readlines()
#it = StringIterator(srcAsLines)
#for l in it:
  #print(l)

