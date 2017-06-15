#from gData import TextData
#from enums import FontStyle

class PaperColumn(gItem):
  '''
  Style unused, but could be several things?
  '''
  def __init__(self, newId = -1):
    #gItem.__init__(self)
    self.uid = newId
    self.root = root
    self.root = None
    self._isUsed = False
    self.boundedByMe = []
    self.isBreakable = False
    
  def new(self, paperColumn):
    return PaperColumn(paperColumn.uid)
    
  def less(self, other):
    return self.uid < other.uid

  def setRoot(self, root):
    self.root = root

  def isUsed(self):
    return (
    self._isUsed 
    or self.boundedByMe
    or self.isBreakable
    )
# interseting:
# break_align_width
#? NB: MAKE_SCHEME_CALLBACK (Paper_column, before_line_breaking, 1);
#before_line_breaking
