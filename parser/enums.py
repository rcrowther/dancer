#!/usr/bin/python3

class Axis():
  X = 0
  Y = 1
  NO_AXES = 2

  def swap(a):
    assert(a < 2)
    return Axis.X if (a == Axis.Y) else Axis.Y

  def toString(self, x):
    if (x == Axis.X): return 'Axis.X'
    elif (x == Axis.Y): return 'Axis.Y'
    elif (x == Axis.No_Axes): return 'Axis.None'
    else: print('unrecognised Axis value: ' + x)

# Display by sibling relative (FLOW) or parent absolute ParentAbs?
# First sibling is taken from parent, so is in practice ParentAbs
class GDisplay():
  Flow = 0
  Parent = 1
  Absolute = 2

  def toString(self, x):
    if (x == GDisplay.Flow): return 'Flow'
    elif (x == GDisplay.Parent): return 'Parent'
    elif (x == GDisplay.Absolute): return 'Absolute'
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
