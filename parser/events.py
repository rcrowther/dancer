#!/usr/bin/python3

#from enums import danceEventClasses, danceEventClassesToString

#from eventStructs import EventStruct
from utils import SimplePrint

BROADCAST = -4
# Why a type property? A hangover from C++, and also because I don't
# want to be too Python.
#EventType = {
  #'CreateContext': 1,
  #'DeleteContext': 2,
  #'MergeProperty': 3,
  #'DeleteProperty': 4,
  #'MomentStart': 5,
  #'MomentEnd': 6,
  #'DanceEvent': 7,
  #'Finish': 8
#}


#EventTypeToString = { v: k for (k, v) in EventType.items()}
  
#! use the word *Event, or not?
#! context is sometimes the parent when relevent, or surrounding self.
#! use SimplePrint
class Event(SimplePrint):
  '''
  Where relevant, context id is the parent. For property events, is the
  local context id. It always exists, but where can be implied, is not
  printed.
  @contextId unique id of the context
  '''
  def __init__(self, contextId):
    assert(isinstance(contextId, int))
    self.hasInputDuration = False
    self._contextId = contextId

    
  @property
  def contextId(self):
    return self._contextId

  @contextId.setter
  def contextId(self, contextId):
    self._contextId = contextId
    
        
    
class CreateContext(Event):
  '''
  @contextId the id of the parent context
  @newId the id of the new context
  @newType is currently a string 'Score', 'Dancer' etc.
  '''
  def __init__(self, contextId, newId, newType):
    assert(isinstance(newId, int))
    assert(isinstance(newType, str))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self._newId = newId
    self._newType = newType
 
    
  @property
  def newId(self):
    return self._newId

  @newId.setter
  def newId(self, newId):
    self._newId = newId
        
  @property
  def newType(self):
    return self._newType
    
  @newType.setter
  def newType(self, newType):
    self._newType = newType

          
  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.newId))
    b.append(', "')
    b.append(self.newType)
    b.append('"')

    

class DeleteContext(Event):
  '''
  @contextId the id of the context
  '''
  def __init__(self, contextId, oldId):
    assert(isinstance(oldId, int))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self._oldId = oldId
 
    
  @property
  def oldId(self):
    return self._oldId

  @oldId.setter
  def oldId(self, oldId):
    self._oldId = oldId


  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.oldId))



class MergeProperty(Event):
  '''
  @contextId the local context (not the parent of the context)
  '''
  def __init__(self, contextId, key, value):
    assert(isinstance(key, str))
    assert(isinstance(value, str))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self._key = key
    self._value = value
    
  @property
  def key(self):
    return self._key
    
  @key.setter
  def key(self, key):
    self._key = key

        
  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    self._value = value
          
  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(self.key)
    b.append(', ')
    b.append(str(self.value))          



class DeleteProperty(Event):
  '''
  @contextId the local context (not the parent of the context)
  '''
  def __init__(self, contextId, key):
    assert(isinstance(key, str))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self._key = key
    
  @property
  def key(self):
    return self._key
    
  @key.setter
  def key(self, key):
    self._key = key
          
  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(self.key)

    
    
class MomentStart(Event):
  '''
  For consistency, has a parent Id, but always set to 0.
  Special moments
  - -1: before Dancer parses
  - -2: List in content has ended
  - -3: Dummy for marking simultaneous music during a parse. Before 
  music streams are interleaved and moment marked inserted.  
  @moment int, for now
  '''
  def __init__(self, moment):
    assert(isinstance(moment, int))
    Event.__init__(self, 0)
    self.hasInputDuration = False
    self._moment = moment
    
  @property
  def moment(self):
    return self._moment

  @moment.setter
  def moment(self, moment):
    self._moment = moment
    
  def extendString(self, b):
    b.append(str(self.moment))
        
        
        
class MomentEnd(Event):
  '''
  For consistency, has a parent Id, but always set to 0.
  @moment int, for now
  '''
  def __init__(self):
    Event.__init__(self, BROADCAST)
    self.hasInputDuration = False

    
  def extendString(self, b):
    pass               
        
        
        
#class DanceEvent(Event):
  #'''
  #The struct sub-categorises DanceEvents. Usually its name will suggest
  #an engraver.
  #structs are found in eventStructs.
  #@contextId the parent context
  #@struct data for dance events. This is a sub-class, see EventStructs.
  #'''  
  #def __init__(self, contextId, struct):
    #assert(isinstance(struct, EventStruct))
    #Event.__init__(self, contextId)
    #self._struct = struct


  #@property
  #def struct(self):
    #return self._struct
    
  #@struct.setter
  #def klass(self, struct):
    #self._struct = struct
        


  #def extendString(self, b):
    #b.append(str(self.contextId))
    #b.append(', ')
    #b.append(str(self.struct))



class Finish(Event):
  def __init__(self):
    Event.__init__(self, 0)
    self.hasInputDuration = False
    self._moment = -2

  @property
  def moment(self):
    return self._moment

  @moment.setter
  def moment(self, moment):
    self._moment = moment
    
    

########################## Dancer events ###############################

#class DisplayDance(Event):
  #def __init__(self):
    #Event.__init__(self, 0)
    #self.hasInputDuration = False
    
class MoveEvent(Event):
  def __init__(self,  contextId,  name, duration, params):
    assert(isinstance(name, str))
    assert(isinstance(duration, int))
    assert(isinstance(params, list))
    Event.__init__(self, contextId)
    self.hasInputDuration = True
    self.name = name
    self.duration = duration
    self.params = params
    
  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(", ")
    b.append(self.name)
    b.append(", ")
    b.append(str(self.duration))
    b.append(', ')
    b.append(str(self.params))



class ManyMoveEvent(Event):
  '''
  When one dancer performs many moves at the same time  e.g. clap/jump.
  This can be expressed by the input language,
  '''
  def __init__(self, contextId, moveEvents):
    #assert(isinstance(moveEvents, list))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self.moveEvents = moveEvents
    
  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.moveEvents))


class RestEvent(Event):
  def __init__(self, contextId, duration):
    assert(isinstance(duration, int))
    Event.__init__(self, contextId)
    self.hasInputDuration = True
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.duration))


    
class RepeatEvent(Event):
  def __init__(self, contextId, duration, params):
    assert(isinstance(duration, int))
    assert(isinstance(params, list))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self.duration = duration
    self.params = params

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.duration))
    b.append(', "')
    b.append(str(self.params))
    b.append('"')    
    

    
    
class BeatsPerBarChangeEvent(Event):
  def __init__(self, contextId, count):
    assert(isinstance(count, int))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self.count = count

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.count))
    
    
    
class TempoChangeEvent(Event):
  def __init__(self, contextId, tempo):
    assert(isinstance(tempo, int))
    Event.__init__(self, contextId)
    self.hasInputDuration = False
    self.tempo = tempo

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.tempo))


    
class NothingEvent(Event):
  def __init__(self, contextId, duration):
    assert(isinstance(duration, int))
    Event.__init__(self, contextId)
    self.hasInputDuration = True
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.duration))


  

########################## Internal events ###############################
  
class SimultaneousEventsEvent(Event):
  '''
  This event is used only in building an event stream from the
  parser. It constructs 'twig' branches holding the simultaneous 
  events.
  The iterators resolve the twigs first into batches of events, ten into
  events surrounded by MomentStart and MomentEnd, for printing, writing 
  down, etc. 
  '''
  def __init__(self, events):
    assert(isinstance(events, list))
    Event.__init__(self, -1)
    self.hasInputDuration = True
    self.events = events
    
  def extendString(self, b):
    b.append('[')
    first = True
    for e in self.events:
      if (first):
        first = False
      else:
        b.append(", ")
      b.append(str(e)) 
    b.append(']')
    #b.append(str(self.duration)) 
    


class BarlineEvent(Event):
  def __init__(self, contextId, style):
    assert(isinstance(style, str))
    Event.__init__(self, contextId)
    self.style = style

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(", ")
    b.append(self.style)    
    #b.append("'")
    
    
def toEvent(s, p):
  '''
  Cheap and shoddy text to class.
  No internal events.  
  '''
  if (s == 'CreateContext'): return CreateContext(int(p[0]), int(p[1]), p[2])
  elif (s == 'DeleteContext'): return DeleteContext(int(p[0]), int(p[1]))
  elif (s == 'MergeProperty'): return MergeProperty(int(p[0]), p[1], p[2])
  elif (s == 'DeleteProperty'): return DeleteProperty(int(p[0]), p[1])
  elif (s == 'MomentStart'): return MomentStart(int(p[0]))
  elif (s == 'MomentEnd'): return MomentEnd()
    #elif (s == 'DanceEvent'): return DanceEvent(eval(p[0]))
  elif (s == 'Finish'): return Finish()
  elif (s == 'MoveEvent'): return MoveEvent(int(p[0]), p[1], int(p[2]), eval(p[3]))
  elif (s == 'ManyMoveEvent'): return ManyMoveEvent(int(p[0]), eval(p[0]))
  elif (s == 'RestEvent'): return RestEvent(int(p[0]), int(p[1]))
  elif (s == 'RepeatEvent'): return RepeatEvent(int(p[0]), eval(p[1]))
  #elif (s == 'PropertyMergeEvent'): return PropertyMergeEvent(p[0], p[1])
  #elif (s == 'PropertyDeleteEvent'): return PropertyDeleteEvent(p[0])
  elif (s == 'BeatsPerBarChangeEvent'): return BeatsPerBarChangeEvent(int(p[0]), int(p[0]))
  elif (s == 'TempoChangeEvent'): return TempoChangeEvent(int(p[0]), int(p[0]))
  elif (s == 'NothingEvent'): return NothingEvent(int(p[0]))
  elif (s == 'BarlineEvent'): return BarlineEvent(int(p[0]), p[1])
  else:
    print('unrecognised event: name{0}'.format(s))
    
    
### Test ###
#from eventStructs import *

#e = CreateContext(0, 1, 'staff')
#print(str(e))
#e = DeleteContext(0, 1)
#print(str(e))
#e = MergeProperty(1, 'indent-stave', '2')
#print(str(e))
#e = DeleteProperty(1, 'indent-stave')
#print(str(e))
#e = MomentStart(9)
#print(str(e)) 
#e = MomentEnd()
#print(str(e))        
##e = DanceEvent(3, (MoveStruct('clap', 2, 'above')))
##print(str(e))
#e = Finish()
#print(str(e))

#print(str(MoveEvent(3, 'clap', 2, ['above'])))
##print(str(ManyMoveEvent()))
#print(str(RestEvent(3, 32)))
#print(str(RepeatEvent(3, 4, [])))
##print(str(PropertyMergeEvent('fig', '5')))
##print(str(PropertyDeleteEvent('fig')))
#print(str(NothingEvent(3, 6)))
#print(str(BeatsPerBarChangeEvent(3, 2)))
#print(str(TempoChangeEvent(3, 62)))
