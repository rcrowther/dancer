#!/usr/bin/python3

#import dancerPDF
import modern

ALL_DANCERS = -1

D_ACTION = 0
D_ISMOVE = 1
D_TARGET = 2
D_ISMANYBEAT = 3
D_PARAMS = 4

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


# bar lines do or do not need to be stated near signatures?
# barlines are trailing. Not at start. Must be one at the end.
# For internal time signatures, must still be a bar.
# tempo must come before time mark
# repeats should not be expanded if notation is intended
dance = {
  'title': 'War Games',
  'performers': 'EastWest',
  'description': "Originating in Bacup, the Coconutters have been described as The Most Original Dance Group in England. Nobody else would dare.",
  'transcribed': 'Robert Crowther',
  'tempo': 60,
  'beatbar' : 4,
  'dancerCount': 2,
  'start': 'hline',
  'moves': [
  ['tempoMark', False, 0, False, 70],
  ['timeMark', False, 0, False, 4],
  
  ['kick', True, 0, False, WEST],
  ['kick', True, 1, False, EAST],
  ['clap', True, 0, False, WEST],
  ['step', True, 1, False, EAST],
  ['bar', 0, False, 70],

  ['step', True, 1, False, EAST],
  ['point', True, 0, False, EAST],
  ['point', True, 1, False, WEST],
  ['step', True, 1, False, WEST],
  ['repeatOpenBar', False, 0, False, 70],

  ['step', True, 0, False, EAST],
  ['point', True, 0, False, SOUTH],
  ['step', True, 0, False, SOUTH],
  ['point', True, 1, False, EAST],
  ['repeatCloseBar', False, 0, False, 70],

  ['point', True, 0, False, NORTH],
  ['step', True, 0, False, NORTH],
  ['point', True, 0, False, SOUTH],
  ['point', True, 1, False, WEST],
  ['bar', False, 0, False, 70],
  ##
  ['point', True, 0, False, WEST],
  ['point', True, 1, False, EAST],
  ['clap', True, 0, False, WEST],
  ['step', True, 1, False, EAST],
  ['bar', False, 0, False, 70],

  ['step', True, 1, False, EAST],
  ['point', True, 0, False, EAST],
  ['point', True, 1, False, WEST],
  ['step', True, 1, False, WEST],
  ['bar', False, 0, False, 70],

  ['step', True, 0, False, EAST],
  ['point', True, 0, False, SOUTH],
  ['step', True, 0, False, SOUTH],
  ['point', True, 1, False, EAST],
  ['bar', False, 0, False, 70],

  ['point', True, 0, False, NORTH],
  ['step', True, 0, False, NORTH],
  ['point', True, 0, False, SOUTH],
  ['point', True, 1, False, WEST],
  
  ['closeBar', False, 0, False, 70],
  ['EOD', False, ALL_DANCERS, False, None]
  ]
}


      
#########################################################
## Demo ##

#g = dancerPDF.DancerPDF()
g = modern.Modern()

## Titles ##

g.title(dance['title'])
g.titleCredits(dance['performers'], dance['transcribed'])


mbr = g.movesblock()



## body ##


i = 0
m = dance['moves']
l = len(m)
while(i < l):
  mbr.addInstruction(m[i])
  i += 1


#path = c.beginPath()
#path.moveTo(inch * 4, inch * 4)
#path.lineTo(inch * 3, inch * 4)
#path.lineTo(inch * 3.5, inch * 5)
#path.lineTo(inch * 4, inch * 4)

# stroke/fill
#c.drawPath(path, True, True)

g.save()

