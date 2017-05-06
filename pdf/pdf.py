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
  ['timeMark', False, 0, False, 4],
  ['tempoMark', False, 0, False, 70],
  
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

#################################################################
def info(msg):
   print('[info] ' + msg)
  
def warning(msg):
   print('[warning] '+ msg)
   
##################################################################
# *Abs. means a coordinate position according to reportlab. These are 
# full-page, centred bottom left.
# *Raw means a coordinate position on stock. This includes
# margins (so the stock).
# *Raw is centred top left stock, even though reportlab works from 
# bottom left.
# *Raw can be converted to reportlab coordinates using the functions
# rawToAbsX() and rawToAbsY()
#

## Page setup ##
c = Canvas("test.pdf", pagesize=A4)

## Stock ##
#! should we map onto this? 
# (bottom left corner) x, y, width, height 
#x = mm * 20
#y = mm * 40

_pageHeight = A4[1]
_pageWidth = A4[0]
# Not raw! From page edge
_centerPage = _pageWidth / 2

leftMargin =  mm * 20
rightMargin =  mm * 20
topMargin =  mm * 20
bottomMargin =  mm * 40


rightStockAbs = _pageWidth - rightMargin
leftStockAbs = leftMargin
topStockAbs = _pageHeight - topMargin
bottomStockAbs = bottomMargin

# passed to renderMoveBlock
stockContext = [topStockAbs, rightStockAbs, leftStockAbs, bottomStockAbs, topMargin]

###########################################################
## Coordinate functions ##
# rawToAbsX() and rawToAbsY() convert *Raw positions to *Abs
#

#? unused 
def rawToAbsX(x):
  return leftMargin + x

def rawToAbsY(y):
  return topStockAbs - y
 
 
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
  c.drawCentredString(_centerPage, rawToAbsY(titleTopSkip), title)
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
  c.drawCentredString(_centerPage, rawToAbsY(sectionTopSkip), title)
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
  c.drawRightString(rightStockAbs, rawToAbsY(_titleHeightRaw + creditsTopSkip), performers)
  _titleHeightRaw += creditsTopSkip + creditsFontSize
  #68
  c.drawRightString(rightStockAbs, rawToAbsY(_titleHeightRaw + creditLineTopSkip), "Trns: " + transcribedBy)


  
## Move block essentials ##
# Declared early because musical directions need to be aligned with the
# opening time signature.

# Fixed allocation for indenting the content at start of lines.
# Used to push the initial data, like time signature, from the start 
# barline. For music scores, there would be a lot of data, like stave 
# marks and key signatures. Not here. Should only be a handful of points.
barlineGlue = 0.5
moveLineContentIndent = 4
#moveLineContentIndent = 0

# Many music scores adopt an indent. Not often applicable here, so will 
# usually be zero. If you have any material starting a move line, use it.
# This variable can not be calculated (font width of time signature, 
# and other material).
# NOT IMPLEMENTED
#moveblockFirstLineIndent = 0

# The last line in any block may not have the right number of bars.
# The simplistic solution here, if the line is within this number of
# bars then it will stretched to full width, otherwise the line is
# rendered as stopping short. To always stretch, make this a relativly
# large number e.g. 12. 0 will never stretch.
lastMovelineGlueMax = 2



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
  #XRaw = moveblockFirstLineIndent + moveLineContentIndent
  XRaw = moveLineContentIndent
  c.drawString(rawToAbsX(XRaw), rawToAbsY(_titleHeightRaw + musicalDirectionTopSkip), 'tempo = ' + str(tempo))
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
timeMarkFontFamily = "Times-Roman"
timeMarkFontSize = 16

# Reserve space for time signatures.
# For marks at line starts and inline.
# This variable can not be calculated (possible width of oversize font).
# If the time signature font size is changed, alter by hand.
# Should be, say, 3/2 of the width of the fonts as written as glyphs.
timeMarkWidth = 24

# How far down from the line to drop a time signature
timeMarkSkipDown = 24

timeMarkContext = [timeMarkFontFamily, timeMarkFontSize, timeMarkWidth, timeMarkSkipDown]




## moveLines ##

# Express an interest in how many bars to a line
# In many circumstances, will not be honoured. But used for open
# bar rendering, so will stretch bars to fit the page width.
#! what about sheet width, etc.?
barPerLineAim = 5

# fixed width for barmarks to occupy
barmarkWidth = 24

# The minimum glue allowed before bars are spilled to the next line
minMoveGlueWidth = 14

moveLineContentFontFamily = "Times-Roman"
moveLineContentFontSize = 12

# space down from the moveline to the move marks
moveLineContentSkipDown = 8


## utils ##

def startVerticalTextEnvironment():
  c.setFont(moveLineContentFontFamily, moveLineContentFontSize)
  c.saveState()
  # scale then translate
  c.rotate(270)
  c.translate(-_pageHeight, 0)

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
   #moveblockFirstLineIndent = moveblockFirstLineIndent,
   lineContentIndent = moveLineContentIndent,
   barlineGlue = barlineGlue,
   timeMarkWidth = timeMarkWidth,
   minMoveGlueWidth = minMoveGlueWidth,
   lastMovelineGlueMax = lastMovelineGlueMax,
   moveLineContentSkipDown = moveLineContentSkipDown,
   timeMarkContext = timeMarkContext
  ):
    

    # useful methods
    #def timeMark(moveLineIdx, xRaw, count):
    #! should be moved in here
    #! tempo markngs should be moved in here 



    # outside properties    
    self.c = c
            
    # stockContext = [topStockAbs, rightStockAbs, leftStockAbs, bottomStockAbs]
    self.topStockAbs = stockContext[0]
    self.rightStockAbs = stockContext[1]
    self.leftStockAbs = stockContext[2]
    self.bottomStockAbs = stockContext[3]
    self.topMargin = stockContext[4]
    print('bottomStockAbs: '+ str(self.bottomStockAbs))
    
    
    self._barsInLineAim = barsInLineAim
    print('_barsInLineAim: '+ str(self._barsInLineAim))
        
    # first page only, reset to topStockAbs
    self._lineTopSkip = lineTopSkip    
    print('lineTopSkip: '+ str(lineTopSkip))


    # calculate the top block absolutely
    self._blockTopAbs = self.topStockAbs - firstPageTopSkip

    # ...rotated environment inverts the y direction (for X positioning)
    self._rotatedBlockLeftAbs = self.topMargin + firstPageTopSkip
    print('firstPageTopSkip: '+ str(firstPageTopSkip))

    #self.moveblockFirstLineIndent = moveblockFirstLineIndent


    self._barlineGlue = barlineGlue
    self.lineContentIndent = lineContentIndent
    print('lineContentIndent: '+ str(self.lineContentIndent))

    self.minMoveGlueWidth = minMoveGlueWidth
    self.moveLineContentSkipDown = moveLineContentSkipDown
    self.lastMovelineGlueMax = lastMovelineGlueMax
    
    self.timeMarkFontFamily = timeMarkContext[0]
    self.timeMarkFontSize = timeMarkContext[1]
    self.timeMarkWidth = timeMarkContext[2]
    self.timeMarkSkipDown = timeMarkContext[3]

    
    # Internal
    
    #? This is plainly a stream queue. However, Python has no standard
    #? queue, and deque is multi-threaded, which I have ojection to(?!).
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
  def rawToAbsY(self, idx):
    #print('_blockTopAbs: '+ str(self._blockTopAbs))
    return self._blockTopAbs - (self._lineTopSkip * idx)
  
  # Do not use for stock placements, takes account of
  # line content indent
  def rawToAbsX(self, XRaw):
    return self.leftStockAbs + self.lineContentIndent + XRaw
    


  ## renderers
  #! pass absY arround in preference
  def moveLineRender(self, toX, absY):
    self.c.line(self.leftStockAbs, absY, toX, absY)
  
  ## calculate
  def renderTimeMark(self, absX, absY, event):
    s = str(event[D_PARAMS])
    #print('count: '+ s)
    self.c.setFont(self.timeMarkFontFamily, self.timeMarkFontSize)
    self.c.drawString(absX, absY - self.timeMarkSkipDown, s)

  def renderBeatCountChange(self, e):
    pass

    # Current strategy for barmarks:
    # 1
    # They take a glue place
    # ...but add a small visual disruption.
    # Probably 1/3 of glue.    
    # They are placed at 2/3 of the resulting glue space
  # Initial barmarks take no space, are placed in the fixed  moveLineContentIndent
      
  # oriented round the line
  def renderBarmark(self, absX, absY):
    #print('_blockTopAbs: '+ str(self.curseX))
    #print('_blockTopAbs: '+ str(self._blockTopAbs))
    #self.c.line(self.curseX, absY, self.curseX, absY - 12)
    self.c.line(absX, absY, absX, absY - 12)

  # oriented round the box
  def renderCloseBarmark(self, absX, absY):
    # width = 6?
    self.c.line(absX - 8, absY, absX - 8, absY - 12)
    self.c.rect(absX - 4,  absY - 12, 4, 12, fill=1)

  # oriented round the box
  def renderRepeatCloseBarmark(self, absX, absY):
    self.c.circle(absX - 10, absY - 6, 1, fill=1)
    self.c.line(absX - 4, absY, absX - 4, absY - 12)
    self.c.rect(absX,  absY - 12, 2, 12, fill=1)

  # oriented round the line
  def renderRepeatOpenBarmark(self, absX, absY):
    self.c.rect(absX - 6,  absY - 12, 2, 12, fill=1)
    self.c.line(absX, absY, absX, absY - 12)
    self.c.circle(absX + 6, absY - 6, 1, fill=1)



    
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


    # render start barmark
    #self.renderBarmark(self.leftStockAbs + moveLineContentIndent, absY)
    self.renderBarmark(self.leftStockAbs, absY)
    
    #print('store size: ' + str(len(self._moveStore)))
   
    ii = 0
    barGlueWidth = glueWidth * self._barlineGlue
    while (ii < numberOfBarsToRender):
      event = self._moveStore.pop(0)
      print('render: ' + event[D_ACTION])

      if (event[D_ISMOVE]):
        moveStash.append([curseX, event])
        curseX += glueWidth
        #print('curseX' + str(curseX))
      else:
        if (event[D_ACTION] == 'bar'):
          self.renderBarmark(curseX , absY)
          curseX += barGlueWidth
          #print('rend bar' + str(ii))
          ii += 1
        elif (event[D_ACTION] == 'closeBar'):
          # could happen, if bars match space exactly
          self.renderCloseBarmark(curseX , absY)
          # irrelevant. To well-formed input...
          curseX += barGlueWidth
          ii += 1
        elif (event[D_ACTION] == 'repeatOpenBar'):
          # could happen, if bars match space exactly
          self.renderRepeatOpenBarmark(curseX , absY)
          # irrelevant. To well-formed input...
          curseX += barGlueWidth
          ii += 1
        elif (event[D_ACTION] == 'repeatCloseBar'):
          # could happen, if bars match space exactly
          self.renderRepeatCloseBarmark(curseX , absY)
          # irrelevant. To well-formed input...
          curseX += barGlueWidth
          ii += 1
        elif (event[D_ACTION] == 'timeMark'):
          self.renderTimeMark(curseX, absY, event)
          curseX += self.timeMarkWidth
        elif (event[D_ACTION] == 'tempo'):
          pass
          
    # now get back to those marks
    i = 0
    l = len(moveStash)
    
    startVerticalTextEnvironment()
    # absY will not work in the rotated envirionment, I measures in
    # reportlab style fro the bottom, rotated 3/4, it must work from
    # the page top.
    rAbsX = self._rotatedBlockLeftAbs + (self._lineTopSkip * self._pageLineI) + self.moveLineContentSkipDown
    #print('rAbsX :' + str(rAbsX))
    #print('self._pageLineI :' + str(self._pageLineI))

    while (i < l):
      e = moveStash[i]
      self.c.drawString(rAbsX, e[0], e[1][D_ACTION])
      i += 1
    endVerticalTextEnvironment()

  #! this assumes full length of movestore?
  #! should count bars
  def calculateGlue(self, toBarcount, lineWidth):
    i = 0
    barcount = 0
    fixedSize = 0
    gluedEventCount = 0
    while(barcount < toBarcount):
      if (not self._moveStore[i][D_ISMOVE]):
        action = self._moveStore[i][D_ACTION]
        if (self.isBar(action)):
          gluedEventCount += self._barlineGlue
          barcount += 1
        #if (action == 'tempo'):
        #  fixedSize += 
        if (action == 'timeMark'):
          fixedSize += self.timeMarkWidth
      else:
        gluedEventCount += 1
      i += 1
    #print('gluedEventCount: ' + str(gluedEventCount))
    # We have a problem at line ends.
    # Everything is aligned to the left.
    # Thats nice, because following space can reflect
    # the symbol contents.
    # but at line ends, the barline goes to the left,
    # leaving a 'T' shape,
    #  --------
    #       |
    # so I remove one barline of glue. Neater than
    # trying to faff with the loop (and study of 
    # musical scores suggests the final bar in a line
    # may benefit from shortened space, not larger).
    gluedEventCount -= self._barlineGlue
    
    return (lineWidth - fixedSize)/gluedEventCount
          
  def isBar(self, action):
    return (
      action == 'bar' or
      action == 'closeBar' or
      action == 'repeatOpenBar' or
      action == 'repeatCloseBar'
      )
      
  def finaliseMovesBlock(self):
    # need to fix last line with remaining moves
    #print('moves remaining:{0}'.format(len(self._moveStore)))

    # render remains
    # get the absY position of the line
    # to be used throughout rendering
    absY = self.rawToAbsY(self._pageLineI)
    #print('absY: '+ str(absY))

    # Test we did not reach stock bottom.
    # if we did, before rendering, trigger new page
    if (absY < self.bottomStockAbs):
      self.newPage()
    
    # decide stretch, or stub?
    
    # for sure we have less bars than we want, otherwise we'd trigger a new 
    # line. But how many?
    # Could be done with a glueAssessment, but would be untidy.
    i = 0
    l = len(self._moveStore)
    barcount = 0
    while(i < l):
      action = self._moveStore[i][D_ACTION]
      if (self.isBar(action)):
        barcount += 1
      i += 1
    print('remaining bars: ' + str(barcount))

    # need the width, whatever 
    absX = self.rawToAbsX(0)
    lineWidth = self.rightStockAbs - absX
    
    decidedBarCount = self._barsInLineAim
    if (barcount < self._barsInLineAim):
      info('bar count at end at end of block is short: requested: {0}: num of bars:{1}'.format(self._barsInLineAim, barcount))


    if (barcount < self._barsInLineAim - self.lastMovelineGlueMax):
      warning('Stubbing the last line')
      #To work this out we,
      # - restrict ourselves to a width ratio of bars found to intended 
      # - calculateGlue
      # - shorten the line render
      # this will render short, but should look ok. For now.
      newWidth = lineWidth * (barcount/self._barsInLineAim)
      glueWidth = self.calculateGlue(barcount, newWidth)      
      # render the line itself
      self.moveLineRender(self.leftStockAbs + newWidth, absY)
    else:
      info('Expanding the last line')
      glueWidth = self.calculateGlue(barcount, lineWidth)
      # render the line itself
      self.moveLineRender(self.rightStockAbs, absY)
        
    decidedBarCount = barcount
          
    #self.renderCloseBarmark(absX, absY)
    self.renderLineContents(
      absX,
      absY, 
      glueWidth,  
      decidedBarCount
    )
    #report
    print('done')

  def newPage(self):
    print('newPage')
    self._pageLineI = 0
    # not first page top, as initialised, but top of stock
    self._blockTopAbs = self.topStockAbs
    self._rotatedBlockLeftAbs = self.topMargin
    self.c.showPage()


  def createMoveLine(self):
    print('mLine: '+ str(self._pageLineI))    
    #print('store size: ' + str(len(self._moveStore)))
    
    # get the absY position of the line
    # to be used throughout rendering
    absY = self.rawToAbsY(self._pageLineI)
    #print('absY: '+ str(absY))

    # Test we did not reach stock bottom.
    # if we did, before rendering, trigger new page
    if (absY < self.bottomStockAbs):
      self.newPage()
      
    # render the line itself
    self.moveLineRender(self.rightStockAbs, absY)

    # Now render contents   
    
    # simple heuristic,
    # - calculate glue width
    # - if too narrow, drop a bar
    
    #1
    absX = self.rawToAbsX(0)
    lineWidth = self.rightStockAbs - absX     
    glueWidth = self.calculateGlue(self._barsInLineAim, lineWidth)      

    #2
    decidedBarCount = self._barsInLineAim
    if (glueWidth < self.minMoveGlueWidth):
      #! if you do this, the glue width needs revising.
      decidedBarCount -= 1
      glueWidth = self.calculateGlue(decidedBarCount, lineWidth)       

    
    #print('fixedSize: '+ str(fixedSize))
    #print('glueWidth:' + str(glueWidth))
    #print('decidedBarCount:' + str(decidedBarCount))

    
    self.renderLineContents(
      absX,
      absY, 
      glueWidth,  
      decidedBarCount
    )
    
    # update accumulators
    self._barI -= decidedBarCount
    self._blockLineI += 1 
    self._pageLineI += 1
    
      
  def addInstruction(self, m):
    self._moveStore.append(m)
    if (not m[D_ISMOVE]):
      nonMoveEvent = m[D_ACTION]
      if (nonMoveEvent == 'EOD'):
        self.finaliseMovesBlock()
      elif (self.isBar(nonMoveEvent)):
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
#moveLineOpeningtimeMark(dance['beatbar'])

print('_titleHeightRaw: ' + str(_titleHeightRaw))

mbr = MoveBlockRender(c, firstPageTopSkip = _titleHeightRaw)
  
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

c.save()
