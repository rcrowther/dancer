

from Position import Position, NoPosition

#  Base class for AST nodes
#! so what is a bar indication?
class Node():
  def __init__(self):
    self.entitySuffix = 'Node'
    self.children = []
    
  def addChildren(self, b):
    b.append('[')
    first = True
    for e in self.children:
      if (first):
        first = False
      else:
        b.append(", ")
      e.addString(b)
    b.append(']')
    
  def extendString(self, b):
    pass

  def addString(self, b):
    b.append(self.entitySuffix)
    b.append('(')
    self.extendString(b)
    self.addChildren(b)
    b.append(')')
    return b
    
  def __str__(self):
    '''
    Print this tree.
    '''
    return "".join(self.addString([]))  

## Base nodes ##

     
# An Instruction is an event, has a time
# may be a structuring element, though, not an instruction for a dancer
# or a direction for visusl lsyout?
# See Move
class Instruction(Node):
  def __init__(self, isMove):
    Node.__init__(self)
    self.entitySuffix = 'Instruction'
    self._isMove = isMove
    
  @property
  def isMove(self):
    return self._isMove

  @isMove.setter
  def params(self, isMove):
    self._isMove = isMove



class MoveInstruction(Instruction):
  def __init__(self):
    Instruction.__init__(self, True)
    self.entitySuffix = 'Instruction'
    self._isMove = isMove
    
  # kill this, never has children
  def addChildren(self, b):
   pass
   
## Generic nodes ##
class Root(Node):
  def __init__(self):
    Node.__init__(self)
    self.entitySuffix = 'Root'

class GenericFunction(Node):
  def __init__(self, name, posParams, namedParams): 
    Node.__init__(self)
    self.entitySuffix = 'GenericFunction'
    self._name = name
    self._posParams = posParams
    self._namedParams = namedParams
    
  @property
  def name(self):
    return self._name     

  @name.setter
  def name(self, name):
    self._name = name   
    
  @property
  def posParams(self):
    return self._posParams 
    
  @posParams.setter
  def posParams(self, posParams):
    self._posParams = posParams 
    
  @property
  def namedParams(self):
    return self._namedParams 
    
  @namedParams.setter
  def namedParams(self, name):
    self._namedParams = namedParams 

  def extendString(self, b):
     b.append(self.name)    
     b.append(', ')    
     b.append(str(self.posParams))    
     #b.append(self.name)    
    
#! revise so fits Instruction
#! so Tempo, etc.
class GenericInstruction(Instruction):
  # defsults to isMove == True
  def __init__(self, cmd, duration, params):
    Instruction.__init__(self, True)
    self.entitySuffix = 'GenericInstruction'
    self._cmd = cmd
    self._duration = duration
    self._params = params
    
  @property
  def cmd(self):
    return self._cmd

  @cmd.setter
  def cmd(self, cmd):
    self._cmd = cmd
    
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

  # kill this, never has children
  def addChildren(self, b):
   pass
   
  def extendString(self, b):
     b.append(self.cmd)    
     b.append(', ')    
     b.append(str(self.duration))  
 
#? do this way, or with a seperate body?
class GenericSimultaneous(Node):
  def __init__(self):
    Node.__init__(self)
    self.entitySuffix = 'GenericSimultaneous'

 
class SimultaneousInstructions(Node):
  def __init__(self):
    Node.__init__(self)
    self.entitySuffix = 'SimultaneousInstructions'

 ###################################################################            
# Context has no time
# It is used for overall dance control
# For dancer, initially, has little use beyond carrying credits.
# However, it could carry many overall details of how we render
# to text?
class Context(Node):
  def __init__(self):
    Node.__init__(self)
    self.entitySuffix = 'Context'


class Score(Context):
  def __init__(self):
    Context.__init__(self)
    self.entitySuffix = 'Score'
    
class Dancer(Context):
  def __init__(self, name):
    Context.__init__(self)
    self.entitySuffix = 'Dancer'
    self.name = name
    
  @property
  def name(self):
    return self.name     
     
     


## Non-move instructions ##
class Repeat(Instruction):
  
  def __init__(value, body, alternatives):
    Instruction.__init__(self, False)
    self.entitySuffix = 'Repeat'
    self._value = value
    self.body = body
    self._alternatives = alternatives
    
  @property
  def value(self):
    return self._value
    
  @value.setter
  def value(self, value):
    self._value = value
    
  @property
  def alternatives(self):
    return self._alternatives

  @alternatives.setter
  def alternatives(self, alternatives):
    self._alternatives = alternatives


class BeatsPerBar(Instruction):
  def __init__(self, value):
    Instruction.__init__(self, False)
    self.entitySuffix = 'BeatsPerBar'
    self._value = value
    
  @property
  def value(self):
    return self._value
    
  @value.setter
  def value(self, value):
    self._value = value

  def extendString(self, b):
     b.append(self.value)

  # kill this, never has children
  def addChildren(self, b):
   pass
    
    
class Tempo(Instruction):  
  def __init__(self, value):
    Instruction.__init__(self, False)
    self.entitySuffix = 'Tempo'
    self._value = value
    
  @property
  def value(self):
    return self._value
    
  @value.setter
  def value(self, value):
    self._value = value

  def extendString(self, b):
     b.append(self.value)    

  # kill this, never has children
  def addChildren(self, b):
   pass
     
         
## Move instructions ##
# A move is something that a dancer will do
class Move(Instruction):
  def __init__(name, duration, params):
    Instruction.__init__(self, True)
    self.entitySuffix = 'Move'
    self.name = name
    self.duration = duration
    self.params = params
    
  @property
  def name(self):
    return self.name
    
  @property
  def duration(self):
    return self.duration

  @property
  def params(self):
    return self.params



class Rest(Move):
  def __init__(duration):
    Move.__init__(self, 'rest', duration)
    self.entitySuffix = 'Rest'
    self.name = name
    self.duration = duration
    self.params = params
    
  @property
  def name(self):
    return self.name
    
  @property
  def duration(self):
    return self.duration

  @property
  def params(self):
    return self.params
