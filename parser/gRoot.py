
# from 'system.cc'
#! needs revist.
class GraphicRoot():
  def __init__(self):
    self.uid = 0
    # id, parent, child
    self.parentX = []
    self.parentY = []
    self.contexts = []
    self.objects = []
    
    self.currentVerticalAlign = []
    self.currentVerticalAlignMaxWidth = 0
    
  def newMoment(self):
    for e in self.currentVerticalAlign:
      e.extentRight = currentVerticalAlignMaxWidth
    self.currentVerticalAlignMaxWidth = 0
    self.currentVerticalAlign = []

  def append(self, gObj):
    self.uid += 1
    self.parentX.append()
    self.parentY.append()
    self.contexts.append()
    self.objects.append(gObj)
    #if(gObj):    
    
#def get_root_system(gOb)
# def get_vertical_alignment(gOb)
#def part_of_line_pure_height
#get"vertical-alignment"
#calc_pure_relevant_grobs()
#def get_maybe_spaceable_staves(gOb)
#get"vertical-alignment"
