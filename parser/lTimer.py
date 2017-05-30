import math
import events


'''
Keeps a barcount.
Needed by other modules
'''
def before(ctx):
  print('...before setup')
  if(not ctx._props.get('beatsPerBar')):
    ctx._props['beatsPerBar'] = 4
  # Moments in the first bar are bar 1
  ctx._props['currentBarCount'] = 0
  # want the first target sum to equal 1, so put into netherland
  #ctx._props['currentBarStart'] = 1 - ctx._props['beatsPerBar']
  # as per definition
  #ctx._prop['currentMoment'] = 0
  ctx.dispatcher.startSayingTo(process, 'BarlineEvent')


  
def process(ctx, e):
  #ctx._props['currentMoment'] = e.moment
  # Fly calculation catches any beatsPerBar changes
  #barTarget = ctx._props['currentBarStart'] + ctx._props['beatsPerBar']
  #print('...MomentStart'+ str(e.moment))
  #if (e.moment >= barTarget):
  #  ctx._props['currentBarStart'] = barTarget
  #  ctx._props['currentBarCount'] += 1
  print('ctx: {0} barNum: {1}'.format(ctx.uid, ctx._props['currentBarCount']))
  ctx._props['currentBarCount'] += 1

def after(ctx):
  pass
