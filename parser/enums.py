#!/usr/bin/python3


# Display by sibling relative (FLOW) or parent absolute ParentAbs?
# First sibling is taken from parent, so is in practice ParentAbs
class GDisplay():
  Flow = 0
  Parent = 1

  def toString(self, x):
    if (x == GDisplay.Flow): return 'Flow'
    elif (x == GDisplay.Parent): return 'Parent'
    else: print('unrecognised GDisplay value: ' + x)
    
#danceEventClassesToString = {v:k for k, v in danceEventClasses.items()}

class FontStyle():
  Normal = 0
  Italic = 1
  Oblique = 2
  Smallcaps = 3

  def toString(self, x):
    if (x == FontStyle.Normal): return 'Normal'
    elif (x == FontStyle.Italic): return 'Italic'
    elif (x == FontStyle.Oblique): return 'Oblique'
    elif (x == FontStyle.Smallcaps): return 'Smallcaps'
    else: print('unrecognised FontStyle value: ' + x)
