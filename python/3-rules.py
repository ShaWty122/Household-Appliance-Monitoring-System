#input:fp_closed_out.dat   ---19th line--- or  fpoutput.dat
#output:rules_output.xlsx

import itertools
import time
import pandas as pd
"""prompt user to enter support and confidence values in percent"""

support = 0.01
confidence = 0.01
"""Compute candidate 1-itemset"""
C1 = {}
"""total number of transactions contained in the file"""
transactions = 0
D = []
T = []
df=pd.DataFrame(columns = ['Antec' , 'Conseq', 'Support' , 'Confi' ,'Lift'])

with open("fp_closed_out.dat", "r") as f:
    for line in f:
        T = []
        transactions += 1
        for word in line.split():
            T.append(word)
            if word not in C1.keys():
                C1[word] = 1
            else:
                count = C1[word]
                C1[word] = count + 1
        D.append(T)


for i in D:
      i.sort(key=int)

def list_of_combs(arr,L1): 
    for i in range(0,len(arr)+1):
        listing=[list(x) for x in itertools.combinations(arr,i)]
        L1.extend(filter(None,listing))
    return L1
    
L1=list()    
for i in range(0,len(D)):
  list_of_combs(D[i],L1)
L1.sort()
new_L=list(i for i,_ in itertools.groupby(L1))
#print(len(new_L))
#print(new_L)
L=list()
L1=list()
new_L.sort(key=len)
max_len=len(new_L[-1])
print(max_len)
j=2
while j<=max_len:
    L1=list()
    for i in new_L:
        if len(i)==j:
           L1.append(i)
    L.append(L1)
    j=j+1
j=1
L1=list()
for i in new_L:
    if len(i)==j:
        L1.append(i)
L.append(L1)

def findsubsets(S,m):
    return set(itertools.combinations(S, m))

def findsup(s):
        flag=0
        for i in new_L:
            count=0
            for j in s:
                if j in i:
                    count=count+1
            if(count==len(s)):
                flag=flag+1
        return flag/len(new_L)
        
        
def findconf(s,m):
    return(findsup(s+list(set(m)-set(s)))/findsup(s))
    
def findlift(s,m):
     return(findconf(s,m)/findsup(s))
    

#print(findsup(['1', '2', '3', '4', '5', '6', '9', '10', '11']))
    
def generate_association_rules():
    s = []
    r = []
    t= []
    length = 0
    count = 1
    inc1 = 0
    inc2 = 0
    num = 1
    m = []
    #L= frequent_itemsets()
    #print("FREQ")
    #print(L)
    print ("---------------------ASSOCIATION RULES------------------")
    print ("RULES \t\t SUPPORT \t\t CONFIDENCE\t\tLIFT")
    print ("--------------------------------------------------------")
    for list in L:
        for l in list:
            length = len(l)
            count = 1
            while count < length: 
                s = []
                r = findsubsets(l,count)
                #t.append(r)
                count += 1
                for item in r:
                    inc1 = 0
                    inc2 = 0
                    s = []
                    m = []
                    for i in item:
                        s.append(i)
                    for T in D:
                        if set(s).issubset(set(T)) == True:
                            inc1 += 1
                        if set(l).issubset(set(T)) == True:
                            inc2 += 1
                    if 100*inc2/inc1 >= confidence:
                        for index in l:
                            if index not in s:
                                m.append(index)
                        df.loc[num-1]=[s, m, findsup(s), findconf(s,m) , findlift(s,m)]
                        #print ("%d   %s  ==>   %s     %f     %f     %f" %(num, s, m, findsup(s), findconf(s,m) , findlift(s,m)))
                        num += 1 
                         
                    
    #print(len(t))
start_time=time.time()
generate_association_rules()
df.to_excel("rules_output.xlsx")
print("Time :::::::::::", (time.time()-start_time) * 100  ,"ms")