#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys

#this part is used for pyspark submit
os.environ['PYSPARK_SUBMIT_ARGS']='--verbose --master=yarn --queue test pyspark-shell'

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


# In[ ]:


from pyspark.sql import SparkSession
spark =SparkSession.builder.appName("part").getOrCreate()


# In[ ]:


import pandas as pd

data = spark.read.option('header','true').option('inferSchema','true').csv('HH/stage/mid_right.csv')
df = data.toPandas()


# In[ ]:


from sklearn.cross_decomposition import PLSRegression
import numpy as np


pls2 = PLSRegression(n_components=2)
x, y = df[data.columns[1:-1]], df['yield']
model = pls2.fit(x, y)


# In[ ]:


def vip(x, y, model):
    t = model.x_scores_
    w = model.x_weights_
    q = model.y_loadings_

    m, p = x.shape
    _, h = t.shape

    vips = np.zeros((p,))

    s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
    total_s = np.sum(s)

    for i in range(p):
        weight = np.array([ (w[i,j] / np.linalg.norm(w[:,j]))**2 for j in range(h) ])
        vips[i] = np.sqrt(p*(s.T @ weight)/total_s)

    return vips

vips = vip(x, y, model).tolist()

for i, vip in enumerate(vips):
    vips[i] = ('WAT{}'.format(i+1), vip)

result = sorted(vips, key=lambda x: x[1], reverse=True)

for i in range(20):
    print(result[i])


# In[ ]:


import pandas as pd
df = pd.DataFrame({
    'a': [1,2,3],
    'b': [4,5,6],
    'c': [7,8,9]
})
print(df)
print(df[[*df.columns[0:-1], 'c']])

