import pylab
import matplotlib.pyplot as mpl
import numpy as np
import math
import scipy.stats as stats
data1 = [80.1978440285,80.2850291729,80.3210718632,80.1623129845,80.0409128666,80.150094986,80.1820938587,78.70561409,80.1455769539,80.0951890945,0,0,0]
data2 = [82.4514968395,82.3665709496,82.5913438797,82.3853888512,82.6252110004,83.015887022,82.4156680107,82.6154780388,82.4987449646,80.5220081806,78.416301012,0,0]
data3 = [87.2795908451,87.1020419598,87.0223500729,87.2792508602,85.908616066,87.4601039886,87.2562019825,87.2490091324,85.29570508,84.39148283,83.5163471699,79.1886370182,0]
data4 = [95.5342559814,95.2675101757,94.2593200207,94.8392989635,94.7588331699,96.7731900215,93.1387479305,93.1441278458,93.1370079517,93.8308980465,89.0460309982,89.0156650543,89.0224301815]
data5 = [112.094958067,113.38303709,111.488659143,111.355453968,111.475857019,109.271573067,109.644687891,109.247980833,111.35271883,111.488021135,113.681798935,113.593528986,113.778628826]
size1 = [256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576]
x = np.exp2(np.arange(21))
mpl.loglog(size1,data1,label = 'No. of jobs = 8')
pylab.hold(True)
mpl.loglog(size1,data2,label = 'No. of jobs = 16')
pylab.hold(True)
mpl.loglog(size1,data3,label = 'No. of jobs = 32')
pylab.hold(True)
mpl.loglog(size1,data4,label = 'No. of jobs = 64')
pylab.hold(True)
mpl.loglog(size1,data5,label = 'No. of jobs = 128')
pylab.hold(True)
mpl.xticks(x,x)
mpl.xlim(256,2097152)
#mpl.ylim(10,200)
pylab.legend(loc=2,prop={'size':8})
pylab.xlabel('Data/Job (no. of elements)')
pylab.ylabel('Execution Time/Job (seconds)')
pylab.title('Data Size vs Execution Time over different number of jobs -- Sierra Remote submission (no. of processes = 8) -- LogLog plot',fontsize = 10)
pylab.show()