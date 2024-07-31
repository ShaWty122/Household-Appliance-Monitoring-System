#input:DATASET_4.1.xlsx

import sys
def calculate_distance(centroid, X):
    distances = []
    c_x = centroid
    for x in X:
        root_diff_x = (x - c_x) ** 2
        distance = np.sqrt(root_diff_x)
        distances.append(distance)
    return distances
 
def clust(df,app_name,centroid):
    time=[]
    for i in df[1]:
        time.append(float((i.strftime('%H:%M')).replace(':','.')))
    data = pd.DataFrame({
        'value':time
    })
    new_centroid=centroid
    for i in range(0,48):
            data[i+1] = calculate_distance(new_centroid[i], data['value'])
    data['Cluster']=data.iloc[:,1:49].idxmin(axis=1)
    new_centroid=[]
    for i in range(0,48):
            new_centroid.append(data[data['Cluster']==i+1]['value'].mean())
    while True:
        for i in range(0,48):
            data[i+1] = calculate_distance(new_centroid[i], data['value'])
        data['Cluster']=data.iloc[:,1:49].idxmin(axis=1)
        new_centroid=[]
        for i in range(0,48):
            new_centroid.append(data[data['Cluster']==i+1]['value'].mean())
        centroid=new_centroid
        if centroid==new_centroid:
            break
    go=data.groupby('Cluster').size()
    for i in df.index:
        data.set_value(i, 'Clustersize', go.get(data.loc[i,'Cluster']))
    data['app']=app_name
    return data

import pandas as pd
import numpy as np
import random
centroid=[0.0,12.0,23.0]
fin=pd.DataFrame()
df=pd.read_excel("DATASET_4.1.xlsx",sheet_name='Sheet1',header=None)
data=clust(df,"aggregate",centroid)                                                                                                                                                  
fin=fin.append(data)
df=pd.read_excel(sys.argv[1],sheet_name='Sheet2',header=None)
data=clust(df,"tv_dvd_digibox_lamp",centroid)
fin=fin.append(data)
df=pd.read_excel(sys.argv[1],sheet_name='Sheet3',header=None)
data=clust(df,"kettle_radio",centroid)
fin=fin.append(data)
df=pd.read_excel(sys.argv[1],sheet_name='Sheet4',header=None)
data=clust(df,"gas_boiler",centroid)
fin=fin.append(data)
df=pd.read_excel(sys.argv[1],sheet_name='Sheet5',header=None)
data=clust(df,"freezer",centroid)
fin=fin.append(data)
df=pd.read_excel(sys.argv[1],sheet_name='Sheet6',header=None)
data=clust(df,"washing_machine_microwave_breadmaker",centroid)
fin=fin.append(data)
#print(data)
import matplotlib.pyplot as plt
plt.figure(figsize=(15,4))
plt.scatter(x=fin['value'],y=fin['app'],c=fin['Clustersize'],cmap='plasma')
plt.xticks(centroid,rotation='vertical')
plt.colorbar()
plt.show()