from gData import GraphicData


class DanceMove(GraphicData):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, text, duration):
    GraphicData.__init__(self)
    self.text = text
    # duration can change the print style
    self.duration = duration
    #self.style = style
  
  def font(self):
    font = 'normal'
    if (self.duration > 1):
      font = 'italic'
    return font
    
  def __str__(self):
    return "{0}".format(self.text)
    
    
    
def before(ctx):
  #?! damm. A rest is a DanceMove?
  ctx.dispatcher.startSayingTo(process, 'DanceEvent')

def process(ctx, event):
  # adapt text to include params?
  txt = event.name
  gd = DanceMove(txt, event.duration)
  ctx.gList.append(gd)  
