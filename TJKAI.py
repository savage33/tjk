# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:50:28 2022

@author: Savage33
"""

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from sklearn.compose import ColumnTransformer
import keras

veri = pd.read_excel(r"C:\Users\Savage33\OneDrive\Masaüstü\TJK_islenmis.xlsx",sheet_name="Sheet1")


X=veri.iloc[:,:8].values
y=veri.iloc[:,8:].values

ohe=ColumnTransformer([("ohe",OneHotEncoder(dtype=float),[1])],remainder="passthrough")



X=ohe.fit_transform(X)

X_train,y_train,X_test,y_test = train_test_split(X,y,test_size=0.33,random_state=0)
sc=StandardScaler(with_mean=False)
X_train=sc.fit_transform(X_train)
X_test=sc.fit_transform(X_test)

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_train2=pca.fit_transform(X_train)
X_test2=pca.transform(X_test)