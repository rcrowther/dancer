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
  
#! need DeleteProperty, sometime
#! use the word *Event, or not?
#! context is the conext ID.
class Event():
  '''
  @parentId parent context id (for property events, the local context id)
  '''
  def __init__(self, parentId, tpe):
    self.entitySuffix = type(self).__name__
    self._parentId = parentId
    self._tpe = tpe
      
  @property
  def parentId(self):
    return self._parentId

  @parentId.setter
  def parentId(self, parentId):
    self._parentId = parentId
    
  @property
  def tpe(self):
    return self._tpe
        
  @tpe.setter
  def tpe(self, tpe):
    self._tpe = tpe

  def extendString(self, b):
    pass
    
  def addString(self, b):
    b.append(self.entitySuffix)
    b.append('(')
    #b.append(EventTypeToString[self.tpe])
    #b.append(', ')
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
  @newType is currently a string 'score', 'dancer' etc.
  '''
  def __init__(self, parentId, newId, newType):
    Event.__init__(self, parentId, EventType['CreateContext'])
    #self.entitySuffix = 'CreateContext'
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
    b.append(str(self.parentId))
    b.append(', ')
    b.append(str(self.newId))
    b.append(', "')
    b.append(self.newType)
    b.append('"')

    

class DeleteContext(Event):
  def __init__(self, uId):
    Event.__init__(self, uId, EventType['DeleteContext'])
    self.uId = uId

  def extendString(self, b):
    b.append(str(self.uId))



class MergeProperty(Event):
  '''
  @parentId the local context (not the parent of the context)
  '''
  def __init__(self, parentId, key, value):
    Event.__init__(self, parentId, EventType['MergeProperty'])
    #self.entitySuffix = 'MergeProperty'
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
    b.append(str(self.parentId))
    b.append(', "')
    b.append(self.key)
    b.append('", ')
    b.append(str(self.value))          


class DeleteProperty(Event):
  '''
  @parentId the local context (not the parent of the context)
  '''
  def __init__(self, parentId, key):
    Event.__init__(self, parentId, EventType['DeleteProperty'])
    self._key = key
    
  @property
  def key(self):
    return self._key
    
  @key.setter
  def key(self, key):
    self._key = key
          
  def extendString(self, b):
    b.append(str(self.parentId))
    b.append(', "')
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
    Event.__init__(self, 0, EventType['MomentStart'])
    #self.entitySuffix = 'MomentStart'
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
    Event.__init__(self, 0, EventType['MomentEnd'])

  def extendString(self, b):
    pass
                
        
class DanceEvent(Event):
  def __init__(self, parentId, name, duration, params):
    Event.__init__(self, parentId, EventType['DanceEvent'])
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
    b.append(str(self.parentId))
    b.append(', "')
    b.append(self.name)
    b.append('", ')
    b.append(str(self.duration))
    b.append(', ')
    b.append(str(self.params))


class Finish(Event):
  def __init__(self):
    Event.__init__(self, 0, EventType['Finish'])
    #self.entitySuffix = 'Finish'
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
