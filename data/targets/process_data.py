import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt




filepath = './modified data/Öko-Institut Sektorale_Abgrenzung_Treibhausgasemissionen_Datenbasis_(Stand 17. Dez 19).xlsx'

data = pd.read_excel(filepath, sheet_name='Tabelle 1-3')

targets = data.iloc[17, 2:30]
targets_exp_trend = data.iloc[17, 59:72]

targets_all = targets.append(targets_exp_trend)

x_values = np.arange(0, 41, 1)
y_values = x_values

ax = sns.pointplot(x=x_values, y=targets_all.to_numpy())
plt.show()


