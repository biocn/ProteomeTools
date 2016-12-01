# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��11��23��

@author: Administrator
'''
from com.zlf.domain.utils.FileOpertor import getDataMatrix

def getMapItermGO(bgPath,level=2):
    data=getDataMatrix(bgPath)[0]
    _mapIterm={}
    for i in range(len(data)):
        gos=data[i][1].split(';')
        goDescs=data[i][2].split(';')
        goLevels=data[i][3].split(';')
        for j in range(len(gos)):
            iterm=(gos[j]+'~'+goDescs[j])
            if goLevels[j]!='' and int(goLevels[j])==level:
                if _mapIterm.has_key(iterm):
                    _mapIterm[iterm].append(data[i][0])
                else:
                    _mapIterm[iterm]=[data[i][0]]
    return _mapIterm

def getMapItermCOG(bgPath):
    data=getDataMatrix(bgPath)[0]
    _mapIterm={}
    for i in range(len(data)):
        gos=data[i][4].split(';')
        for j in range(len(gos)):
            iterm=(gos[j])
            if iterm!='':
                if _mapIterm.has_key(iterm):
                    _mapIterm[iterm].append(data[i][0])
                else:
                    _mapIterm[iterm]=[data[i][0]]
    return _mapIterm

def getMapItermSubCellur(bgPath):
    data=getDataMatrix(bgPath)[0]
    _mapIterm={}
    for i in range(len(data)):
        gos=data[i][1]
        iterm=(gos)
        if iterm!='':
            if _mapIterm.has_key(iterm):
                _mapIterm[iterm].append(data[i][0])
            else:
                _mapIterm[iterm]=[data[i][0]]
    return _mapIterm

def outClassFuncionGO(_mapIterm,diffSet,outPath):
    f=open(outPath,'w')
    for iterm in _mapIterm:
        if iterm.find('GO')==0:
            upPro=[]
            for pro in set(_mapIterm[iterm]):
                if pro in diffSet:
                    upPro.append(pro)
            if len(upPro)>0:
                f.write(iterm[0:iterm.find('~')]+'\t'+iterm[iterm.find('~')+1:len(iterm)])
                f.write('\t'+str(len(upPro))+'\t'+';'.join(upPro)+'\n')
    f.close()
def outClassFuncionCOG(_mapIterm,diffSet,outPath):
    f=open(outPath,'w')
    for iterm in _mapIterm:
        if iterm.find('[')==0:
            upPro=[]
            for pro in set(_mapIterm[iterm]):
                if pro in diffSet:
                    upPro.append(pro)
            if len(upPro)>0:
                f.write(iterm[1:iterm.find(']')]+'\t'+iterm[iterm.find(']')+1:len(iterm)].rstrip().lstrip())
                f.write('\t'+str(len(upPro))+'\t'+';'.join(upPro)+'\n')
            else:
                f.write(iterm[1:iterm.find(']')]+'\t'+iterm[iterm.find(']')+1:len(iterm)].rstrip().lstrip())
                f.write('\t0\t\n')
    f.close()
def outClassFuncionSubCelur(_mapIterm,diffSet,outPath):
    f=open(outPath,'w')
    for iterm in _mapIterm:
        if iterm!='':
            upPro=[]
            for pro in set(_mapIterm[iterm]):
                if pro in diffSet:
                    upPro.append(pro)
            if len(upPro)>0:
                f.write(iterm.rstrip().lstrip())
                f.write('\t'+str(len(upPro))+'\t'+';'.join(upPro)+'\n')
    f.close()
if __name__ == '__main__':
    pass