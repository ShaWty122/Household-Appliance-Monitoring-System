#input:rules.xlsx
import xlrd
def rec(search_ante):
    loc=("rules.xlsx")
    wb=xlrd.open_workbook(loc)
    sheet=wb.sheet_by_index(0)
    #search_ante=(input("The appliance_id:\n"))
    
    #for i in range(1,sheet.nrows):
       # print(sheet.cell_value(i,0))
    #print(search_ante.split(' ')) 
    list1=[]
    for i in range(1,sheet.nrows):
    	row_list=sheet.cell_value(i,0)
    	if((set(sheet.cell_value(i,0).replace('[','').replace(']','').split(','))) == set(search_ante.split(' '))):
             if((float(sheet.cell_value(i,2))>=0.5) & (float(sheet.cell_value(i,3))>=1)):
                list1.append((sheet.cell_value(i,1)))
    print(list1)
    return list1
                
import tkinter as tk
from math import *

def evaluate(event):
    listToStr = '\n'.join([str(elem) for elem in rec(entry.get())])
    res.configure(text = "Recommended:\n " + listToStr)
    
w = tk.Tk()
tk.Label(w, text="Appliance_ID:").pack()
entry = tk.Entry(w)
print(entry.get())
entry.bind("<Return>", evaluate)
entry.pack()
res = tk.Label(w)
res.pack()
w.mainloop()