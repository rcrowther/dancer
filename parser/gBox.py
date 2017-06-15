
from enums import Axis
from gInterval import *
from utils import SimplePrint


class gBox(SimplePrint):
  def __init__(self, intervalX, intervalY):
    self.boxX = intervalX
    self.boxY =  intervalY
    
  def boxX(self):
    return self.boxX

  def boxY(self):
    return self.boxY
  
  def isEmptyAll(self):
    return self.boxX and self.boxY
    
  def isEmpty(self, axis):
    if (axis == Axis.X):
      return self.boxX
    else:
      return self.boxY

  def scale(self, v):
    self.boxX.scale(v)
    self.boxY.scale(v)

    
  def translate(self, v):
    self.boxX.translate(v)
    self.boxY.translate(v)
    
  def centre(self):
    #! wrong, needs offset
    self.boxX.centre(v)
    self.boxY.centre(v)

  def extendString(self, b):
    b.append(str(self.boxX))
    b.append(', ')
    b.append(str(self.boxY))
