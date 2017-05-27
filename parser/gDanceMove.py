from gData import TextData
from enums import FontStyle

class DanceMove(TextData):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, text, duration):
    TextData.__init__(self, text)
    # duration can change the print style
    #self.duration = duration
    if (duration > 1):
      self.fontStyle = FontStyle.Italic
    # push down a little
    self.yOffset = 0.25



    
    
    
def before(ctx):
  #?! damm. A rest is a DanceMove?
  ctx.dispatcher.startSayingTo(process, 'MoveEvent')

def process(ctx, event):
  # adapt text to include params?
  #print('ne...')
  txt = event.name
  gd = DanceMove(txt, event.duration)
  ctx.gList.append(gd)  
