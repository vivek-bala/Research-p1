import pylab
import matplotlib.pyplot as mpl
import numpy as np
import math
import scipy.stats as stats
data1 = [0,0,0,0,10.0247305036,10.0356286466,10.0401339829,10.0202891231,10.0051141083,10.0187618733,10.0227617323,9.8382017613,10.0181971192,10.0118986368]
data2 = [0,0,0,5.1532185525,5.1479106844,5.1619589925,5.1490868032,5.1640756875,5.1884929389,5.1509792507,5.1634673774,5.1561715603,5.0326255113,4.9010188133]
data3 = [0,0,2.7274872139,2.7219388112,2.7194484398,2.7274765894,2.6846442521,2.7331282496,2.726756312,2.7265315354,2.6654907838,2.6372338384,2.6098858491,2.4746449068]
data4 = [0,1.4927227497,1.4885548465,1.4728018753,1.4818640463,1.4806067683,1.5120810941,1.4552929364,1.4553769976,1.4552657492,1.466107782,1.3913442343,1.3908697665,1.3909754716]
data5 = [0.8757418599,0.8858049773,0.8710051496,0.8699644841,0.870905133,0.8536841646,0.8565991241,0.8534998503,0.8699431159,0.8710001651,0.8881390542,0.8874494452,0.8888955377,0]
size1 = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384]
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
mpl.xlim(2,32768)
#mpl.ylim(10,200)
pylab.legend(loc=2,prop={'size':8})
pylab.xlabel('Data/Job (no. of elements)')
pylab.ylabel('Execution Time/Job (seconds)')
pylab.title('Data Size/Job vs Execution Time/Job over different number of jobs -- Sierra Remote submission (no. of processes = 8) -- LogLog plot',fontsize = 10)
pylab.show()
