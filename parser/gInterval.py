from utils import SimplePrint




class GInterval(SimplePrint):
  def __init__(self, frm, to):
    self.frm = frm
    self.to = to
    
  def translate(self, value):
    self.frm += value
    self.to += value
    
  def widen(self, value):
    self.frm -= value
    self.to += value

  def size(self):
    if (self.to > self.frm):
      return self.to - self.frm
    else:
      return self.frm - self.to
   
  def isEmpty(self):
    return (self.frm > self.to)
    
  def contains(self, value):
    return ((value > self.frm) and (value < self.to))

  def containsInterval(self, i):
    return ((i.frm > self.frm) and (i.to < self.to))
        
  def addInterval(self, i):
    self.frm += i.frm
    self.to += i.to
     
  def negate(self):
    frm = -self.frm 
    to = -self.to
    self.frm = to 
    self.to = frm
    
  def swap(self):
    frm = self.frm
    self.frm = self.to 
    self.to = frm
    
  def centre(self):
    assert(not self.isEmpty())
    return ((self.to - self.to) / 2)

  def extendString(self, b):
    b.append(str(self.frm))
    b.append(', ')
    b.append(str(self.to))



def GIntervalEmpty(self):
  return GInterval(0, 0)
