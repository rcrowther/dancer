from gData import StencilData


class Barline(StencilData):
  '''
  '''
  def __init__(self,  style):
    StencilData.__init__(self, 'barline')
    self.style = style
    
    self.width = 0
    self.height = 1
    self.paddingRight = 0.2
    self.paddingLeft = 0
    self.setExtents()



def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'MomentEnd')
  ctx._props['barlineStyle'] = None
  
def process(ctx, event):
  # adapt text to include params?
  gd = Barline(ctx.readPropOption('barlineStyle'))
  # reset immediately
  ctx.setProp('barlineStyle', None)
  ctx.gList.append(gd)  
