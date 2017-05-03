#!/usr/bin/python3

# requires python3-reportlab

#! need vertical words

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
#A4 is default
#from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica

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
  ['point', 0, False, WEST],
  ['point', 1, False, EAST],
  ['step', 0, False, WEST],
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
  ['point', 1, False, EAST]
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

## foreword ##
bottomForewordRaw = 95


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
  #pdf.setFont("Times-Roman", 12)
  pdf.setFont("Times-Roman", 24)
  pdf.saveState()
  # scale then translate
  pdf.rotate(270)
  #pdf.rotate(315)
  print('ttrns at:' + str(-pageHeight) + ' ' + str(-pageWidth))
  pdf.translate(-pageHeight, 0)

def endMoveEnvironment():
  pdf.restoreState()


def text(xp, yp, txt):
  # x ok, y inverted
  print('clap at:' + str(lineYRaw(yp)) + ' ' + str(textPosRawX(xp)))
  #pdf.drawString(173, 89, txt)
  pdf.drawString(lineYRaw(yp), dotPosRawX(xp), txt)


# specialist helpers #

def timeSignature(count):
  yd = lineYRaw(0) + 24
  pdf.setFont("Times-Bold", 24)
  ts = pdf.beginText(x(0), y(yd))
  ts.textLine(str(count))
  #print(str(count))
  pdf.drawText(ts)
  
#pdf.setStrokeColorRGB(1, 0, 0)
#pdf.setFillColorRGB(0, 1, 0)

## Titles ##
pdf.setFont("Times-Roman", 24)
pdf.drawCentredString(A4[0] / 2, y(18), dance['title'])


pdf.setFont("Times-Roman", 18)
#perf = pdf.beginText(x(0), y(48))
#perf.textLine(dance['performers'])
#pdf.drawText(perf)
pdf.drawRightString(rightStock, y(48), dance['performers'])

#author = pdf.beginText(x(0), y(68))
#author.textLine("Trns: " + dance['transcribed'])
pdf.drawRightString(rightStock, y(68), "Trns: " + dance['transcribed'])

## body ##
timeSignature(dance['beatbar'])




i = 8
while(i >= 0):
  hline(lineYRaw(i))
  i -= 1

i = 8
while(i >= 0):
  dot(dotPosRawX(i), dotPosRawY(0))
  i -= 1

startMoveEnvironment()

i = 0
m = dance['moves']
while(i < 14):
  text(i, 1, m[i][0])
  i += 1
  
mv = pdf.beginText(x(0), y(dotPosRawY(0)))
print('mental at:' + str(x(0)) + ' ' + str( y(dotPosRawY(0))))

mv.textLine('absolute mental')
# forget the scale and
pdf.drawText(mv)

#mv.setTextTransform(0.866,0.5,-0.5,0.866,0,0)
#pdf.translate(2.4*inch, 1.5*inch)
#pdf.drawString(40, -60, "Kick")
pdf.drawString(0, 0, "Kick")

#coords(canvas)
endMoveEnvironment()

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
pdf.showPage()

pdf.save()
