from gData import TextData
from enums import FontStyle

class DanceMove(TextData):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, text, duration):
    TextData.__init__(self, 0, 0, 1, 12, text)
    # duration can change the print style
    self.duration = duration

    # push down a little
    #self.yOffset = 0.25



    

def before(ctx):
  #?! damm. A rest is a DanceMove?
  ctx.dispatcher.startSayingTo(process, 'MoveEvent')
  ctx.dispatcher.startSayingTo(endProcess, 'MomentEnd')
  ctx._props['moveEvents'] = []
  
  
def endProcess(ctx, event):
  #print('.........clear')
  #print (''.join(str(moveEvents)))
  for e in ctx._props['moveEvents']:
    # set the text
    #! more options here
    txt = e.name
    gd = DanceMove(txt, e.duration)
    #! make_item or layout_proc puts them someplace, as process_music
    #! doesn't return them???
    #! announce_grob, creation_callback in engraver? 
    # typeset according to duration
    if (gd.duration > 1):
      gd.fontStyle = FontStyle.Italic
      
  ctx._props['moveEvents'] = []
   

def process(ctx, event):
  ctx._props['moveEvents'].append(event)
  print (''.join(str(ctx._props['moveEvents'])))

  # adapt text to include params?
  #print('ne...')
  #txt = event.name
  #gd = DanceMove(txt, event.duration)
  #ctx.gRoot.append(gd)  
