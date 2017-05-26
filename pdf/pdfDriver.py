#!/usr/bin/python3

# requires python3-reportlab
# reportlab coordinates, bottom left.

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.graphics.shapes import Drawing, String
#import reportlab.graphics.shapes
import math


import os
import reportlab
#s.dumpProperties()
# Type 1
#folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
#afmFile = os.path.join(folder, 'DarkGardenMK.afm')
#pfbFile = os.path.join(folder, 'DarkGardenMK.pfb')
#from reportlab.pdfbase import pdfmetrics
#justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
#faceName = 'DarkGardenMK' # pulled from AFM file
#pdfmetrics.registerTypeFace(justFace)
#justFont = pdfmetrics.Font('DarkGardenMK',
#faceName,
#'WinAnsiEncoding')
#pdfmetrics.registerFont(justFont)

#tryuetype
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#/usr/share/fonts/truetype/freefont/FreeSans.ttf
#pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
#pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
#pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
#pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSF', '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'))
#/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf
#canvas.setFont('Vera', 32)
#canvas.drawString(10, 150, "Some text encoded in UTF-8")
#canvas.drawString(10, 100, "In the Vera TT Font!")

class PDFWriter():
  def __init__(self):
    ## Page size ##
    self.stock = A4
    self._stockHeight = self.stock[1]
    self._stockWidth = self.stock[0]

    ## base font ##
    self.baseFontFamily = "Times-Roman"
    self.baseFontSize = 12
    
    self.currentFontFamily = self.baseFontFamily
    self.currentFontSize = self.baseFontSize

    
    ## block sizing ##       
    self.c = Canvas("test.pdf", pagesize=self.stock)
    self.marginTop = mm * 20
    self.marginRight = mm * 20
    self.marginBottom =mm * 40
    self.marginLeft = mm * 20
    
    self.c.translate(self.marginLeft, self.marginBottom)
    self.blockHeight =  self._stockHeight - self.marginTop - self.marginBottom
    self.blockWidth = self._stockWidth - self.marginLeft - self.marginRight
    self.blockXCenter = self.blockWidth / 2
    self.blockYCenter = self.blockHeight / 2

    ## font ##
    self.resetFont()

  def startVerticalTextEnvironment(self):
    self.c.saveState()
    # translate back to corner
    self.c.translate(-self.marginLeft, -self.marginBottom)
    # rotate
    self.c.rotate(270)
    # translate to bottom corner
    self.c.translate(-self._stockHeight + self.marginTop, self.marginLeft)

  def endVerticalTextEnvironment(self):
    self.c.restoreState()
  
  def verticalString(self, x, y, s):
    '''
    Only to be called in the vertical environment.
    Places at xy as if nothing moved.
    '''
    self.c.drawString(self.blockHeight - y, x, s)
    
  def setFont(self, family, size):
    self.currentFontFamily = family
    self.c.setFont(self.currentFontFamily, size)
    
  def setFontSize(self, size):
    self.currentFontSize = size
    self.c.setFont(self.currentFontFamily, size)
    
  def setFontFamily(self, family):
    self.c.setFont(family, self.currentFontSize)    

  def resetFont(self):
    self.c.setFont(self.baseFontFamily, self.baseFontSize)
          
  def save(self):
    self.c.save()
    
  def vLine(self, x, y, toY):    
    self.c.line(x, y, x, toY)
    
  def hLine(self, x, toX, y):    
    self.c.line(x, y, toX, y)

  def string(self, x, y, s): 
    return self.c.drawString(x, y, s)

  def centeredString(self, x, y, s): 
    return self.c.drawCentredString(x, y, s)

  def stencil(self, points, close):
    self.c.setLineWidth(5)
    p = self.c.beginPath()
    xs, ys = points.pop(0)
    p.moveTo(xs, ys)
    for x1, y1 in points:
      p.lineTo(x1, y1)
    if (close):
      p.close()
    self.c.drawPath(p)

  def invertY(self, y):
    '''
    Y coorinates relative to top left corner
    '''
    return self.blockHeight - y
    
    
  def test(self):
    self.hLine(0,  self.blockWidth, self.blockHeight)    
    self.vLine(0,  0, self.blockHeight)    
    self.hLine(0,  self.blockWidth, 0)    
    self.vLine(self.blockWidth,  0, self.blockHeight)    
    #self.hLine(self._centerPage,  self._blockWidth, self._blockHeight/2)    
    self.setFontSize(32)
    self.setFontFamily('LiberationSF')
    self.centeredString(self.blockXCenter, self.blockYCenter, 'doya?')
    self.resetFont()
    self.startVerticalTextEnvironment()
    self.verticalString(self.blockXCenter, self.invertY(0), 'hangin...')
    self.endVerticalTextEnvironment()
    self.string(self.blockXCenter, self.blockYCenter - 40, 'teh ah')
    self.stencil([(30, 30),(100, 30), (100, 25)], False)
    self.save()

w = PDFWriter()
w.test()
