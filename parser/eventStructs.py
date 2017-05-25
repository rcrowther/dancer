#!/usr/bin/python3

from utils import SimplePrint


class EventStruct(SimplePrint):
  pass
  

class MoveStruct(EventStruct):
  def __init__(self, name, duration, params):
    assert(isinstance(name, str))
    assert(isinstance(duration, int))
    assert(isinstance(params, list))
    self.hasInputDuration = True
    self.name = name
    self.duration = duration
    self.params = params
    
  def extendString(self, b):
    b.append('"')
    b.append(self.name)
    b.append('", ')
    b.append(str(self.duration))
    b.append(', ')
    b.append(str(self.params))



class ManyMoveStruct(EventStruct):
  '''
  When one dancer performs many moves at the same time  e.g. clap/jump.
  This can be expressed by the input language,
  '''
  def __init__(self, moveStructs):
    #assert(isinstance(moveStructs, list))
    self.hasInputDuration = False
    self.moveStructs = moveStructs
    
  def extendString(self, b):
    b.append(str(self.moveStructs))


# is
class RestStruct(EventStruct):
  def __init__(self, duration):
    assert(isinstance(duration, int))
    self.hasInputDuration = True
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.duration))


    
class RepeatStruct(EventStruct):
  def __init__(self, duration, params):
    assert(isinstance(duration, int))
    assert(isinstance(params, str))
    self.hasInputDuration = False
    self.duration = duration
    self.params = params

  def extendString(self, b):
    b.append(str(self.duration))
    b.append(', "')
    b.append(str(self.params))
    b.append('"')    
    
    
class PropertyMergeStruct(EventStruct):
  def __init__(self, k, v):
    assert(isinstance(k, str))
    assert(isinstance(v, str))
    self.hasInputDuration = False
    self.k = k
    self.v = v
    
  def extendString(self, b):
    b.append('"')
    b.append(self.k)
    b.append('", "')
    b.append(str(self.v))
    b.append('"')

            
            
class PropertyDeleteStruct(EventStruct):
  def __init__(self, k):
    assert(isinstance(k, str))
    self.hasInputDuration = False
    self.k = k

  def extendString(self, b):
    b.append('"')
    b.append(self.k)
    b.append('"')
    
    
    
class BeatsPerBarChangeStruct(EventStruct):
  def __init__(self, count):
    assert(isinstance(count, int))
    self.hasInputDuration = False
    self.count = count

  def extendString(self, b):
    b.append(str(self.count))
    
    
    
class TempoChangeStruct(EventStruct):
  def __init__(self, tempo):
    assert(isinstance(tempo, int))
    self.hasInputDuration = False
    self.tempo = tempo

  def extendString(self, b):
    b.append(str(self.tempo))
    
    

class NothingStruct(EventStruct):
  def __init__(self, duration):
    assert(isinstance(duration, int))
    self.hasInputDuration = True
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.duration))
  

    
class SimultaneousEventsStruct(EventStruct):
  '''
  This event is used only in building an event stream from the
  parseer. It constructs 'twig' branches holding the simultaneous 
  events.
  The iterators reolve the twigs firs tinto batches of events, ten into
  events surrounded by MomentStart and MomentEnd, for printing, writing 
  down, etc. 
  '''
  def __init__(self, events):
    #assert(isinstance(duration, int))
    assert(isinstance(events, list))
    self.hasInputDuration = True
    #self.duration = duration
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
       
## test
#print(str(MoveStruct('clap', 2, ['above'])))
##print(str(ManyMoveStruct()))
#print(str(RestStruct(32)))
##print(str(RepeatStruct(32, '4')))
#print(str(PropertyMergeStruct('fig', '5')))
#print(str(PropertyDeleteStruct('fig')))
#print(str(NothingStruct(6)))
#print(str(BeatsPerBarChangeStruct(2)))
#print(str(TempoChangeStruct(62)))
