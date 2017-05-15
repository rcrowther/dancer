#!/usr/bin/python3

from parser import Parser
from trees.Trees import *


#?! isthere a Python builder for Python ? :)
class PythonBuilder(Parser):
    def __init__(self, it, reporter):
      self.b = []
      self.tree = Score()
      Parser.__init__(self, it, reporter)

    def result(self):
      return self.tree
      
    def commentCB(self, text):
      #print('comment...')
      #print('"' + text + '"')
      pass
      
    def _addComma(self):
      if (self.first):
        self.first = False
      else:
        self.b.append(", ")
                
    def functionCallOpenCB(self, name, posParams, namedParams):
      #print('function open...')
      #print(name + ':' + str(posParams) +str(namedParams))

      for kv in namedParams:
        self.b.append(kv[0])
        self.b.append(':')
        self.b.append(kv[1])
        self.b.append(',\n')


    def functionCallCloseCB(self, name):
      self.b.append('\n}')
      # Must be false, in wider scope we wrote something
      self.first = False
      pass 
            
    def functionBodyOpenCB(self):
      #print('  functionBody open...')
      pass      

    def functionBodyCloseCB(self):
      #print('  functionBody close...')
      pass        

    def simultaneousFunctionBodyOpenCB(self):
      #print('  simultaneousFunctionBody open...')
      self.b.append(',\n"simultaneousBody" : {')
      pass      

    def simultaneousFunctionBodyCloseCB(self):
      #print('  simultaneousFunctionBody close...')
      self.b.append('\n}')
      pass       
      

    def simultaneousInstructionsOpenCB(self):
      #print('  simultaneousInstructions open...')
      self._addComma()
      self.b.append("\n[")
      self.inSimutaneous = True
      # for contents
      self.first = True
      pass      

    def simultaneousInstructionsCloseCB(self):
      #print('  simultaneousInstructions close...')
      self.b.append("]")
      self.inSimutaneous = False
      # Must be false, in wider scope we wrote something
      self.first = False
      pass  
      
    def instructionCB(self, cmd, params):
      #print('ins...')
      #print(cmd)
      pass      
