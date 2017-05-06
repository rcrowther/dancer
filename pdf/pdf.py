#!/usr/bin/python3

# requires python3-reportlab

#! should provide bar counts
#! how about replacement symbols like arrows for direction?
#! asserts
#! titleheight doesn't respect top margin - initialize!
#print(c.getAvailableFonts())  
#c.setStrokeColorRGB(1, 0, 0)
#c.setFillColorRGB(0, 1, 0)


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
#A4 is default
#from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
import math

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
  ['timeSignature', False, 0, False, 4],
  ['tempo', False, 0, False, 70],
  
  ['kick', True, 0, False, WEST],
  ['kick', True, 1, False, EAST],
  ['clap', True, 0, False, WEST],
  ['step', True, 1, False, EAST],
  ['bar', 0, False, 70],

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
  ['bar', False, True, 0, False, 70],

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
# Not raw! From page edge
_centerPage = pageWidth / 2

leftMargin =  mm * 20
rightMargin =  mm * 20
topMargin =  mm * 20
bottomMargin =  mm * 40


rightStock = pageWidth - rightMargin
leftStock = leftMargin
topStock = pageHeight - topMargin
bottomStock = bottomMargin

# passed to renderMoveBlock
stockContext = [topStock, rightStock, leftStock, bottomStock, topMargin]

###########################################################
## Coordinate functions ##
# *Raw means a coordinate position on stock. This includes
# margins (so the stock).
# *Raw is centred top left stock, even though reportlab works from 
# bottom left.
# *Raw can be converted to reportlab coordinates using the functions
# x() and y()
#
# Mentions of 'top' 'center' etc. refer to reportlab full-page 
# coordinates. Though widths and heights may be usable for positioning
# on stock.
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
  c.drawCentredString(_centerPage, y(titleTopSkip), title)
  _titleHeightRaw = titleTopSkip + titleFontSize



## Sections ##
sectionFontFamily = "Times-Roman"
sectionFontSize = 24
sectionTopSkip = 8

#! TODO  
def section(title):
  # initialize
  self.c.showPage()
  _titleHeightRaw = 0
  
  # render
  c.setFont(sectionFontFamily, sectionFontSize)
  c.drawCentredString(_centerPage, y(sectionTopSkip), title)
  _titleHeightRaw = sectionTopSkip + sectionFontSize
  


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
barlineWidth = 24
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


# Opens a movesblock
def movesblock():
  global _titleHeightRaw
  _titleHeightRaw += movesBlockTopSkip 


## Utils ##
#x deprecated, when we get times and tempo in the block class
def moveLineYRaw(idx):
  # positioning for each line 
  global _titleHeightRaw
  return _titleHeightRaw + (movesLineTopSkip * idx)



  
  
## Time signature ##
timeSignatureFontFamily = "Times-Roman"
timeSignatureFontSize = 24
# How far down from the line to drop a time signature
timeSignatureSkipDown = 32


def timeSignature(moveLineIdx, xRaw, count):
  c.setFont(timeSignatureFontFamily, timeSignatureFontSize)
  c.drawString(x(xRaw), y(moveLineYRaw(moveLineIdx) + timeSignatureSkipDown), str(count))

def moveLineOpeningTimeSignature(count):
  # note that the indent is the same as musicalDirections
  xRaw = moveblockFirstLineIndent + moveLineContentIndent
  timeSignature(0, xRaw, count)



## moveLines ##

# Express an interest in how many bars to a line
# In many circumstances, will not be honoured. But used for open
# bar rendering, so will stretch bars to fit the page width.
#! what about sheet width, etc.?
barPerLineAim = 4

# fixed width for barmarks to occupy
barmarkWidth = 24

# The minimum glue allowed before bars are spilled to the next line
minMoveGlueWidth = 14

# space down from the moveline to the move marks
moveLineContentSkipDown = 8

# internal
#x?
# keeps track of current value for rendering
_beatsPerBar = dance['beatbar']


## utils ##

#def dot(xd, yd):  
#  c.circle(x(xd), y(yd), 4, False, True)

def startVerticalTextEnvironment():
  c.setFont("Times-Roman", 12)
  #c.setFont("Times-Roman", 10)
  c.saveState()
  # scale then translate
  c.rotate(270)
  #c.rotate(315)
  #print('ttrns at:' + str(-pageHeight) + ' ' + str(-pageWidth))
  c.translate(-pageHeight, 0)

def endVerticalTextEnvironment():
  c.restoreState()



# if I don't use a class, Python cant privatise, and we end up with a 
# lot of publiized specifics. Tex won't privatise either, but for
# the sake of clarity... This does mean a certain amount of non-DRY
# reimplementation in the class, but for this critical, large. and 
# largely self-contained method, probably worth it.
class MoveBlockRender():
  def __init__(self,
   c,
   stockPositions = stockContext,
   barsInLineAim = barPerLineAim,
   lineTopSkip = movesLineTopSkip, 
   firstPageTopSkip = _titleHeightRaw,
   lineContentIndent = moveLineContentIndent,
   barlineWidth = barlineWidth,
   timeSignatureWidth = timeSignatureWidth,
   minMoveGlueWidth = minMoveGlueWidth,
   moveLineContentSkipDown = moveLineContentSkipDown
  ):
    

    # useful methods
    #def timeSignature(moveLineIdx, xRaw, count):
    #! should be moved in here
    #! tempo markngs should be moved in here 
    global timeSignature


    # outside properties    
    self.c = c
            
    # stockContext = [topStock, rightStock, leftStock, bottomStock]
    self.topStock = stockContext[0]
    self.rightStock = stockContext[1]
    self.leftStock = stockContext[2]
    self.bottomStock = stockContext[3]
    self.topMargin = stockContext[4]
    print('bottomStock: '+ str(self.bottomStock))
    
    
    self._barsInLineAim = barsInLineAim
    print('_barsInLineAim: '+ str(self._barsInLineAim))
        
    # first page only, reset to topStock
    self._lineTopSkip = lineTopSkip    
    print('lineTopSkip: '+ str(lineTopSkip))


    # absolute
    self._blockTop = self.topStock - firstPageTopSkip
    
    # Rotated environment inverts the y direction (for X positioning)
    self._rotatedBlockLeft = self.topMargin + firstPageTopSkip
    print('firstPageTopSkip: '+ str(firstPageTopSkip))

    self._barlineWidth = barlineWidth
    self._lineContentIndent = lineContentIndent
    print('lineContentIndent: '+ str(lineContentIndent))

    self.timeSignatureWidth = timeSignatureWidth
    self.minMoveGlueWidth = minMoveGlueWidth
    self.moveLineContentSkipDown = moveLineContentSkipDown
    
    # Internal
    
    #? This is plainly a stream queue. However, Python has no standard
    #? queue, and deque is multi-threaded, which I have ojection to(!).
    #? Using a list, even if slow.
    self._moveStore = []
    
    # count lines in block
    self._blockLineI = 0
    
    # count lines per page
    self._pageLineI = 0

    # count bars loaded
    self._barI = 0
    
    # cursor for x positions when rendering
    # absolute page positioned
    self.curseX = 0


  ## helpers
  #! pass absY around in preference
  def y(self, idx):
    #print('_blockTop: '+ str(self._blockTop))
    return self._blockTop - (self._lineTopSkip * idx)
  
  # Do not use for stock placements, takes account of
  # line content indent
  def x(self, XRaw):
    return self.leftStock + lineContentIndent + XRaw
    

  ## renderers
  #! pass YAbs arround in preference
  def moveLineRender(self, absY):
    self.c.line(self.leftStock, absY, self.rightStock, absY)
  
  ## calculate
  def renderBeatCountChange(self, e):
    pass
    
  def renderBarmark(self, absX, absY):
    #print('_blockTop: '+ str(self.curseX))
    #print('_blockTop: '+ str(self._blockTop))

    #self.c.line(self.curseX, absY, self.curseX, absY - 12)
    self.c.line(absX, absY, absX, absY - 12)

    
  def renderLineContents(self,
      absX,
      absY,
      glueWidth,
      numberOfBarsToRender
    ):
    print('absX: '+ str(absX))
    print('absY: '+ str(absY))
    print('glueWidth: '+ str(glueWidth))
    print('numberOfBarsToRender: '+ str(numberOfBarsToRender))

    # accumulate X progress. Start at absX.
    curseX = absX
    
    # We'll stash movemarks to do all at once?
    moveStash = []


    #! render start barmark
    self.renderBarmark(absX, absY)
    curseX += self._barlineWidth
     
    print('store size: ' + str(len(self._moveStore)))
   
    ii = 0
    while (ii < numberOfBarsToRender):
      #print('ii ' + str(ii))
      event = self._moveStore.pop(0)
      if (event[D_ISMOVE]):
        moveStash.append([curseX, event])
        curseX += glueWidth
        #print('curseX' + str(curseX))
      else:
        if (event[D_ACTION] == 'bar'):
          self.renderBarmark(curseX , absY)
          #print('rend bar' + str(ii))
          curseX += self._barlineWidth
          ii = ii + 1
        else:
          #self.renderSignature(event, curseX , absY)
          # now a signature
          curseX += self.timeSignatureWidth

    # now get back to those marks
    i = 0
    l = len(moveStash)
    
    startVerticalTextEnvironment()
    # absY will not work in the rotated envirionment, I measures in
    # reportlab style fro the bottom, rotated 3/4, it must work from
    # the page top.
    rAbsX = self._rotatedBlockLeft + (self._lineTopSkip * self._pageLineI) + self.moveLineContentSkipDown
    print('rAbsX :' + str(rAbsX))
    print('self._pageLineI :' + str(self._pageLineI))

    while (i < l):
      e = moveStash[i]
      self.c.drawString(rAbsX, e[0], e[1][D_ACTION])
      i += 1
    endVerticalTextEnvironment()
      
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
    # not first page top, as initialised, but top of stock
    self._blockTop = self.topStock
    self._rotatedBlockLeft = self.topMargin

    self.c.showPage()


  def createMoveLine(self):
    print('mLine: '+ str(self._pageLineI))    
    #print('store size: ' + str(len(self._moveStore)))
    
    # get the absY position of the line
    # to be used throughout rendering
    absY = self.y(self._pageLineI)
    #print('absY: '+ str(absY))

    # Test we did not reach stock bottom.
    # if we did, before rendering, trigger new page
    if (absY < self.bottomStock):
      self.newPage()
      
    # render the line itself
    self.moveLineRender(absY)

    # Now render contents   
    
    # simple heuristic, 
    # - work out fixed widths
    # - work out line fixed space
    # - calculate glue width
    # - if too narrow, drop a bar
    # work out widths overall
    #! remove to seperate method, check for multiple bar drops, etc.
       
    #1
    # Currently assumes _moveStore contains _barsInLineAim 
    i = 0
    l = len(self._moveStore)
    barcount = 0
    fixedSize = 0
    gluedEventCount = 0
    while(i < l):
      if (not self._moveStore[i][D_ISMOVE]):
        action = self._moveStore[i][D_ACTION]
        if (action == 'bar'):
          fixedSize += self._barlineWidth
          barcount += 1
        #if (action == 'tempo'):
        #  fixedSize += 
        if (action == 'timeSignature'):
          fixedSize += self.timeSignatureWidth
      else:
        gluedEventCount += 1
      i += 1

    #2
    absX = x(0)
    lineWidth = self.rightStock - absX 
    
    #3
    glueWidth = (lineWidth - fixedSize)/gluedEventCount
    
    #4
    decidedBarCount = self._barsInLineAim
    if (glueWidth < self.minMoveGlueWidth):
      #! if you do this, the glue width needs revising.
      decidedBarCount -= 1

    
    #print('fixedSize: '+ str(fixedSize))
    #print('glueWidth:' + str(glueWidth))
    #print('decidedBarCount:' + str(decidedBarCount))
    
      
    decidedBarCount = self._barsInLineAim

    
    self.renderLineContents(
      absX,
      absY, 
      glueWidth,  
      decidedBarCount
    )
    
    self._barI -= decidedBarCount
    
    self._blockLineI += 1 
    self._pageLineI += 1
    
      
  def addInstruction(self, m):
    self._moveStore.append(m)
    if (not m[D_ISMOVE]):
      nonMoveEvent = m[D_ACTION]
      if (nonMoveEvent == 'EOD'):
        self.finaliseMovesBlock()
      elif (nonMoveEvent == 'bar'):
        self._barI = self._barI + 1
        if(self._barI >= self._barsInLineAim):
          self.createMoveLine()

      
    
#########################################################
## Demo ##

## Titles ##

title(dance['title'])
titleCredits(dance['performers'], dance['transcribed'])
musicalDirections(dance['tempo'])

movesblock()



## body ##
moveLineOpeningTimeSignature(dance['beatbar'])

print('_titleHeightRaw: ' + str(_titleHeightRaw))

mbr = MoveBlockRender(c, firstPageTopSkip = _titleHeightRaw)
  
i = 0
m = dance['moves']
l = len(m)
while(i < l):
  #text(i, 1, m[i][0])
  mbr.addInstruction(m[i])
  i += 1


#path = c.beginPath()
#path.moveTo(inch * 4, inch * 4)
#path.lineTo(inch * 3, inch * 4)
#path.lineTo(inch * 3.5, inch * 5)
#path.lineTo(inch * 4, inch * 4)

# stroke/fill
#c.drawPath(path, True, True)

c.save()
