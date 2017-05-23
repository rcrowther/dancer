from gData import GraphicData


class DanceMove(GraphicData):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, text, duration):
    self.text = text
    # duration changes the move style
    self.duration = duration
    #self.style = style
  
  def font(self):
    font = 'normal'
    if (self.duration > 1):
      font = 'italic'
    return font
    

    
def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'DanceEvent')

def process(ctx, event):
  # adapt text to include params?
  txt = event.name
  gd = DanceMove(txt, event.duration)
  ctx.gList.append(gd)  
