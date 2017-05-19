#!/usr/bin/python3

#from iterators import *

from events import *


# Not for threads (you know it)
_uid = 1

def uid():
  global _uid
  _uid += 1
  return _uid
   
#! need error reporting
#! contexts need to be able to toEvents their own
#! build creation events. For use from parsing. 
class Context():
  '''
  Every context knows the iterator it will use if it needs one. 
  Iterators are used at their most complex to walk a parse and
  interleave it. One iterator calls another down the Context tree.
  
  The StreamContext takes a pre-compiled, interleaved stream and has
  its own iterator. Due to the compilation, this is a simple
  configuration.
  
  '''
  def __init__(self, uid, name):
    self.entitySuffix = type(self).__name__

    self._name = name
    # doubles up meanings, either subcontexts or a list of music
    # events. Both children, both iterable, though. 
    self.children = []
    self.uid = uid
    
    '''
    Every context can process it's input stream.
    The stack of processors is built here.
    '''
    self.processors  = []
    
    # The iterator can be
    # building from source AST
    # - child stream
    # - other iterators
    # bulding from a stream
    self.it = None
    
    # properties could e on the object
    # but I don't want this too Python
    # general. Written to streams
    self.properties = {}
    # internal. Ued for temp
    self._iProperties = {}
    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name
    
  #?x
  def mergeProperty(self, k, v):
    self.properties[k] = v
  #?x
  def readProperty(self, k):
    return self.properties[k]
  #?x
  def deleteProperty(self, k):
    del self.properties[k]
    
    
  def isLeaf(self):
    return (len(self.children) == 0)

  def prepareAsParsedData():
    pass
    
  def _toPropertyEvents(self, b):
    for k, v in self.properties.items():
      e = MergeProperty(self.uid, k, v)
      b.append(e)
    for child in self.children:
      # contexts are the first in a child list, so breaking is ok.
      # ...and spares us iterting every DanceMove child
      if (isinstance(child, Context)):
        child._toPropertyEvents(b)
      else:
        break
    return b
    
  def toPropertyEvents(self):
    return self._toPropertyEvents([])
    
    
  def _toCreateEvents(self, parentId, b):
    e = CreateContext(parentId, self.uid, self.name)
    b.append(e)
    for child in self.children:
      # contexts are the first in a child list, so breaking is ok.
      # ...and spares us iterting every DanceMove child
      if (isinstance(child, Context)):
        child._toCreateEvents(self.uid, b)
      else:
        break
    return b
    
  def toCreateEvents(self):
    '''
    Should only be called on Global, or parents are undetermined?
    '''
    return self._toCreateEvents(0, [])

  def extendString(self, b):
    b.append(str(self.uid))
    b.append(', ')
    b.append(str(self.properties))


  def addChildren(self, b):
    b.append(', [')
    first = True
    for e in self.children:
      if (first):
        first = False
      else:
        b.append(", ")
      e.addString(b)
    b.append(']')
    
  def addString(self, b):
    b.append(self.entitySuffix)
    b.append('(')
    self.extendString(b)
    self.addChildren(b)
    #b.append(str(self.children))
    b.append(')')
    return b
    
  def __str__(self):
    return "".join(self.addString([]))  
    
    
    
class DancerContext(Context):
  def __init__(self):
    Context.__init__(self, uid(), 'Dancer')
    #self.eventStream = [Finish()]
    #self.it = eventIt
    #self.it.contextUID = self.uid
  
  #? unused
  def prepare(self):
    #self.it = StreamIterator(self.eventStream)
    pass

  def prepareAsParsedData(self):
    self.it = ParsedDanceeventIterator()
    self.it.prepare(self.uid, self.children)


class ScoreContext(Context):
  def __init__(self):
    Context.__init__(self, uid(), 'Score')
    #self.it = ChildContextIterator()
    #self.it.contextUID = self.uid

  #x unused
  def prepare(self):
    #self.it = ChildContextIterator()
    for c in self.children:
      # recurse
      c.prepare()
      #self.it.addChild(c)

  def _delete(self, lst, uid):
    i = 0
    l = len(lst)
    while(i < l):
      if (lst[i].contextUID == uid):
        lst.pop(i)
        break
      else:
        i += 1
        
  def addChild(self, context):
    self.children.append(context)
    self.it.addChild(context.it)  
    
  def deleteChild(self, uid):
    self._delete(children, uid)
    # on iterator exhaustion, is autodeleted anyhow?
    #? do we ever manually delete before exhaustion?
    self.it.deleteChild(uid) 

# we need to be able to modify properties...
class Processor():
  def __init__(self, context):
    self.context = context
    
  def process(self, context, moment, inStream):
    pass
    
class PrintStage(Processor):
  def process(self, context, moment, inStream):
    print('moment: ' + str(moment))
    b = ''
    for e in inStream:
      b += str(e)
      b += ', '
    print(b) 
    return inStream

class Build(Processor):
  def __init__(self, context):
    Processor.__init__(self, context)
    self.b = ''
    #context._iProperties['stream-builder'] = []

  def process(self, context, moment, inStream):
    for e in inStream:
      #self.b.append(str(e))
      #self.b.append(', ')
      self.b += str(e)
      self.b += ', '
    return inStream 
  
#class Timing(Processor):
  ## Should update currentMoment and currentBar
  #def __init__(self, context):
    #Processor.__init__(self, context)
    #self.momentCount = 0
    #context._iProperties['currentMoment'] = 4
    #context._iProperties['currentBar'] = 0
    #context._iProperties['currentBeatsPerBar'] = 4

  #def process(self, context, moment, inStream):
    #return inStream 
    
    
class GlobalContext(Context):
  def __init__(self):
    Context.__init__(self, 0, 'Global')
    self.outStream = []
    #self.score = Score()
    #self.it = self.score.it
    #! A lot not right
    #! how to output results from a process phase? In the phase?
    #! howto initially load phases?
    #!
    p = PrintStage(self)
    self.processors  = [
    p.process
    ]
    #p = Build(self)
    #self.processors  = [
    #p.process
    #]
    
    
  #x unused
  def prepare(self):
    # recurse
    self.score.prepare()
    #self.it = self.score.it
    
  def pendingMoment(self):
     return self.it.pendingMoment()

  #! should we process events singly? Probably yes?
  #! this will not work for parser-sourced events with no moments?
  #! how to return events to te stream. This isnt. Do we need deletions?
  def process(self, moment, events):
    r = events
    for p in self.processors:
      p(self, moment, r)
    #self.outStream.append(PrepareEvent('context', 1))
    #self.outStream.extend(events)

  #? Should iterators be part of process?
  #? context names need to be set on events.
  def runIterator(self):
    it = g.score.it
    while(True):
      pm = it.pendingMoment()
     # print('pending:' + str(pm))
      if (pm == -2):
        break
      r = it.__next__()
      self.process(pm, r)
    print('done')



from events import *
from iterators import *





#d1 = DancerContext()
#d1.properties['dancerName'] = 'frontman'

#d2 = DancerContext()
#d2.properties['dancerName'] = 'Eric'
#d2.properties['beatsPerBar'] = 6

#s = ScoreContext()
#s.children.append(d1)
#s.children.append(d2)
#s.properties['beatsPerBar'] = 4
#s.properties['tempo'] = 80

#g = GlobalContext()
#g.children.append(s)
#g.properties['title'] = "Coconutters"
#g.properties['style'] = 'clog'

#print(str(g))

#xe = g.toCreateEvents()
#for e in xe:
  #print(e)

#xe = g.toPropertyEvents()
#for e in xe:
  #print(e)

#g.runIterator()

stream = [DanceEvent(4, "clap", 1, []), DanceEvent(4, "clap", 1, ['overhead']), DanceEvent(4, "step", 1, ['west']), MomentStart(-3), DanceEvent(4, "cross", 1, ['legs']), DanceEvent(4, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(4, "jump", 1, ['south']), DanceEvent(4, "hands", 1, ['ears']), MomentEnd(), DanceEvent(4, "r", 6, []), DanceEvent(4, "swipe", 2, ['low']), DanceEvent(4, "jump", 1, ['spot'])]
d = DancerContext()
d.children.extend(stream)
d.prepareAsParsedData()
print(str(d.it))
