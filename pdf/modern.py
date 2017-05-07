#!/usr/bin/python3

from dancerPDF  import DancerPDF

class Modern(DancerPDF):
  
  def __init__(self):
    DancerPDF.__init__(self)
    self.titleFontFamily = "Helvetica-Bold"
    self.titleFontSize = 32
    self.sectionFontFamily = "Helvetica-Bold"
    self.creditsFontFamily = "Helvetica"
    self.creditsFontSize = 10
    self.musicalDirectionFontFamily = "Helvetica"
    self.musicalDirectionFontSize = 40
    self.timeMarkFontFamily = "Times-Roman-Bold"

    self.creditsTopSkip = 14
    self.creditLineTopSkip = 2
    
    self.movesBlockTopSkip = 64


#def titleCredits(performers, transcribedBy):

#c.drawRightString(rightStock, y(_titleHeightRaw + creditLineTopSkip), "Trns: " + transcribedBy.upper())
