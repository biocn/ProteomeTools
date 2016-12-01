# -*- coding:utf-8 -*-
'''
Created on 2016��10��23��

@author: Administrator
'''

from os.path import os
import types
import shutil

def mkdir(_path):
    try:
        os.makedirs(_path)
    except:
        pass

def getLines(_path):
    f=open(_path,'r')
    lines=f.readlines()
    f.close()
    return lines    

#返回一个二维矩阵，和最长列数
def getDataMatrix(_path):
    lines=getLines(_path)
    _list=[]
    _max=0;
    for line in lines:
        cols=line.lstrip().rstrip('\n').split('\t')
        if _max<len(cols):
            _max=len(cols)
        _list.append(cols)
    return (_list,_max);
    
def getMapByData(_list,key,head=True):
    _ind=0
    if type(key) is types.IntType:
        _ind=key
    else:
        for i in range(len(_list[0])):
            if _list[0][i].lstrip().rstrip()==key:
                _ind=i
                break
    if head:
        _list1=_list[1:len(_list)]
    else:
        _list1=_list
    _map={}
    for cols in _list1:
        _map[cols[_ind]]=cols
    return _map

def mergeTable(_path1,keys1,_path2,keys2,key1,key2,outPath,head=True):
    data1=getDataMatrix(_path1)
    data2=getDataMatrix(_path2)
    _map1=getMapByData(data1[0], key1,head)
    _map2=getMapByData(data2[0], key2,head)
    fw=open(outPath,'w')
    if head:
        fw.write('Key')
        for i in keys1:
            fw.write('\t'+data1[0][0][i])
        for i in keys2:
            fw.write('\t'+data2[0][0][i])
        fw.write('\n')
    _ls=_map1.keys()
    _ls.extend(_map2.keys())
    for k in set(_ls):
        fw.write(k)
        if _map1.has_key(k):
            if keys1 and type(keys1[0]) is types.IntType:
                for i in keys1:
                    fw.write('\t'+(_map1[k][i]))
            else:
                fw.write('\t'+'\t'.join(_map1[k]))
        else:
            if keys1 and type(keys1[0]) is types.IntType:
                for i in range(len(keys1)):
                    fw.write('\t')
            else:
                for i in range(len(data1[1])):
                    fw.write('\t')
        if _map2.has_key(k):
            if keys2 and type(keys2[0]) is types.IntType:
                for i in keys2:
                    fw.write('\t'+(_map2[k][i]))
            else:
                fw.write('\t'+'\t'.join(_map2[k]))
        else:
            if keys2 and type(keys2[0]) is types.IntType:
                for i in range(len(keys2)):
                    fw.write('\t')
            else:
                for i in range(len(data2[1])):
                    fw.write('\t')
        fw.write('\n')
    fw.close()

def copyFile(file1,file2):
    if os.path.isfile(file1):
        shutil.copy(file1,file2)
        return 1
    return 0

def copyFolder(f1,f2):
    if os.path.exists(f2) and os.path.isdir(f2):
        shutil.rmtree(f2)
    if os.path.exists(f1) and os.path.isdir(f1):
        shutil.copytree(f1, f2)
def copyImage(p1,p2):
    copyFile(p1+'.jpg', p2+'.jpg')
    try:
        copyFile(p1+'.png', p2+'.png')
    except:
        pass
    return copyFile(p1+'.pdf', p2+'.pdf')    

def getCommonList(list1,list2):
    return list(set(list1).intersection(set(list2)))  

def getLineDatas(_path):
    lines=getLines(_path)
    _list=[]
    for line in lines:
        _list.append(line.rstrip().lstrip().rstrip('\n').rstrip('\r'))
    return _list

def writeLines(lines,_path):
    fw=open(_path,'w')
    for line in lines:
        fw.write(line+'\n')
    fw.close()
def writeMatrix(lines,_path):
    fw=open(_path,'w')
    for cols in lines:
        line=''
        for col in cols:
            line=line+'\t'+str(col)
        fw.write(line[1:len(line)]+'\n')
    fw.close()


if __name__ == '__main__':
    folder='E:/Work/MH/MH-B16061603/ProteinTrans'
    mergeTable(folder+'/Rep1/ProteinExprossion.txt', [1,10,11,12,13,14,15],
            folder+'/Rep2/ProteinExprossion.txt', [1,10,11,12,13,14,15], 0,0, folder+'/ProteinExprossion.txt')

