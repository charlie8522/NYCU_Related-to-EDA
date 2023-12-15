# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:32:06 2021

@author: USER
""" 
import time 
import argparse

def takeSecond(elem):
    return elem[1]

parser = argparse.ArgumentParser(description='Add some I/O Command')
parser.add_argument("infile", type=str)
parser.add_argument("outfile",type=str)
args = parser.parse_args()
inputfile = args.infile
outputfile = args.outfile
  
start = time.time()
nl,wl,hl,llx,lly,urx,ury = ([]for i in range(7))
llxx,llyy,urxx,uryy = ([]for i in range(4))
f = open(inputfile,'r')
nf = open(outputfile,'w')
lines = f.readlines()
block = []
for line in lines:
    n,w,h = line.split()
    nl.append(n)
    wl.append(int(w))
    hl.append(int(h))
    llx.append(0)
    lly.append(0)
    urx.append(0)
    ury.append(0)
    llxx.append(0)
    llyy.append(0)
    urxx.append(0)
    uryy.append(0)

#init parameters
count = 0
cost1 = 0
cost2 = 0
t_prev = 0
target = 1
max_x = 0
max_y = 0

#init condition
llx[0] = 0
lly[0] = 0
urx[0] = wl[0]
ury[0] = hl[0]
max_x = wl[0]
max_y = hl[0]

for a,b,c in zip(nl,wl,hl):
    if count+1 < len(llx):
        llxx[count+1] = b + llxx[count]
    if count-1 == -1: 
        urxx[count] = b 
    else:
        urxx[count] = b + urxx[count-1]
    uryy[count] = c
    #print(llx[count],lly[count],urx[count],ury[count])
    count += 1


while(target < len(nl)):
    cost1 = max(max_x,urx[t_prev]+wl[target])*max(max_y,lly[t_prev]+hl[target]) #put right
    cost2 = max(max_x,llx[t_prev]+wl[target])*max(max_y,ury[t_prev]+hl[target]) #put up
    if cost1 <= cost2:
        llx[target] = urx[t_prev]
        lly[target] = lly[t_prev]
    else:
        llx[target] = llx[t_prev]
        lly[target] = lly[t_prev]+hl[target]  
    urx[target] = llx[target]+wl[target]
    ury[target] = lly[target]+hl[target]
    max_x = max(max_x,urx[target])
    max_y = max(max_y,ury[target])
    t_prev += 1
    target += 1

area1 = max_x*max_y
area2 = urxx[-1] * max(uryy)

if area1 < area2:
    end = time.time()  
    exectime = end - start
    nf.write(str(area1)+'\n')
    nf.write(str(max_x)+'\n')
    nf.write(str(max_y)+'\n')
    nf.write("%.9f" % exectime+'\n')    
    for i in range(len(nl)-1):
        nf.write("{} {} {} {} {}".format(nl[i],llx[i],lly[i],urx[i],ury[i])+'\n')
    nf.write("{} {} {} {} {}".format(nl[-1],llx[-1],lly[-1],urx[-1],ury[-1]))
    nf.close()
else:
    area2 = urxx[-1] * max(uryy)
    end = time.time()  
    exectime = end - start
    nf.write(str(area2)+'\n')
    nf.write(str(urxx[-1])+'\n')
    nf.write(str(max(uryy))+'\n')
    nf.write("%.9f" % exectime+'\n')    
    for i in range(len(nl)-1):
        nf.write("{} {} {} {} {}".format(nl[i],llxx[i],llyy[i],urxx[i],uryy[i])+'\n')
    nf.write("{} {} {} {} {}".format(nl[-1],llxx[-1],llyy[-1],urxx[-1],uryy[-1]))
    nf.close()