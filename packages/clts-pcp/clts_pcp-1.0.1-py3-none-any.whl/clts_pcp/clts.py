import time

elapt={}

def listtimes():
    global context
    try:
        context # does a exist in the current namespace
    except NameError:
        context ='Please define `context` variable.'

    cols=[90, 19, 19]
    sepa="+"
    for c in cols:
      sepa=sepa+"-"*c+"+"
 
    print(sepa)
    topp= '|' + f" Task(s) by {context:<76s} " + ' | watch time (secs) |  proc time (secs) |'
    print(topp)
    print(sepa)

    toem=f"<table style=''font-family:montserrat;'' border=1 cellspacing=0><tr background=`whitesmoke` style=`font-weight:bold;`><td> Task(s) of {context}. <td align=center> watch time (secs) <td align=center>proc time (secs)"

    for k in elapt.keys():                                   # dict elapt contains a series of entries key -> elapsed time
        topp = f'| {k:88s} | {elapt[k]["tt"]:17.2f} | {elapt[k]["tp"]:17.2f} |'
        print (topp)
        toem=toem+f"<tr><td>{k}<td align=right>{elapt[k]['tt']:.2f}<td align=right>{elapt[k]['tp']:.2f}"

    print(sepa)
    toem +="</table>"
    return(toem)


def getts():
    return({'tt':time.time(), 'tp':time.process_time()})

def deltat(p):
    return({'tt':time.time()-p['tt'], 'tp':time.process_time()-p['tp']})

def setcontext(p):
    global context
    context=p
