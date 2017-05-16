#!/usr/bin/python3


class Context():
  #NB: put properties on the object
  def __init__(self, idx, name):
    self.name = name
    self.children = []
    # The itertor can be
    # building from source AST
    # - child stream
    # - other terators
    # bulding from a stream
    self.childIterator = None
    self.stream = []
    
    
  @property
  def name(self):
    return self._name
    
  @name.setter
  def name(self, name):
    self._name = name
    
  def createChild():
    c = Context()
    self.children.append(c)
    return c
    
  def isLeaf():
    return (len(self.children) == 0)
    
