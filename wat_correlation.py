#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[2]:


_sp = SparkSession.builder.master("local").appName("TSMC_WAT&YIELD").getOrCreate()


# In[3]:


Wat = _sp.read.format("csv"). option("header","true"). load("WAT.csv")


# In[4]:


Yield = _sp.read.format("csv"). option("header","true"). load("Yield.csv")


# In[5]:


import numpy as np


# In[6]:


w = Wat.toPandas()


# In[7]:


yy = Yield.toPandas()


# In[8]:


data = w.merge(yy,right_on=["_c0"],left_on=["wafer_id"],how="inner")


# In[9]:


data = data.drop(["_c0_x","wafer_id","_c0_y"],axis=1)


# In[10]:


data = data.convert_objects(convert_numeric=True)


# In[11]:


rate = data.corr("pearson")
print(rate)


# In[12]:


rank = rate.sort_values(by=["yield"],ascending=[False])


# In[13]:


print(rank["yield"][0:10])


# In[14]:


import matplotlib.pyplot as plt

f=plt.figure()


# In[15]:


f, (ax1) = plt.subplots(sharex=True, sharey=True)

ax1.scatter(data["yield"],data["WAT1036"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT1036"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][1])

f, (ax2) = plt.subplots(sharex=True, sharey=True)
ax2.scatter(data["yield"],data["WAT2985"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT2985"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][2])

f, (ax3) = plt.subplots(sharex=True, sharey=True)
ax3.scatter(data["yield"],data["WAT2848"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT2848"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][3])

f, (ax4) = plt.subplots(sharex=True, sharey=True)
ax4.scatter(data["yield"],data["WAT748"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT748"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][4])

f, (ax5) = plt.subplots(sharex=True, sharey=True)
ax5.scatter(data["yield"],data["WAT517"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT517"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][5])

f, (ax6) = plt.subplots(sharex=True, sharey=True)
ax6.scatter(data["yield"],data["WAT1477"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT1477"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][6])

f, (ax7) = plt.subplots(sharex=True, sharey=True)
ax7.scatter(data["yield"],data["WAT33"])
plt.ylim(max(data["WAT33"]), min(data["WAT33"]))
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT33"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= -%f'%rank["yield"][7])

f, (ax8) = plt.subplots(sharex=True, sharey=True)
ax8.scatter(data["yield"],data["WAT2064"])
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT2064"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= %f'%rank["yield"][8])

f,(ax9) = plt.subplots(sharex=True, sharey=True)
ax9.scatter(data["yield"],data["WAT2086"])
plt.ylim(max(data["WAT2086"]), min(data["WAT2086"]))
A = np.vstack([data["yield"],np.ones(len(data["yield"]))]).T
m,c = np.linalg.lstsq(A,np.array(data["WAT2086"]))[0]
plt.plot(data["yield"],data["yield"]*m+c,color="r")
plt.title('corr= -%f'%rank["yield"][9])


# In[ ]:




