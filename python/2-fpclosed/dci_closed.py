import numpy
import pandas

def readDataFromFileToDataBase(dataBase, filePath):
    fHandle = open(filePath, "r")
    nTId = 0
    maxItemId = 0
    for i in fHandle.readlines():
        nTId += 1
        lineSplitted = i.split()
        for value in lineSplitted:
            item = int(value)
            if(item in dataBase):
                dataBase[item] = numpy.append(dataBase[item], nTId)
            else:
                dataBase[item] = numpy.array([nTId])
            if(item > maxItemId):
                maxItemId = item

    fHandle.close()
    return maxItemId
                
def createPostSet(dataBase, maxItemId, minSuppRelative):
    postSet = []
    for i in range(1, maxItemId + 1):
        try:
            tidSet = dataBase[i]
        except:
            continue
        if(len(tidSet) >= minSuppRelative):
            postSet.append(i)
    return numpy.array(postSet)

def isDup(newGenTIds, preset, dataBase):
    for i in preset:
        if(set(newGenTIds).issubset(set(dataBase[i]))):
            return True   
    return False

def intersectTIdSet(tIdSet1, tIdSet2):
    #print('tIs1',tIdSet1,'tIs1',tIdSet2)
    newTIdSet = []
    if(len(tIdSet1) > len(tIdSet2)):
        for tId in tIdSet2:
            if(numpy.any(tIdSet1 == tId)):
                newTIdSet.append(tId)
    else:
        for tId in tIdSet1:
            if(numpy.any(tIdSet2 == tId)):
                #print("tId",tId)
                newTIdSet.append(tId)
    return numpy.array(newTIdSet)

def isSmallerAccordingToOrder(a, b, dataBase):
    if(a < b):
        return True
    else:
        return False

def isSmallerAccordingToSupport(a, b, dataBase):
    sizeA = len(dataBase[a])
    sizeB = len(dataBase[b])
    if(sizeA != sizeB):
        return sizeA < sizeB
    else:
        return isSmallerAccordingToOrder(a, b, dataBase)


def sortPostSet(postSet, dataBase):        
    for i in range(len(postSet)):
        minimum = i       
        for j in range(i + 1, len(postSet)):
            if(isSmallerAccordingToSupport(postSet[minimum], postSet[j], dataBase)):
                minimum = j
        postSet[minimum], postSet[i] = postSet[i], postSet[minimum]          
    return numpy.flip(postSet)     

def getSupport(item, dataBase):
    return len(dataBase[item])
    
fp=list()
def dci_closed(isFirstTime, closedSet, closedSetTIds, postSet, preSet, minSupp, dataBase, f_out):
    
    for i in postSet:
        
        newGenTIds = []

        if(isFirstTime):
            newGenTIds = dataBase[i]
        else:
            newGenTIds = intersectTIdSet(closedSetTIds, dataBase[i])
       
        if(len(newGenTIds) >= minSupp):
            newGen = numpy.append(closedSet, numpy.array([i]))
         
            if(isDup(newGenTIds, preSet, dataBase) == False):
                closedSetNew = numpy.array(newGen)
               
                if(isFirstTime):
                    closedNewTIds = dataBase[i]
                else:
                    closedNewTIds = numpy.array(newGenTIds)
                
                postSetNew = []
             
                for j in postSet:
                   
                    if(isSmallerAccordingToSupport(i, j, dataBase)):

                        if(set(newGenTIds).issubset(dataBase[j])):
                            #print("j",j)
                            closedSetNew = numpy.append(closedSetNew, [j])

                            jTIds = dataBase[j]

                            closedNewTIds = intersectTIdSet(closedNewTIds, jTIds)
                        else:
                            #print('j',j)
                            postSetNew = numpy.append(postSetNew, [j])
                
                temp=[','.join(map(repr, closedSetNew.astype(int))), len(closedNewTIds)]
                
                if(len(temp)!=0):
                    fp.append(temp)
            
                preSetNew = numpy.array(preSet)
             
                dci_closed(False, closedSetNew, closedNewTIds, postSetNew, preSetNew,  minSupp, dataBase, f_out)

                preSet = numpy.append(preSet, [i])
   
    return fp         
