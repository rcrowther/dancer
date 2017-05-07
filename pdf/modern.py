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


#! mod to capitalize credit names?

  def titleCredits(self, performers, transcribedBy):
    self.c.setFont(self.creditsFontFamily, self.creditsFontSize)
    #48
    self.c.drawRightString(self.rightStockAbs, self.rawToAbsY(self._titleHeightRaw + self.creditsTopSkip), performers)
    self._titleHeightRaw += self.creditsTopSkip + self.creditsFontSize
    #68
    self.c.drawRightString(self.rightStockAbs, self.rawToAbsY(self._titleHeightRaw + self.creditLineTopSkip), "Trns: " + transcribedBy.upper())
  
