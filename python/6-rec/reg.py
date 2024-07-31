#input:rules_output.xlsx
import pandas as pd
df=pd.read_excel('rules_output.xlsx')
df["value"]=1
matrix = df.pivot_table(index='Antec', columns='Conseq',values="value",fill_value=0)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(matrix,matrix, test_size=0.2)
clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)
from sklearn.metrics import mean_squared_error,r2_score 
print(mean_squared_error(y_test,y_pred))
print("Regression Coefficient......." ,r2_score(y_test,y_pred))
	