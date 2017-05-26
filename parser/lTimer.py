import math
import events


'''
Keeps a barcount.
Needed by other modules
'''
def before(ctx):
  if(not ctx.readPropOption('beatsPerBar')):
    ctx.mergeProp('beatsPerBar', 4)
  # Moments in the first bar are bar 1
  ctx.mergeProp('currentBarCount', 0)
  # want the first target sum to equal 1, so put into netherland
  ctx._props['currentBarStart'] = 1 - ctx._props['beatsPerBar']
  # as per definition
  ctx.mergeProp('currentMoment', 0)
  ctx.dispatcher.startSayingTo(process, 'MomentStart')

  
  
def process(ctx, e):
  ctx._props['currentMoment'] = e.moment
  # Fly calculation catches any beatsPerBar changes
  barTarget = ctx._props['currentBarStart'] + ctx._props['beatsPerBar']
  #print('...MomentStart'+ str(e.moment))
  if (e.moment >= barTarget):
    ctx._props['currentBarStart'] = barTarget
    ctx._props['currentBarCount'] += 1
    print('barNum: ' + str(ctx._props['currentBarCount']))
  return e

def after(ctx):
  pass
