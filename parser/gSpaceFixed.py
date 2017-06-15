
import gData
from gInterval import *

# from lily/item.cc
class SpaceFixed(gData.GraphicData):
  '''
  A gData with fixed-size spacing e.g. notes, barlines, etc.
  '''
  def __init__(self, isMusical, offsetX, offsetY, sizeX, sizeY):
    gData.GraphicData.__init__(self, offsetX, offsetY, sizeX, sizeY)
    self.isMusical = isMusical
    
  def getColumnOption(self):
    parent = self.getParent(Axis.X)
    return self.parent.getColumn() if (parent) else None
    
  def getSystemOption(self):
    parent = self.getParent(Axis.X)
    return parent.system if (parent) else None


  def spannedColumnIdInterval(self):
    c = self.getColumn().uid
    return Interval(c, c)

  #'def pure_height (self, Grob *g, start, end):
  #  if (cached_pure_height_valid_)
  #    return cached_pure_height_ + pure_relative_y_coordinate (g, start, end)
  # Note: cached_pure_height_ does not notice if start changes, implicitly
  #   assuming that Items' pure_heights do not depend on 'start' or 'end'.
  #   Accidental_interface::pure_height(), however, does depend on 'start'.
  

  #  cache_pure_height (pure_height(self, start, end))
  #  return cached_pure_height_ + pure_relative_y_coordinate (g, start, end)

#? Most of rest to do with breaking and rendering?


    
#class StencilData(GraphicData):
  #'''
  #render info is _x, _y,
  #'''
  #def __init__(self, offsetX, offsetY, sizeX, sizeY, stencilName, stencilStyle):
    #GraphicData.__init__(self, offsetX, offsetY, sizeX, sizeY)
    #self.stencilName = stencilName
    #self.stencilStyle = stencilStyle
    
  #def __str__(self):
    #return "{0}".format(type(self.stencil)._name__)
    

