#!/usr/bin/python3

from utils import SimplePrint


class EventStruct(SimplePrint):
  pass
  
  
class MoveStruct(EventStruct):
  def __init__(self, name, duration, params):
    assert(isinstance(name, str))
    assert(isinstance(duration, int))
    self.name = name
    self.duration = duration
    self.params = params
    
  def extendString(self, b):
    b.append('"')
    b.append(self.name)
    b.append('", ')
    b.append(str(self.duration))
    b.append(', "')
    b.append(str(self.params))
    b.append('"')



class ManyMoveStruct(EventStruct):
  '''
  When one dancer performs many moves at the same time  e.g. clap/jump.
  This can be expressed by the input language,
  '''
  def __init__(self, moveStructs):
    #assert(isinstance(duration, int))
    self.moveStructs = moveStructs
    
  def extendString(self, b):
    b.append(str(self.moveStructs))


  
class RestStruct(EventStruct):
  def __init__(self, duration):
    assert(isinstance(duration, int))
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.duration))


    
class RepeatStruct(EventStruct):
  def __init__(self, duration, alternatives):
    assert(isinstance(duration, int))
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.duration))
    
    
    
class PropertyMergeStruct(EventStruct):
  def __init__(self, k, v):
    assert(isinstance(k, str))
    assert(isinstance(v, str))
    self.k = k
    self.v = v
    
  def extendString(self, b):
    b.append('"')
    b.append(self.k)
    b.append('", ')
    b.append(str(self.v))
            
            
            
class PropertyDeleteStruct(EventStruct):
  def __init__(self, k):
    assert(isinstance(k, str))
    self.k = k

  def extendString(self, b):
    b.append('"')
    b.append(self.k)
    b.append('"')
    
    
    
class BeatsPerBarChangeStruct(EventStruct):
  def __init__(self, count):
    assert(isinstance(count, int))
    self.count = count

  def extendString(self, b):
    b.append(str(self.count))
    
    
    
class TempoChangeStruct(EventStruct):
  def __init__(self, tempo):
    assert(isinstance(tempo, int))
    self.tempo = tempo

  def extendString(self, b):
    b.append(str(self.tempo))
    
    
        
class NothingStruct(EventStruct):
  def __init__(self, duration):
    assert(isinstance(duration, int))
    self.duration = duration

  def extendString(self, b):
    b.append(str(self.duration))
    
    
## test
print(str(MoveStruct('clap', 2, 'above')))
print(str(RestStruct(32)))
print(str(PropertyMergeStruct('fig', '5')))
print(str(PropertyDeleteStruct('fig')))
print(str(NothingStruct(6)))
print(str(BeatsPerBarChangeStruct(2)))
print(str(TempoChangeStruct(62)))
