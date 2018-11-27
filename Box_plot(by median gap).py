#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys

#this part is used for pyspark submit
os.environ['PYSPARK_SUBMIT_ARGS']='--verbose --master=yarn --deploy-mode=client pyspark-shell'

os.environ['JAVA_HOME']='/usr/lib/jvm/java-8-openjdk-amd64/'
os.environ['YARN_CONF_DIR']='/etc/alternatives/hadoop-conf/'

#this line is used for spark1.6
#os.environ['SPARK_HOME']='/opt/cloudera/parcels/CDH/lib/spark'

#this line is used for spark2.2
os.environ['SPARK_HOME']='/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2'

# this line is used for python2.7
#os.environ['PYSPARK_PYTHON']='/usr/bin/python'

#this line is used for python3.5
os.environ['PYSPARK_PYTHON']='/usr/bin/python3'

spark_home = os.environ.get('SPARK_HOME', None)
sys.path.insert(0, os.path.join(spark_home, 'python'))
sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.10.4-src.zip'))  
#execfile(os.path.join(spark_home, 'python/pyspark/shell.py'))
exec(open(os.path.join(spark_home, 'python/pyspark/shell.py')).read())


# In[2]:


from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
import pyspark.sql.functions as func
from pyspark.sql.functions import col
from pyspark.sql.window import Window
import plotly.plotly as py
import plotly.graph_objs as go
from pyspark.sql.functions import desc


# In[3]:


_sp = SparkSession.builder.master("local").appName("TSMC_WAT&YIELD_HW2").getOrCreate()


# In[4]:


Yield = _sp.read.csv("/user/homework_1/Yield.csv", header=True,inferSchema=True)
Waferlog = _sp.read.csv("/user/homework_2/WaferLog.csv", header=True,inferSchema=True)


# In[5]:


w = Waferlog.withColumnRenamed('Wafer.ID', 'waferid')
data = Yield.join(w, Yield._c0 == w.waferid)
data = data.drop("_c0","Time")
data = data.withColumnRenamed('Tool.ID', 'toolid').withColumnRenamed('Process.stage', 'Processstage')


# In[6]:


data = data.withColumn('Processstage',data["Processstage"].astype("double"))
data = data.withColumn('Process',data["Process"].astype("double"))


# In[7]:


grp_window = Window.partitionBy(["Processstage","toolid"])
baby_percentile = func.expr('percentile_approx(yield, 0.5)')
data = data.withColumn('median', baby_percentile.over(grp_window))


# In[8]:


grp_ = Window.partitionBy("Processstage")
sexy_percentile = func.expr('percentile_approx(yield, 0.5)')
data_ = data.withColumn('stage_median', sexy_percentile.over(grp_))


# In[9]:


data = data_.drop("Process")


# In[10]:


data.printSchema()


# In[11]:


g = data["stage_median"]-data["median"]
data = data.withColumn("median_gap", g)
data1 = data.withColumn('median_gap',func.abs(data.median_gap))


# In[12]:


w = Window.partitionBy("Processstage").orderBy(desc("median_gap"))
data2 = data1.withColumn("rank", func.row_number().over(w))


# In[13]:


data3 = data2.where("rank<2")
data4 = data3.orderBy('median_gap' ,ascending=False)


# In[15]:


data4.show(5)


# In[21]:


data102 = data2.where("Processstage == 102.0")
data209 = data2.where("Processstage == 209.0")
data200 = data2.where("Processstage == 200.0")
data207 = data2.where("Processstage == 207.0")
data95  = data2.where("Processstage == 95.0")


# In[22]:


data_102 = data102.toPandas()
data_209 = data209.toPandas()
data_200 = data200.toPandas()
data_207 = data207.toPandas()
data_95  = data95.toPandas()


# In[23]:


pic1=data_102.boxplot(by='toolid',column=['yield'])
pic2=data_209.boxplot(by='toolid',column=['yield'])
pic3=data_200.boxplot(by='toolid',column=['yield'])
pic4=data_207.boxplot(by='toolid',column=['yield'])
pic5=data_95.boxplot(by='toolid',column=['yield'])
pic1.set(xlabel='process_stage 209')
pic2.set(xlabel='process_stage 102')
pic3.set(xlabel='process_stage 200')
pic4.set(xlabel='process_stage 207')
pic5.set(xlabel='process_stage 95')
pic1.axhline(y=73.1360347196551,color='r')
pic2.axhline(y=73.1360347196551,color='r')
pic3.axhline(y=73.1360347196551,color='r')
pic4.axhline(y=73.1360347196551,color='r')
pic5.axhline(y=73.1360347196551,color='r')


# In[ ]:




