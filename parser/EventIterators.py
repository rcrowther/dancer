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
      params = line[13:]
      p = params[1:-2].split(', ')
      #print('@'.join(p))
      event = CreateContext(int(p[0]), int(p[1]), p[2][1:-1])
    elif (line.startswith('DeleteContext')):
      params = line[13:]
      p = params[1:-2].split(', ')
      event = DeleteContext(int(p[0]), int(p[1]))
    elif (line.startswith('MergeProperty')):
      params = line[13:]
      p = params[1:-2].split(', ')
      event = MergeProperty(int(p[0]), p[1][1:-1], p[2])
    elif (line.startswith('DeleteProperty')):
      params = line[14:]
      p = params[1:-2].split(', ')
      event = DeleteProperty(int(p[0]), p[1][1:-1])
    elif (line.startswith('MomentStart')):
      params = line[11:]
      p = params[1:-2].split(', ')
      event = MomentStart(int(p[0]))
    elif (line.startswith('MomentEnd')):
      #params = line[14:]
      #p = params[1:-1].split(', ')
      event = MomentEnd()
    elif (line.startswith('DanceEvent')):
      params = line[10:]
      p = params[1:-2].split(', ')
      event = DanceEvent(int(p[0]), int(p[1]), p[2][1:-1], int(p[3]), p[4])
    elif (line.startswith('Finish')):
      #params = line[14:]
      #p = params[1:-1].split(', ')
      event = Finish()
    else:
      print('Eventparser: unrecognised text input:'.format(line))
    return event
    
  def next(self): 
    self.hasCached = False
    return self.parse(self.cache) 
    
    
########################################
from events import *


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
