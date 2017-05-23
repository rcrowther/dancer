

# like grob?
class GraphicData():
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, text, style):
    self.parent = None
    
    # position
    self.relativeX = 0
    self.relativeY = 0
    # x + width
    self.extentX = 0
    # y + height
    self.extentY = 0
    self.minimumExtentX = 1
    self.minimumExtentY = 1
    #? How relate to relative y?
    #? step variable?
    self.staffPosition = 0

    # graphic properties
    self.stencil = None
    self.colour = None
    self.properties = []
    
    
 
