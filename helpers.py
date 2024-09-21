'''
Created on Dec. 25, 2020

@author: Jacob H.

functions I find myself using across multiple source files

helpers.py
'''

def hms_to_s (hms):
    if hms is None or len(hms) == 0:
        return None
    negative = hms[0] == '-'
    if negative:
        hms = hms[1:]
    
    hms = hms.split(':')
    
    secs = 0
    for exp, n in enumerate(reversed(hms)): # s --> m --> h
        n = float(n) if '.' in n else int(n)
        secs += n * 60**exp
    
    if negative:
        secs *= -1
    
    return secs

def s_to_hms (s : 'float or int', precision):        
    negative = True if s < 0 else False
    s = abs(s)
    
    h = int(s//3600)
    s -= 3600*h
    m = int(s//60)
    s -= 60*m

    # formatted strings round up, but it shouldn't matter because stopwatch already does the 
    #    correct rounding/flooring, so there should never be an instance where there's too much
    #    precision
    s = ('0' if (h or m) and s < 10 else '') + ('%.' + str(precision) + 'f')%s
    
    m = ('0' if h and m < 10 else '') + (str(m) + ':' if m or h else '')
    h = str(h) + ':' if h else ''
        
    return ("-" if negative else "") + h + m + s
