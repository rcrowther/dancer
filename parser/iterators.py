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
    self.contextId = None

        
  
  def pendingMoment(self):
    '''
    Should be repeatedly callable without side effects
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
  '''
  Iterates a parsed event list.
  use prepare() to set data and contextId
  used in DancerContext
  '''
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
    DataIterator.__init__(self)
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
        self._pendingMomentIncrement = int(e.duration) 
      else:
        # handle simultaneous form
        # skip moment start
        self.cache = []
        self.curse += 1
        e = self._data[self.curse]
        longest = 0          
        while(not isinstance(e, MomentEnd)):
          if (isinstance(e, DanceEvent) and int(e.duration) > longest):
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

        



class ChildContextIterator(DataIterator):
  '''
  Interlaces events from child iterators by Moment.
  use prepare() to set data and contextId
  used in intermediade contexts like ScoreContext.
  '''
  def __init__(self):
    DataIterator.__init__(self)
    self._childIts = []
    self.pendingIterators = []
    #? MOMENT_EXHAUSTED
    self._pendingMoment = -1
  
  def prepare(self, contextId, data): 
    self.contextId = contextId
    self._childIts = data
    # need to ask our position
    self.stepForward()

  def addChild(self, it):
    self._childIts.append(it)
    
  def _deleteChild(self, uid):
    i = 0
    l = len(self._childIts)
    while(i < l):
      if (self._childIts[i].contextId == uid):
        self._childIts.pop(i)
        break
      else:
        i += 1
        
        
  def pendingMoment(self):
    return self._pendingMoment

  def stepForward(self):
    low = sys.maxsize 
    self.pendingIterators = []
    exhaustedIteratorIds = []
    for it in self._childIts:
      newLow = it.pendingMoment()
      if (newLow == MOMENT_EXHAUSTED):
        exhaustedIteratorIds.append(it.contextId)
      elif(newLow < low):
        low = newLow
        self.pendingIterators = [it]
      elif(newLow == low):
        self.pendingIterators.append(it)
    
    # delete exhausted iterators
    for uid in exhaustedIteratorIds:
      self._deleteChild(uid)

    # Now check anything left
    if (self._childIts):  
      self._pendingMoment = low
    else:
      self._pendingMoment = MOMENT_EXHAUSTED 

    
  def __next__(self):
    events = []
    for it in self.pendingIterators:
      events.extend(it.__next__())
    self.stepForward()    
    return events


class ParseCompileIterator(DataIterator):
  '''
  Inserts Moment events from pending calls.
  Can prepend and append extra events.
  Reduces clutches  of events to a steady stream of single events.
  use prepare() to set data and contextId
  used at base in GlobalContext.
  '''
  def __init__(self):
    DataIterator.__init__(self)
    self._childIt = None
    self._startEvents = None
    self._endEvents = None
    self.finished = False
    self.start = True
    self.eventsCache = []
   
  def prepare(self, contextId, data): 
    self.contextId = contextId
    self._startEvents = data[0]
    self._endEvents = data[1]
    self._childIt = data[2]
        
  def hasNext(self):
    return not self.finished or len(self.eventsCache) > 0
    
  def __next__(self):
    if (not self.eventsCache):
      if (self.start):
        self.start = False
        self.eventsCache.extend(self._startEvents)
        # Will return empty moment zero data...
        self._childIt.__next__()
      elif (not self._childIt.pendingMoment() == MOMENT_EXHAUSTED):
        self.eventsCache.append(MomentStart(self._childIt.pendingMoment()))
        self.eventsCache.extend(self._childIt.__next__())
        self.eventsCache.append(MomentEnd())
      else:
        if (not self.finished):
          self.finished = True
          self.eventsCache = self._endEvents
          #print('final' + ''.join(self.eventsCache))
      # reverse for easy popping
      self.eventsCache.reverse()
    return self.eventsCache.pop()


  def __str__(self):
    b = ''
    while(self.hasNext()):
      e = self.__next__()
      #for e in r:
      b += str(e)
      b += ', '
    return b
    

####################################################################
## Stream iterators ##

class StreamIterator(DataIterator):
  '''
  Iterates a compiled event queue.
  Stream must end with Finish()
  use prepare() to set data and contextId
  used to read compiled event streams.
  '''
  # 
  def __init__(self):
    DataIterator.__init__(self)
    self._data = None
    self.curse = 0
    self.length = 0

  def prepare(self, data): 
    self.length = len(data)
    self._data = data


  def hasNext(self):
    return self.curse < self.length 
    
    
  def __next__(self):
    r = self._data[self.curse]
    self.curse += 1   
    return r

  def __str__(self):
    b = ''
    while(self.hasNext()):
      e = self.__next__()
      #for e in r:
      b += str(e)
      b += ', '
    return b
    
    
    
#from events import *

#stream1 = [DanceEvent(6, "clap", 1, []), DanceEvent(6, "clap", 1, ['overhead']), DanceEvent(6, "step", 1, ['west']), MomentStart(-3), DanceEvent(6, "cross", 1, ['legs']), DanceEvent(6, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(6, "jump", 1, ['south']), DanceEvent(6, "hands", 1, ['ears']), MomentEnd(), DanceEvent(6, "bend", 1, ['knees']), DanceEvent(6, "slap", 1, ['other']), DanceEvent(6, "slap", 2, ['knees']), DanceEvent(6, "twirl", 1, ['right']), DanceEvent(6, "split", 1, ['knees']), DanceEvent(6, "turn", 1, ['west']), MergeProperty(6, "beatsPerBar", 3), MergeProperty(6, "tempo", 80), DanceEvent(6, "kick", 1, ['low'])]
#stream2 = [DanceEvent(4, "clap", 1, []), DanceEvent(4, "clap", 1, ['overhead']), DanceEvent(4, "step", 1, ['west']), MomentStart(-3), DanceEvent(4, "cross", 1, ['legs']), DanceEvent(4, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(4, "jump", 1, ['south']), DanceEvent(4, "hands", 1, ['ears']), MomentEnd(), DanceEvent(4, "r", 6, []), DanceEvent(4, "swipe", 2, ['low']), DanceEvent(4, "jump", 1, ['spot'])]


#it1 = ParsedDanceeventIterator()
#it1.prepare(4, stream1)
#it2 = ParsedDanceeventIterator()
#it2.prepare(5, stream2)
##print(str(it.length))
##print(str(it))

#cit = ChildContextIterator()
#cit.prepare(8, [it1, it2])
##print(str(it.length))
##print(str(cit))

#pit = ParseCompileIterator()
#pit.prepare(0, [[CreateContext(0, 0, 'Global')], [Finish()], cit])
##print(str(len(pit._childIts)))
#print(str(pit))

########################################
#eStream = [
#CreateContext(0, 0, "Global"),
#CreateContext(0, 5, "Score"),
#CreateContext(5, 6, "Dancer"),
#CreateContext(5, 7, "Dancer"),
#MergeProperty(0, "performer", "Bacup"),
#MergeProperty(0, "style", "clog"),
#MergeProperty(0, "tempo", 120),
#MergeProperty(0, "title", "Coconutters"),
#MergeProperty(0, "beatsPerBar", 4),
#MergeProperty(0, "dancers", 3),
#MergeProperty(0, "date", None),
#MomentStart(1),
#DanceEvent(6, "clap", 1, []),
#DanceEvent(7, "clap", 1, []),
#MomentEnd(),
#MomentStart(2),
#DanceEvent(6, "clap", 1, ['overhead']),
#DanceEvent(7, "clap", 1, ['overhead']),
#MomentEnd(),
#Finish()
#]

#it = StreamIterator()
#it.prepare(eStream)
#print(str(it))
