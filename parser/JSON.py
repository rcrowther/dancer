#!/usr/bin/python3

from parser import Parser

#?! isthere a Python builder for JSON
class JSONParser(Parser):
    def __init__(self, it, reporter):
      self.b = ['\n{']
      self.comments = False
      Parser.__init__(self, it, reporter)

    def result(self):
      self.b.append('\n}')
      return self.b
      
    def commentCB(self, text):
      #print('comment...')
      #print('"' + text + '"')
      if (self.comments):
        # Javascript has no multiline comments
        s = text.split('\n')
        for l in s:
          self.b.append('\n// ')
          self.b.append(l)
        pass
       
    def namedParameterCB(self, name, value):
      #print('namedParameter...')
      self.b.append('\n')
      self.b.append(name)
      self.b.append(': ')
      self.b.append(value)
      self.b.append(',')
            
    def functionNameCB(self, name):
      #print('function name...')
      #print(name)
      if (name == 'about'):
        self.b.append('\nabout: {')
      pass

    def instructionCB(self, cmd, params):
      #print('ins...')
      #print(cmd)
      self.b.append("\n[['")
      self.b.append(str(cmd))
      for p in params:
        self.b.append("', '")
        self.b.append(str(p))
      self.b.append("']],")
      pass
      
    def simultaneousInstructionsOpenCB(self):
      #print('  simultaneousInstructions open...')
      pass      

    def simultaneousInstructionsCloseCB(self):
      #print('  simultaneousInstructions close...')
      pass  
            
    def functionBodyOpenCB(self):
      #print('  functionBody open...')
      pass      

    def functionBodyCloseCB(self):
      #print('  functionBody close...')
      pass        
      
    def variableNameCB(self, name):
      #print('variable name...')
      #print(name)  
      pass
