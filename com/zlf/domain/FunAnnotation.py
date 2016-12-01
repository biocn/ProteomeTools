# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��11��22��

@author: Administrator
'''
from com.zlf.domain.BlastM8Parse import getMappingForKOG, getMappingForCOG, \
    parseFun, parseM8, parseBlastByM8
from com.zlf.domain.GoOpertor import annotationGO, parserObO, format2GO, _map
from com.zlf.domain.KeggOpertor import proteinMappingPathway, getKoMap
from com.zlf.domain.net.KAAS import getQueryKO
from com.zlf.domain.utils.FastaOpertor import extractProteinID
from com.zlf.domain.utils.FileOpertor import getDataMatrix, getMapByData


def getGOLine(_gos):
    ids=''
    names=''
    levels=''
    for _go in _gos:
        ids=ids+_go.id+';'
        names=names+_go.name+';'
        levels=levels+str(_go.getLevel())+';'
    return ids+'\t'+names+'\t'+levels

def goAnnotation(_list,folder,iprPath=None, merge=None):
    _mapping=annotationGO(set(_list),iprPath, merge)
    parserObO()
    allProMap=format2GO(_mapping, _map)
    fBP=open(folder+'/BP_GOs.txt','w')
    fCC=open(folder+'/CC_GOs.txt','w')
    fMF=open(folder+'/MF_GOs.txt','w')
    for key in allProMap:
        _gos=allProMap[key]
        bp=[]
        cc=[]
        mf=[]
        for _go in _gos:
            if _go.namespace=='biological_process':
                bp.append(_go)
            elif _go.namespace=='molecular_function':
                mf.append(_go)
            elif _go.namespace=='cellular_component':
                cc.append(_go)
        if len(bp)>0:
            fBP.write(key+'\t'+getGOLine(bp)+'\n')
        if len(cc)>0:
            fCC.write(key+'\t'+getGOLine(cc)+'\n')
        if len(mf)>0:
            fMF.write(key+'\t'+getGOLine(mf)+'\n')
    fBP.close()
    fCC.close()
    fMF.close()

def keggAnnotation(folder,_proteinlist,osas='hsa,mmu'):
    if getQueryKO(folder,-1):
        print 'getQueryKO successful'
        f=open(folder+'/query.ko','r')
        lines=f.readlines()
        f.close()
        _list=[]
        _set=set(_proteinlist)
        for line in lines:
            cols=line.rstrip().lstrip('\n').split('\t')
            if len(cols)>1 and cols[1].find('K')==0 and cols[0] in _set:
                _list.append(cols)
        proteinMappingPathway(_list, getKoMap(), folder+'/KEGG_Paths.txt', osas) 
    else:
        print 'please try again leter'

def cogAnnotation(blastM8Path,proteinList,folder,kog):
    parseBlastByM8(blastM8Path,blastM8Path+'.clear.id')
    _mapping={}
    if kog=='kog':
        _mapping=getMappingForKOG()
    else:
        _mapping=getMappingForCOG()
    _funMap=parseFun()
    _m8Map=parseM8(blastM8Path+'.clear.id')
    fw=open(folder+'/COG_ClassFuns.txt','w')
    for key in _m8Map:
        if _mapping.has_key(_m8Map[key]['pro']) and key in set(proteinList):
            fw.write(key+'\t'+_m8Map[key]['pro']+'\t'+str(_m8Map[key]['score']))
            line=''
            line1=''
            for A in _mapping[_m8Map[key]['pro']]:
                line=line+_funMap[A]+';'
                line1=line1+A
            fw.write('\t'+line1+'\t'+line+'\n')
    fw.close()
    

def domainAnnotation(iprPath,folder,proteinList):
    data=getDataMatrix(iprPath)
    _map={}
    for cols in data[0]:
        key=extractProteinID(cols[0])
        if key in set(proteinList):
            if _map.has_key(key):
                _map[key].append(cols)
            else:
                _map[key]=[cols]
    fw=open(folder+'/Ipr_Domains.txt','w')
    for key in _map:
        iprs=''
        iprsDesc=''
        _list=[]
        for pro in _map[key]:
            if len(pro)>12 and pro[11]!='':
                _list.append(pro[11]+'~'+pro[12])
        if len(_list)>0:
            for l in list(set(_list)):
                iprs=iprs+l[0:l.find('~')]+';'
                iprsDesc=iprsDesc+l[l.find('~')+1:len(l)]+';'
        if iprs!='' and iprsDesc!='':
            fw.write(key+'\t'+iprs+'\t'+iprsDesc+'\n')
    fw.close()

def subCellurAnnotation(folder,_proteinList,subPath):
    f=open(subPath,'r')
    lines=f.readlines()
    f.close()
    _map={}
    for line in lines:
        cols=line.rstrip().lstrip('\n').split('\t')
        if len(cols)>1:
            _map[extractProteinID(cols[0])]=cols[1]
    _set=set(_proteinList)
    fw=open(folder+'/SubCellur_loactions.txt','w')
    for p in _map:
        if p in _set:
            fw.write(p+'\t'+_map[p]+'\n')
    fw.close()

def getAnnotationMap(_path):
    f=open(_path,'r')
    lines=f.readlines()
    f.close()
    _map={}
    for line in lines:
        cols=line.rstrip().lstrip('\n').split('\t')
        if len(cols)>1 and cols[1].rstrip().lstrip()!='':
            _map[cols[0]]=cols[1:len(cols)]
    return _map

def mergeRegulatedAnnation(combineAnnoPath,keys,outPath):
    _list=getDataMatrix(combineAnnoPath)[0]
    fw=open(outPath,'w')
    fw.write('\t'.join(_list[0])+'\n')
    _map=getMapByData(_list, 0, True)
    for key in keys:
        fw.write('\t'.join(_map[key])+'\n')
    fw.close()
    
def mergeAnnotation(folder,keyPath,outPath):
    _mapGO_BP=getAnnotationMap(folder+'/BP_GOs.txt')
    _mapGO_CC=getAnnotationMap(folder+'/CC_GOs.txt')
    _mapGO_MF=getAnnotationMap(folder+'/MF_GOs.txt')
    _mapDomain=getAnnotationMap(folder+'/Ipr_Domains.txt')
    _mapKEGG=getAnnotationMap(folder+'/KEGG_Paths.txt')
    _mapSubcelur=getAnnotationMap(folder+'/SubCellur_loactions.txt')
    _mapCOG=getAnnotationMap(folder+'/COG_ClassFuns.txt')
    f=open(keyPath,'r')
    fw=open(outPath,'w')
    line=f.readline()
    fw.write(line.rstrip().lstrip('\n'))
    fw.write('\tBP_GO_ID\tBP_GO_Desc\tBP_GO_Level')
    fw.write('\tCC_GO_ID\tCC_GO_Desc\tCC_GO_Level')
    fw.write('\tMF_GO_ID\tMF_GO_Desc\tMF_GO_Level')
    fw.write('\tKEGG_KO\tKEGG_Pathway_ID\tKEGG_Pathway_Desc')
    fw.write('\tDomain_ID\tDomain_Desc')
    fw.write('\tSubcellurLocation')
    fw.write('\tCOG_Gene\tBlastScore\tCOG_Code\tCOG_Desc\n')
    
    line=f.readline()
    while line:
        line=line.rstrip().lstrip('\n')
        cols=line.split('\t')
        fw.write(line)
        if _mapGO_BP.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapGO_BP[cols[0]]))
        else:
            fw.write('\t\t\t')
        if _mapGO_CC.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapGO_CC[cols[0]]))
        else:
            fw.write('\t\t\t')
        if _mapGO_MF.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapGO_MF[cols[0]]))
        else:
            fw.write('\t\t\t')
        if _mapKEGG.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapKEGG[cols[0]]))
            if len(_mapKEGG[cols[0]])<3:
                fw.write('\t\t')
        else:
            fw.write('\t\t\t')
        if _mapDomain.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapDomain[cols[0]]))
        else:
            fw.write('\t\t')
        if _mapSubcelur.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapSubcelur[cols[0]]))
        else:
            fw.write('\t')
        if _mapCOG.has_key(cols[0]):
            fw.write('\t'+'\t'.join(_mapCOG[cols[0]])+'\n')
        else:
            fw.write('\t\t\t\t\n')
        line=f.readline()
    f.close()
    fw.close()

if __name__ == '__main__':
    pass