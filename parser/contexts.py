#!/usr/bin/python3

#from iterators import *


from events import *
from dispatchers import *

from EventIterators import EventIterator, EventIteratorFile
import Timer

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
    # - child danceevents
    # - child context iterators
    # or from an event stream
    self.it = None
    
    # Used to dispatch events to builder classes
    self.dispatcher = None
    
    # hanger for lists of graphic objects
    self.gList = []
    
    # properties could be on the Context object
    # but I don't want this too Python
    # general. This one general and written to streams
    self.properties = {}
    
    # internal. Used for temp properties, not persited 
    # by event streams
    self._props = {}
    

    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name
    
  # Following are useful for external controls i.e. dancerc
  #? make general API, even for chainLinks?
  def mergeProperty(self, k, v):
    self.properties[k] = v

  def containsProperty(self, k):
    return (self.properties.get(k) == None)

  def readProperty(self, k):
    return self.properties[k]

  def readPropertyOption(self, k):
    return self.properties.get(k)
    
  def deleteProperty(self, k):
    del self.properties[k]

  ## props ##
  def mergeProp(self, k, v):
    self._props[k] = v

  def containsProp(self, k):
    return (self._props.get(k) == None)

  def readProp(self, k):
    return self._props[k]

  def readPropOption(self, k):
    return self._props.get(k)
    
  def deleteProp(self, k):
    del self._props[k]
        
        
  def appendChild(self, v):
    '''
    This accessor allows us to reimplement if necessary.
    Notably, DummyContext, which has no tree-building needs,
    disables this method.
    '''
    self.children.append(v)
  
  def isLeaf(self):
    return (len(self.children) == 0)


  ## parse data actions ##
  def prepareAsParsedData(self):
    pass


  ## event stream actions ##

    
  ## Dispatch methods ##
  # @ctx stub parameter to satisfy dispatch callback 
  def createChildContext(self, ctx, event):
    assert(isinstance(event, CreateContext))
    assert(event.newType != 'Global')
    ctx = None
    tpe = event.newType
    if (tpe == 'Score'):
      ctx = ScoreContext()
    if (tpe == 'Dancer'):
      ctx = DancerContext()
    #if (tpe == 'DancerGroup'):
      #ctx = DancerGroup()
    ctx.uid = event.newId
    self.appendChild(ctx)
    # print('Child appended contextType: {0}: id:{1}'.format(oldId))
    
    # set up the dispatcher
    ctx.dispatcher = Dispatcher(ctx)
    self.dispatcher.startSayingToDispatcher(ctx.dispatcher)
    # new context can hear context creation
    ctx.dispatcher.startSayingTo(ctx.createChildContext, 'CreateContext')
    ctx.dispatcher.startSayingTo(ctx.deleteChildContext, 'DeleteContext')

  # @ctx stub parameter to satisfy dispatch callback 
  def deleteChildContext(self, ctx, event):
    assert(isinstance(event, DeleteContext))
    oldId = event.oldId
    broken = False
    for idx, e in enumerate(self.children):
      if (e.uid == oldId):
        del (self.children[idx])
        broken = True
        break
    #! should be warning report
    if(not broken):
      print('Child to delete not found parentName: {0} : parentId: {1} : id to remove: {2}'.format(self.name, self.uid, oldId))
    else:
      # we found and deleted a context.
      # remove deleted context from this dispatcher
      self.dispatcher.stopSayingToDispatcher(oldId)


  ## toEvent returns ##    
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
    
  #! merge with property events
  def _toCreateEvents(self, parentId, b):
    '''
    Top-down, for saner creation
    '''
    # ignore the top global, it will already exist to build the rest
    # of the tree. Not putting in the stream means sparing us nasty
    # detection when processing streams.
    if (self.uid != 0):
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

  def _toDeleteEvents(self, parentId, b):
    '''
    Bottom-up, for saner destruction
    '''
    for child in self.children:
      # contexts are the first in a child list, so breaking is ok.
      # ...and spares us iterting every DanceMove child
      if (isinstance(child, Context)):
        child._toDeleteEvents(self.uid, b)
      else:
        break
        
    # ignore the top GlobalContext, it can not delete itself 
    # (not in Python).
    # Not putting in the stream means sparing us nasty
    # detection when processing streams.
    if (self.uid != 0):
      e = DeleteContext(parentId, self.uid)
      b.append(e)
    return b
    
  #! move to global?
  def toDeleteEvents(self):
    '''
    Should only be called on Global, or parents are undetermined?
    '''
    return self._toDeleteEvents(0, [])
    
  def extendString(self, b):
    b.append(str(self.uid))
    b.append(', ')
    b.append(str(self.properties))


  ## Printers ##
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
    



class DummyContext(Context):
  '''
  A near-empty version of context.
  This is used to parse variables, where we have no need to collect 
  data.
  So appendChild is passed.
  '''
  def __init__(self):
    Context.__init__(self, -1, 'Dummy')
  
  #! all these actions should generate errors
  def appendChild(self, v):
    pass
    
  def createChildContext(self, event):
    pass
    
  def deleteChildContext(self, event):
    pass
    
  def prepareAsParsedData(self):
    pass

  ## Dispatchers ##
   
    
    
    
    
#? A Dancer can not create a child context
#? but has a dispatcher?
class DancerContext(Context):
  def __init__(self):
    Context.__init__(self, uid(), 'Dancer')


  def prepareAsParsedData(self):
    self.it = ParsedDanceeventIterator()
    self.it.prepare(self.uid, self.children)

  ## dispatch building ###


  def createChildContext(self, event):
    print("DancerContext" + "error, no child context")



      
class ScoreContext(Context):
  def __init__(self):
    Context.__init__(self, uid(), 'Score')


  def prepareAsParsedData(self):
    #recurse
    for c in self.children:
      c.prepareAsParsedData()
    self.it = ChildContextIterator()
    self.it.prepare(self.uid, [ctx.it for ctx in self.children])


  def _delete(self, lst, uid):
    i = 0
    l = len(lst)
    while(i < l):
      if (lst[i].contextUID == uid):
        lst.pop(i)
        break
      else:
        i += 1
        
  #x
  #def addChild(self, context):
    #self.children.append(context)
    #self.it.addChild(context.it)  
    
  #def deleteChild(self, uid):
    #self._delete(children, uid)
    ## on iterator exhaustion, is autodeleted anyhow?
    ##? do we ever manually delete before exhaustion?
    #self.it.deleteChild(uid) 


  #def createChildContext(self, event):
  #  Context.createChildContext(event)
    
    
  ## dispatch building ###

      



    
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
    self.processors  = []
    #p = Build(self)
    #self.processors  = [
    #p.process
    #]
    # Set this on ititialization
    self.dispatcher = Dispatcher(self)
    self.dispatcher.startSayingTo(self.createChildContext, 'CreateContext')
    self.dispatcher.startSayingTo(self.deleteChildContext, 'DeleteContext')



  ## parse data actions ##
  def prepareAsParsedData(self, srcName):
    # sets up parse data iterators
    # must be called when data in place
    assert(len(self.children) == 1)
    #recurse
    for c in self.children:
      c.prepareAsParsedData()
    self.it = ParseCompileIterator(srcName)
    de = self.toDeleteEvents()
    de.append(Finish())
    ctxEvents = self.toCreateEvents()
    ctxEvents.extend(self.toPropertyEvents())
    self.it.prepare(0, [ctxEvents, de, self.children[0].it])



  ## event stream actions ##
    #self.createChildContext(event)
  def prepareForEventSteamData(self, eventIterator):
    # sets up stream data iterator
    assert( isinstance(eventIterator, EventIterator) )
    assert( not(self.children) )
    self.it = eventIterator

    
  ## chain processing actions ##
  def setChainAs(self, chain):
    self.processors = chain

  #! should we process events singly? Probably yes?
  #! this will not work for parser-sourced events with no moments?
  #! how to return events to te stream. This isnt. Do we need deletions?
  def runProcessChain(self):
    for p in self.processors:
      p.before(self.properties)
    while(self.it.hasNext()):
      e = self.it.next()
      for p in self.processors:
         p.process(self.properties, e)
    for p in self.processors:
      p.after(self.properties)

  ## dispatch building ###
  def runIteratorToDispachBuilders(self):
    while(self.it.hasNext()):
      e = self.it.next()
      self.dispatcher.say(e)


  def runGraphicsChain(self):
    for p in self.processors:
      p.before(self)
    # cant happen because this creates/deletes contexts
    # so creating needs to load the appropriate process queue
    # then run init...
    #self.runIteratorToDispachBuilders()

## Tests ##
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

## Event printing ##
#xe = g.toCreateEvents()
#for e in xe:
  #print(e)

#xe = g.toPropertyEvents()
#for e in xe:
  #print(e)



## Parse building ##  

#stream1 = [DanceEvent(6, "clap", 1, []), DanceEvent(6, "clap", 1, ['overhead']), DanceEvent(6, "step", 1, ['west']), MomentStart(-3), DanceEvent(6, "cross", 1, ['legs']), DanceEvent(6, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(6, "jump", 1, ['south']), DanceEvent(6, "hands", 1, ['ears']), MomentEnd(), DanceEvent(6, "bend", 1, ['knees']), DanceEvent(6, "slap", 1, ['other']), DanceEvent(6, "slap", 2, ['knees']), DanceEvent(6, "twirl", 1, ['right']), DanceEvent(6, "split", 1, ['knees']), DanceEvent(6, "turn", 1, ['west']), MergeProperty(6, "beatsPerBar", 3), MergeProperty(6, "tempo", 80), DanceEvent(6, "kick", 1, ['low'])]
#stream2 = [DanceEvent(4, "clap", 1, []), DanceEvent(4, "clap", 1, ['overhead']), DanceEvent(4, "step", 1, ['west']), MomentStart(-3), DanceEvent(4, "cross", 1, ['legs']), DanceEvent(4, "cross", 1, ['hands']), MomentEnd(), MomentStart(-3), DanceEvent(4, "jump", 1, ['south']), DanceEvent(4, "hands", 1, ['ears']), MomentEnd(), DanceEvent(4, "r", 6, []), DanceEvent(4, "swipe", 2, ['low']), DanceEvent(4, "jump", 1, ['spot'])]
#d1 = DancerContext()
#d1.children.extend(stream1)
#d2 = DancerContext()
#d2.children.extend(stream2)
#s = ScoreContext()
#s.children.extend([d1, d2])
#g = GlobalContext() 
#g.children.append(s)
#g.prepareAsParsedData()
##print(str(g.it))
#g.runProcessChain()
#print(str(g.properties))

## Event-driven building ##
#events = [
#CreateContext(0, 2, "Score"),
#CreateContext(2, 3, "Dancer"),
#CreateContext(2, 4, "Dancer")
#]

#dEvents = [
#DeleteContext(0, 2),
#DeleteContext(2, 3),
#DeleteContext(2, 4),
#]

#g = GlobalContext() 
#for e in events:
  #g.dispatcher.say(e)
#print(str(g))

#for e in dEvents:
  #g.dispatcher.say(e)
#print(str(g))
