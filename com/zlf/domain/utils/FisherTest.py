'''
Created on 2016-5-20

@author: Administrator
'''
from fisher.cfisher import pvalue

#11    47    83    1449    4.085875417    0.000165271
def fisherTestPvalue(data,full=1,tail='right'):
    diffMapping=data[0]-full
    diffAll=data[1]
    bgMapping=data[2]
    bgAll=data[3]
    
    p = pvalue(diffMapping, diffAll-diffMapping, bgMapping-diffMapping, bgAll-bgMapping-diffAll+diffMapping)
    if tail=='right':
        return p.right_tail
    elif tail=='left':
        return p.left_tail
    else:
        return p.two_tail

if __name__ == '__main__':
#     a = np.arange(0,12,0.5).reshape(4,-1)
#     print a
    diffMapping=1
    diffAll=1
    bgMapping=18
    bgAll=558
#     p = pvalue(diffMapping, diffAll-diffMapping, bgMapping-diffMapping, bgAll-bgMapping-diffAll+diffMapping)
#     print p.right_tail
#     print fisherTestPvalue([diffMapping,diffAll,bgMapping,bgAll],0)
    

