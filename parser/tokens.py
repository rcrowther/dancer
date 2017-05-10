
'''
Enum for UTF-8/Latin1 codepoiints  
'''
LINE_FEED = 10
HASH = 35
PLUS = 43
HYPHEN_MINUS = 45
ICOMMAS = 34
ICOMMA = 39
PERIOD = 46
COMMA = 44
COLON = 58
SEMI_COLON = 59
SOLIDUS = 47
BACKSLASH = 92
ASSIGN = 61
UNDERSCORE = 95
LEFT_BRACKET = 40
RIGHT_BRACKET = 41
RIGHT_ANGLE = 62
LEFT_ANGLE = 60
LEFT_CURLY = 123
RIGHT_CURLY = 125
LEFT_SQR = 91
RIGHT_SQR = 93

#? unused, so far
tokens = {
# represents null, None, whatever
'null' : 0,


# types
'multilineComment': 21,
'comment' : 22,
'identifier' : 23,
'unmarkedText' : 24,
'intNum' : 25,
'floatNum' : 26,
'string' : 27,


# keywords


'init' : 51,
'about' : 52,
'score' : 53,
'let' : 54,

'staff' : 60,

'tempo' : 70,
'barCount' : 71,


'repeat' : 80,
'alternative' : 81,
'r' : 83,

# special tokens
'endBar' : 101,

}

tokenToString =  {}
for k, v in tokens.items():
    tokenToString[v] = k


def tokensToString(tokens, sep = ', '):
    b = []
    for t in tokens:
       b.append(tokenToString[t])
    return sep.join(b)

