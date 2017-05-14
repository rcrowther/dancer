#!/usr/bin/python3

from parser import Parser

#?! isthere a Python builder for JSON
class JSONPrintGenerator(Parser):
    def __init__(self, it, reporter):
      self.b = ['\n{']
      self.comments = False
      self.inSimutaneous = False

      # keep track of list indexing, for commas 
      self.first = True
      Parser.__init__(self, it, reporter)

    def result(self):
      self.b.append('\n}')
      return self.b
      
      
    def commentCB(self, text):
      #No comments in JSON
      pass


    def _addComma(self):
        if (self.first):
          self.first = False
        else:
          self.b.append(", ")
                
    def functionCallOpenCB(self, name, posParams, namedParams):
      #print('function name...')
      #print(name + ':' + str(posParams) +str(namedParams))

      self._addComma()
      self.b.append('\n"')
      self.b.append(name)
      self.b.append('" : {')
            
      self.b.append('\n"posParams": [') 

      #positional parameters
      self.first = True      
      for p in posParams:
        self._addComma()
        self.b.append(p)
      self.b.append("]")

      # named params             
      
      for kv in namedParams:
        # always posParams, if empty
        # so always preceeding comma
        self.b.append(',\n"')
        self.b.append(kv[0])
        self.b.append('": ')
        v = kv[1]
        vo = v if(v) else 'null'
        self.b.append(vo)


    def functionCallCloseCB(self, name):
      self.b.append('\n}')
      # Must be false, in wider scope we wrote something
      self.first = False
      pass

    def functionBodyOpenCB(self):
      #print('  functionBody open...')
      # always posParams, if empty
      self.b.append(',\n"body" : [')
      # for contents
      self.first = True
      pass      

    def functionBodyCloseCB(self):
      #print('  functionBody close...')
      self.b.append('\n]')
      pass  

    def simultaneousFunctionBodyOpenCB(self):
      #print('  simultaneousFunctionBody open...')
      self.b.append(',\n"simultaneousBody" : {')
      pass      

    def simultaneousFunctionBodyCloseCB(self):
      #print('  simultaneousFunctionBody close...')
      self.b.append('\n}')
      pass       
      
      
    def _addInstruction(self, cmd, params):
        self.b.append('["')
        self.b.append(str(cmd))
        # its a move, not a system instruction
        self.b.append('", true')
        for p in params:
          self.b.append(', "')
          self.b.append(str(p))
        if (params):
                  self.b.append('"')
        self.b.append(']')
              
    def instructionCB(self, cmd, params):
      #print('ins...')
      #print(cmd + ' '.join(params))
      if (self.inSimutaneous):
        self._addComma()
        self._addInstruction(cmd, params)
      else:
        self._addComma()
        self.b.append("\n[")
        self._addInstruction(cmd, params)
        self.b.append("]")
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
