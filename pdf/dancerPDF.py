#!/usr/bin/python3

# requires python3-reportlab

#! should provide bar counts
#! how about replacement symbols like arrows for direction?
#! asserts
#! are all variables reacting?
#! tidying still to do in MoveBlockRender
#! more messages to 'reporter'
#! where established, remove 'print'

#print(c.getAvailableFonts())  
#c.setStrokeColorRGB(1, 0, 0)
#c.setFillColorRGB(0, 1, 0)


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
#A4 is default
#from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
import math


D_ACTION = 0
D_ISMOVE = 1
D_TARGET = 2
D_ISMANYBEAT = 3
D_PARAMS = 4



# if I don't use a class, Python cant privatise, and we end up with a 
# lot of publiized specifics. Tex won't privatise either, but for
# the sake of clarity... This does mean a certain amount of non-DRY
# reimplementation in the class, but for this critical, large. and 
# largely self-contained method, probably worth it.
class MoveBlockRender():
  def __init__(self,
   c,
   reporter,
   stockContext,
   barsInLineAim,
   lineTopSkip, 
   firstPageTopSkip,
   #moveblockFirstLineIndent,
   barlineGlue,
   minMoveGlueWidth,
   lastMovelineGlueMax,
   musicalDirectionContext,
   timeMarkContext,
   moveLineContentContext
  ):
    

    # useful methods

    # outside properties    
    self.c = c
    self.reporter = reporter
    
    # stockContext = [topStockAbs, rightStockAbs, leftStockAbs, bottomStockAbs]
    self.pageHeight = stockContext[0]
    self.pageWidth = stockContext[1]
    self.topStockAbs = stockContext[2]
    self.rightStockAbs = stockContext[3]
    self.leftStockAbs = stockContext[4]
    self.bottomStockAbs = stockContext[5]
    self.topMargin = stockContext[6]
    self.typeBlockWidth = self.rightStockAbs - self.leftStockAbs
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


    self.minMoveGlueWidth = minMoveGlueWidth
    self.lastMovelineGlueMax = lastMovelineGlueMax

    self.musicalDirectionFontFamily = musicalDirectionContext[0]
    self.musicalDirectionFontSize = musicalDirectionContext[1]
    self.musicalDirectionBottomSkip = musicalDirectionContext[2]
    #print('musicalDirectionFontSize: '+ str(self.musicalDirectionFontSize))

    self.timeMarkFontFamily = timeMarkContext[0]
    self.timeMarkFontSize = timeMarkContext[1]
    self.timeMarkWidth = timeMarkContext[2]
    self.timeMarkSkipDown = timeMarkContext[3]
    self.timeMarkLeftSkip = timeMarkContext[4]
    print('timeMarkLeftSkip: '+ str(self.timeMarkLeftSkip))
    
    self.moveLineContentFontFamily = moveLineContentContext[0]
    self.moveLineContentFontSize = moveLineContentContext[1]
    self.moveLineContentSkipDown = moveLineContentContext[2]
    self.moveLineMusicOnlyLeftSkip = moveLineContentContext[3]
    
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
  

  ## utils ##
  
  def startVerticalTextEnvironment(self):
    self.c.setFont(self.moveLineContentFontFamily, self.moveLineContentFontSize)
    self.c.saveState()
    # scale then translate
    self.c.rotate(270)
    self.c.translate(-self.pageHeight, 0)
  
  def endVerticalTextEnvironment(self):
    self.c.restoreState()


  ## renderers
  #! pass absY arround in preference
  def moveLineRender(self, toX, absY):
    self.c.line(self.leftStockAbs, absY, toX, absY)
  
  #? too simple. Could do with being extended, and visually stacking.
  def renderMusicalDirectionMarks(self, absX, absY, tempo):
    '''
    such as tempo.
    '''
    self.c.setFont(self.musicalDirectionFontFamily, self.musicalDirectionFontSize)
    self.c.drawString(absX, absY + self.musicalDirectionBottomSkip, 'tempo = ' + str(tempo))


  def renderTimeMark(self, absX, absY, event):
    s = str(event[D_PARAMS])
    self.c.setFont(self.timeMarkFontFamily, self.timeMarkFontSize)
    self.c.drawString(absX, absY - self.timeMarkSkipDown, s)

  def renderBeatCountChange(self, e):
    pass

  # Current strategy for barmarks:
  # They take a glue place
  # ...but add a small visual disruption. Probably 1/3 - 1/2 of glue.    
  # This places them maybe 2/3 between two sets of moves
  # Initial barmarks take no space, preceed whatever comes next
      
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
    #print('absX: '+ str(absX))
    #print('absY: '+ str(absY))
    #print('glueWidth: '+ str(glueWidth))
    #print('numberOfBarsToRender: '+ str(numberOfBarsToRender))

    # accumulate X progress. Start at absX.
    #? Nearly always left typeBlock. but if we introduce a 
    #? firstLineLeftIndent 
    curseX = absX
    
    if (self._moveStore[0][D_ISMOVE]):
      curseX += self.moveLineMusicOnlyLeftSkip

    # We'll stash movemarks to do all at once?
    moveStash = []


    # render start barmark
    self.renderBarmark(self.leftStockAbs, absY)
    
    #print('store size: ' + str(len(self._moveStore)))
   
    ii = 0
    barGlueWidth = glueWidth * self._barlineGlue
          
    while (ii < numberOfBarsToRender):
      event = self._moveStore.pop(0)
      #print('render: ' + event[D_ACTION])

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
          curseX += self.timeMarkLeftSkip
          self.renderTimeMark(curseX, absY, event)
          curseX += self.timeMarkWidth
        elif (event[D_ACTION] == 'tempoMark'):
          # NB adding leftskip is a cheat, but should mostly work.
          self.renderMusicalDirectionMarks(curseX + self.timeMarkLeftSkip, absY, event[D_PARAMS])
          
    # now get back to those marks
    i = 0
    l = len(moveStash)
    
    self.startVerticalTextEnvironment()
    # absY will not work in the rotated environment, It measures in
    # reportlab style from the bottom, rotated 3/4, so must work from
    # the page top.
    rAbsX = self._rotatedBlockLeftAbs + (self._lineTopSkip * self._pageLineI) + self.moveLineContentSkipDown


    while (i < l):
      e = moveStash[i]
      self.c.drawString(rAbsX, e[0], e[1][D_ACTION])
      i += 1
    self.endVerticalTextEnvironment()



  def calculateGlue(self, toBarcount, lineWidth):
    i = 0
    barcount = 0
    fixedSize = 0
    if (self._moveStore[0][D_ISMOVE]):
      fixedSize = self.moveLineMusicOnlyLeftSkip
    gluedEventCount = 0
    while(barcount < toBarcount):
      if (not self._moveStore[i][D_ISMOVE]):
        action = self._moveStore[i][D_ACTION]
        if (self.isBar(action)):
          gluedEventCount += self._barlineGlue
          barcount += 1
        #if (action == 'tempoMark'):
        # no effect on glue
        if (action == 'timeMark'):
          fixedSize += self.timeMarkWidth
          fixedSize += self.timeMarkLeftSkip
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
    # for sure we have less bars than we want, otherwise we'd trigger
    # a new line. But how many?
    # Could be done with a computeGlue(), but would be untidy.
    i = 0
    l = len(self._moveStore)
    barcount = 0
    while(i < l):
      action = self._moveStore[i][D_ACTION]
      if (self.isBar(action)):
        barcount += 1
      i += 1
    #print('remaining bars: ' + str(barcount))

    # need the width, whatever
    lineWidth = self.typeBlockWidth
    
    decidedBarCount = self._barsInLineAim
    if (barcount < self._barsInLineAim):
      self.reporter.info('bar count at end at end of block is short: requested:{0} : num of bars:{1}'.format(self._barsInLineAim, barcount))


    if (barcount < self._barsInLineAim - self.lastMovelineGlueMax):
      self.reporter.warning('Stubbing the last line (to change this, change lastMovelineGlueMax)')
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
      self.reporter.info('Expanding the last line')
      glueWidth = self.calculateGlue(barcount, lineWidth)
      # render the line itself
      self.moveLineRender(self.rightStockAbs, absY)
        
    decidedBarCount = barcount
          
    #self.renderCloseBarmark(absX, absY)
    self.renderLineContents(
      self.leftStockAbs,
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
    glueWidth = self.calculateGlue(self._barsInLineAim, self.typeBlockWidth)      

    #2
    decidedBarCount = self._barsInLineAim
    if (glueWidth < self.minMoveGlueWidth):
      self.reporter.warning('bar spilled because moves are too compressed :line {0}'.format(self._pageLineI + 1))
      #! if you do this, the glue width needs revising.
      decidedBarCount -= 1
      glueWidth = self.calculateGlue(decidedBarCount, self.typeBlockWidth)       

    
    #print('fixedSize: '+ str(fixedSize))
    #print('glueWidth:' + str(glueWidth))
    #print('decidedBarCount:' + str(decidedBarCount))

    
    self.renderLineContents(
      self.leftStockAbs,
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


######################################################################
class Reporter():
  def info(self, msg):
     print('[info] ' + msg)
    
  def warning(self, msg):
     print('[warning] '+ msg)









################################################
class DancerPDF():

  def __init__(self):
    self.reporter = Reporter()

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
  
    ## Page size ##
    self.pageStock = A4
    
      
    ## reportlab canvas ##
    #! as instance?
    self.c = Canvas("test.pdf", pagesize=self.pageStock)
    
    
    ## Stock ##
    #! no, 'typeblock'
    
    self._pageHeight = self.pageStock[1]
    self._pageWidth = self.pageStock[0]
    self._centerPage = self._pageWidth / 2
    
    self.leftMargin =  mm * 20
    self.rightMargin =  mm * 20
    self.topMargin =  mm * 20
    self.bottomMargin =  mm * 40
    
    
    self.rightStockAbs = self._pageWidth - self.rightMargin
    self.leftStockAbs = self.leftMargin
    self.topStockAbs = self._pageHeight - self.topMargin
    self.bottomStockAbs = self.bottomMargin
    
    # passed to renderMoveBlock
    self.stockContext = [self._pageHeight, self._pageWidth, self.topStockAbs, self.rightStockAbs, self.leftStockAbs, self.bottomStockAbs, self.topMargin]
   
     
    ###########################################################
    ## Page ##
  
    
    
    
    ## Title ##
    # carries space if necessary (when sections start)
    self.titleFontFamily = "Times-Roman"
    self.titleFontSize = 24
    self.titleTopSkip = 8
    
         
    # Internal
    # tracks the start height of the moves block
    # allowing space for main or section titles 
    self._titleHeightRaw = 0
    # currently 114, should be 95
        
  
    ## Sections ##
    self.sectionFontFamily = "Times-Roman"
    self.sectionFontSize = 24
    self.sectionTopSkip = 8
      

    
    
    ## Credits ##
    # If used, credits are aligned under the title. However, they do not
    # contribute to the overall space above the 
    # musicalDirections. This is to give maximum flexibility in overriding 
    # (for example, they could be in a column to the right of musical 
    # directions). To make space for them, increase musicalDirectionsTopSkip.
    self.creditsFontFamily = "Times-Roman"
    self.creditsFontSize = 14
    # above first credit
    self.creditsTopSkip = 0
    # above each credit
    self.creditLineTopSkip = 4
      
    ## Move block essentials ##
    # Declared early because musical directions need to be aligned with the
    # opening time signature.
    

    
    # fixed space to go before music.
    # This is inserted at the beginning of lines which
    # contain only music.
    # This needs to be something, or the first move will sit on the
    # first barline. About a quarter of the overall glue/note spacing
    # is ok.
    self.moveLineMusicOnlyLeftSkip = 14
    
    # Many music scores adopt an indent. Not often applicable here, so will 
    # usually be zero. If you have any material starting a move line, use it.
    # This variable can not be calculated (font width of time signature, 
    # and other material).
    # NOT IMPLEMENTED
    #moveblockFirstLineIndent = 0
    
    # Amount of glue for a barline (apears after the barline), by our
    # current calculation. Works best round 0.5.
    self.barlineGlue = 0.5
      
    # The last line in any block may not have the right number of bars.
    # The simplistic solution here, if the line is within this number of
    # bars then it will stretched to full width, otherwise the line is
    # rendered as stopping short. To always stretch, make this a relativly
    # large number e.g. 12. 0 will never stretch.
    self.lastMovelineGlueMax = 2
    
    
    
    ## MusicalDirections ##
    self.musicalDirectionFontFamily = "Times-Bold"
    self.musicalDirectionFontSize = 9
    self.musicalDirectionBottomSkip = 12
    
    self._musicalDirectionContext = [self.musicalDirectionFontFamily, self.musicalDirectionFontSize, self.musicalDirectionBottomSkip]
    
    
    ####################################################################
    ## The move block ##
    # The move block is almost all automatic layout. This has it's 
    # diadvantages, but we will see....
    
    # Space above the block.
    # Used to add space for the top line of tempo marks, clearing the
    # freely placed credits.
    self.movesBlockTopSkip = 24
    
    # gap between lines. Don't make too small.
    self.movesLineTopSkip = 96
    
    
    
    ####################################################################
    ## Time signature ##
    self.timeMarkFontFamily = "Times-Roman"
    self.timeMarkFontSize = 16
    
    # Reserve space for time signatures.
    # For marks at line starts and inline.
    # This variable can not be calculated (possible width of oversize font).
    # If the time signature font size is changed, alter by hand.
    # Should be, say, 3/2 of the width of the fonts as written as glyphs.
    self.timeMarkWidth = 24
    
    # How far down from the line to drop a time signature
    self.timeMarkSkipDown = 24

    # Fixed allocation for indenting a time mark.
    # The time mark sits at the beginning of it's allocation. this is 
    # used to push from barlines (and other preceeding content?). 
    # Should only be a handful of points.
    #! while this is necessary and good, more is needed. A pre-music 
    # indent to go after time signatures and before lines without time 
    # marks would be helpful.
    self.timeMarkLeftSkip = 4
    #timeMarkLeftSkip = 0
        
    self._timeMarkContext = [self.timeMarkFontFamily, self.timeMarkFontSize, self.timeMarkWidth, self.timeMarkSkipDown, self.timeMarkLeftSkip]
    
    
    
    
    ## moveLines ##
    
    # Express an interest in how many bars to a line
    # In many circumstances, will not be honoured. But used for open
    # bar rendering, so will stretch bars to fit the page width.
    #! what about sheet width, etc.?
    self.barPerLineAim = 5
    
    # fixed width for barmarks to occupy
    self.barmarkWidth = 24
    
    # The minimum glue allowed before bars are spilled to the next line
    self.minMoveGlueWidth = 14
    
    self.moveLineContentFontFamily = "Times-Roman"
    self.moveLineContentFontSize = 12
    
    # space down from the moveline to the move marks
    self.moveLineContentSkipDown = 8
    
    self.moveLineContentContext = [self.moveLineContentFontFamily, self.moveLineContentFontSize, self.moveLineContentSkipDown, self.moveLineMusicOnlyLeftSkip]
  
    
              
  def addInstruction(self, m):
    self.mbr.addInstruction(m)

  def save(self):
    self.c.save()
    
  #################################################################

     

  ###########################################################
  ## Coordinate functions ##
  # rawToAbsX() and rawToAbsY() convert *Raw positions to *Abs
  #
  
  #? unused 
  def rawToAbsX(self, x):
    return self.leftMargin + x
  
  def rawToAbsY(self, y):
    return self.topStockAbs - y
   
   
  def title(self, title):
    self.c.setFont(self.titleFontFamily, self.titleFontSize)
    self.c.drawCentredString(self._centerPage, self.rawToAbsY(self.titleTopSkip), title)
    self._titleHeightRaw = self.titleTopSkip + self.titleFontSize
  
  
  
  #! TODO  
  def section(self, title):
    # initialize
    self.c.showPage()
    self._titleHeightRaw = 0
    
    # render
    self.c.setFont(self.sectionFontFamily, self.sectionFontSize)
    self.c.drawCentredString(self._centerPage, self.rawToAbsY(self.sectionTopSkip), title)
    self._titleHeightRaw = self.sectionTopSkip + self.sectionFontSize
    

  def titleCredits(self, performers, transcribedBy):
    self.c.setFont(self.creditsFontFamily, self.creditsFontSize)
    #48
    self.c.drawRightString(self.rightStockAbs, self.rawToAbsY(self._titleHeightRaw + self.creditsTopSkip), performers)
    self._titleHeightRaw += self.creditsTopSkip + self.creditsFontSize
    #68
    self.c.drawRightString(self.rightStockAbs, self.rawToAbsY(self._titleHeightRaw + self.creditLineTopSkip), "Trns: " + transcribedBy)
  
  

  
  

  
  # Opens a movesblock
  def movesblock(self):
    self._titleHeightRaw += self.movesBlockTopSkip 
    return MoveBlockRender(
     self.c,
     self.reporter,
     stockContext = self.stockContext,
     barsInLineAim = self.barPerLineAim,
     lineTopSkip = self.movesLineTopSkip, 
     firstPageTopSkip = self._titleHeightRaw,
     #moveblockFirstLineIndent = moveblockFirstLineIndent,
     barlineGlue = self.barlineGlue,
     minMoveGlueWidth = self.minMoveGlueWidth,
     lastMovelineGlueMax = self.lastMovelineGlueMax,
     musicalDirectionContext = self._musicalDirectionContext,
     timeMarkContext = self._timeMarkContext,
     moveLineContentContext = self.moveLineContentContext
    )
  
  ## Utils ##
  #x deprecated, when we get times and tempo in the block class
  def moveLineYRaw(self, idx):
    # positioning for each line 
    return self._titleHeightRaw + (self.movesLineTopSkip * idx)
  
  
  
    
    
