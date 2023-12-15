# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:27:02 2021

@author: USER
"""
import random
import argparse
import math
import time
import operator
from collections import defaultdict
start = time.time()
'''
parser = argparse.ArgumentParser(description='Add some I/O Command')
parser.add_argument("infile", type=str)
parser.add_argument("outfile",type=str)
args = parser.parse_args()
inputfile = args.infile
outputfile = args.outfile

f = open(inputfile,'r')
nf = open(outputfile,'w')
'''
f = open('case1.in','r')
nf = open('res.txt','w')
lines = f.readlines()
input_pin = []
net_data = []
bi_net1 = []
bi_net2 = []
net_list = {}
cell_list = {}
net_count = 0

for line in lines:
    #print(line[13:-2])
    #print(cell_list)
    if line[0:2] == '0.':
        print('Recept factor:{}'.format(line))
        pass
    elif line[0:3] == 'NET' and line[-2] == ';':
        #print('Line:{}'.format(line))
        net_data.append(line[12:-2].split())
        a = line[12:-2].split()      
        #print(line[4:11].split())
        net_list[line[4:11].split()[0]] = a
        for i in range(len(a)):
            #print(a[i])
            if a[i] not in input_pin:
                input_pin.append(a[i])
                cell_list[a[i]] = line[4:11].split()
            else:
                cell_list[a[i]].append(line[4:11].split()[0]) 
        net_name = line[4:11].split()
        net_count += 1
    elif line[0:3] == 'NET' and line[-2] != ';':
        a = line[12:-1].split()
        net_list[line[4:11].split()[0]] = a
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
                cell_list[a[i]] = line[4:11].split()
            else:
                cell_list[a[i]].append(line[4:11].split()[0]) 
        net_name = line[4:11].split()
        b = line[12:-1].split()
        net_data.append(b)
        net_count += 1
    elif line[0:3] == '   ' and line[-2] == ';' and line[13] != ';':
        a = line[:-2].split()
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
                cell_list[a[i]] = net_name
            else:
                cell_list[a[i]].append(net_name[0])
            net_data[net_count-1].append(a[i])
            net_list[net_name[0]].append(a[i])   
    elif line[0:3] == '   ' and line[-2] != ';':
        a = line[12:-1].split()
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
                cell_list[a[i]] = net_name
            else:
                cell_list[a[i]].append(net_name[0])
            net_list[net_name[0]].append(a[i])
            net_data[net_count-1].append(a[i])
    else:
        pass

cell_relation = defaultdict(list)
for cell in cell_list:
    for i in cell_list[cell]:
        #print(i)
        for net,cells in net_list.items():
            #print(net)
            if net == i:              
               for j in cells:
                   if (j != cell):
                       if j not in cell_relation[cell]:
                           cell_relation[cell].append(j)
#print(cell_relation['c12078'])

#Bipartite pins
#for i in range(math.floor(len(input_pin)/2)):
for i in range(int(len(input_pin)/2)):
    a = random.choice(input_pin)
    input_pin.remove(a)
    bi_net1.append(a)
    b = random.choice(input_pin)
    input_pin.remove(b)
    bi_net2.append(b)

cut = 0

for a in range(len(net_data)):
    one_count = 0
    two_count = 0
    for b in range(len(net_data[a])) :
        if net_data[a][b] in bi_net1:
            one_count += 1
        else:
            two_count += 1
    cut +=  (one_count * two_count) 
print('cut:{}'.format(cut))
print('Cutsize calculatation complete')



if input_pin:
    lists = ['b1','b2']
    c = input_pin
    d = random.choice(lists)
    if d == 'b1':
        bi_net1.append(c[0])
    else:
        bi_net2.append(c[0])
print('Bipartion Done')





GainL = {}
GainR = {}
for i in bi_net1:
    GainL[i] = None
for j in bi_net2:
    GainR[j] = None
print('Gain initialize Done')


for cell in cell_list:
    gain = 0
    for i in cell_list[cell]:
        for net,cells in net_list.items():
            if net == i:
                for j in cells:
                   if (j != cell):
                       if cell in bi_net1:
                           if j in bi_net1:
                               gain += 1
                           else:
                               gain -= 1
                       else:
                           if j in bi_net2:
                               gain += 1
                           else:
                               gain -= 1
    if cell in bi_net1:
        print('Cell {}:{}'.format(cell,gain))
        GainL[cell] = gain
    else:
        print('Cell {}:{}'.format(cell,gain))
        GainR[cell] = gain
                           


sortL = sorted(GainL.items(), key = operator.itemgetter(1), reverse = True)
sortR = sorted(GainL.items(), key = operator.itemgetter(1), reverse = True)
print('Gain Sort complete')

cnt = 0
total_gain = 0
m = 0
n = 0


while(cnt < 100):
    print('FM exchange start')
    loopstart = time.time()
    if sortL[m][1] >= sortR[n][1]:
        new_cut = 0
        bi_net1.remove(sortL[m][0])
        bi_net2.append(sortL[m][0])
        for a in range(len(net_data)):
            one_count = 0
            two_count = 0
            for b in range(len(net_data[a])) :
                if net_data[a][b] in bi_net1:
                    one_count += 1
                else:
                    two_count += 1
            new_cut +=  (one_count * two_count) 
        m += 1
        if new_cut < cut:
            cut = new_cut
            cnt += 1
        print('Cut:{}'.format(cut))
        loopend = time.time()
        looptime = loopend - loopstart
        print('Looptime:{}'.format(looptime))  
    else:
        new_cut = 0
        bi_net2.remove(sortR[n][0])
        bi_net1.append(sortR[n][0])
        for a in range(len(net_data)):
            one_count = 0
            two_count = 0
            for b in range(len(net_data[a])) :
                if net_data[a][b] in bi_net1:
                    one_count += 1
                else:
                    two_count += 1
            new_cut +=  (one_count * two_count) 
        n += 1
        if new_cut < cut:
            cut = new_cut
            cnt += 1
        print('Cut:{}'.format(cut))
        loopend = time.time()
        looptime = loopend - loopstart
        print('Looptime:{}'.format(looptime))  

end = time.time()  
exectime = end - start
print('Exectime:{}'.format(exectime))    

nf.write('Cutsize = ')
nf.write(str(cut)+'\n')
nf.write('G1 ')
nf.write(str(len(bi_net1))+'\n')
for i in range(len(bi_net1)):
    #nf.write('{} '.format(bi_net1[i]),'')
    nf.write(bi_net1[i]+' ')
nf.write(';'+'\n')
nf.write('G2 ')
nf.write(str(len(bi_net2))+'\n')
for j in range(len(bi_net1)):
    nf.write(bi_net2[j]+' ')
nf.write(';')
print('Write file Done')

f.close()
nf.close()

