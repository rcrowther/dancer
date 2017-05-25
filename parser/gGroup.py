from gData import GraphicData


# like axis-group-interface?
class GraphicGroup(GraphicData):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self):
    GraphicData.__init__(self)
    self.children = []
    
def before(ctx):
  ctx.dispatcher.startSayingTo(process, 'CreateContext')
  ctx.dispatcher.startSayingTo(process, 'DeleteContext')

def process(ctx, event):
  # adapt text to include params?
  gd = GraphicGroup(event)
  ctx.gList.append(gd)
