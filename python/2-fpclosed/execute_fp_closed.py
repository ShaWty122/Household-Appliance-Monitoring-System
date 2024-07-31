#input:fpdata.dat
#output:fp_closed_out.xlsx

import dci_closed as dci
import pandas

minSupp = 0
dataBase = {}
maxItemId = dci.readDataFromFileToDataBase(dataBase, "fpdata.dat")

postSet = dci.createPostSet(dataBase, maxItemId, minSupp)

postSet = dci.sortPostSet(postSet, dataBase)

closedSet = []
closedSetTIds = []
preSet = []


f_out = open("fpclosed_out.dat","w")
fp=dci.dci_closed(True, closedSet, closedSetTIds, postSet, preSet, 0.3 ,dataBase, f_out)
df=pandas.DataFrame(fp)
print(fp)
df.to_excel("fp_closed_out.xlsx", sheet_name = 'Sheet1', index = False)