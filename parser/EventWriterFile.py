import events

import os.path
import os



def before(ctx):
  fp = ctx.readPropOption('outfile')
  assert(fp != None)
  h = open(fp, 'w') # encoding=properties['outfileEncoding']) 
  ctx.mergeProp('fileHandle', h) 
  
def process(ctx, e):
  ctx.readProp('fileHandle').write(str(e))
  ctx.readProp('fileHandle').write('\n')
  
def after(ctx):
  ctx.readProp('fileHandle').close()
  ctx.deleteProp('fileHandle')
