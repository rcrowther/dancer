#!/usr/bin/python3

#from enum import Enum


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

class Event():
  '''
  Where relevant, context id is the parent. For property events, is the
  local context id.
  @contextId unique id of the context
  '''
  def __init__(self, contextId):
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
  def __init__(self,  contextId):
    Event.__init__(self, contextId)

  def extendString(self, b):
    b.append(str(self.contextId))




class MergeProperty(Event):
  '''
  @contextId the local context (not the parent of the context)
  '''
  def __init__(self, contextId, key, value):
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
    b.append('", ')
    b.append(str(self.value))          



class DeleteProperty(Event):
  '''
  @contextId the local context (not the parent of the context)
  '''
  def __init__(self, contextId, key):
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
  @contextId the parent context
  '''  
  def __init__(self, contextId, name, duration, params):
    Event.__init__(self, contextId)
    self._name = name
    self._duration = duration
    self._params = params

    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name
    
  @property
  def duration(self):
    return self._duration

  @duration.setter
  def duration(self, duration):
    self._duration = duration
    
  @property
  def params(self):
    return self._params

  @params.setter
  def params(self, params):
    self._params = params

  def extendString(self, b):
    b.append(str(self.contextId))
    b.append(', "')
    b.append(self.name)
    b.append('", ')
    b.append(str(self.duration))
    b.append(', ')
    b.append(str(self.params))


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
    
#e = CreateContext(4, 'staff')
#print(str(e))

#e = DeleteContext('context')
#print(str(e))
#e = MergeProperty('context', 'indent-stave', 2)
#print(str(e))
#e = MomentStart('context', 'moment')
#print(str(e))        
#e = DanceEvent('context', 'clap', 2, 'above')
#print(str(e))
#e = Finish()
#print(str(e))
