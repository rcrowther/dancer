

# like grob?
#http://lilypond.org/doc/v2.18/Documentation/learning/outside_002dstaff-objects#grob-sizing
class GraphicData():
  '''
  Style unused, but could be several things?
  '''
  def __init__(self):
    ## tree
    self.parent = None
    
    ## position
    #? Relative to sibling or parent?
    #? parent I think, so initially zero except for compound
    #? marks
    self.xOffset = 0
    self.yOffset = 0
    # ok, a grid. Given our issue that dance moves, the majority of 
    # printing, are fonts, set a font-height as one virtual unit.
    # x + width
    self.width = 1
    #? sensible default
    # y + height
    self.height = 12
    # glue
    #? am I interested right now?
    #self.minWidth = self._width
    #self.minHeight = self._height
    #! Relate to yOffset
    #? Only applies to staff-placed marks
    #? step variable?
    self.staffPosition = 0

    ## graphic
    # Only applies to stenciled graphics
    self.stencil = None
    self.colour = 'black'
    self.properties = []

