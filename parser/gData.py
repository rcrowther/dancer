



from enums import GDisplay, FontStyle

    
# like grob?
#http://lilypond.org/doc/v2.18/Documentation/learning/outside_002dstaff-objects#grob-sizing
class GraphicData():
  '''
  Style unused, but could be several things?
  '''
  def __init__(self):
    ## tree
    self.parent = None
    self.sibling = None
    
    ## position
    # ok, a grid. Given our issue that dance moves, the majority of 
    # printing, are fonts, set a font-height as one virtual unit.
    # the grid is located top left.
    # All glyph printing is top left (no, this is not natural).
    
    # internal. Final pos values.
    self._x = 0
    self._y = 0
    
    # Display by offset from sibling (FLOW) or exactly on parent PARENT?
    # split into X/Y behaviour, because this program needs the below
    # default mostly.
    self.xDisplay = GDisplay.Flow
    self.yDisplay = GDisplay.Parent

    # positioning from parents needs offsets. 
    # Could use padding top/left, but here special.
    self.xOffset = 0
    self.yOffset = 0

    # Extents are the surrounding box from the print point, top left.
    # These values are used for overall sibling calculations.
    self.extentTop = 0
    self.extentRight = 1
    self.extentBottom = 1
    self.extentLeft = 0
    
    
    # The above positioning is not natural for a user. Nor experienced
    # like an API user.
    # They must sum the size of the printing with the extensions
    # They can use these instead, then setExtents()
    self.width = 1
    self.height = 1
    
    self.paddingTop = 0
    self.paddingRight = 0.25
    self.paddingBottom = 0.25
    self.paddingLeft = 0
    
    # x11/CSS color names as a simple list
    self.colour = 7
    

    #self.properties = []


    def setExtents(self):
      self.extentTop = self.paddingTop
      self.extentRight = self.paddingLeft + self.width + self.paddingRight
      self.extentBottom = self.paddingTop + self.height + self.paddingBottom
      self.extentLeft = self.paddingLeft

    def x():
      if (self.xDisplay == GDisplay.Parent):
        return parent.x() + self.xOffset
      else:
        return sibling.x() + sibling.extentRight

    def y():
      if (self.yDisplay == GDisplay.Parent):
        return parent.y() + self.yOffset
      else:
        return sibling.y() + sibling.extentBottom
     
     
class StencilData(GraphicData):
  '''
  render info is _x, _y,
  '''
  def __init__(self, stencil):
    GraphicData.__init__(self)
    self.stencil = stencil
    
  def __str__(self):
    return "{0}".format(type(self.stencil)._name__)
    
    
    
      
class TextData(GraphicData):
  '''
  render info is _x, _y, and attributes here.
  '''
  def __init__(self, text):
    GraphicData.__init__(self)
    ## Text
    self.text = text
    # normal, italic, oblique, smallcaps
    self.fontStyle = FontStyle.Normal
    self.fontBold = False
    #? Ever use this, or preset?
    self.fontSize = 12
    
    
  def __str__(self):
    return "{0}".format(self.text)
