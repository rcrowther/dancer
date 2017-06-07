from enums import Axis

from collections import namedtuple
from gInterval import GIntervalEmpty
from utils import SimplePrint

#GCacheData = namedtuple('GCacheData', 'offset parent extent')

class GCacheData(SimplePrint):
  def __init__(self, offset, parent, extent):
    self.offset = offset
    self.parent = parent
    self.extent = extent
    
  def extendString(self, b):
    b.append(str(self.offset))
    b.append(', ')
    b.append(str(self.extent))
    
  #def isEmpty(self):
  #  return 
    
def GCacheDataEmpty():
  return GCacheData(0, None, GIntervalEmpty)


