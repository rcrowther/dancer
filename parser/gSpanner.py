


import gData
from gInterval import *

# from lily/item.cc
class Spanner(gData.GraphicData):
  '''
  A gData with fixed-size spacing e.g. notes, barlines, etc.
  '''
  def __init__(self, isMusical, offsetX, offsetY, sizeX, sizeY):
    gData.GraphicData.__init__(self, offsetX, offsetY, sizeX, sizeY)
    self.fromItem = None
    self.toItem = None
    # Moments
    self.spannedTime = Interval()
    self.spannedPaperCols = Interval()
    #self.length = 0
    
  def spannedPaperColInterval(self):
    
  #! wrong
  def length(self):
    i = self.fromItem.toRelativeCoordinate(None, Axis.X)
    j = self.toItem.toRelativeCoordinate(None, Axis.X)
    return j - i
    
  def getSystem(self):
    if (not self.fromItem or not self.toItem):
      return None
    s = self.fromItem.getSystem()
    t = self.toItem.getSystem()
    return None if (s != t) else: s
      
