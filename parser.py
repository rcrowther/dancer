#!/usr/bin/python3


import os.path
import os
import re
import argparse
import sys
import subprocess

import StringIterator

def printMessage(msg):
    print(msg)

def printInfo(msg):
    print('[info] {0}'.format(msg))

def printError(msg):
    print('[error] {0}'.format(msg))    

CURLEY_LEFT = 123
CURLY_RIGHT = 125
BACKSLASH = 92
ASSIGN = 61
RIGHT_ANGLE = 60
LEFT_ANGLE = 62


class Parser:
    '''
    '''
    def __init__(self, it):
        self.it = it
        self.prevLineNo = 1
        self.prevOffset = 1
        self.tok = 0
        # ...prime
        self._next()
        # let's go
        self.root()

    def error(self, msg):
        print("[{0}, {1}] {2}".format(self.prevLineNo, self.prevOffset, msg))

    def expectedError(self, msg):
        self.error("Expected {0} but found '{1}'".format(msg, chr(self.tok)))

    def _next(self):
        self.prevLineNo = self.it.lineCount
        self.prevOffset = self.it.lineOffset
        self.tok = self.it.__next__()

    def skipWhitespace(self):
        while(self.tok <= 32):
            self._next()
        return False

    def block(self):
        commit = (self.tok == CURLEY_LEFT)
        if(commit):
           self._next()
           # sequence contents, instructions, angle brackets...
        return commit

    def isAlphaChar(self):
        return ((self.tok >= 65 and self.tok <= 90) or (self.tok >= 97 and self.tok <= 122))

    def identifier(self):
        commit = self.isAlphaChar()
        if(commit):
           while(self.isAlphaChar()):
               self._next()
               # gather and do something
        return commit

    def instruction(self):
        commit = (self.tok == BACKSLASH)
        if(commit):
           self._next()
           if(not self.identifier()):
             self.expectedError('identifier')
        return commit

    def rootSeq(self):
        while(
        self.skipWhitespace()
        or self.instruction()
        #or variable()
        or self.block()
        ):
          pass

    def root(self):
        try:
            self.rootSeq()
            #self.seqContents(self.treeRoot.body)
            # if we don't except on StopIteration...
            self.error('Parsing did not complete')
        except StopIteration:
            # All ok
            pass




def parse(srcAsLines):
    #print(srcAsLines)
    it = StringIterator.StringIterator(srcAsLines)
    #for c in it:
    #  print(c)
    Parser(it)



def main(argv):
    parser = argparse.ArgumentParser(
        #epilog= "NB: keynames in the internal 'stanza' variable must be adjusted to match input files"
        )


    parser.add_argument("-c", "--codec",
        default='UTF-8',
        help="encoding of source file."
        )
        
    parser.add_argument("-p", "--pair", 
        default=None,
        help="a pair to use for translation. Will assume Apertium is installed on the system"
        )
        
    parser.add_argument("-o", "--outfile", 
        default='',
        help="file path for output"
        )
        
    parser.add_argument("infile", 
        default='in.dn',
        help="file for input"
        )
                
    args = parser.parse_args()

    # assert infile as absolute path
    args.infile = os.path.abspath(args.infile)

    f = args.infile
    if (not os.path.exists(f)):
        printError('Path not exists path: {0}'.format(f))
        return 1
        
    if (os.path.isdir(f)):
        printError('Path is dir path: {0}'.format(f))
        return 1

    # set output directory to inFile directory            
    (args.workingDir, name) = os.path.split(args.infile)
    
    # baseName is everything to the dot separator for extension, if it exists
    idx = name.find('.')
    args.baseName = name if(idx == -1) else name[0:idx]
 


    # if no outfile, invent one
    if (not args.outfile):
        args.outfile = os.path.join(args.workingDir, '{0}.dnc'.format(args.baseName))

    print ('infile:' + str(args.infile))
    print ('workingDir:' + str(args.workingDir))
    print ('baseName:' + str(args.baseName))
    print ('codec:' + str(args.codec))
    print ('outfile:' + str(args.outfile))
    print ('\n')
    
    
    
    #try:


    # do something
    with open(args.infile, 'r', encoding=args.codec) as f:
        srcAsLines = "\n".join(f.readlines())


    parse(srcAsLines)

    printInfo("written final 'dnc' file: path: {0}".format(args.outfile))

    #with open(args.outfile, 'w', encoding=args.codec) as f:
        #f.write(parser.result())

    #except Exception as e:
     #   print('Error: most errors are caused by wrong format for source. Other errors from malformed files?\n{0}'.format(e))
        
        
if __name__ == "__main__":
        main(sys.argv[1:])
