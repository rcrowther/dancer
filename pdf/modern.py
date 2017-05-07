#!/usr/bin/python3

from dancerPDF  import DancerPDF

class Modern(DancerPDF):
  
  def __init__(self):
    DancerPDF.__init__(self)
    self.titleFontFamily = "Helvetica"



#def titleCredits(performers, transcribedBy):

#c.drawRightString(rightStock, y(_titleHeightRaw + creditLineTopSkip), "Trns: " + transcribedBy.upper())
