#!/usr/bin/python3


# A hearer looks like this...

#def before(self, ctx):
  #ctx.dispatcher.startSayingTo(process, 'MomentStart')

  
#def hear(self, ctx, event):
  #print('  hearer heard event: ' + str(event))
    
#def hear(self, event):
#    print('  hearer heard event: ' + str(event))
      
#? Seems to me better if event dispatching bubbles down, lower 
#? context ids firing first. Needs prioritising. 
#? But they do, due to the order of build? ensure?
#? printers
class Dispatcher():
  '''
  Simple dispatcher for events.
  Dispatchers can say ('send') to other dispatchers. So events will
  bubble through.  
  Dispatchers can say ('send') to functions. These hearers ('listeners')
  are a function taking an event. On a module,
  
  hear(event):
    ...
    ...
    
  The contextId of the the event and dispatcher is definitive. If they 
  do not match, the event is bubbled to child dispatchers. If the 
  contextIds match, then the event is instead tried on 'hearer' functions
  '''
  #! what are these classes to Lillypond?
  #? We need to distribute to contexts...
  def __init__(self, context):
    self.listeners = {}
    self.childDispatchers = []
    self.context = context
    self.contextId = context.uid
    
  def say(self, event):
    # Say to children first
    # unless the event is for this id
    #? unfortunately, this will bubble event down branches terminated
    #? by irrelevant contexts?
    
    # only for debug logging, otherwise information overload.
    #print('dispatcher{0}: recieved : forwarding:{1} : event: {2}'.format(self.contextId, event.contextId != self.contextId, event))

    if (event.contextId != self.contextId):
      for e in self.childDispatchers:
        e.say(event)
        
    # say to any listeners on this id
    # for now, filter for contextId e.g. a dancer need not
    # know about Tempochange (or is that ok throufh properties?)
    else: 
      eventClass = type(event).__name__
      if(not eventClass in self.listeners):
        print('Dispatcher: not hearing: klass:{0} : event: {1}'.format(eventClass, event))
      else:
        print('<Dispatched {0}>'.format(eventClass) )
        for listener in self.listeners[eventClass]:
          listener(self.context, event)
  
  ## child dispatcher registration
  def startSayingToDispatcher(self, dispatcher):
    self.childDispatchers.append(dispatcher)
    
  def stopSayingToDispatcher(self, contextId):
      for idx, e in enumerate(self.childDispatchers):
        if (e.contextId == contextId):    
          del( self.childDispatchers[idx] )
          broken = True
          break
      if (not broken):
        print('Dispatcher: dispatcher child, attempted delete failed: contextId:'.format(contextId))
            
  ## listener registration
  def startSayingTo(self, listener, eventClass):
    '''
    @klass event class
    '''
    ll = self.listeners.get(eventClass)
    if (not ll):
      self.listeners[eventClass] = [listener]
    else:
      self.listeners[eventClass].append(listener)
    #listener.dispatchers.append(self)
    
  def stopSayingTo(self, listener, eventClass):
    xc = self.listeners.get(eventClass)
    if (not xc):
      print('Dispatcher: delete hearer, event class not recognised: ' + eventClass)
    else:
      broken = False
      for idx, e in enumerate(xc):
        if (e == listener):    
          del( xc[idx] )
          broken = True
          break
      if (not broken):
        print('Dispatcher: attempted hearer delete failed: contextId:{0} : eventClass: {1}'.format(contextId, eventClass))

  def __str__(self):
    s = 'Dispatcher('
    s += 'contextId:'
    s += str(self.contextId)  
    s += ', hearerClassKeys('
    for k, v in self.listeners.items():
      s += ", "
      s += "'"
      s += k
      s += "'"
    s += '), childDispatchIds('
    for e in self.childDispatchers:
      s += ", "
      s += str(e.contextId)
    s += '))'
    return s

#x
#class DispatcherContext():
  #'''
  #Dispatch to contexts
  #Used in GlobalContext  
  #'''
  ##! what are these classes to Lillypond?
  ##? We need to distribute to contexts...
  #def __init__(self):
    #self.hearers = {}
    
  #def say(self, event):
    #targetContext = event.contextId
    #if(not targetContext in self.hearers):
      #print('ContextDispatcher: not listening: contextId:{0} : event: {1}'.format(targetContext, event))
    #else:
      #print('<ContextDispatched {0}>'.format(event) )
      #self.hearers[targetContext].say(event)

        
  #def startSayingTo(self, contextId, hearer):
    #'''
    #@klass event class
    #'''
    #ll = self.hearers.get(contextId)
    #if (not ll):
      #self.hearers[contextId] = hearer
    #hearer.dispatchers = self
    
  #def stopSayingTo(self, contextId):
    #lId = self.hearers.get(contextId)
    #if (not lId):
      #print('DispatcherContext: delete context id not recognised: ' + str(contextId))
    #else:   
      #del( self.hearers[contextId] )

  #def __str__(self):
    #s = 'DispatcherContext('
    #for k, v in self.hearers.items():
      #s += ", "
      #s += "'"
      #s += str(k)
      #s += "'"
    #s += ')'
    #return s

    
#from events import *

#def hear(event):
    #print('  hearer heard event: ' + str(event))

#e0 = MergeProperty(5, 'beatsPerBar', 8)
#e1 = MomentEnd()


#d0 = Dispatcher(0)
#d1 = Dispatcher(5)
#d0.startSayingToDispatcher(d1)
##l0 = Hearer()
#d0.startSayingTo('MomentEnd', hear)
#d1.startSayingTo('MergeProperty', hear)
#print(str(d1))
#d0.say(e0)
#d0.say(e1)
#d0.stopSayingTo('MomentEnd', hear)
#print(str(d0))

#d1 = Dispatcher()
#d2 = Dispatcher()
#l0 = Hearer()
#d2.startSayingTo('MergeProperty', l0)
#d = DispatcherContext()
#d.startSayingTo(4, d1)
#d.startSayingTo(5, d2)
#print(str(d))

#d.say(e0)
#d.say(e1)

#d.stopSayingTo(4)
#d.stopSayingTo(5)
#print(str(d))
