# -*- coding: utf-8 -*-
"""Eesha Rizwan - PreLabC

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I2XWZQo4YQI3ww-uqXgTZLDToQZi9Az2

# Laboratory Lecture C #

This lab builds on the theory of classification.
&nbsp;
&nbsp;
&nbsp;

## Preamble ##
"""

import math
import io
import os

import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns
import matplotlib.pyplot as plt

# New package
from sklearn import tree
from sklearn.model_selection import train_test_split

"""## Data ##

### Import the data ###
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

pathname = "/content/drive/My Drive/STAT 312/Laboratory Activity C/"
os.chdir(pathname)

### Now, we load the datafile
#   and drop a few states

filename = "RuralAtlasData24.xlsx"
dtP = pd.read_excel(filename, sheet_name="People")
dtC= pd.read_excel(filename, sheet_name="County Classifications")
dtI= pd.read_excel(filename, sheet_name="Income")


dtC = dtC.rename(columns = {"FIPStxt": "FIPS"})
dtI = dtI.rename(columns = {"FIPStxt": "FIPS"})

dtP = pd.merge(dtP, dtC, on="FIPS")
dtP = pd.merge(dtP, dtI, on="FIPS")

dtP = dtP[dtP['State'] != "PR"]
dtP = dtP[dtP['State'] != "AK"]
dtP = dtP[dtP['State'] != "HI"]

dtP=dtP.dropna()

dtP

"""&nbsp;
&nbsp;
&nbsp;

## Decision Trees ##
"""

features = dtP[ ["AvgHHSize","FarmDependent2003", "Poverty_Rate_ACS"] ]
target   = dtP[ "Hipov"]

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.40, random_state = 780088)

### Train the tree classifier

stTree = tree.DecisionTreeClassifier()           # defining decision tree classifier (basic)
stTree = stTree.fit(X_train,y_train)   # fit model on training data

stTree.get_depth()

levels = np.arange(18)
accTR = []
accTE = []

for i in levels:
  stTree = tree.DecisionTreeClassifier(max_depth=i+1)
  stTree = stTree.fit(X_train,y_train)

  predTR = stTree.predict(X_train)
  predTE = stTree.predict(X_test)

  accTR.append( round( np.sum(y_train==predTR)/len(y_train)*100,1) )
  accTE.append( round( np.sum(y_test==predTE)/len(y_test)*100,1)   )

plt.figure (figsize= ( 15, 8 ))

plt.rcParams["axes.labelsize"] = 14
plt.rcParams["axes.labelweight"] = "bold"

plt.scatter( levels, accTR)
plt.scatter( levels, accTE)

plt.title("Gini")

plt.xlabel("\nMaximum Depth of Tree")
plt.ylabel("Accuracy Percent\n")


plt.ylim(0, 105);

plt.savefig("GiniDepth.png")

np.argmax(accTE)

accTE[1]

levels = np.arange(18)
accTR = []
accTE = []

for i in levels:
  stTree = tree.DecisionTreeClassifier(criterion="entropy", max_depth=i+1)
  stTree = stTree.fit(X_train,y_train)

  predTR = stTree.predict(X_train)
  predTE = stTree.predict(X_test)

  accTR.append( round( np.sum(y_train==predTR)/len(y_train)*100,1) )
  accTE.append( round( np.sum(y_test==predTE)/len(y_test)*100,1)   )

plt.figure (figsize= ( 15, 8 ))

plt.rcParams["axes.labelsize"] = 14
plt.rcParams["axes.labelweight"] = "bold"

plt.scatter( levels, accTR)
plt.scatter( levels, accTE)

plt.title("Entropy")
plt.xlabel("\nMaximum Depth of Tree")
plt.ylabel("Accuracy Percent\n")


plt.ylim(0, 105);

plt.savefig("EntropyDepth.png")

np.argmax(accTE)

accTE[4]

"""## Accuracy ###"""

### Training final tree classifier

stTreeF = tree.DecisionTreeClassifier(max_depth=1)
stTreeF = stTreeF.fit(X_train,y_train)   # fit model on training data

prediction = stTreeF.predict(X_test)
print("Accuracy:", round( np.sum(y_test==prediction)/len(y_test)*100,1),"%")

dtP["Hipov"].mode()

print("Accuracy:", round( np.sum(y_test==dtP["Hipov"].mode()[0])/len(y_test)*100,1),"%")

z = 93-81.8
print ("Accuracy Improvement", z, "%")

print("Relative Improvement in Accuracy", round(z/81.8*100,1),"%")

"""
### References ###

```
@misc{RuralAtlasData23,
  title        = "Atlas of Rural and Small-Town {A}merica",
  author       = "{US Economic Research Service}",
  howpublished = "\url{https://www.ers.usda.gov/data-products/atlas-of-rural-and-small-town-america/download-the-data/}",
  year         = 2021,
  note         = "Accessed: 2021-06-08"
}
```

<br>

```
@article{scikit-learn,
  title={Scikit-learn: Machine Learning in {P}ython},
  author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
         and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
         and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and
         Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
  journal={Journal of Machine Learning Research},
  volume={12},
  pages={2825--2830},
  year={2011}
}
```

"""
