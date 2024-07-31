#input:fpdata.xlsx
#output:freqitems.xlsx

from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth
import matplotlib.pyplot as plt
import xlrd
import pandas
import sys
wb = xlrd.open_workbook("fpdata.xlsx")
sheet = wb.sheet_by_index(0)
fpdata=list()
fpdata2=list()
fp=list()
for i in range(sheet.nrows):
   fpdata.append((sheet.cell_value(i,0)).split(','))
for i in fpdata:
   fpdata1=list()
   for j in i:
      fpdata1.append(int(j))
   fpdata2.append(fpdata1)
spark = SparkSession \
     .builder \
     .appName("Python Spark SQL basic example") \
     .config("spark.some.config.option", "some-value") \
     .getOrCreate()
for i in range(0,len(fpdata2)):
     p=(i,fpdata2[i])
     fp.append(p)
df=spark.createDataFrame(fp,["id","items"])
fpGrowth = FPGrowth(itemsCol="items", minSupport=0, minConfidence=0)
model = fpGrowth.fit(df)
model.freqItemsets.show(model.freqItemsets.count(),False)
x=[0.0]
y=[model.freqItemsets.count()]
r=0.0
while round(r,1)<0.9:
   r=r+0.1
   fpGrowth = FPGrowth(itemsCol="items", minSupport=round(r,1), minConfidence=0)
   model = fpGrowth.fit(df)
   y.append(model.freqItemsets.count())
   x.append(r)
plt.plot(x,y)
plt.show()
#model.freqItemsets.toPandas().to_excel("freqitems.xlsx", sheet_name = 'Sheet1', index = False)
print(model.freqItemsets.toPandas())
model.freqItemsets.toPandas().to_excel("freqitems.xlsx", sheet_name = 'Sheet1', index = False)

