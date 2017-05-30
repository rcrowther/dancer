import events

import os.path
import os



def before(ctx):
  fp = ctx._props.get('outfile')
  assert(fp != None)
  h = open(fp, 'w') # encoding=properties['outfileEncoding']) 
  ctx._props['fileHandle'] = h 
  
def process(ctx, e):
  ctx._props['fileHandle'].write(str(e))
  ctx._props['fileHandle'].write('\n')
  
def after(ctx):
  ctx._props['fileHandle'].close()
  del (ctx._props['fileHandle'])
