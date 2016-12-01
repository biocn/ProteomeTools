# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��11��3��

@author: Administrator
'''
from com.zlf.domain.utils.FastaOpertor import extractProteinID
from com.zlf.domain.utils.FileOpertor import getDataMatrix


#解析m8的结果
def parseM8(_path):
    matrix=getDataMatrix(_path)[0];
    _map={}
    for cols in matrix:
        key=extractProteinID(cols[0])
        if _map.has_key(key):
            if _map[key][1]<float(cols[2]):
                _map[key]=(extractProteinID(cols[1]),float(cols[2]),int(cols[3]))
        else:
            _map[key]=(extractProteinID(cols[1]),float(cols[2]),int(cols[3]))
    return _map;

if __name__ == '__main__':
    
    pass




