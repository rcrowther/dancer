from enums import Axis

from collections import namedtuple
from gInterval import GIntervalEmpty

GCacheData = namedtuple('GCacheData', 'offset parent extent')

def GCacheDataEmpty():
  return GObjData(0, None, GIntervalEmpty)


