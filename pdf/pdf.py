#!/usr/bin/python3

# requires python3-reportlab

#! should provide bar counts
#! how about replacement symbols like arrows for direction?

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
#A4 is default
#from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica


ALL_DANCERS = -1

D_ACTION = 0
D_TARGET = 1
D_ISMANYBEAT = 2
D_PARAMS = 3

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


dance = {
  'title': 'War Games',
  'performers': 'EastWest',
  'description': "Originating in Bacup, the Coconutters have been described as the Most original dance in England. Nobody else would dare.",
  'transcribed': 'Robert Crowther',
  'tempo': 60,
  'beatbar' : 4,
  'dancerCount': 2,
  'start': 'hline',
  'moves': [
  ['beatsInBar', 0, False, 4],
  ['tempo', 0, False, 70],
  ['kick', 0, False, WEST],
  ['kick', 1, False, EAST],
  ['clap', 0, False, WEST],
  ['step', 1, False, EAST],
  ['step', 1, False, EAST],
  ['point', 0, False, EAST],
  ['point', 1, False, WEST],
  ['step', 1, False, WEST],
  ['step', 0, False, EAST],
  ['point', 0, False, SOUTH],
  ['step', 0, False, SOUTH],
  ['point', 1, False, EAST],
  ['point', 0, False, NORTH],
  ['step', 0, False, NORTH],
  ['point', 0, False, SOUTH],
  ['point', 1, False, WEST],
  ['point', 1, False, EAST],
  ##
  ['point', 0, False, WEST],
  ['point', 1, False, EAST],
  ['clap', 0, False, WEST],
  ['step', 1, False, EAST],
  ['step', 1, False, EAST],
  ['point', 0, False, EAST],
  ['point', 1, False, WEST],
  ['step', 1, False, WEST],
  ['step', 0, False, EAST],
  ['point', 0, False, SOUTH],
  ['step', 0, False, SOUTH],
  ['point', 1, False, EAST],
  ['point', 0, False, NORTH],
  ['step', 0, False, NORTH],
  ['point', 0, False, SOUTH],
  ['point', 1, False, WEST],
  ['point', 1, False, EAST],
  ['EOD', ALL_DANCERS, False, None]
  ]
}


##################################################################
## Page setup ##
c = Canvas("test.pdf", pagesize=A4)

## Stock ##
#! should we map onto this? 
# (bottom left corner) x, y, width, height 
x = mm * 20
y = mm * 40

pageHeight = A4[1]
pageWidth = A4[0]

leftMargin =  mm * 20
rightMargin =  mm * 20
topMargin =  mm * 20
bottomMargin =  mm * 40

stockWidth = pageWidth - leftMargin - rightMargin
stockHeight = pageHeight - topMargin - bottomMargin
rightStock = leftMargin + stockWidth
leftStock = leftMargin
topStock = bottomMargin + stockHeight
bottomStock = bottomMargin

###########################################################
## Coordinate functions ##
# *Raw means a coordinate position on stock. This includes
# margins (so the stock).
# *Raw is centred top left, even though reportlab works from bottom
# left.
# *Raw can be converted to reportlab coordinates using the functions
# x() and y()

def x(x):
  return leftMargin + x

def y(y):
  return topStock - y
 
 
###########################################################
## Page ##
# Internal
# tracks the start height of the moves block
# allowing space for main or section titles 
_titleHeightRaw = 0
# currently 114, should be 95



## Title ##
# carries space if necessary (when sections start)
titleFontFamily = "Times-Roman"
titleFontSize = 24
titleTopSkip = 8


def title(title):
  global _titleHeightRaw
  c.setFont(titleFontFamily, titleFontSize)
  c.drawCentredString(A4[0] / 2, y(titleTopSkip), title)
  _titleHeightRaw = titleTopSkip + titleFontSize



## Sections ##
#! TODO  
  


## Credits ##
# If used, credits are aligned under the title. However, they do not
# contribute to the overall space above the 
# musicalDirections. This is to give maximum flexibility in overriding 
# (for example, they could be in a column to the right of musical 
# directions). To make space for them, increase musicalDirectionsTopSkip.
creditsFontFamily = "Times-Roman"
creditsFontSize = 14
# above first credit
creditsTopSkip = 0
# above each credit
creditLineTopSkip = 4

def titleCredits(performers, transcribedBy):
  global _titleHeightRaw
  c.setFont(creditsFontFamily, creditsFontSize)
  #48
  c.drawRightString(rightStock, y(_titleHeightRaw + creditsTopSkip), performers)
  _titleHeightRaw += creditsTopSkip + creditsFontSize
  #68
  c.drawRightString(rightStock, y(_titleHeightRaw + creditLineTopSkip), "Trns: " + transcribedBy)


  
## Move block essentials ##
# Declared early because musical directions need to be aligned with the
# opening time signature.

# Fixed allocation for a barline.
# Also used to calculate a start indent on every line before constent.
# There would see to be purpose in this (though this is a new art).
# should only be a handful of points.
barlineWidth = 4
moveLineContentIndent = barlineWidth >> 1

# Many music scores adopt an indent. Not often applicable here, so will 
# usually be zero. If you have any material starting a move line, use it.
# This variable can not be calculated (font width of time signature, 
# and other material).
moveblockFirstLineIndent = 0

# Reserve space for time signatures.
# This is currently sets with at line starts, and works as a minimum 
# width on inline time signature changes (usually, the code will try to
# tuck in after a barline, but if the width is not enough, this may be used).
# This variable can not be calculated (possible width of oversize font).
# If the time signature font size is changed, alter by hand.
timeSignatureWidth = 24



## MusicalDirections ##
musicalDirectionFontFamily = "Times-Bold"
musicalDirectionFontSize = 14
musicalDirectionTopSkip = 12

#? bit crude. Could do with being extendable, and stacking.
def musicalDirections(tempo):
  '''
  such as tempo.
  If used, sits over the opening of sections.
  '''
  global _titleHeightRaw
  c.setFont(musicalDirectionFontFamily, musicalDirectionFontSize)
  XRaw = moveblockFirstLineIndent + moveLineContentIndent
  c.drawString(x(XRaw), y(_titleHeightRaw + musicalDirectionTopSkip), 'tempo = ' + str(tempo))
  _titleHeightRaw += musicalDirectionTopSkip + musicalDirectionFontSize



#######################################################################
## The move block ##
# The move block is almost all automatic layout. This has it's 
# diadvantages, but we will see....

# Space above the block.
# Rarely used?
movesBlockTopSkip = 0

# gap between lines. Don't make too small.
movesLineTopSkip = 96


## Utils ##
def moveLineYRaw(idx):
  # positioning for each line 
  global _titleHeightRaw
  return _titleHeightRaw + (movesLineTopSkip * idx)


def hline(yRaw):
  c.line(leftStock, y(yRaw), rightStock, y(yRaw))
  
  
## Time signature ##
timeSignatureFontFamily = "Times-Roman"
timeSignatureFontSize = 24
# How far down from the line to drop a time signature
timeSignatureSkipDown = 32


def timeSignature(moveLineIdx, xRaw, count):
  c.setFont(timeSignatureFontFamily, timeSignatureFontSize)
  c.drawString(x(xRaw), y(moveLineYRaw(moveLineIdx) + timeSignatureSkipDown), str(count))

#! must be capable of being written mid-block, too
def moveLineOpeningTimeSignature(count):
  # note that the indent is the same as musicalDirections
  xRaw = moveblockFirstLineIndent + moveLineContentIndent
  timeSignature(0, xRaw, count)



## moves ##

# Opens a movesblock
def movesblock():
  global _titleHeightRaw
  _titleHeightRaw += movesBlockTopSkip 



  
####################################################################
#! asserts

## helpers ##
print(c.getAvailableFonts())
 




#def lineYRaw(idx):
  #return bottomForewordRaw + (lineHeightRaw * idx)
  #return _titleHeightRaw + (lineHeightRaw * idx)

#def dotPosRawY(idx):
#    return lineYRaw(idx) + 8
    
#def dotPosRawX(idx):
#    return leftStock + (dotSpacing * idx)    

#def textPosRawX(idx):
    # in coords, for y
#    return leftStock + (dotSpacing * idx) 
    
#def textPosRawY(idx):
    # in coods, for x
    #return bottomForewordRaw + (lineHeightRaw * idx) 
#    return _titleHeightRaw + (lineHeightRaw * idx) 

def dot(xd, yd):  
  c.circle(x(xd), y(yd), 4, False, True)

def startMoveEnvironment():
  c.setFont("Times-Roman", 12)
  #c.setFont("Times-Roman", 10)
  c.saveState()
  # scale then translate
  c.rotate(270)
  #c.rotate(315)
  #print('ttrns at:' + str(-pageHeight) + ' ' + str(-pageWidth))
  c.translate(-pageHeight, 0)

def endMoveEnvironment():
  c.restoreState()


#def text(xp, yp, txt):
  # x, y inverted
  #print('clap at:' + str(lineYRaw(yp)) + ' ' + str(textPosRawX(xp)))
  #c.drawString(173, 89, txt)
  #c.drawString(lineYRaw(yp), dotPosRawX(xp), txt)


# specialist helpers #


  
#c.setStrokeColorRGB(1, 0, 0)
#c.setFillColorRGB(0, 1, 0)

#########################################################
# Express an interest in how many bars to a line
# In many circumstances, may not be honoured. But used for open
# bar rendering, so will stretch bars to fit the page width.
#! what about sheet width, etc.?
barPerLineAim = 4

# fixed width for barmarks to occupy
barmarkWidth = 24

# internal
# 'beatbar' should come by move instruction, but we have not enabled 
# this yet, so rig in for now
_beatsPerLineAim = barPerLineAim * dance['beatbar']

# keeps track of current value for rendering
_beatsPerBar = dance['beatbar']



class MoveBlockRender():
  def __init__(self, c, barPerLineAim):
    #? This is plainly a stream queue. However, Python has no standard
    #? queue and deque is multi-threaded, which I have ojection to(!),
    #? so using a list, even if slow.
    self._moveStore = []
    
    self.c = c
    self.barPerLineAim = barPerLineAim
    
    # counts lines in block
    self._blockLineI = 0
    
    # resets per page
    self._pageLineI = 0

    # cursor for x positions when rendering
    # absolute page positioned
    self.curseX = 0

  def renderBeatCountChange(self, e):
    pass
    
  def renderBarmark(self, yd):
    self.c.line(self.curseX, y(yd), self.curseX, y(yd + 12))
    pass

  def renderMove(self, yd, m):
    global x
    global y
    startMoveEnvironment()
    #text(self.curseX, y, m[D_ACTION])
    #print(topStock)
    #print(yd)
    self.c.drawString(yd + topMargin + 8, self.curseX, m[D_ACTION])
    endMoveEnvironment()
    
    
  def renderbar(self, y, glueWidth):
    global timeSignatureWidth
    global _beatsPerBar
    
    # peek the first element
    first = self._moveStore[0]
    firstIns = first[D_ACTION]

    if (firstIns == 'beatsPerbar'):
      e = self._moveStore.pop()
      self.renderBeatCountChange(e)
      _beatsPerBar = e[D_PARAMS]
      self.curseX += timeSignatureWidth
    else:
      #self.renderbarMark()
      self.renderBarmark(y)
      self.curseX += barmarkWidth

    i = 0      
    while(i < _beatsPerBar):
      e = self._moveStore.pop()
      #print(e)
      #ins = e[D_ACTION]
      #! for now, until we get other marks in there
      self.renderMove(y, e)
      self.curseX += glueWidth
      i += 1        
      
      
    
  def renderLineContents(self,
      x,
      y,
      width,
      numberOfBarsToRender,
      numberOfInstructionsToRender
    ):
    global barmarkWidth
    #renderBarticks(self._pageLineI)
    
    # ok, bar marks are fixed with space
    #! need to add tempo marks here too.
    #! bars will be replacable by tempo marks, not direct calculated
    #? includes two half barwidth for each end 
    fixedWidthTotal = numberOfBarsToRender * barmarkWidth
    gluedWidthCount = 0
    l = numberOfInstructionsToRender
    i = 0
    while(i < l):
      #      print(e
      #! for now, until we get other marks in there
      gluedWidthCount += 1
      i += 1
      
    # key value now found
    glueWidth = (width - fixedWidthTotal)/gluedWidthCount
    
    i = numberOfBarsToRender
    self.curseX = x
    while(i > 0):
      self.renderbar(y, glueWidth)
      i -= 1
      
    # render closing barmark
    self.renderBarmark(y)
      
  def finaliseMovesBlock(self):
    # need to fix last line with remaining moves
    print('moves remaining:{0}'.format(len(self._moveStore)))

    # render remains
    #???
    #report
    print('done')

  def newPage(self):
    print('newPage')
    self._pageLineI = 0
    self.c.showPage()

  def createMoveLine(self):
    global moveLineYRaw
    global bottomStock
    global dance
    global hline
    global _beatsPerLineAim
    
    # Test we did not reach stock bottom (new page)
    lineYRaw = moveLineYRaw(self._pageLineI)
    if (lineYRaw < bottomStock):
      self.newPage()
      
    # render the line
    hline(lineYRaw)
    
    # now work out widths overall
    #???

          
    # make a decision, how many bars?
    #? tmp for now. later, run through and pre-calculate widths. 
    #? the feed beats one-by-one. Later.
    # key value, now have it
    decidedBarCount = self.barPerLineAim
    
    # add remove bars as necessary
    #???
    
    self.renderLineContents(
      leftStock, 
      lineYRaw, 
      rightStock - leftStock,  
      decidedBarCount,
      decidedBarCount * dance['beatbar']
    )
    
    
    self._blockLineI += 1 
    self._pageLineI += 1
    # remove used moves
    #_moveStore = 
      
  def addMove(self, m):
    global _beatsPerLineAim
    #print('ho' + m[D_ACTION])
    if (m[D_ACTION] != 'EOD'):
      self._moveStore.append(m)
      
      # pick a point for assessment, usually 5 bars. We aim at
      # four bars a line
      #! what about sheet width, etc.?
      #print('ho' +str(_beatsPerLineAim))
      if(len(self._moveStore) > _beatsPerLineAim):
        # Should have enough to make a line
        self.createMoveLine()
    else:
      self.finaliseMovesBlock()
      
    
#########################################################
## Demo ##

## Titles ##

title(dance['title'])
titleCredits(dance['performers'], dance['transcribed'])
musicalDirections(dance['tempo'])

movesblock()

print(str(_titleHeightRaw))


## body ##
moveLineOpeningTimeSignature(dance['beatbar'])


mbr = MoveBlockRender(c, barPerLineAim)
i = 0
m = dance['moves']
l = len(m)
while(i < l):
  #text(i, 1, m[i][0])
  mbr.addMove(m[i])
  i += 1


#path = c.beginPath()
#path.moveTo(inch * 4, inch * 4)
#path.lineTo(inch * 3, inch * 4)
#path.lineTo(inch * 3.5, inch * 5)
#path.lineTo(inch * 4, inch * 4)

# stroke/fill
#c.drawPath(path, True, True)

c.save()
