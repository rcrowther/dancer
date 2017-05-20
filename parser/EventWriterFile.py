import events

import os.path
import os



def before(properties):
  assert(properties.get('outfile') != None)
  properties['fileHandle'] = open(properties['outfile'], 'w') # encoding=properties['outfileEncoding']) 
  
def process(properties, e):
  properties['fileHandle'].write(str(e))
  properties['fileHandle'].write('\n')
  
def after(properties):
  properties['fileHandle'].close()
  del (properties['fileHandle'])
