#!/usr/bin/python3


from events import *
import sys


MOMENT_PARSEDSTART = -3
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
    '''
    Should return MOMENT_EXHAUSTED when done 
    '''
    pass
          
  def __next__(self):
    '''
    On parse, return packs of events at a moment
    '''
    pass
     
  def __str__(self):
    b = ''
    while(self.pendingMoment() != MOMENT_EXHAUSTED):
      b += '\npending:'
      b += str(self.pendingMoment())
      b += '\n'
      r = self.__next__()
      for e in r:
        b += str(e)
        b += ', '
    return b
       

#? This is a big messy method?
#! error and stats report. Bar counts, validationn?
class ParsedDanceeventIterator(DataIterator):
  # This has parser-based form to account for.
  # - MomentEvents are dummies to mark simutaneous operation.
  # - *Property events may appear. Like the input language, these
  # are associated with following events. Not marked as simultaneous.
  # - DanceEvent is a step in time.
  # No Finish and no end is marked to the DanceEvent chain. 
  # - *Context does not appear at all.
  # - Finish does not appear
  # No premoment instructions exist.
  # Due to Python's error throwing, finish is hard to catch here.
  # So chain length is monitored.
  # PendingMoment can not be resolved without caching.
  
  def __init__(self):
    self.contextId = None
    self._data = None
    self._pendingMoment = 0
    self._pendingMomentIncrement = 1
    self.curse = 0
    self.length = 0
    self.cache = []
  
  def prepare(self, contextId, data):
    self.contextId = contextId
    self.length = len(data)
    self._data = data

  def pendingMoment(self):
    return self._pendingMoment 
                 
  def __next__(self):
    r = self.cache
    self.cache = []
    self._pendingMoment += self._pendingMomentIncrement
    #print(str(self.curse))
    #print(str(self.length))

    if (self.curse < self.length):
      e = self._data[self.curse]
      
      # cache property events
      while(isinstance(e, MergeProperty) or isinstance(e, DeleteProperty)):
        self.cache.append(e)
        self.curse += 1 
        e = self._data[self.curse]          

      if (isinstance(e, DanceEvent)):
        self.cache = [e]
        self._pendingMomentIncrement = e.duration 
      else:
        # handle simultaneous form
        # skip moment start
        self.cache = []
        self.curse += 1
        e = self._data[self.curse]
        longest = 0          
        while(not isinstance(e, MomentEnd)):
          if (isinstance(e, DanceEvent) and e.duration > longest):
            longest = e.duration
          self.cache.append(e)
          self.curse += 1
          e = self._data[self.curse]  
        self._pendingMomentIncrement = longest 
    else:
      if (not self.cache):
        # kill. the test means this will not run until the last cached 
        # entry is returned by __next__
        self._pendingMomentIncrement = 0 
        self._pendingMoment = MOMENT_EXHAUSTED    
    self.curse += 1
    return r

        


    
  
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


from events import *

#stream1 = [DanceEvent(6, "clap", 1, []), DanceEvent(6, "clap", 1, ['overhead']), DanceEvent(6, "step", 1, ['west']), MomentStart(-3), DanceEvent(6, "cross", 1, ['legs']), DanceEvent(6, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(6, "jump", 1, ['south']), DanceEvent(6, "hands", 1, ['ears']), MomentEnd(), DanceEvent(6, "bend", 1, ['knees']), DanceEvent(6, "slap", 1, ['other']), DanceEvent(6, "slap", 2, ['knees']), DanceEvent(6, "twirl", 1, ['right']), DanceEvent(6, "split", 1, ['knees']), DanceEvent(6, "turn", 1, ['west']), MergeProperty(6, "beatsPerBar", 3), MergeProperty(6, "tempo", 80), DanceEvent(6, "kick", 1, ['low'])]
#stream2 = [DanceEvent(4, "clap", 1, []), DanceEvent(4, "clap", 1, ['overhead']), DanceEvent(4, "step", 1, ['west']), MomentStart(-3), DanceEvent(4, "cross", 1, ['legs']), DanceEvent(4, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(4, "jump", 1, ['south']), DanceEvent(4, "hands", 1, ['ears']), MomentEnd(), DanceEvent(4, "r", 6, []), DanceEvent(4, "swipe", 2, ['low']), DanceEvent(4, "jump", 1, ['spot'])]


#it = ParsedDanceeventIterator()
#it.prepare(4, stream2)
#print(str(it.length))
#print(str(it))
