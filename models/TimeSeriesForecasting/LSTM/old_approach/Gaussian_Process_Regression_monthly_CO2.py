import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, ConstantKernel, RBF
from sklearn.gaussian_process import GaussianProcessRegressor


#%% Define Kernel

k0 = WhiteKernel(noise_level=0.3**2, noise_level_bounds=(0.1**2, 0.5**2))

k1 = ConstantKernel(constant_value=10, constant_value_bounds=(1e-2, 1e3)) * \
    RBF(length_scale=100.0, length_scale_bounds=(1, 1e4))

kernel = k0 + k1


#%% Define GaussianProcessRegressor object

gp = GaussianProcessRegressor(
    kernel=kernel, 
    n_restarts_optimizer=10, 
    normalize_y=True,
    alpha=0.0
)

#%% Load the dataset

targets = pd.read_excel('./training_data_(targets_only).xlsx')
targets = targets.values

X = targets[:,0].reshape(-1,1)
y = targets[:,1].reshape(-1,1)

#%% Fit GPR

gp.fit(X, y)

y_pred, y_std = gp.predict(X, return_std=True)

X=targets[:,0]

y_pred = y_pred.reshape(-1)
y = y.reshape(-1)

fig, ax = plt.subplots()

#sns.lineplot(x=X, y=y_pred, color = 'black', ax=ax)
#sns.pointplot(x=X, y=y, color = 'green', linestyle='.')

new = np.arange(1990, 2020.5, (1/12))
new = new.reshape(-1,1)

y_pred_monthly, y_std_monthly = gp.predict(new, return_std=True)
sns.lineplot(x=X, y=y, color = 'black', ax=ax)
sns.lineplot(x=(new.reshape(-1)), y = (y_pred_monthly.reshape(-1)), ax=ax)

#%% Fit GPR with Features

data = pd.read_excel('./training_data.xlsx')

X_train = (data.iloc[:,2:-1]).to_numpy()


X_train = X_train.astype('float32')


gp2 = GaussianProcessRegressor(
    kernel=kernel, 
    n_restarts_optimizer=10, 
    normalize_y=True,
    alpha=0.0
)

gp2.fit(X_train, y_pred_monthly)
y_pred_train, y_std_train = gp2.predict(X_train, return_std=True)

fig, ax = plt.subplots()
sns.lineplot(x=X, y=y, color = 'black', ax=ax)
sns.lineplot(x=(new.reshape(-1)), y = (y_pred_train.reshape(-1)), color = 'red', ax=ax)

new2030 = np.arange(2020.5, 2030, (1/12))
new2030 = new2030.reshape(-1,1)

y_pred_2030, y_std_2030 = gp2.predict(new2030, return_std=True)


