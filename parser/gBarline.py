from gData import GraphicData


class Barline(GraphicData):
  '''
  '''
  def __init__(self, style):
    self.minWidth = 4
    self.style = style
    
  def stencil(self):
    stencil = barline[self.style]
    return stencil



def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'MomentEnd')
  ctx.setProp('barlineStyle', '')
  
def process(ctx, event):
  # adapt text to include params?
  gd = Barline(ctx.getProp('barlineStyle'))
  # reset immediately
  ctx.setProp('barlineStyle', '')
  ctx.gList.append(gd)  
