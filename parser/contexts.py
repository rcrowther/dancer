#!/usr/bin/python3

from iterators import *



# Not for threads (you know it)
_uid = 1

def uid():
  global _uid
  _uid += 1
  return _uid
   
#! contexts need to be able to toEvents their own
#! build creation events. For use from parsing. 
class Context():

  def __init__(self, uid, name):
    self._name = name
    # To some means doubles up, either subcontexts or a list of music
    # events. Both children, both iterable, though. 
    self.children = []
    self.uid = uid
    # The itertor can be
    # building from source AST
    # - child stream
    # - other terators
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
    
    
  def mergeProperty(self, k, v):
    self.properties[k] = v

  def readProperty(self, k):
    return self.properties[k]
        
  def deleteProperty(self, k):
    del self.properties[k]
    
    
  def isLeaf(self):
    return (len(self.children) == 0)



    
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

#stream1 = [
  #CreateContext(4, 'dancer'),
  #MergeProperty('context', 'indent-stave', 2),
  #PrepareEvent('context', 0),
  #MusicEvent('context', 'clap', 1, 'mid'),
  #MusicEvent('context', 'clap', 1, 'mid'),
  #PrepareEvent('context', 1),
  #MusicEvent('context', 'step', 1, 'south'),
  #PrepareEvent('context', 2),
  #MusicEvent('context', 'point', 1, 'right'),
  #Finish()
#]
#stream2 = [
  #MergeProperty('dancer2', 'indent-stave', 2),
  #Finish()
#]


#d1 = Dancer(StreamIterator(stream1))
#d1.eventStream = stream1

#it = d1.it
#while(True):
  #print('pending:' + str(it.pendingMoment()))
  #r = it.__next__()
  #b = ''
  #for e in r:
    #b += str(e)
    #b += ', '
  #print(b)

#d1 = Dancer(StreamIterator(stream1))
#d2 = Dancer(StreamIterator(stream2))



#g = Global()

#g.score.addChild(d1)
#g.score.addChild(d2)


#g.runIterator()
