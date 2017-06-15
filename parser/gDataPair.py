from utils import SimplePrint



# flower/include/drul-array.hh
class DataPair(SimplePrint):
  def __init__(self, frm, to):
    self.frm = frm
    self.to = to
    
  def set(self, frm, to):
    self.frm = frm
    self.to =  to  
    
#? do we need scale?
