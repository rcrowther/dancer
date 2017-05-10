#!/usr/bin/python3




class StringIterator:
    '''
     Raises error on end of iteration
    '''
    def __init__(self, srcLines):
        self.src = srcLines
        self.i = 0
        self.size = len(srcLines)
        self.lineCount = 1


    def __iter__(self):
        return self


    def __next__(self):
        ls = ""
        while(not ls and self.i < self.size):
          l = self.src[self.i]
          ls = l.lstrip()
          self.i += 1
          self.lineCount += 1
          
        if (self.i < self.size):
            return (len(l) - len(ls), ls)
        else:
            raise StopIteration

# Test
#with open('../test/test', 'r') as f:
#    srcAsLines = f.readlines()
#it = StringIterator(srcAsLines)
#for l in it:
#  print(l)

