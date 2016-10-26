# -*- coding:utf-8 -*-
'''
Created on 2016-5-20

@author: Administrator
'''
import json

from com.zlf.beans.Global import _oboPath, _idMappingPath


_map={}

class Go:  
    id = ''
    alt_ids=None
    name=''
    namespace=''
    __parent=None
    level=-1  
    def __init__(self,_id):  
        self.id = _id  
    def parseParent(self,is_as):
        self.__parent=[]
        for isa in is_as:
            _go=isa[isa.find('GO'):isa.find('GO')+10]
            if _map.has_key(_go):
                pass
            else:
                cGo=Go(_go)
                _map[_go]=cGo
            self.__parent.append(_go)
                
    def getLevel(self):
        _min=100000
        if len(self.__parent)==0:
            return 1;
        for g in self.__parent:
            if _min>_map[g].getLevel():
                _min=_map[g].getLevel()
#                 print g+'-----'+str(_min)
        return _min+1
    
    def getAllParent(self):
        _prs=[self.id]
        if len(self.__parent)==0:
            return _prs;
        for g in self.__parent:
            _prs=_prs+_map[g].getAllParent()
        rp=set(_prs)
        _prs=[]
        for r in rp:
            _prs.append(r)
        return _prs     

def parseGO(_goText):
    _id=None
    _name=''
    _namespace=''
    _is_as=[]
    _alt_ids=[]
    for _txt in _goText:
        if _txt.find('id:')==0:
            _id=_txt[_txt.find('GO'):_txt.find('GO')+10]
        elif _txt.find('name:')==0:
            _name=_txt[5:len(_txt)].rstrip().lstrip()
        elif _txt.find('namespace:')==0:
            _namespace=_txt[10:len(_txt)].rstrip().lstrip()
        elif _txt.find('alt_id:')==0:
            _alt_ids.append(_txt[_txt.find('GO'):_txt.find('GO')+10]) 
        elif _txt.find('is_a:')==0 or _txt.find('relationship:')==0:
            _is_as.append(_txt) 
    if _id:
        _go=None
        if _map.has_key(_id):
            _go=_map[_id]
        else:
            _go=Go(_id)   
        _go.name=_name
        _go.namespace=_namespace   
        _go.parseParent(_is_as)
        _go.alt_ids=_alt_ids
        _map[_id]=_go
        if len(_alt_ids)>0:
            for _alt in _alt_ids:
                _map[_alt]=_go        

def parserObO():
    f=open(_oboPath,'r')
    line=f.readline()
    flag=False
    _goText=[]
    while line:
        line=line.rstrip().lstrip('\n')
        if flag:
            if line=='':
                parseGO(_goText)
                _goText=[]
                flag=False
            else:
                _goText.append(line)
        if line.find('[Term]')==0:
            flag=True
        line=f.readline()
    f.close()
    
#proteinList is Set 
#return {}   
#ע�͵�����GO�У�������ipr�ģ�merge��ʾ�ϲ����ν��
def annotationGO(proteinList,iprPath=None,merge=None,ind=13):
    _mapping={}
    if iprPath:
        if merge:
            _mapping1=idMapping2GO(proteinList)
            _mapping2=iprMapping2GO(proteinList,iprPath,ind)
            for key in proteinList:
                _all=[]
                if _mapping1.has_key(key):
                    _all=_mapping1[key]
                if _mapping2.has_key(key):
                    _all=_all+_mapping2[key]
                if len(_all):
                    _mapping[key]=_all    
        else:
            _mapping=iprMapping2GO(proteinList, iprPath,ind)
    else:
        _mapping=idMapping2GO(proteinList)
    return _mapping
    
#proteinList is Set  
#根据自定义的GOMapping进行解析  
def iprMapping2GO(proteinList,iprPath,ind=13):
    f=open(iprPath,'r')
    lines=f.readlines()
    f.close()
    _mappings={}
    for line in lines:
        cols=line.lstrip('\n').split('\t')
        if not proteinList or cols[0] in proteinList:
            if len(cols)>ind:
                if _mappings.has_key(cols[0]):
                    if cols[ind].find('|')>-1:
                        _mappings[cols[0]]=_mappings[cols[0]]+cols[ind].split('|')
                    elif cols[ind].find(';')>-1:
                        _mappings[cols[0]]=_mappings[cols[0]]+cols[ind].split(';')
                    elif cols[ind].rstrip().lstrip()!='':
                        _mappings[cols[0]]=_mappings[cols[0]]+[cols[ind]]
                else:
                    if cols[ind].find('|')>-1:
                        _mappings[cols[0]]=cols[ind].split('|')
                    elif cols[ind].find(';')>-1:
                        _mappings[cols[0]]=cols[ind].split('|')
                    elif cols[ind].rstrip().lstrip()!='':
                        _mappings[cols[0]]=[cols[ind].rstrip().lstrip()]
                        
    return _mappings
    
#proteinList is Set    
def idMapping2GO(proteinList):
    f=open(_idMappingPath,'r')
    lines=f.readlines(100000)
    _mappings={}
    while lines:
        for line in lines:
            cols=line.rstrip().lstrip('\n').split('\t')
            if cols[0] in proteinList:
                _mappings[cols[0]]=cols[1].split(';')
        lines=f.readlines(100000)
    f.close()
    return _mappings;

#_mapping={}
#_map={}
#return {}
def format2GO(_mapping,_map):
    _mappingGO={}
    for key in _mapping:
        _list=[]
        for gos in _mapping[key]:
            gos=gos.lstrip().rstrip()
            if gos.find('GO')==0:
                _list.append(gos[0:10])
        _list1=[]
        for gos in set(_list):
            _list1=_list1+list(_map[gos].getAllParent())
        _list=[]
        for go in set(_list1):
            _list.append(_map[go])
        _mappingGO[key]=_list
    return _mappingGO
 
def go2Dist(_go):
    return {
            'id':_go.id,
            'name':_go.name,
            'namespace':_go.namespace,
            'parents':_go.getAllParent(),
            'level':_go.getLevel()            
            } 
def outGOJson(outPath,_mapping):
    f=open(outPath,'w')
#     f.write(json_dumps(aot,default=go2Dist))
    f.close()
def readGOJson(inPath):
    f=file(inPath)
    data = json.load(f)    
    f.close()
    return data

def writeGOAnnotation(outPath,_mapping):
    fw=open(outPath,'w')
    for key in _mapping:
        fw.write(key)
        fw.write('\t')
        for _go in _mapping[key]:
            pass
    
    fw.close()

def getLeafs(_set):
    parserObO()
    _parents=[]
    for _id in _set:
        parent=set(_map[_id].getAllParent())
        parent.remove(_id)    
        _parents=_parents+list(parent)
    _list=[]
    for _id in _set:
        if _id not in set(_parents):
            _list.append(_id)
    return _list
    
#step1:annotationGO
#step2:parserObO init onlyOne
#step3:format2GO
#step4:outJson
#step4:writeGOAnnotation
           
        
if __name__ == '__main__':
#     parserObO()
#     pros=['Q9QXE0']
#     _mapping=annotationGO(set(pros))
#     print _mapping['Q9QXE0']
#     aot=(format2GO(_mapping, _map))
#     for go in aot['Q9QXE0']:
#         print go.id
#         print '---'+go.namespace
#     print _map['GO:0001561'].id
#     print aot
#     outGOJson('E:/Work/MH/BgData/go.json', aot)
#     readGOJson('E:/Work/MH/BgData/go.json')
    
    print getLeafs(set(['GO:0008202','GO:0042445','GO:0006629']))
#     print json_dumps(aot,default=go2Dist)
#     _go=_map['GO:0044700']
#     print _go.getAllParent()
#     print _go.namespace
#     a = [1,3,5,7]
#     b = [1,3,4,6,8]
#     print a+b
    
    
    