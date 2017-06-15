from gSpaceFixed import SpaceFixed
from enums import FontStyle


# Note heads engraver
#? Honestly, how does it get this infrmation out?
class DanceMove(SpaceFixed):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, text):
    SpaceFixed.__init__(self,
    isMusical = True,
    offsetX = 0,
    offsetY = 0,
    sizeX = 1, 
    sizeY = 25
    )
    self.text = text
    # normal, italic, oblique, smallcaps
    self.fontStyle = FontStyle.Normal
    self.fontBold = False
    #? Ever use this, or preset?
    self.fontSize = 12
    
        
  def __str__(self):
    return "{0}".format(self.text)

    # duration can change the print style
    #self.duration = duration

    # push down a little
    # set by stem, but matters little to us.
    #self.xOffset = 0
    #sef.yOffset = 0.25
    #self.xExtent = 1
    #self.yExtent = 12



    

def before(ctx):
  #?! damm. A rest is a DanceMove?
  ctx.dispatcher.startSayingTo(process, 'MoveEvent')
  ctx.dispatcher.startSayingTo(endProcess, 'MomentEnd')
  ctx._props['moveEvents'] = []
  
 
def process(ctx, event):
  ctx._props['moveEvents'].append(event)
  print (''.join(str(ctx._props['moveEvents'])))

  # adapt text to include params?
  #print('ne...')
  #txt = event.name
  #gd = DanceMove(txt, event.duration)
  #ctx.gRoot.append(gd)  
  
def endProcess(ctx, event):
  #print('.........clear')
  #print (''.join(str(moveEvents)))
  for e in ctx._props['moveEvents']:
    # set the text
    #! more options here
    txt = e.name
    gd = DanceMove(txt)
    #! make_item or layout_proc puts them someplace, as process_music
    #! doesn't return them???
    #! announce_grob, creation_callback in engraver? 
    # typeset according to duration
    if (e.duration > 1):
      gd.fontStyle = FontStyle.Italic
      
  ctx._props['moveEvents'] = []
   


