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

pdf = Canvas("test.pdf", pagesize=A4)

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

## Page
# Internal
# tracks the start height of the moves block
# allowing space for main or section titles 
_titleHeight = 0


## Titling ##
# carries space if necessaary (when sections start)
titleFontFamily = "Times-Roman"
titleFontSize = 24
titleTopSkip = 18


def title(title):
  global _titleHeight
  pdf.setFont(titleFontFamily, titleFontSize)
  pdf.drawCentredString(A4[0] / 2, y(titleTopSkip), title)
  bottomForewordRaw = titleTopSkip
  _titleHeight = titleTopSkip + titleFontSize


## Credits ##
creditsFontFamily = "Times-Roman"
creditsFontSize = 18
creditsTopSkip = 6
creditLineTopSkip = 4

def titleCredits(performers, transcribedBy):
  global _titleHeight
  pdf.setFont(creditsFontFamily, creditsFontSize)
  #48
  pdf.drawRightString(rightStock, y(_titleHeight + creditsTopSkip), performers)
  _titleHeight += creditsTopSkip + creditsFontSize
  #68
  pdf.drawRightString(rightStock, y(_titleHeight + creditLineTopSkip), "Trns: " + transcribedBy)
  _titleHeight += creditLineTopSkip + creditsFontSize


## MusicalDirections ##
musicalDirectionFontFamily  = "Times-Bold"
musicalDirectionFontSize = 14
musicalDirectionTopSkip = 12
musicalDirectionLeftSkip = 0

#! bit crude. Could do with being extendable, and stacking.
#! also, this sholud be able to sit alongside title credits, and
#!  _titleHeight be chaned accordingly (choosing the higher of the two 
#! blocks)
def musicalDirections(tempo):
  '''
  such as tempo.
  If used, sits over the opening of sections.
  '''
  global _titleHeight
  pdf.setFont(musicalDirectionFontFamily, musicalDirectionFontSize)
  pdf.drawString(leftStock + musicalDirectionLeftSkip, y(_titleHeight + musicalDirectionTopSkip), 'tempo = ' + str(tempo))
  _titleHeight += musicalDirectionTopSkip + musicalDirectionFontSize


  
  
bottomForewordRaw = 95



## The move block ##


## Time signature ##
timeSignatureFontFamily  = "Times-Roman"
timeSignatureFontSize = 24
# Locked to the musicalDirectionLeftSkip.
# Can be set seperately.
timeSignatureLeftSkip = musicalDirectionLeftSkip 

#! indentable by a bit?
#! must be capable of being written mid-block, too
def timeSignature(count):
  pdf.setFont(timeSignatureFontFamily, timeSignatureFontSize)
  # space down from the line position
  ySkipDown = 24
  pdf.drawString(x(timeSignatureLeftSkip), y(moveLineYRaw(0) + ySkipDown), str(count))
  # don't auto-set movesFirstLineIndent, it can not be calculated



## moves ##
#movesFontFamily = "Times-Roman"
#movesFontSize = 18
movesTopSkip = 0
# gap between lines. Don't make too small.
movesLineTopSkip = 96
# Tracks the indendent of the first line of moves
# to allow for time signature and/or other aspects
# of style (such as dancer name?) 
# This variable can not be calculated (font width of time sinature, 
# etc.). If a time signature is used, and the font size is changed,
# alter by hand. 
movesFirstLineIndent = 32
movesTimeSignatureSkip = 32



def movesblock():
  global _titleHeight
  #pdf.setFont("Times-Roman", 10)
  _titleHeight += movesTopSkip 
    
def moveLineYRaw(idx):
  # used a lot as a start for 
  global _titleHeight
  return _titleHeight + (movesLineTopSkip * idx)

def moveLine(idx):
  hline(moveLineYRaw(idx))


  
####################################################################
#! asserts

## move consts ##
dotSpacing = 32

## helpers ##
print(pdf.getAvailableFonts())
 
def x(x):
  return leftMargin + x

def y(y):
  return topStock - y
 
 
## helpers ##
#! need line helpers

lineHeightRaw = 78

def hline(yd):
  pdf.line(leftStock, y(yd), rightStock, y(yd))




def lineYRaw(idx):
  return bottomForewordRaw + (lineHeightRaw * idx)

def dotPosRawY(idx):
    return lineYRaw(idx) + 8
    
def dotPosRawX(idx):
    return leftStock + (dotSpacing * idx)    

def textPosRawX(idx):
    # in coords, for y
    return leftStock + (dotSpacing * idx) 
    
def textPosRawY(idx):
    # in coods, for x
    return bottomForewordRaw + (lineHeightRaw * idx) 

def dot(xd, yd):  
  pdf.circle(x(xd), y(yd), 4, False, True)

def startMoveEnvironment():
  pdf.setFont("Times-Roman", 12)
  #pdf.setFont("Times-Roman", 10)
  pdf.saveState()
  # scale then translate
  pdf.rotate(270)
  #pdf.rotate(315)
  print('ttrns at:' + str(-pageHeight) + ' ' + str(-pageWidth))
  pdf.translate(-pageHeight, 0)

def endMoveEnvironment():
  pdf.restoreState()


def text(xp, yp, txt):
  # x, y inverted
  #print('clap at:' + str(lineYRaw(yp)) + ' ' + str(textPosRawX(xp)))
  #pdf.drawString(173, 89, txt)
  pdf.drawString(lineYRaw(yp), dotPosRawX(xp), txt)


# specialist helpers #


  
#pdf.setStrokeColorRGB(1, 0, 0)
#pdf.setFillColorRGB(0, 1, 0)

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
    global movesTimeSignatureSkip
    global _beatsPerBar
    
    # peek the first element
    first = self._moveStore[0]
    firstIns = first[D_ACTION]

    if (firstIns == 'beatsPerbar'):
      e = self._moveStore.pop()
      self.renderBeatCountChange(e)
      _beatsPerBar = e[D_PARAMS]
      self.curseX += movesTimeSignatureSkip
    else:
      #self.renderbarMark()
      self.renderBarmark(y)
      self.curseX += barmarkWidth

    i = 0      
    while(i < _beatsPerBar):
      e = self._moveStore.pop()
      print(e)
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
## Main ##

## Titles ##

title(dance['title'])
titleCredits(dance['performers'], dance['transcribed'])
musicalDirections(dance['tempo'])

movesblock()

print(str(_titleHeight))

#pdf.setFont("Times-Roman", 18)
#pdf.drawRightString(rightStock, y(48), dance['performers'])

#author = pdf.beginText(x(0), y(68))
#author.textLine("Trns: " + dance['transcribed'])
#pdf.drawRightString(rightStock, y(68), "Trns: " + dance['transcribed'])

## body ##
timeSignature(dance['beatbar'])




##i = 5
##while(i >= 0):
  #hline(lineYRaw(i))
##  hline(moveLineYRaw(i))
##  i -= 1

##i = 8
##while(i >= 0):
##  dot(dotPosRawX(i), dotPosRawY(0))
##  i -= 1

##startMoveEnvironment()

mbr = MoveBlockRender(pdf, barPerLineAim)
i = 0
m = dance['moves']
l = len(m)
while(i < l):
  #text(i, 1, m[i][0])
  mbr.addMove(m[i])
  i += 1

##mv = pdf.beginText(x(0), y(dotPosRawY(0)))
##print('mental at:' + str(x(0)) + ' ' + str( y(dotPosRawY(0))))

##mv.textLine('absolute mental')
# forget the scale and
##pdf.drawText(mv)

#mv.setTextTransform(0.866,0.5,-0.5,0.866,0,0)
#pdf.translate(2.4*inch, 1.5*inch)
#pdf.drawString(40, -60, "Kick")
##pdf.drawString(0, 0, "Kick")

#coords(canvas)
##endMoveEnvironment()

# forget the scale and
#pdf.drawText(mv)

#canvas.rotate(90)
#mv.setTextTransform(a,b,c,d,e,f)

#path = pdf.beginPath()
#path.moveTo(inch * 4, inch * 4)
#path.lineTo(inch * 3, inch * 4)
#path.lineTo(inch * 3.5, inch * 5)
#path.lineTo(inch * 4, inch * 4)

# stroke/fill
#pdf.drawPath(path, True, True)

#pdf.setFont("Courier", 30)
#pdf.drawString(2 * inch, inch, "For Your Eyes Only")

# move to next page
##pdf.showPage()

pdf.save()
