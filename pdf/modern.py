#!/usr/bin/python3


titleFontFamily = "Helvetica"



def titleCredits(performers, transcribedBy):
  global _titleHeightRaw
  c.setFont(creditsFontFamily, creditsFontSize)
  #48
  c.drawRightString(rightStock, y(_titleHeightRaw + creditsTopSkip), performers)
  _titleHeightRaw += creditsTopSkip + creditsFontSize
  #68
  c.drawRightString(rightStock, y(_titleHeightRaw + creditLineTopSkip), "Trns: " + transcribedBy.upper())
