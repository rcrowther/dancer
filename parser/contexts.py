#!/usr/bin/python3

from iterators import *



# Not for threads (you know it)
_uid = 1

def uid():
  global _uid
  _uid += 1
  return _uid
   
      
class Context():
  #NB: put properties on the object
  def __init__(self, uid, name):
    self.name = name
    self.children = []
    self.uid = uid
    # The itertor can be
    # building from source AST
    # - child stream
    # - other terators
    # bulding from a stream
    self.it = None
    
    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name
    
 # def addChild(self, child):
 #   self.children.append(child)
 #   return child
    
  def isLeaf(self):
    return (len(self.children) == 0)



    
class Dancer(Context):
  def __init__(self, eventIt):
    Context.__init__(self, uid(), 'Dancer')
    self.eventStream = [Finish()]
    self.it = eventIt
    self.it.contextUID = self.uid
  
  def prepare(self):
    #self.it = StreamIterator(self.eventStream)
    pass



class Score(Context):
  def __init__(self):
    Context.__init__(self, uid(), 'Score')
    self.it = ChildContextIterator()
    self.it.contextUID = self.uid

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


class Global(Context):
  def __init__(self):
    Context.__init__(self, 0, 'Global')
    self.outStream = []
    self.score = Score()
    #self.it = self.score.it
      
  def prepare(self):
    # recurse
    self.score.prepare()
    #self.it = self.score.it
    
  def pendingMoment(self):
     return self.it.pendingMoment()

  def process(self, moment, events):
      print('moment:' + str(moment))
      b = ''
      for e in events:
        b += str(e)
        b += ', '
      print(b) 
      self.outStream.append(PrepareEvent('context', 1))
      self.outStream.extend(events)

          
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

stream1 = [
  CreateContext(4, 'dancer'),
  MergeProperty('context', 'indent-stave', 2),
  PrepareEvent('context', 0),
  MusicEvent('context', 'clap', 1, 'mid'),
  MusicEvent('context', 'clap', 1, 'mid'),
  PrepareEvent('context', 1),
  MusicEvent('context', 'step', 1, 'south'),
  PrepareEvent('context', 2),
  MusicEvent('context', 'point', 1, 'right'),
  Finish()
]
stream2 = [
  Finish()
]


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

d1 = Dancer(StreamIterator(stream1))
d2 = Dancer(StreamIterator(stream2))



g = Global()

g.score.addChild(d1)
g.score.addChild(d2)

#print(g)
#g.prepare()
##print(str(g.pendingMoment()))

g.runIterator()
