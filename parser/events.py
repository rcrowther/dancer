#!/usr/bin/python3

#from enums import danceEventClasses, danceEventClassesToString

from eventStructs import EventStruct
from utils import SimplePrint


# Why a type property? A hangover from C++, and also because I don't
# want to be too Python.
EventType = {
  'CreateContext': 1,
  'DeleteContext': 2,
  'MergeProperty': 3,
  'DeleteProperty': 4,
  'MomentStart': 5,
  'MomentEnd': 6,
  'DanceEvent': 7,
  'Finish': 8
}


EventTypeToString = { v: k for (k, v) in EventType.items()}
  
#! use the word *Event, or not?
#! context is sometimes the parent when relevent, or surrounding self.
#! use SimplePrint
class Event():
  '''
  Where relevant, context id is the parent. For property events, is the
  local context id. It always exists, but where can be implied, is not
  printed.
  @contextId unique id of the context
  '''
  def __init__(self, contextId):
    assert(isinstance(contextId, int))
    self.entitySuffix = type(self).__name__
    self._contextId = contextId

    
  @property
  def contextId(self):
    return self._contextId

  @contextId.setter
  def contextId(self, contextId):
    self._contextId = contextId
    
  def extendString(self, b):
    pass
    
  def addString(self, b):
    b.append(self.entitySuffix)
    b.append('(')
    self.extendString(b)
    b.append(')')
    return b
    
  def __str__(self):
    '''
    String representation of this class.
    The representation is valid constructor code.
    '''
    return "".join(self.addString([]))
    
        
    
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
    b.append(', "')
    b.append(self.key)
    b.append('", "')
    b.append(str(self.value))          
    b.append('"')



class DeleteProperty(Event):
  '''
  @contextId the local context (not the parent of the context)
  '''
  def __init__(self, contextId, key):
    assert(isinstance(key, str))
    Event.__init__(self, contextId)
    self._key = key
    
  @property
  def key(self):
    return self._key
    
  @key.setter
  def key(self, key):
    self._key = key
          
  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', "')
    b.append(self.key)
    b.append('"')

    
    
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
    Event.__init__(self, 0)

    
  def extendString(self, b):
    pass               
        
        
        
class DanceEvent(Event):
  '''
  The struct sub-categorises DanceEvents. Usually its name will suggest
  an engraver.
  structs are found in eventStructs.
  @contextId the parent context
  @struct data for dance events. This is a sub-class, see EventStructs.
  '''  
  def __init__(self, contextId, struct):
    assert(isinstance(struct, EventStruct))
    Event.__init__(self, contextId)
    self._struct = struct


  @property
  def struct(self):
    return self._struct
    
  @struct.setter
  def klass(self, struct):
    self._struct = struct
        


  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', ')
    b.append(str(self.struct))
    #b.append(', "')
    #b.append(self.name)
    #b.append('", ')
    #b.append(str(self.duration))
    #b.append(', ')
    #b.append(str(self.params))


class Finish(Event):
  def __init__(self):
    Event.__init__(self, 0)
    self._moment = -2

  @property
  def moment(self):
    return self._moment

  @moment.setter
  def moment(self, moment):
    self._moment = moment
    
    
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
#e = DanceEvent(3, (MoveStruct('clap', 2, 'above')))
#print(str(e))
#e = Finish()
#print(str(e))
