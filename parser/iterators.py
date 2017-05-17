#!/usr/bin/python3


from events import *
import sys



# -2 moment = finished stream
MOMENT_EXHAUSTED  = -2
# -1 moment = pre-play stream
MOMENT_PREPLAY  = -1

class DataIterator():
  '''
  Iterate over data given to Dancer code.
  The itertor can be
  - building from source AST
  -- child stream
  -- music instruction iterators
  - bulding from a stream
  '''
  def __init__(self):
    self.contextUID = None

  def __iter__(self):
    return self
        
  def pendingMoment(self):
    pass
          
  def __next__(self):
    pass
     
     
       
#! need to rethink form
'''
class InstructionIterator(DataIterator):
  def __init__(self, ast):
    self.astIt = iter(ast)
    self.currentDuration = 0
    self.cache = []
    
  def _next
    while(True):
      e = astIt.next()    
    if (not music or simuutaneous event):
        self.cache.append(e)
      else:
        break
    self.currentDuration += e.duration
    self._nextMoment = 
          
  def __iter__(self):
    return self
        
  def pendingMoment(self):
    return self._nextMoment
         
  def __next__(self):
    self.cache = []
    self._cacheToNextMoment()
    return self.cache
'''
    
    
class StreamIterator(DataIterator):
  '''
  Only works with a whole provided stream.
  Stream must end with Finish()
  needs contextUID to be set
  '''
  def __init__(self, stream):
    DataIterator.__init__(self)
    self.streamIt = iter(stream)
    self.cache = []
    self._nextMoment = -1

  def _cacheToNextMoment(self):
    while(True):
      e = self.streamIt.__next__()
      if (not( isinstance(e, PrepareEvent) or isinstance(e, Finish))):
        self.cache.append(e)
      else:
        break
    self._nextMoment = e.moment
             
  def __iter__(self):
    return self
        
  def hasNext(self):
    return self._nextMoment == MOMENT_EXHAUSTED
    
  def pendingMoment(self):
    return self._nextMoment
         
  def __next__(self): 
    self.cache = []
    self._cacheToNextMoment()
    return self.cache



class ChildContextIterator(DataIterator):
  '''
  pendingMoment() must be called before next.
  needs contextUID to be set
  
  '''
  def __init__(self):
    DataIterator.__init__(self)
    self._childIts = []
    self.pendingIterators = []
    
  def addChild(self, it):
    self._childIts.append(it)
    
  def _delete(self, lst, uid):
    i = 0
    l = len(lst)
    while(i < l):
      if (lst[i].contextUID == uid):
        lst.pop(i)
        break
      else:
        i += 1
        
  def deleteChildIterator(self, uid):
    print('deletechild uid: ' + str(uid))
    # delete iterator
    self._delete(self._childIts, uid)
          
  def __iter__(self):
    return self
        
  def pendingMoment(self):
    low = sys.maxsize 
    self.pendingIterators = []
    exhausted = []
    for c in self._childIts:
      newLow = c.pendingMoment()
      if (newLow == MOMENT_EXHAUSTED):
        exhausted.append(c.contextUID)
      elif(newLow < low):
        low = newLow
        self.pendingIterators = [c]
      elif(newLow == low):
        self.pendingIterators.append(c)
      
    # delete exhausted iterators
    for uid in exhausted:
      self.deleteChildIterator(c.contextUID)
    if (low == sys.maxsize):
      low = MOMENT_EXHAUSTED
    return low
    
  def __next__(self):
    events = []
    if (not self.pendingIterators):
      raise StopIteration
    for it in self.pendingIterators:
      events.extend(it.__next__())
    return events


#from events import *

#stream1 = [
  #CreateContext(4, 'dancer'),
  #MergeProperty('context', 'indent-stave', 2),
  #PrepareEvent('context', 0),
  #MusicEvent('context', 'clap', 1, 'mid'),
  #MusicEvent('context', 'clap', 1, 'mid'),
  #PrepareEvent('context', 1),
  #MusicEvent('context', 'step', 1, 'south'),
  #PrepareEvent('context', 2),
  #MusicEvent('context', 'point', 1, 'right'),
  #Finish()
#]
#stream2 = [
  #Finish()
#]
#sit = StreamIterator(99, stream)
#while(True):
  #print('pending:' + str(sit.pendingMoment()))
  #r = sit.__next__()
  #b = ''
  #for e in r:
    #b += str(e)
    #b += ', '
  #print(b)


#cit = ChildContextIterator()
#it1 = StreamIterator(stream1)
#it1.contextUID = 9
#it2 = StreamIterator(stream2)
#it2.contextUID = 99
#cit.addChild(it1)
#cit.addChild(it2)

#while(True):
  #print('pending:' + str(cit.pendingMoment()))
  #r = cit.__next__()
  #b = ''
  #for e in r:
    #b += str(e)
    #b += ', '
  #print(b)
