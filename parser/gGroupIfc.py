from gData import GraphicData
from gInterval import *

# like axis-group-interface?
#? inherited into what?
class GraphicGroupIfc():
  '''
  Style unused, but could be several things?
  @axes list of axes. For an  alignment grob, only one.
  '''
  def __init__(self):
    GraphicData.__init__(self, axes)
    self.children = []
    self.axes = axes
    self.children = []
    
  def add(self, gObj):
    for ax in self.axes:
      gObj.setParent(ax, self)
    #Pointer_group_interface::add_grob (me, ly_symbol2scm ("elements"), gObj);

  #def hasAxis(self):
  #  return
    
  def extent(self, axis):
    r = GIntervalEmpty()
    for obj in children:
      if (obj.dims):
        r.unionInterval(obj.cache[axis].extent)
    return r
    
  #! and a lot of pure/skyline/line break stuff...
    
  ############################################
def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'CreateContext')
  ctx.dispatcher.startSayingTo(process, 'DeleteContext')

def process(ctx, event):
  # adapt text to include params?
  gd = GraphicGroup(event)
  ctx.gList.append(gd)
