
from Position import NoPosition
from trees.Trees import *
import sys


class CompilationUnit():
  def __init__(self, ast):
    self.ast = ast
    self.score = None
    self.staves = []
    
    
    
class Phase():
  def __init__(self, name, compilationUnit, reporter):
    self._name = name
    self._compilationUnit = compilationUnit
    self._reporter = reporter

  @property
  def name(self):
    return self._name     

  @name.setter
  def name(self, name):
    self._name = name   
    
  @property
  def compilationUnit(self):
    return self._compilationUnit     

  @compilationUnit.setter
  def compilationUnit(self, compilationUnit):
    self._compilationUnit = compilationUnit 
        
  @property
  def reporter(self):
    return self._reporter 
    
  @reporter.setter
  def reporter(self, reporter):
    self._reporter = reporter 

  def error(self, msg):
      self.reporter.error(self.name + ': ' + msg, NoPosition)
      #? Might introduce some finness by allowing recovery sometimes?
      sys.exit(1)
        
        
class GatherInfoPhase(Phase):
  '''
  Assembles the compilation unit, runnind various verification tests. 
  Must always be first in the phase chain. Required.
  '''
  def __init__(self, compilationUnit, reporter):
    Phase.__init__(self, 'BaseInfo', compilationUnit, reporter)
    
    
  def process(self):
    ast = self.compilationUnit.ast
    for e in ast.children:
      # parser enforces these as always functions
      if (e.name == 'score'):        
        self.compilationUnit.score = e
    if (not self.compilationUnit.score):
      self.error('no "\\score" function found in root')

    for e in self.compilationUnit.score.children:
      if (e.name != 'staff'):
        self.error('can only have functions with name "staff" in a score: found: \\' + e.name)
      self.compilationUnit.staves.append(e.children)

        
class NormaliseInstructionsPhase(Phase):
  '''
  Turn functions in staves into plain instruction.
  Functions can not be serialised, not in JSON anyway. And it is the job
  of the parsing to sort them out, not a rendering engine.  
  Must always be first in the phase chain. Required.
  '''
  def __init__(self, compilationUnit, reporter):
    Phase.__init__(self, 'NormaliseInstructions', compilationUnit, reporter)
    
  def expandToSimultaneousInstruction(self, stave, idx, newChild):
    stave.pop(idx)
    insertIns = stave[idx - 1]
    if(not isinstance(insertIns, SimultaneousInstructions)):
      insertIns = SimultaneousInstructions()
      origI = stave.pop(idx - 1)
      # is insertBefore
      stave.insert(idx - 1, insertIns)
      insertIns.children.append(origI)
    insertIns.children.append(newChild)
    
  #! test recovered parameters
  def processStave(self, stave):
    #for idx, ins in enumerate(stave):
    i = 0
    l = len(stave)
    while (i < l):
      ins = stave[i]
      if (isinstance(ins, GenericFunction)):
        print(ins.name + " is genfunc")
        fname = ins.name
        if (fname == 'beatsPerBar'):
          #? can this be nicer?
          newChild = BeatsPerBar(ins.posParams[0])
          self.expandToSimultaneousInstruction(stave, i, newChild)
          i -= 1
          l -= 1
        elif (fname == 'tempo'):
          #? can this be nicer?
          newChild = Tempo(ins.posParams[0])
          self.expandToSimultaneousInstruction(stave, i, newChild)
          i -= 1
          l -= 1
        elif (fname == 'repeat'):
          # non-visual
          rIns = stave.pop(i)
          repeatCount = int(rIns.posParams[0])
          repeatBody = rIns.children
          
          # get alternative endings
          alts = []
          while(True):
            nxt = stave[i]
            if (isinstance(nxt, GenericFunction) and nxt.name == 'alternative'):
              alts.append(stave.pop(i).children)
            else:
              break
          altsLen = len(alts)
          if (altsLen > repeatCount):
            self.error('Count of //alternative endings exceeds count of //repeat: alt endings: {0} : repeats: {1}'.format(altsLen, repeatCount))
          j = repeatCount
          k = altsLen - 1
          while(j > 0):
            if (k >= 0):
              stave[i:i] = alts[k]
              k -= 1
            stave[i:i] = repeatBody
            j -= 1
          # May even be faster to do this, rather than add up
          l = len(stave)
          
        elif (fname == 'alternative'):
          self.error('//alternative not following //repeat')
        elif (fname == 'endBar'):
          # implies an engraver/layout?
          
          pass
        else:
          self.error('Unrecognised function in a \\staff :\\' + fname)
      i += 1
      pass
      
  def process(self):
    for s in self.compilationUnit.staves:
      self.processStave(s)
