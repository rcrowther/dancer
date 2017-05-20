import math
import events

beatsPerBar = 4

def before(properties):
  if(not properties.get('beatsPerBar')):
    properties['beatsPerBar'] = 4
  properties['barCount'] = 0
  properties['barStartMoment'] = 1
  
  
def process(properties, e):
  #! dispatch to correct context
  if (isinstance(e, events.MergeProperty)):
    properties[e.key] = e.value
  #! dispatch to correct context
  if (isinstance(e, events.DeleteProperty)):
    del (properties[e.key])    
  barTarget = properties['barStartMoment'] + properties['beatsPerBar']

  if (isinstance(e, events.MomentStart) and e.moment >= (properties['barStartMoment'] + properties['beatsPerBar'])):
    properties['barStartMoment'] += properties['beatsPerBar']
    properties['barCount'] += 1
    print('bar: ' + str(properties['barCount']))
  return e
