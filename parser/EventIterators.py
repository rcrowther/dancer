#!/usr/bin/python3





#x
class EventIterator():
  '''
  Iterate over event data.
  '''
  def __init__(self, srcName):
    self._srcName = srcName

  @property
  def srcName(self):
    return self._srcName
        
  
  def hasNext(self):
    '''
    Should be repeatedly callable without side effects
    '''
    return False
          
  def next(self):
    '''
    On parse, return single events
    '''
    pass
     
  def __str__(self):
    b = ''
    while(self.hasNext()):
      b += str(self.next())
      b += '\n'
    return b
    

class EventIterator2():
  '''
  Iterate over event data.
  '''
  
  def hasNext(self):
    '''
    Should be called before next()
    Not repeatedly callable
    '''
    return False
          
  def next(self):
    '''
    On parse, return single events
    '''
    pass
     
  def __str__(self):
    b = ''
    while(self.hasNext()):
      b += str(self.next())
      b += '\n'
    return b
    
    
####################################################################
## Event iterators ##

#x Use SrcIterators.EventIterator?
#? Well, its an example EventIterator, but is it needed?
class EventIteratorList(EventIterator):
  '''
  Iterates a compiled event queue.
  Stream must end with Finish()
  use prepare() to set data and contextId
  used to read compiled event streams.
  '''
  # 
  def __init__(self, lst):
    EventIterator.__init__(self, 'internal list')
    self._data = lst
    self.curse = 0
    self.length = len(lst)


  def hasNext(self):
    return self.curse < self.length 
    
    
  def next(self):
    r = self._data[self.curse]
    self.curse += 1   
    return r


class EventIteratorFile(EventIterator):
  '''
  Iterates a compiled event queue.
  Stream must end with Finish()
  use prepare() to set data and contextId
  used to read compiled event streams.
  '''
  # 
  def __init__(self, inPath, encode='utf-8'):
    EventIterator.__init__(self, inPath)
    self.f = open(inPath, 'r', encoding=encode)
    self.cache = ''
    self.hasCached = False
    self.length = 0


  def hasNext(self):
    if (not self.hasCached):
      self.cache = self.f.readline()
      self.hasCached = True
    r = (self.cache != '')
    if (not r):
      self.f.close()
    return r
    
  #! needs splitting out
  #! no error checking, depends on regularity of source, including 
  #! hidden newline presence.
  #! shoddy code, revise sometime.
  def parse(self, line):
    params = None
    event = None
    if (line.startswith('CreateContext')):
      p = line[14:-2].split(', ')
      #print('@'.join(p))
      event = CreateContext(int(p[0]), int(p[1]), p[2][1:-1])
    elif (line.startswith('DeleteContext')):
      p = line[14:-2].split(', ')
      event = toEvent('DeleteContext', p)
    elif (line.startswith('MergeProperty')):
      p = line[14:-2].split(', ')
      event = toEvent('MergeProperty', p)
    elif (line.startswith('DeleteProperty')):
      p = line[15:-2].split(', ')
      event = toEvent('DeleteProperty', p)
    elif (line.startswith('MomentStart')):
      p = line[12:-2].split(', ')
      event = toEvent('MomentStart', p)
    elif (line.startswith('MomentEnd')):
      event = MomentEnd()
    elif (line.startswith('Finish')):
      event = Finish()
    elif (line.startswith('MoveEvent')):
      p = line[10:-2].split(', ')
      event = toEvent('MoveEvent', p)
    #elif (line.startswith('ManyMoveEvent')):
     # p = line[10:-2].split(', ') 
      #event = toEvent('ManyMoveEvent', p)
    elif (line.startswith('RestEvent')):
      p = line[10:-2].split(', ') 
      event = toEvent('RestEvent', p)
    elif (line.startswith('RepeatEvent')):
      p = line[12:-2].split(', ') 
      event = toEvent('RepeatEvent', p)
    elif (line.startswith('BeatsPerBarChangeEvent')):
      p = line[23:-2].split(', ') 
      event = toEvent('BeatsPerBarChangeEvent', p)
    elif (line.startswith('TempoChangeEvent')):
      p = line[17:-2].split(', ') 
      event = toEvent('TempoChangeEvent', p)
    elif (line.startswith('NothingEvent')):
      p = line[13:-2].split(', ') 
      event = toEvent('NothingEvent', p)
    else:
      print('Eventparser: unrecognised text input: {0}'.format(line))
    return event
    
  def next(self): 
    self.hasCached = False
    return self.parse(self.cache) 
    
    
########################################
from events import *
#from eventStructs import toEventStruct

#eventList = [
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

#it = EventIteratorList(eventList)
#print(str(it))

#inPath = '../test/test.dnc'
#it = EventIteratorFile(inPath)
#print(str(it))
