#!/usr/bin/python3

#from enum import Enum

EventType = {
  'CreateContext': 1,
  'DeleteContext': 2,
  'MergeProperty': 3,
  #SetProperty = 2
  'Prepare': 4,
  'MusicEvent': 5,
  'Finish': 6
}


EventTypeToString = { v: k for (k, v) in EventType.items()}
  
#! need DeleteProperty, sometime
#! use the word *Event, or not?
#! context is the conext ID.
class Event():
  def __init__(self, context, tpe):
    self.entitySuffix = 'Event'
    self._context = context
    self._tpe = tpe
      
  @property
  def context(self):
    return self._context

  @context.setter
  def tpe(self, context):
    self._context = context
    
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
    b.append(EventTypeToString[self.tpe])
    b.append(', ')
    b.append(str(self.context))
    self.extendString(b)
    b.append(')')
    return b
    
  def __str__(self):
    '''
    Print this tree.
    '''
    return "".join(self.addString([]))
    
        
    
class CreateContext(Event):
  def __init__(self, idx, name):
    Event.__init__(self, None, EventType['CreateContext'])
    self.entitySuffix = 'CreateContext'
    self._idx = idx
    self._name = name
      
  @property
  def idx(self):
    return self._idx

  @idx.setter
  def idx(self, idx):
    self._idx = idx
        
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name

          
  def extendString(self, b):
    b.append(', ')
    b.append(str(self.idx))
    b.append(', "')
    b.append(self.name) 
    b.append('"')

    

class DeleteContext(Event):
  def __init__(self, context):
    Event.__init__(self, context, EventType['DeleteContext'])
    self.entitySuffix = 'DeleteContext'




class MergeProperty(Event):
  def __init__(self, context, name, value):
    Event.__init__(self, context, EventType['MergeProperty'])
    self.entitySuffix = 'MergeProperty'
    self._name = name
    self._value = value
    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name

        
  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    self._value = value
          
  def extendString(self, b):
    b.append(', "')
    b.append(self.name)
    b.append('", ')
    b.append(str(self.value))          


            
class PrepareEvent(Event):
  '''
  @moment int, for now
  '''
  def __init__(self, context, moment):
    Event.__init__(self, context, EventType['Prepare'])
    self.entitySuffix = 'PrepareEvent'
    self._moment = moment
      
  @property
  def moment(self):
    return self._moment

  @moment.setter
  def moment(self, moment):
    self._moment = moment
    
  def extendString(self, b):
    b.append(', ')
    b.append(str(self.moment))
        
        
        
class MusicEvent(Event):
  def __init__(self, context, name, duration, params):
    Event.__init__(self, context, EventType['MusicEvent'])
    self.entitySuffix = 'MusicEvent'
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
    b.append(', "')
    b.append(self.name)
    b.append('", ')
    b.append(str(self.duration))
    b.append(', ')
    b.append(self.params)


class Finish(Event):
  def __init__(self):
    Event.__init__(self, None, EventType['Finish'])
    self.entitySuffix = 'Finish'
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
#e = PrepareEvent('context', 'moment')
#print(str(e))        
#e = MusicEvent('context', 'clap', 2, 'above')
#print(str(e))
#e = Finish()
#print(str(e))
