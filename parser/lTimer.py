import math
import events


'''
Keeps a barcount.
Needed by other modules
'''
def before(ctx):
  if(not ctx.readPropOption('beatsPerBar')):
    ctx.mergeProp('beatsPerBar', 4)
  ctx.mergeProp('currentBarCount', 1)
  ctx.mergeProp('currentBarStart', 0)
  ctx.dispatcher.startSayingTo(process, 'MomentStart')

  
  
def process(ctx, e):
  barTarget = ctx.readProp('currentBarStart') + ctx.readProp('beatsPerBar')

  if (e.moment >= barTarget):
    ctx.mergeProp('currentBarStart', barTarget)
    ctx.mergeProp('currentBarCount', ctx.readProp('currentBarCount') + 1)
    print('barNum: ' + str(ctx._props['currentBarCount']))
  return e

def after(properties):
  pass
