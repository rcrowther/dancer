#!/usr/bin/python3

from parser import Parser

#?! isthere a Python builder for Python ? :)
class PythonParser(Parser):
    def __init__(self, it, reporter):
      self.b = []
      Parser.__init__(self, it, reporter)

    def result(self):
      return self.b
      
    def commentCB(self, text):
        print('comment...')
        print('"' + text + '"')

    def namedParameterCB(self, name, value):
      #print('namedParameter...')
      self.b.append(name)
      self.b.append(':')
      self.b.append(value)
      self.b.append(',\n')
            
    def functionNameCB(self, name):
      print('function name...')
      print(name)

    def instructionCB(self, cmd, params):
      print('ins...')
      print(cmd)
      
    def simultaneousInstructionsOpenCB(self):
      print('  simultaneousInstructions open...')
      pass      

    def simultaneousInstructionsCloseCB(self):
      print('  simultaneousInstructions close...')
      pass  
            
    def functionBodyOpenCB(self):
      print('  functionBody open...')
      pass      

    def functionBodyCloseCB(self):
      print('  functionBody close...')
      pass        
      
