



from enums import GDisplay, FontStyle, Axis
from gCacheData import *
from gInterval import *
    
    
# like grob?
#http://lilypond.org/doc/v2.18/Documentation/learning/outside_002dstaff-objects#grob-sizing
class GraphicData():
  '''
  Style unused, but could be several things?
  '''
  #? original has lots of gear for 'set from this user-defined property'
  #? which I am skipping
  def __init__(self, offsetX, offsetY, sizeX, sizeY):
    self.cache = [0, 0, 0, 0]
    self.cache[Axis.X] = GCacheData(offsetX, None, GInterval(offsetX, sizeX + offsetX))
    self.cache[Axis.Y] =  GCacheData(offsetY, None, GInterval(offsetY, sizeY + offsetY))
    self.cache[Axis.NO_AXES] = GCacheDataEmpty()
    
    ## tree
    #self.parentX = None
    #self.parentY = None
    
    ## position
    # ok, a grid. Given our issue that dance moves, the majority of 
    # printing, are fonts, set a font-height as one virtual unit.
    # the grid is located top left.
    # All glyph printing is top left (no, this is not natural).
    
    # internal. Calculated values.
    self._x = 0
    self._y = 0

    #self._width = 1
    #self._height = 1
    
    # absolute positioning from parents needs offsets. 
    # Could use padding top/left, but here special.
    #self.offsetX = 0
    #self.offsetY = 0
    
    # new
    #self.sizeX = 1
    #self.sizeY = 1

    # Extents are the surrounding box from the print point, top left.
    # These values are used for overall sibling calculations.
    self.extentTop = 0
    self.extentRight = 1
    self.extentBottom = 1
    self.extentLeft = 0

  
    # The above positioning is not natural for a user. Nor experienced
    # users like an API user.
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
    # new
  def offsetX(self):
    '''
    @return an int
    '''
    return self.cache[Axis.X].offset
    
  def offsetY(self):
    '''
    @return an int
    '''
    return self.cache[Axis.Y].offset
    
  def sizeX(self):
    '''
    @return an interval
    '''
    return self.cache[Axis.X].extent

  def sizeY(self):
    '''
    @return an interval
    '''
    return self.cache[Axis.Y].extent

  def axisScale(self, axis, offset):
    self.cache[axis].offset += offset

  def offsetRelative(self, gData, axis):
    if (gData == self): 
      return 0.0
    else:
      o = self.cache[axis].offset
      o += self.cache[axis].parent.offset_relative(gData, axis)
      return o
  
  def getOffset(self, axis):
    return self.cache[axis].offset
    
  def flushExtent(self, axis):
    self.cache[axis].extent = GIntervalEmpty()
    p = get_parent(axis)
    if (p):
      p.flushExtent(axis)
        
  def extent(self, axis):
    return self.cache[axis].extent
    
  def width(self):
    return self.cache[Axis.X].extent
    
  def height(self):
    return self.cache[Axis.Y].extent
      
      
  def getParent(self, axis):
    return self.cache[axis].parent

  def setParent(self, axis, p):
    self.cache[axis].parent = p

  #! prob need more, like mutual parent, etc.
  def root(self):
    o = self
    #get root by going doen parents
    while (not isinstance(o.parent, gRoot)):
      o = o.parent
    return o
    

  def setExtents(self):
    self.extentTop = self.paddingTop
    self.extentRight = self.paddingLeft + self.width + self.paddingRight
    self.extentBottom = self.paddingTop + self.height + self.paddingBottom
    self.extentLeft = self.paddingLeft


  def __str__(self):
    return "{0}".format(type(self)._name__)



