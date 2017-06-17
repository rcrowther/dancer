
from utils import SimplePrint

class DancePart(SimplePrint):
  def __init__(self, template, level, meta, dance):
    self.template = template
    self.level = level
    self.dance = None
    self.meta = meta
    
  def process(self):
    self.template.writeHeadline(self.level, self.meta.title)
    if (self.meta.subhead):
      self.template.writeSubhead(self.level, self.meta.subhead)
    if (self.dance):
      #! More here, unwrap, paging, etc.?
      self.template.writeDance(self.dance)

    



