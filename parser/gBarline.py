#from gData import StencilData
from gSpaceFixed import SpaceFixed


class Barline(SpaceFixed):
  '''
  '''
  def __init__(self,  style):
    SpaceFixed.__init__(self,
    isMusical = False,
    offsetX = 0,
    offsetY = 0,
    sizeX = 0.2, 
    sizeY = 25
    )
    self.style = style




def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'MomentEnd')
  ctx._props['barlineStyle'] = None
  
def process(ctx, event):
  # adapt text to include params?
  #gd = Barline(ctx._props.get('barlineStyle'))
  # reset immediately
  #ctx._props['barlineStyle'] = None
  #ctx.gList.append(gd) 
  pass 
