#!/usr/bin/python

hint = "?????$$$$$$????????$$$$$$$$$$?????$$$$$$$$$$$$???$$$$$$$$$$$$$$??$$$$'$$$$$$$$$?$$$$'??????'$$$$$$$$'?'$'??$$$$$$$$$'''''??$$$$$$$$$$$$''??$$$$$$$$$$$$$'?<$$$$$$$$$$$$$'?<$$$$$?$$$'''$'?<$$$$??$$$$$'''$$'$$$???$$$$$$$$$$$$?????$$$$$$$$$$????????$$$$$$?????"



def calcColors(c, key):
    x = c ^ key
    fg = x & 7
    bg = (x >> 3) & 7
    return fg, bg

def findNextChar(fg, bg, c):
    for key in range(63, 0, -1):
        nfg, nbg = calcColors(c, key)
        if nfg != fg and nbg != bg:
            print fg,nfg, "-", bg, nbg
            return key
    print "No new character found!"
    return "?"
        

payload = ""

xfg = 9
xbg = 9

for i in xrange(0, 256):
  c = ord(hint[i])
  key = findNextChar(xfg, xbg, c)
  payload += chr(key)
  if (i+1) % 16 == 0:
    xfg = 7
    xbg = 0
  else:
    xfg, xbg = calcColors(c, key)

print repr(payload)