'''
Created on 2016-5-21

@author: Administrator
'''
from numpy.random.mtrand import np

from com.zlf.beans.Global import _funPath, _wogPath, _kogPath, _cogPath
from com.zlf.domain.utils.FastaOpertor import extractProteinID
from com.zlf.domain.utils.FileOpertor import getDataMatrix


def parseFun():
    f=open(_funPath,'r')
    line=f.readline()
    _funMap={}
    while line:
        line=line.rstrip().lstrip().lstrip('\n')
        if line.find('[')==0:
            _funMap[line[1:line.find(']')]]=line
        line=f.readline()
    f.close()
    return _funMap

def parseMapping(_all):
    _pro_ids=[]
    _header=_all[0][1:_all[0].find(']')]
    for line in _all:
        if line.find(':')==-1 and line.find('[')!=0:
            cols=line.split(' ')
            for col in cols:
                c=col.rstrip().lstrip()
                if c!='':
                    _pro_ids.append(col)  
    
    return {'ids':_pro_ids,'header':_header}

def parseMappingKog(_all):
    _pro_ids=[]
    _header=_all[0][1:_all[0].find(']')]
    for line in _all:
        if line.find(':')>-1 and line.find('[')!=0:
            cols=line.split(' ')
            for col in cols:
                c=col.rstrip().lstrip()
                if c!='' and c.find(':')==-1:
                    _pro_ids.append(col)  
    
    return {'ids':_pro_ids,'header':_header}

def parseWog():
    f=open(_wogPath,'r')
    line=f.readline();
    flag=False
    _all=[]
    _mapping={}
    while line:
        line=line.rstrip().lstrip('\n')
        if line.find('[')==0:
            flag=True
        elif line=='':
            _map=parseMapping(_all)
            _header=_map['header']
            for l in _map['ids']:
                for A in _header:
                    if A!='X' and _mapping.has_key(l):
                        _mapping[l].append(A)
                    elif A!='X':
                        _mapping[l]=[A] 
            _all=[]
            flag=False
        if flag:
            _all.append(line) 
        line=f.readline()
    f.close()
    return _mapping
def parseKOG(_path):
    f=open(_path,'r')
    line=f.readline()
    flag=False
    _all=[]
    _mapping={}
    while line:
        line=line.rstrip().lstrip('\n')
        if line.find('[')==0:
            flag=True
        elif line=='':
            _map=parseMappingKog(_all)
            _header=_map['header']
            for l in _map['ids']:
                for A in _header:
                    if A!='X' and _mapping.has_key(l):
                        _mapping[l].append(A)
                    elif A!='X':
                        _mapping[l]=[A] 
            _all=[]
            flag=False 
        if flag:
            _all.append(line)
        line=f.readline()
    f.close()
    return _mapping

def getMappingForKOG():
    _mapping1=parseWog()
    _mapping2=parseKOG(_kogPath)
    for key in _mapping1:
        if _mapping2.has_key(key):
            _mapping2[key]=list(set(_mapping2[key]+_mapping1[key]))
        else:
            _mapping2[key]=_mapping1[key]
    return _mapping2

def getMappingForCOG():
    return parseKOG(_cogPath)

def parseBlastByM8(_path,outPath):
    matrix=getDataMatrix(_path)[0];
    _map={}
    for cols in matrix:
        key=extractProteinID(cols[0])
        if _map.has_key(key):
            if _map[key][1]<float(cols[2]):
                _map[key]=(extractProteinID(cols[1]),float(cols[2]))
        else:
            _map[key]=(extractProteinID(cols[1]),float(cols[2]))
    if outPath:
        f=open(outPath,'w')
        for key in _map:
            f.write(key+"\t"+_map[key][0]+'\t'+str(_map[key][1])+'\n')
        f.close()
    return _map;  

def parseM8(m8Path):
    mapp=np.loadtxt(m8Path,dtype=np.str)[:,(0,1,2)]
    _map={}
    for m in mapp:
        score=float(m[2])
        if score>0.4:
            if _map.has_key(m[0]):
                if score>_map[m[0]]['score']:
                    _map[m[0]]={'pro':m[1],'score':score}
            else:
                _map[m[0]]={'pro':m[1],'score':score}
#     print _map
    return _map

def writeCOGClassAnnotation(_m8Map,outPath,kog=None):
    _mapping={}
    if kog:
        _mapping=getMappingForKOG()
    else:
        _mapping=getMappingForCOG()
    _funMap=parseFun()
    fw=open(outPath,'w')
    for key in _m8Map:
        if _mapping.has_key(_m8Map[key]['pro']):
            fw.write(key+'\t'+_m8Map[key]['pro']+'\t'+str(_m8Map[key]['score']))
            line=''
            line1=''
            for A in _mapping[_m8Map[key]['pro']]:
                line=line+_funMap[A]+';'
                line1=line1+A
            fw.write('\t'+line1+'\t'+line+'\n')
    fw.close()
def writeCOGClassAnnotationByKeys(_proteinSet,_m8Map,outPath,kog=None):
    _mapping={}
    if kog=='kog':
        _mapping=getMappingForKOG()
    else:
        _mapping=getMappingForCOG()
    _funMap=parseFun()
    fw=open(outPath,'w')
    for key in _m8Map:
        if _mapping.has_key(_m8Map[key]['pro']) and key in _proteinSet:
            fw.write(key+'\t'+_m8Map[key]['pro']+'\t'+str(_m8Map[key]['score']))
            line=''
            line1=''
            for A in _mapping[_m8Map[key]['pro']]:
                line=line+_funMap[A]+';'
                line1=line1+A
            fw.write('\t'+line1+'\t'+line+'\n')
    fw.close()
    
    
#setp1:parseM8
#step2:writeCOGClassAnnotation

if __name__ == '__main__':
#     print len(parseWog())
#     print len(getMappingForKOG())
#     print len(getMappingForCOG())
    folder='E:/Work/MH/BgData'
    writeCOGClassAnnotation(parseM8(folder+'/seq.m8'), folder+'/Cog.tab', 'kog')
    
    
