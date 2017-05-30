#!/usr/bin/python3

#from iterators import *


from events import *
from dispatchers import *

from EventIterators import EventIterator, EventIteratorFile
from iterators import ParsedEventIterator, ChildContextIterator2, ClutchToStreamIterator, ParseIterator, ParsedDanceeventIterator, ChildContextIterator, ParseCompileIterator

import gChains, chains
import sys

# Not for threads (you know it)
_uid = 1

def uid():
  global _uid
  _uid += 1
  return _uid
   
def resetUID():
  _uid = 1

class ContextType():
  '''
  Enumerate base context names.
  This is needed because we have an imaginary type behind the real 
  types, so cannot use the entityNames  (which are, for example,
  'ScoreNode' and 'ScoreContext', not 'Score').
  Do not write the enumeration, only full text. Enumeration values
  are not guaranteed stable.
  '''
  Global = 0
  Score = 1
  DancerGroup = 2
  Dancer = 3

  @classmethod
  def fromString(self, x):
    assert(isinstance(x, str))
    if (x == 'global'): return ContextType.Global
    elif (x == 'score'): return ContextType.Score
    elif (x == 'dancerGroup'): return ContextType.DancerGroup
    elif (x ==  'dancer'): return ContextType.Dancer 
    else:
      print('ContextType: stringified enumeration not recognised : value:' + x)
      sys.exit(1)
    
  @classmethod
  def toString(self, x):
    assert(isinstance(x, int))
    if (x == ContextType.Global): return 'global'
    elif (x == ContextType.Score): return 'score'
    elif (x == ContextType.DancerGroup): return 'dancerGroup'
    elif (x == ContextType.Dancer): return 'dancer'    
    else:
      print('ContextType: enumeration not recognised : value:' + str(x))
      sys.exit(1)
  
  
  
#! should be base for other contexts
class ContextBase(SimplePrint):
  '''
  A context with children and a few utilities.
  Used standalone in the parser, for gathering parsed instructions.
  For these purposes, the uid should be set to the current context uid.
  '''
  def __init__(self, uid):
    self.children = []  
    self.uid = uid
    self.contextType = None

    # properties could be on the Context object
    # but I don't want this too Python.
    '''
    These values are public and persiting and are written to streams
    '''
    self.properties = {}
    #entityName()
    
  def appendChild(self, v):
    '''
    This accessor allows us to reimplement if necessary.
    Notably, DummyContext, which has no tree-building needs,
    disables this method.
    '''
    self.children.append(v)    

    
  def extendString(self, b):
    b.append(str(self.uid))
    b.append(', ')
    b.append(str(self.properties))
    b.append(', [')
    first = True
    for e in self.children:
      if (first):
        first = False
      else:
        b.append(", ")
      e.addString(b)
    b.append(']')



class DummyContext(ContextBase):
  #'''
  #A near-empty version of context.
  #This is used to parse variables, where we have no need to collect 
  #data.
  #So appendChild is passed.
  #'''
  def __init__(self):
    ContextBase.__init__(self, -1)
  
  ##! all these actions should generate errors
  def appendChild(self, v):
    pass

    
#################################################
    
class ParseNodeContext(ContextBase):
  '''
  The base of contexts for parsing.
  Based in context base, the children of this class are used to build
  an AST from parsed data.
  Although the base is a context, these classes vary from the contexts 
  used in building objects in many ways,
  - They auto-generate their own ids, becuase the input language needs
  no definitions
  - No reporters are included, as the parse generates errors, not the 
  AST tree
  - They can generate their own build events from themselves 
  - They all carry self-initialized iterators, to iterate the material
  supplied by an input language parse (or a sub-context handling that 
  material)
  '''
  def __init__(self, uid):
    ContextBase.__init__(self, uid)
    self.it = None
    
  ## toEvent returns ##    
  def _toPropertyEvents(self, b):
    for k, v in self.properties.items():
      e = MergeProperty(self.uid, k, v)
      b.append(e)
    for child in self.children:
      # contexts are the first in a child list, so breaking is ok.
      # ...and spares us iterting every DanceMove child
      if (isinstance(child, ParseNodeContext)):
        child._toPropertyEvents(b)
      else:
        break
    return b
    

  #! merge with property events
  def _toCreateEvents(self, parentId, b):
    '''
    Top-down, for saner creation
    '''
    # ignore the top global, it will already exist to build the rest
    # of the tree. Not putting in the stream means sparing us nasty
    # detection when processing streams.
    if (self.uid != 0):
      e = CreateContext(parentId, self.uid, ContextType.toString(self.contextType))
      b.append(e)
    for child in self.children:
      # contexts are the first in a child list, so breaking is ok.
      # ...and spares us iterting every DanceMove child
      if (isinstance(child, ParseNodeContext)):
        child._toCreateEvents(self.uid, b)
      else:
        break
    return b
    

  def _toDeleteEvents(self, parentId, b):
    '''
    Bottom-up, for saner destruction
    '''
    for child in self.children:
      # contexts are the first in a child list, so breaking is ok.
      # ...and spares us iterating every DanceMove child
      if (isinstance(child, ParseNodeContext)):
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



class DancerNode(ParseNodeContext):
  def __init__(self):
    ParseNodeContext.__init__(self, uid())
    self.it = ParsedEventIterator(self)
    self.contextType = ContextType.Dancer

  def appendChild(self, v):
    #! no reporter
    assert(v != ContextBase)
    self.children.append(v)
    #print('DancerNode: Can not add context to dancernodes {0}'.format(v))
    
  def extendString(self, b):
    b.append(str(self.uid))
    b.append(', ')
    b.append(str(self.properties))
    b.append(', [<stream children count:')
    b.append(str(len(self.children)))
    b.append('>]')

   
    
class ScoreNode(ParseNodeContext):
  def __init__(self):
    ParseNodeContext.__init__(self, uid())
    self.it = ChildContextIterator2(self)
    self.contextType = ContextType.Score

  def appendChild(self, v):
    assert(isinstance(v, ParseNodeContext))
    self.children.append(v)
    
    
    
class GlobalNode(ParseNodeContext):
  def __init__(self):
    ParseNodeContext.__init__(self, 0)
    # auto reset the ids
    resetUID()
    self.it = ClutchToStreamIterator(self)     
    self.contextType = ContextType.Global

  def appendChild(self, v):
    assert(not len(self.children) > 1)
    #recurse
    #for c in self.children:
    #  c.prepareAsParsedData()
    self.children.append(v)

  def toCreateEvents(self):
    '''
    Should only be called on Global, or parents are undetermined?
    '''
    return self._toCreateEvents(0, [])

  def toPropertyEvents(self):
    return self._toPropertyEvents([])
        

  def toDeleteEvents(self):
    '''
    Should only be called on Global, or parents are undetermined?
    '''
    return self._toDeleteEvents(0, [])
    






#################################################
class ProcessorContext(ContextBase):
  '''
  The base of contexts for processing.
  Based in context base, the children of this class are used to process 
  event lists.
  Although the base is a context, these classes vary from the contexts 
  used for parsing the input language,
  - They need their ids setting explicitly, from the event lists.
  - Reporters are included, as the building generates errors.
  - They carry only one iterator, in the Global context, for supplying 
  the event list
  - They all carry self-initialized dispatchers. These dispatch the 
  events supplied by the iterator to parts of the structure being built.
  - They all carry lists of processors to handle recieved events.

  
  @name context name as lowercase string
  '''
  def __init__(self, uid, reporter):
    ContextBase.__init__(self, uid)
    self.reporter = reporter

    # internal. Used for temp properties, not persited 
    # by event streams
    self._props = {}

    
    '''
    Every context can process it's input stream.
    The stack of processors is built here.
    '''
    self.processors = []
    
        
    # Used to dispatch events to builder classes
    self.dispatcher = None

    '''
    Processing chain data is held here.
    When a context for processing is built, it refers
    here to find the chains it must load and initialize.
    '''
    self._chainData = {}
        
    # hanger for lists of graphic objects
    self.gList = []

    
    
  ## Dispatch methods ##
  # @ctx is 'self', to satisfy dispatch callback 
  def createChildContext(self, ctx, event):
    assert(isinstance(event, CreateContext))
    print('... ' + str(event))
    
    #Make the new context
    newCtx = None
    tpe = ContextType.fromString(event.newType)
    #print(str(tpe))
    assert(tpe != ContextType.Global)
    if (tpe == ContextType.Score):
      newCtx = ScoreContext2(event.newId, self.reporter)
    if (tpe == ContextType.Dancer):
      newCtx = DancerContext2(event.newId, self.reporter)
    #if (tpe == ContextType.DancerGroup'):
      #newCtx = DancerGroupContext2(event.newId, self.reporter)
    assert(newCtx != None)
    
    #parent the new context
    self.appendChild(newCtx)
    # print('Child appended contextType: {0}: id:{1}'.format(oldId))

    # set up the dispatcher
    newCtx.dispatcher = Dispatcher(newCtx)
    self.dispatcher.startSayingToDispatcher(newCtx.dispatcher)
    # new context can hear context creation and deletion
    newCtx.dispatcher.startSayingTo(newCtx.createChildContext, 'CreateContext')
    newCtx.dispatcher.startSayingTo(newCtx.deleteChildContext, 'DeleteContext')
    
    # set up the chain (may depend on the dispatcher existing)
    newCtx._chainData = self._chainData
    newCtx.processors = self._chainData[ContextType.toString(newCtx.contextType)]
    # initialize
    for p in newCtx.processors: 
      p.before(newCtx)
      


  # @ctx stub parameter to satisfy dispatch callback 
  def deleteChildContext(self, ctx, event):
    assert(isinstance(event, DeleteContext))
    #if (self.containsProp('displayDance')):
   # print('context glist:\n' + self.gListToString())

      
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
    #? need to
    # finalize the chain (dont speak to old context)
    # self._finaliseChain(self)
    print('... ' + str(event))


  ### Glist printing ###
  def addGListChildren(self, b):
    first = True
    for e in self.children:
      if (first):
        first = False
      else:
        b.append(", ")
      e.addGListString(b)
    
  def addGListString(self, b):
    b.append(self.entitySuffix)   
    b.append(str(self.uid))    
 
    b.append('(')
    first = True
    for e in self.gList:
      if (first):
        first = False
      else:
        b.append("-")
      b.append(str(e))      
    #self.addGListChildren(b)
    #b.append(str(self.children))
    b.append(')')
    return b
        
  #? This is a tricky print, as the lists may be very long.
  #? Undecided about the best way to go, but needed, for sure.
  def gListToString(self):
    return "".join(self.addGListString([]))  

  
  
class DancerContext2(ProcessorContext):  
  def __init__(self, uid, reporter):
    ProcessorContext.__init__(self, uid, reporter)
    self.contextType = ContextType.Dancer


class DancerGroupContext2(ProcessorContext):  
  def __init__(self, uid, reporter):
    ProcessorContext.__init__(self, uid, reporter)
    self.contextType = ContextType.DancerGroup


class ScoreContext2(ProcessorContext):  
  def __init__(self, uid, reporter):
    ProcessorContext.__init__(self, uid, reporter)
    self.contextType = ContextType.Score

          
class GlobalContext2(ProcessorContext):  
  def __init__(self, reporter):
    ProcessorContext.__init__(self, 0, reporter)
    self.contextType = ContextType.Global

    # The iterator delivering streamed events
    # May be from a parse or a compiled file
    self.eventIterator = None
    
    ## When an event list runs in a global context, it creates
    # and destroys the subtree as necessary.
    # That means we must prime any tree and it's list activity
    # beforehand, as we have no input into the process once active.
    #  The below, and associated methods, allow us to do that. 

    # Set this on ititialization
    self.dispatcher = Dispatcher(self)
    self.dispatcher.startSayingTo(self.createChildContext, 'CreateContext')
    self.dispatcher.startSayingTo(self.deleteChildContext, 'DeleteContext')
    
      
  def setChainData(self, chainData):      
    '''
    @data map of contextname->list(processors)
    '''
    assert(isinstance(chainData, dict))
    assert(chainData.get(ContextType.toString(ContextType.Dancer)) != None)
    assert(chainData.get(ContextType.toString(ContextType.DancerGroup)) != None)
    assert(chainData.get(ContextType.toString(ContextType.Score)) != None)
    assert(chainData.get(ContextType.toString(ContextType.Global)) != None)
    # Need to set this data in global immediately
    # data is then autopassed and generated by createChildContext()     
    self._chainData = chainData
    chain = chainData[ContextType.toString(ContextType.Global)]
    assert(isinstance(chain, list))
    self.processors = chain
    # initialize
    for p in self.processors: 
      p.before(self)
            
          
  def unsetChainData(self):  
    # after
    for p in self.processors: 
      p.after(self) 
    self.processors = []
    self._chainData = []

    

            
  ## chain processing actions ##

  def runIteratorToGlobalChain(self, chainData):
    '''
    Run the event iterator directly over the global processing chain.
    Bypasses dispatching, all events go to the global chain.
    '''
    assert(self.eventIterator != None)
    self.setChainData(chainData)
    while(self.eventIterator.hasNext()):
      e = self.eventIterator.next()
      for p in self.processors:
         p.process(self, e)
    self.unsetChainData()


  ## dispatch building ###
  def runIteratorToContextDispatcher(self, chainData):
    '''
    Run the event iterator to the dispatch tree.
    Will auto-build a model. Events are dispatched to the
    marked context.
    '''
    assert(self.eventIterator != None)
    self.setChainData(chainData)
    while(self.eventIterator.hasNext()):
      e = self.eventIterator.next()
      #print(str(e))
      self.dispatcher.say(e)
    # currently no finalize?


########################################################          
#class Context(BuildingContext):
#    reporter
    
#! need error reporting
#! contexts need to be able to toEvents their own
#! build creation events. For use from parsing.
#! name is ContextSubclass? 
#class Context():
  #'''
  #Every context knows the iterator it will use if it needs one. 
  #Iterators are used at their most complex to walk a parse and
  #interleave it. One iterator calls another down the Context tree.
  
  #The StreamContext takes a pre-compiled, interleaved stream and has
  #its own iterator. Due to the compilation, this is a simple
  #configuration.
  
  #@name context name as lowercase string
  #'''
  #def __init__(self, uid, name, reporter):
    #self.entitySuffix = type(self).__name__

    #self._name = name
    ## doubles up meanings, either subcontexts or a list of music
    ## events. Both children, both iterable, though. 
    #self.children = []
    #self.uid = uid
    #self.reporter = reporter
    
    #'''
    #Every context can process it's input stream.
    #The stack of processors is built here.
    #'''
    #self.processors  = []
    
    ## The iterator can be
    ## building from source AST
    ## - child MoveEvents
    ## - child context iterators
    ## or from an event stream
    #self.it = None
    
    ## Used to dispatch events to builder classes
    #self.dispatcher = None
    
    ## hanger for lists of graphic objects
    #self.gList = []
    
    ## properties could be on the Context object
    ## but I don't want this too Python
    ## general. This one general and written to streams
    #self.properties = {}
    
    ## internal. Used for temp properties, not persited 
    ## by event streams
    #self._props = {}
    

    
  #@property
  #def name(self):
    #return self._name
    
  #@name.setter
  #def name(self, name):
    #self._name = name
    
  ## Following are useful for external controls i.e. dancerc
  ##? make general API, even for chainLinks?
  #def mergeProperty(self, k, v):
    #self.properties[k] = v

  #def containsProperty(self, k):
    #return (self.properties.get(k) != None)

  #def readProperty(self, k):
    #return self.properties[k]

  #def readPropertyOption(self, k):
    #return self.properties.get(k)
    
  #def deleteProperty(self, k):
    #del self.properties[k]

  ### props ##
  #def mergeProp(self, k, v):
    #self._props[k] = v

  #def containsProp(self, k):
    #return (self._props.get(k) != None)

  #def readProp(self, k):
    #return self._props[k]

  #def readPropOption(self, k):
    #return self._props.get(k)
    
  #def deleteProp(self, k):
    #del self._props[k]
        
        
  #def appendChild(self, v):
    #'''
    #This accessor allows us to reimplement if necessary.
    #Notably, DummyContext, which has no tree-building needs,
    #disables this method.
    #'''
    #self.children.append(v)
  
  #def isLeaf(self):
    #return (len(self.children) == 0)


  ### parse data actions ##
  #def prepareAsParsedData(self):
    #pass


  ### chain processing actions ##

          
  #def _initializeChain(self):
    #for p in self.processors:
      #p.before(self)
     
  ##? needed? useful? 
  #def _finalizeChain(self):
    #for p in self.processors:
      #p.after(self)
      
      
  ### Dispatch methods ##
  ## @ctx stub parameter to satisfy dispatch callback 
  #def createChildContext(self, ctx, event):
    #assert(isinstance(event, CreateContext))
    #assert(event.newType != 'Global')
    #print('create context...')
    #ctx = None
    #tpe = event.newType
    #if (tpe == 'Score'):
      #ctx = ScoreContext(self.reporter)
    #if (tpe == 'Dancer'):
      #ctx = DancerContext(self.reporter)
    ##if (tpe == 'DancerGroup'):
      ##ctx = DancerGroup()
    #ctx.uid = event.newId
    #self.appendChild(ctx)
    ## print('Child appended contextType: {0}: id:{1}'.format(oldId))

    ## initialise the chain (speakTo hearers)
    #ctx.chainData = self.chainData
    #ctx.processors = ctx.chainData[self.name]
    ## initialize
    #for p in ctx.processors:
      #p.before(ctx)
          
    ## set up the dispatcher
    #ctx.dispatcher = Dispatcher(ctx)
    #self.dispatcher.startSayingToDispatcher(ctx.dispatcher)
    ## new context can hear context creation
    #ctx.dispatcher.startSayingTo(ctx.createChildContext, 'CreateContext')
    #ctx.dispatcher.startSayingTo(ctx.deleteChildContext, 'DeleteContext')
    



  ## @ctx stub parameter to satisfy dispatch callback 
  #def deleteChildContext(self, ctx, event):
    #assert(isinstance(event, DeleteContext))
    ##if (self.containsProp('displayDance')):
    #print('context glist:\n' + self.gListToString())

      
    #oldId = event.oldId
    #broken = False
    #for idx, e in enumerate(self.children):
      #if (e.uid == oldId):
        #del (self.children[idx])
        #broken = True
        #break
    ##! should be warning report
    #if(not broken):
      #print('Child to delete not found parentName: {0} : parentId: {1} : id to remove: {2}'.format(self.name, self.uid, oldId))
    #else:
      ## we found and deleted a context.
      ## remove deleted context from this dispatcher
      #self.dispatcher.stopSayingToDispatcher(oldId)
    ##? need to
    ## finalize the chain (dont speak to old context)
    ## self._finaliseChain(self)


  ### toEvent returns ##    
  #def _toPropertyEvents(self, b):
    #for k, v in self.properties.items():
      #e = MergeProperty(self.uid, k, v)
      #b.append(e)
    #for child in self.children:
      ## contexts are the first in a child list, so breaking is ok.
      ## ...and spares us iterting every DanceMove child
      #if (isinstance(child, Context)):
        #child._toPropertyEvents(b)
      #else:
        #break
    #return b
    
  #def toPropertyEvents(self):
    #return self._toPropertyEvents([])
    
  ##! merge with property events
  #def _toCreateEvents(self, parentId, b):
    #'''
    #Top-down, for saner creation
    #'''
    ## ignore the top global, it will already exist to build the rest
    ## of the tree. Not putting in the stream means sparing us nasty
    ## detection when processing streams.
    #if (self.uid != 0):
      #e = CreateContext(parentId, self.uid, self.name)
      #b.append(e)
    #for child in self.children:
      ## contexts are the first in a child list, so breaking is ok.
      ## ...and spares us iterting every DanceMove child
      #if (isinstance(child, Context)):
        #child._toCreateEvents(self.uid, b)
      #else:
        #break
    #return b
    
  #def toCreateEvents(self):
    #'''
    #Should only be called on Global, or parents are undetermined?
    #'''
    #return self._toCreateEvents(0, [])

  #def _toDeleteEvents(self, parentId, b):
    #'''
    #Bottom-up, for saner destruction
    #'''
    #for child in self.children:
      ## contexts are the first in a child list, so breaking is ok.
      ## ...and spares us iterting every DanceMove child
      #if (isinstance(child, Context)):
        #child._toDeleteEvents(self.uid, b)
      #else:
        #break
        
    ## ignore the top GlobalContext, it can not delete itself 
    ## (not in Python).
    ## Not putting in the stream means sparing us nasty
    ## detection when processing streams.
    #if (self.uid != 0):
      #e = DeleteContext(parentId, self.uid)
      #b.append(e)
    #return b
    
  ##! move to global?
  #def toDeleteEvents(self):
    #'''
    #Should only be called on Global, or parents are undetermined?
    #'''
    #return self._toDeleteEvents(0, [])
    
  #def extendString(self, b):
    #b.append(str(self.uid))
    #b.append(', ')
    #b.append(str(self.properties))


  ### Printers ##
  

  #### Context printer ###
  #def addChildren(self, b):
    #b.append(', [')
    #first = True
    #for e in self.children:
      #if (first):
        #first = False
      #else:
        #b.append(", ")
      #e.addString(b)
    #b.append(']')
    
  #def addString(self, b):
    #b.append(self.entitySuffix)
    #b.append('(')
    #self.extendString(b)
    #self.addChildren(b)
    ##b.append(str(self.children))
    #b.append(')')
    #return b
    
  #def __str__(self):
    #return "".join(self.addString([]))  
    



#class DummyContext(Context):
  #'''
  #A near-empty version of context.
  #This is used to parse variables, where we have no need to collect 
  #data.
  #So appendChild is passed.
  #'''
  #def __init__(self, reporter):
    #Context.__init__(self, -1, 'Dummy', reporter)
  
  ##! all these actions should generate errors
  #def appendChild(self, v):
    #pass
    
  #def createChildContext(self, event):
    #pass
    
  #def deleteChildContext(self, event):
    #pass
    
  #def prepareAsParsedData(self):
    #pass

  ### Dispatchers ##
   
    

 
 
    
##? A Dancer can not create a child context
##? but has a dispatcher?
#class DancerContext(Context):
  #def __init__(self, reporter):
    #Context.__init__(self, uid(), 'Dancer', reporter)
    #self.processors = gChains.Dancer


  #def prepareAsParsedData(self):
    #self.it = ParsedDanceeventIterator()
    #self.it.prepare(self.uid, self.children)

  ### chain processing actions ##


    
  ### dispatch building ###


  #def createChildContext(self, event):
    #print("DancerContext" + "error, no child context")


 
 
    
##class DancerGroupContext(Context):
##  def __init__(self):
##    Context.__init__(self, uid(), 'DancerGroup')
 
 
 
      
#class ScoreContext(Context):
  #def __init__(self, reporter):
    #Context.__init__(self, uid(), 'Score', reporter)
    #self.processors = gChains.Score


  #def prepareAsParsedData(self):
    ##recurse
    #for c in self.children:
      #c.prepareAsParsedData()
    #self.it = ChildContextIterator()
    #self.it.prepare(self.uid, [ctx.it for ctx in self.children])

    
    
  #def _delete(self, lst, uid):
    #i = 0
    #l = len(lst)
    #while(i < l):
      #if (lst[i].contextUID == uid):
        #lst.pop(i)
        #break
      #else:
        #i += 1
        
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

      



    
#class GlobalContext(Context):
  #def __init__(self, reporter):
    #Context.__init__(self, 0, 'Global', reporter)
    
    ##! is what?
    #self.outStream = []
    
    ##! A lot not right
    ##! how to output results from a process phase? In the phase?
    ##! howto initially load phases?
    ##!
    ## Currently hard-set by
    ## - runIteratorToContextDispatcher
    ## - runIteratorToGlobalChain
    ## Underlying context chains are pre-set to graphic process chains.
    ## These are never used unless the iterator is fed to the dispatcher,
    ## runIteratorToDispacher()
    ##
    #self.processors = []


    ## Set this on ititialization
    #self.dispatcher = Dispatcher(self)
    #self.dispatcher.startSayingTo(self.createChildContext, 'CreateContext')
    #self.dispatcher.startSayingTo(self.deleteChildContext, 'DeleteContext')
    
    #'''
    #Processing chain data is held here.
    #When a context for processing is built, it referrs to
    #here to find the chains it must load and initialize.
    #'''
    #self.chainData = []

  ### Alt chains ##
  
  #def setStatisticsChain(self):
    #self.processors = chains.GlobalStatistics

  #def setGraphicsChain(self):
    #self.processors = gChains.Global

  ### parse data actions ##
  #def prepareAsParsedData(self, srcName):
    ## sets up parse data iterators
    ## must be called when data in place
    #assert(len(self.children) == 1)
    ##recurse
    #for c in self.children:
      #c.prepareAsParsedData()
    #self.it = ParseCompileIterator(srcName)
    #de = self.toDeleteEvents()
    #de.append(Finish())
    #ctxEvents = self.toCreateEvents()
    #ctxEvents.extend(self.toPropertyEvents())
    #self.it.prepare(0, [ctxEvents, de, self.children[0].it])



  ### event stream actions ##
    ##self.createChildContext(event)
  #def prepareForEventSteamData(self, eventIterator):
    ## sets up stream data iterator
    #assert( isinstance(eventIterator, EventIterator) )
    #assert( not(self.children) )
    #self.it = eventIterator

    
  ### chain processing actions ##
  #def setChains(self, chainData):
    #'''
    #@data map of contextname->list(processors)
    #'''
    #print('set chains...' + str(self.uid))
    #self.chainData = chainData
    ## load (self) global context data
    #self.processors = self.chainData['Global']
    ## initialize
    #for p in self.processors: 
      #p.before(self)
      
  ##! runIteratorToGlobalChain
  #def runIteratorToGlobalChain(self, chain):
    #self.processors = chain
    #self._initializeChain()
    #while(self.it.hasNext()):
      #e = self.it.next()
      #for p in self.processors:
         #p.process(self, e)
    #self._finalizeChain()

  ### dispatch building ###
  #def runIteratorToContextDispatcher(self):
    #self._initializeChain()
    #while(self.it.hasNext()):
      #e = self.it.next()
      ##print(str(e))
      #self.dispatcher.say(e)
    ## currently no finalize?






## Tests ##
from events import *
#from iterators import *


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






###############################################################
## ContextNodes ##

#from ConsoleStreamReporter import ConsoleStreamReporter
#r = ConsoleStreamReporter()

#n1 = DancerNode()
#n1.children.extend(stream1)
##print(str(n1))
##print(str(n1.it))

#n2 = DancerNode()
#n2.children.extend(stream2)
##print(str(n2))
##print(str(n2.it))

#sn = ScoreNode()
##sn.children.append(n1)
##sn.children.append(n2)
#sn.children.extend([n1, n2])

##print(str(ns))
##print(str(sn.it))

#gn = GlobalNode()
#gn.children.append(sn)

##print(str(gn.it))


## Event printing ##
#xe = gn.toCreateEvents()
#for e in xe:
  #print(e)

#xe = gn.toPropertyEvents()
#for e in xe:
  #print(e)

#eEvents = [Finish()]
#eEvents.extend(gn.toDeleteEvents())
#pi = ParseIterator(gn, gn.toCreateEvents(), eEvents)
##pi = ParseIterator(gn, [MomentEnd()], [Finish()])
#print(str(pi))

######################################################################
## Build contexts ##
#from ConsoleStreamReporter import ConsoleStreamReporter

stream1 = [MoveEvent(6, "clap", 1, []), MoveEvent(6, "clap", 1, ['overhead']), MoveEvent(6, "step", 1, ['west']), SimultaneousEventsEvent( [MoveEvent(6, "cross", 1, ['legs']), MoveEvent(6, "cross", 1, ['hands'])]), SimultaneousEventsEvent([MoveEvent(6, "jump", 1, ['south']), MoveEvent(6, "hands", 1, ['ears'])]), MoveEvent(6, "bend", 1, ['knees']), MoveEvent(6, "slap", 1, ['other']), MoveEvent(6, "slap", 2, ['knees']), MoveEvent(6, "twirl", 1, ['right']), MoveEvent(6, "split", 1, ['knees']), MoveEvent(6, "turn", 1, ['west']), MergeProperty(6, "beatsPerBar", "3"), MergeProperty(6, "tempo", "80"), MoveEvent(6, "kick", 1, ['low'])]
stream2 = [MoveEvent(4, "clap", 1, []), MoveEvent(4, "clap", 1, ['overhead']), MoveEvent(4, "step", 1, ['west']), SimultaneousEventsEvent( [MoveEvent(4, "cross", 1, ['legs']), MoveEvent(4, "cross", 1, ['hands'])]), SimultaneousEventsEvent([MoveEvent(4, "jump", 1, ['south']), MoveEvent(4, "hands", 1, ['ears'])]), MoveEvent(4, "r", 6, []), MoveEvent(4, "swipe", 2, ['low']), MoveEvent(4, "jump", 1, ['spot'])]


#r = ConsoleStreamReporter()
#gc = GlobalContext2(r)


## building from events ##

#cEvents = [
 #CreateContext(0, 2, "score"),
 #CreateContext(2, 3, "dancer"),
 #CreateContext(2, 4, "dancer")
#]

#dEvents = [
 #DeleteContext(2, 4),
 #DeleteContext(2, 3),
 #DeleteContext(0, 2)
#]

#for e in cEvents:
  #gc.dispatcher.say(e)

#for e in dEvents:
  #gc.dispatcher.say(e)


#gc.setChainData(chains.GlobalStatistics)
