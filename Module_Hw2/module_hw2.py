# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:27:02 2021

@author: USER
"""
import random
import argparse
import math
import time

start = time.time()
'''
parser = argparse.ArgumentParser(description='Add some I/O Command')
parser.add_argument("infile", type=str)
parser.add_argument("outfile",type=str)
args = parser.parse_args()
inputfile = args.infile
outputfile = args.outfile

f = open(inputfile,'r')
nf = open(outputfile,'w')'''
f = open('case1.in','r')
nf = open('res.txt','w')
lines = f.readlines()
net_data = []
input_pin = []
input_net = []
bi_net1 = []
bi_net2 = []
net_count = 0

for line in lines:
    #print(line[13:-2])
    if line[0:2] == '0.':
        print('Recept factor:{}'.format(line))
        pass
    elif line[0:3] == 'NET' and line[-2] == ';':
        #print('Line:{}'.format(line))
        net_data.append(line[12:-2].split())
        a = line[12:-2].split()
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
        net_count += 1
        #print(net_count)
    elif line[0:3] == 'NET' and line[-2] != ';':
        a = line[12:-1].split()
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
        b = line[12:-1].split()
        net_data.append(b)
        net_count += 1
        #print(net_count)
    elif line[0:3] == '   ' and line[-2] == ';' and line[13] != ';':
        a = line[:-2].split()
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
            net_data[net_count-1].append(a[i])       
    elif line[0:3] == '   ' and line[-2] != ';':
        a = line[12:-1].split()
        #print(a)
        for i in range(len(a)):
            if a[i] not in input_pin:
                input_pin.append(a[i])
        net_data[net_count-1].append(a[i])
    else:
        pass
'''
input_pin.sort()
print('Total Pin:{}'.format(input_pin))
print('==============================================')
print('Total Input:{}'.format(net_data))
print('==============================================')
'''

#Bipartite pins
for i in range(int(len(input_pin)/2)):
    a = random.choice(input_pin)
    input_pin.remove(a)
    bi_net1.append(a)
    b = random.choice(input_pin)
    input_pin.remove(b)
    bi_net2.append(b)
print('Bipartion Done')
#print(len(net_data))
print(len(bi_net1))
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
    print('Loop {} Done:{}*{}'.format(a,one_count,two_count))      
print('cut:{}'.format(cut))    

test_cut = cut

for i in range(int(len(bi_net1)/500)):
    print('iteration:{}'.format(i+1))
    origin_cut = test_cut
    print('origin cut:{}'.format(origin_cut))
    while(origin_cut <= test_cut):
        print('Reducing cut number...')
        cut = 0
        test1 = random.choice(bi_net1)
        print('Choose {} swap to bi_net2'.format(test1))      
        test2 = random.choice(bi_net2)
        print('Choose {} swap to bi_net1'.format(test2))  
        bi_net1.remove(test1)
        bi_net2.append(test1)
        bi_net2.remove(test2)
        bi_net1.append(test2)
    
        for a in range(len(net_data)):
            one_count = 0
            two_count = 0
            for b in range(len(net_data[a])) :
                if net_data[a][b] in bi_net1:
                    one_count += 1
                else:
                    two_count += 1
            cut +=  (one_count * two_count)
        if origin_cut <= cut:
            print('cut:{}'.format(cut))
            print('Swap fail QAQ Prepare for next iter')
            bi_net1.remove(test2)
            bi_net2.append(test2)
            bi_net2.remove(test1)
            bi_net1.append(test1) 
        else:
            test_cut = cut
            print('cut:{}'.format(test_cut))

end = time.time()  
exectime = end - start
print('Exectime:{}'.format(exectime))    
nf.write('Cutsize = ')
nf.write(str(test_cut)+'\n')
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
