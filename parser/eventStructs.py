#!/usr/bin/python3

from utils import SimplePrint


class EventStruct(SimplePrint):
  '''
  The purpose of hasInputDuration: Events and EventStructs are built 
  directly from the parser. At that point, after the parse, we need to
  know which of the commands a user is summing, or should be summing,
  to make bars. Then we can tell if they intended a dance moment.
  
  The GlobalContext iterator, a ParseCompileIterator, makes sense of
  this by wrapping in momentStart/MomentEnd calls.
  '''
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


def toEventStruct(s, p):
  if (s == 'MoveStruct'): return MoveStruct(p[0], int(p[1]), eval(p[2]))
  elif (s == 'ManyMoveStruct'): return ManyMoveStruct(eval(p[0]))
  elif (s == 'RestStruct'): return RestStruct(int(p[0]))
  elif (s == 'RepeatStruct'): return RepeatStruct(int(p[0]), eval(p[1]))
  elif (s == 'PropertyMergeStruct'): return PropertyMergeStruct(p[0], p[1])
  elif (s == 'PropertyDeleteStruct'): return PropertyDeleteStruct(p[0])
  elif (s == 'BeatsPerBarChangeStruct'): return BeatsPerBarChangeStruct(int(p[0]))
  elif (s == 'TempoChangeStruct'): return TempoChangeStruct(int(p[0]))
  elif (s == 'NothingStruct'): return NothingStruct(int(p[0]))
  else:
    print('unrecognised eventStruct: name{0}'.format(s))
    
    
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
