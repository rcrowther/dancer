


def before(ctx):
  print('...set stats')
  ctx.dispatcher.startSayingTo(process, 'Finish')
  
  
def process(ctx, e):
   ctx.reporter.info('barcount: {0}'.format(ctx._props['currentBarCount']))
   #! Tricky this. Count has right number of marks if last moment
   #! has duration to this point... 
   lastBeatOfLastBar = ctx._props['currentBarStart'] + ctx._props['beatsPerBar'] -1
   #!... we don't have that material, so this only works if there is
   #! a moment there, on the last beat.
   if( ctx._props['currentMoment'] < lastBeatOfLastBar):
      ctx.reporter.warning('Events do not fit into bar scheme:\n  last beat in last bar: {0}\n  anticipated last beat: {1}'.format(ctx._props['currentBarStart'],  lastBeatOfLastBar ))

def after(ctx):
  pass

  
