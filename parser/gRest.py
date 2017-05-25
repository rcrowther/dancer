from gData import GraphicData


class Rest(GraphicData):
  '''
  '''
  def __init__(self, duration):
    GraphicData.__init__(self)
    # duration changes the rest shape
    self.duration = duration
    
    self.width = 0.5
    if (self.duration > 1):
      self.width = 1
    #self.minWidth = self.width
    
    #self.style = style
    self.staffPosition = -3 
    
  def stencil(self):
    stencil = 'squiggle'
    if (self.duration > 1):
      stencil = 'squashed-squiggle'
    return stencil
    
    
def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'DanceEvent')
  
def process(ctx, event):
  # adapt text to include params?
  gd = Rest(event.duration)
  ctx.gList.append(gd)  
