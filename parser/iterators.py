#!/usr/bin/python3


from events import *
#from eventStructs import *
import sys


MOMENT_PARSEDSTART = -3
# -2 moment = finished stream
MOMENT_EXHAUSTED  = -2
# -1 moment = pre-play stream
# No, thatsMoment = 0 now.
MOMENT_PREPLAY  = -1



#! Should be ParseDataIterators
class DataIterator():
  '''
  Iterate over data given to Dancer code by parsers.
  '''
  def __init__(self):
    self.contextId = None

        
  
  def pendingMoment(self):
    '''
    leaf iterators should be repeatedly callable without side effects.
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
#x
class ParsedDanceeventIterator(DataIterator):
  '''
  Iterates a parsed event list.
  use prepare() to set data and contextId
  Returns pending duration, then a clutch of calls. These clutches are 
  based on finding events in input which have real uration (property 
  changes, tempo signals and similar activity are bundled into the 
  current clutch)
  Used after parsing, in a DancerContext, iterating parsed dancemove data.
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
  # So, currently, chain length is monitored.
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

    while (self.curse < self.length):
      e = self._data[self.curse]
      self.curse += 1 
      if(not(e.hasInputDuration)):
        self.cache.append(e)
      else:
        break

    if (self.curse < self.length):
        
      # even if simultaneous, has a length
      if (not(isinstance(e, SimultaneousEventsEvent))):
        # it's just a move
        self.cache.append(e)
        self._pendingMomentIncrement = e.duration 
      else:
        xe = e.events
        longest = 0
        for ee in xe:
          if (
            ee.hasInputDuration
            and ee.duration > longest
            ):
            longest = ee.duration
          self.cache.append(ee)
        self._pendingMomentIncrement = longest 
    else:
      if (not self.cache):
        # kill. the above test means this will not run until the last cached 
        # entry is returned by __next__
        self._pendingMomentIncrement = 0 
        self._pendingMoment = MOMENT_EXHAUSTED    
    #self.curse += 1
    return r

        

class ParsedEventIterator(DataIterator):
  '''
  Iterates a parsed event list.
  use prepare() to set data and contextId
  Returns pending duration, then a clutch of calls. These clutches are 
  based on finding events in input which have real uration (property 
  changes, tempo signals and similar activity are bundled into the 
  current clutch)
  Used after parsing, in a DancerContext, iterating parsed dancemove data.
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
  # So, currently, chain length is monitored.
  # PendingMoment can not be resolved without caching.
  
  def __init__(self, context):
    #assert(context == DancerContext)
    DataIterator.__init__(self)
    self._data = None
    # No before material in a parsed list. First moment is one..
    self._pendingMoment = 1
    self._pendingIncrement = 0
    self.curse = 0
    self.cache = []
    self.stepped = False
    self.contextId = context.uid
    self.context = context


  def stepForward(self):
    if (not self.stepped):
      self.cache = []
  
      # get material
      try:
        # skip until some event with length appears      
        while (True):
          e = self.context.children[self.curse]
          self.curse += 1 
          if(not(e.hasInputDuration)):
            self.cache.append(e)
          else:
            break
    
  
        if (not(isinstance(e, SimultaneousEventsEvent))):
          # a move
          self.cache.append(e)
          self._pendingIncrement = e.duration 
        else:
          # simultaneous
          xe = e.events
          
          # find longest event in there
          longest = 0
          for ee in xe:
            if (
              ee.hasInputDuration
              and ee.duration > longest
              ):
              longest = ee.duration
            self.cache.append(ee)
          self._pendingIncrement = longest 
  
      except IndexError:
        # exhaused data.
        # may have cached non-duration items (e.g. barlines)
        # The argument for doing nothing goes like this;
        # the previous next() worked out where this pending moment
        # will be. So pending moment or increment calculation is not
        # needed.
        # And, next iteration, cache is emptied only to except again.
        # This time, pending moment is st to exhausted. 
        if (not self.cache):
          # set directly. 
          self._pendingMoment = MOMENT_EXHAUSTED    
      
      
    
    
  def pendingMoment(self):
    self.stepForward()
    self.stepped = True
    return self._pendingMoment 
                 
  def __next__(self):
    self._pendingMoment += self._pendingIncrement
    self.stepped = False
    return self.cache


#x
class ChildContextIterator(DataIterator):
  '''
  Interlaces events from child iterators by Moment.
  has pendingMoment, and returns clutches of events, like 
  ParsedDanceeventIterator, which should be children to this.
  Use prepare() to set data and contextId
  Used on parsed data, in intermediade contexts like ScoreContext.
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


class ChildContextIterator2(DataIterator):
  '''
  Interlaces events from child iterators by Moment.
  Has pendingMoment, and returns clutches of events, like 
  ParsedDanceeventIterator.
  Use prepare() to set data and contextId
  pendingMoment() can not be called twice.
  Used on parsed data, in intermediate contexts like ScoreContext
  or Staff Group.
  '''
  def __init__(self, context):
    DataIterator.__init__(self)
    self.pendingIterators = []
    self._pendingMoment = MOMENT_EXHAUSTED
    self.stepped = False
    self.contextId = context.uid
    self.context = context


  def _deleteChild(self, uid):
    i = 0
    l = len(self.context.children)
    while(i < l):
      if (self.context.children[i].uid == uid):
        self.context.children.pop(i)
        break
      else:
        i += 1
        

  def stepForward(self):
    if(not self.stepped):
      # get material 
      low = sys.maxsize 
      self.pendingIterators = []
      exhaustedIteratorIds = []
      for ctx in self.context.children:
        newLow = ctx.it.pendingMoment()
        if (newLow == MOMENT_EXHAUSTED):
          exhaustedIteratorIds.append(ctx.uid)
        elif(newLow < low):
          low = newLow
          self.pendingIterators = [ctx.it]
        elif(newLow == low):
          self.pendingIterators.append(ctx.it)
      
      # delete exhausted iterators
      for uid in exhaustedIteratorIds:
        self._deleteChild(uid)
  
      # Now check existance of iterators to provide data
      if (self.pendingIterators):  
        self._pendingMoment = low
      else:
        self._pendingMoment = MOMENT_EXHAUSTED 


  def pendingMoment(self):
    self.stepForward()
    self.stepped = True
    return self._pendingMoment

    
  def __next__(self):
    self.stepped = False
    events = []
    for it in self.pendingIterators:
      events.extend(it.__next__())
    return events


#########################################################
from EventIterators import EventIterator, EventIterator2

#x
# Aside from the prepare(), this is an EventIterator 
class ParseCompileIterator(EventIterator):
  '''
  Inserts Moment events into a stream, working from pendingMoments calls.
  Can prepend and append extra events.
  Reduces clutches of events to a steady stream of single events.
  use prepare() to set data and contextId
  used at base in GlobalContext.
  '''
  def __init__(self, srcName):
    EventIterator.__init__(self, srcName)
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
    
  def next(self):
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


  #def __str__(self):
    #b = ''
    #while(self.hasNext()):
      #e = self.__next__()
      ##for e in r:
      #b += str(e)
      #b += ', '
    #return b
    

    
    

class ClutchToStreamIterator(EventIterator2):
  '''
  Reduces clutches of events to a steady stream, adding moment marks.
  Can only work with one child
  Use in GlobalContext, after child-combine iteration ends.
  '''
  # The API interface here is an EventIterator 
  def __init__(self, context):
    EventIterator2.__init__(self)
    #assert(context == GlobalContext)
    self.eventsCache = []
    self.pendingMoment = MOMENT_EXHAUSTED
    self.contextId = context.uid
    self.context = context
    

  def hasNext(self):
    self.pendingMoment = self.context.children[0].it.pendingMoment()
    return self.pendingMoment != MOMENT_EXHAUSTED or len(self.eventsCache) > 0

    
  def next(self):
    if (not self.eventsCache):
      if (self.pendingMoment != MOMENT_EXHAUSTED):
        self.eventsCache.append(MomentStart(self.pendingMoment))
        self.eventsCache.extend(self.context.children[0].it.__next__())
        self.eventsCache.append(MomentEnd())
        # reverse for easy popping
        self.eventsCache.reverse()
        
    return self.eventsCache.pop()



class ParseIterator(EventIterator2):
  '''
  Prepend and append extra events to an event stream.
  Works on a steady stream of single events.
  Wraps a parsing GlobalContext to create an event iterator.
  '''
  # The API interface here is an EventIterator 
  def __init__(self, context, startEvents, endEvents):
    EventIterator2.__init__(self)

    self.startEvents = startEvents
    # reverse for easy popping
    self.startEvents.reverse() 
        
    self.endEvents = endEvents
    # reverse for easy popping
    self.endEvents.reverse()
    
    self.iteratorExhausted = False
    self.endLoaded = False

    self.context = context
    self.contextId = context.uid
        
  def hasNext(self):
    self.iteratorExhausted = not(self.context.it.hasNext())
    return not self.iteratorExhausted or len(self.endEvents) > 0
    
  def next(self):
    r = None

    if (self.startEvents):
      r = self.startEvents.pop()
    elif (not self.iteratorExhausted):
      r = self.context.it.next()
    else:
      r = self.endEvents.pop()

    return r


######################################################################
from events import *

stream1 =  [MoveEvent(3, 'clap', 1, []), MoveEvent(3, 'clap', 1, ['overhead']), MoveEvent(3, 'step', 1, ['west']), SimultaneousEventsEvent([MoveEvent(3, 'cross', 1, ['legs']), MoveEvent(3, 'cross', 1, ['hands'])]), SimultaneousEventsEvent([MoveEvent(3, 'jump', 1, ['south']), MoveEvent(3, 'hands', 1, ['ears'])]), MoveEvent(3, 'bend', 1, ['knees']), MoveEvent(3, 'slap', 1, ['other']), MoveEvent(3, 'slap', 2, ['knees']), MoveEvent(3, 'twirl', 1, ['right']), MoveEvent(3, 'split', 1, ['knees']), MoveEvent(3, 'turn', 1, ['west']), BeatsPerBarChangeEvent(3, 3), TempoChangeEvent(3, 80), MoveEvent(3, 'kick', 1, ['low']), BarlineEvent(4, 'end')]
#stream2 =  [MoveEvent(4, 'clap', 1, []), MoveEvent(4, 'clap', 1, ['overhead']), MoveEvent(4, 'step', 1, ['west']), SimultaneousEventsEvent([MoveEvent(4, 'cross', 1, ['legs']), MoveEvent(4, 'cross', 1, ['hands'])]), SimultaneousEventsEvent([MoveEvent(4, 'jump', 1, ['south']), MoveEvent(4, 'hands', 1, ['ears'])]), RestEvent(4, 6), MoveEvent(4, 'swipe', 2, ['low']), MoveEvent(4, 'jump', 1, ['spot']), BarlineEvent(4, 'end')]


#it1 = ParsedDanceeventIterator()
#it1.prepare(4, stream1)
#it2 = ParsedDanceeventIterator()
#it2.prepare(5, stream2)
###print(str(it.length))
#print(str(it1))

#cit = ChildContextIterator()
#cit.prepare(8, [it1, it2])
####print(str(it.length))
##print(str(cit))

#pit = ParseCompileIterator('qih')
#pit.prepare(0, [[CreateContext(0, 0, 'Global')], [Finish()], cit])
##print(str(len(pit._childIts)))
#print(str(pit))

################################################
