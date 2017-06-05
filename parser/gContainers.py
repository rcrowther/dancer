

#! might have special staff groups?

class Container(GraphicData):
  '''
  render info is _x, _y,
  '''
  def __init__(self):
    GraphicData.__init__(self)
    # Display by offset from sibling (FLOW) or exactly on parent PARENT?
    # split into X/Y behaviour, because this program needs the below
    # default mostly.
    # GDisplay.Flow
    # GDisplay.Parent
    self.displayX = None
    self.displayY = None
    

class Box(Container):
  def __init__(self):
    Container.__init__(self)
    self.displayX = GDisplay.Absolute
    self.displayY = GDisplay.Absolute
    
  #def addObj(self, gObj):
  #  gObj.parentY = self
    
  def height(self):
    sz = 0
    # and descendant children?
    for c in children:
      sz += c.offsetY 
      sz += c.height
    return sz    



class VAlign(Container):
  def __init__(self):
    Container.__init__(self)
    self.displayX = GDisplay.Absolute
    self.displayY = GDisplay.Flow
    
  #def addObj(self, gObj):
  #  gObj.parentY = self
    
  def height(self):
    sz = 0
    # and descendant children?
    for c in children:
      sz += c.offsetY 
      sz += c.height
    return sz

    
class HAlign(Container):
  def __init__(self):
    Container.__init__(self)
    self.displayX = GDisplay.Flow
    self.displayY = GDisplay.Absolute
    
  #def addObj(self, gObj):
  #  gObj.parentY = self
    
  def width(self):
    sz = 0
    # and descendant children?
    for c in children:
      sz += c.offsetX 
      sz += c.width
    return sz
