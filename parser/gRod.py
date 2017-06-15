from utils import SimplePrint



# lily/rod.cc
class Rod(SimplePrint):
  def __init__(self):
    self.fromItem = None
    self.toItem = None
    self.distance = 0
    
  def columnize(self):
    if(not self.fromItem or not self.toItem):
      return
    i = self.fromItem.getColumn()
    self.fromItem = i
    j = self.toItem.getColumn()
    self.toItem = j
    # The original is not this, but for now...    
    #          distance_ += -d * item_drul_[d]->relative_coordinate (pc, X_AXIS);
    self.distance = j.relativeCoordinate(Axis.X) - i.relativeCoordinate(Axis.X)
    
  def addToCols(self, fromItem, toItem):
    self.columnize()
    if (self.fromItem and self.toItem and (self.fromItem != self.toItem)):
      #Spaceable_grob::add_rod(self.fromItem, self.toItem, self.distance)
      pass
