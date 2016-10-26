# -*- coding:utf-8 -*- 
'''��
Created on 2016-8-3

@author: Administrator
'''
import os

from com.zlf.domain.utils.FisherTest import fisherTestPvalue
from com.zlf.domain.KeggOpertor import proteinMappingPathway, getKoMap, \
    getKEGGPathData, plotPathway
import pandas as pd


#获取带-的修饰位点中的蛋白ID
def getKeyAndSite(_path,header=None):
    f=open(_path,'r')
    if header:
        f.readline()
    line=f.readline()
    _list=[]
    while line:
        cols=line.rstrip().lstrip('\n').split('\t')
        cols[0]=cols[0].rstrip('"').lstrip('"').rstrip().lstrip()
        _list.append(cols[0][0:cols[0].find('-')])
        line=f.readline()
    f.close()
    return _list

#获取ID
def getKey(_path,header=None):
    f=open(_path,'r')
    if header:
        f.readline()
    line=f.readline()
    _list=[]
    while line:
        cols=line.rstrip().lstrip('\n').split('\t')
        _list.append(cols[0])
        line=f.readline()
    f.close()
    return _list

#获取背景的数据，    
def getBackGround(_path,header=True,ind=None):
    f=open(_path,'r')
    if header:
        f.readline()
    line=f.readline()
    _map={}
    while line:
        cols=line.rstrip().lstrip('\n').split('\t')
        if ind and len(cols)>ind:
            terms=cols[ind].split(';')
            for t in terms:
                if t.rstrip().lstrip()!='':
                    if _map.has_key(cols[0]):
                        _map[cols[0]].append(t)
                    else:
                        _map[cols[0]]=[t]
        else:
            _map[cols[0]]=[]
        line=f.readline()
    f.close()
    return _map


    
#创建KEGG富集背景
def createKEGGBg(proteinList,folder,prot_koPath,osas):
    f=open(prot_koPath,'r')
    lines=f.readlines()
    _list=[]
    _set=set(proteinList)
    for line in lines:
        cols=line.rstrip().lstrip('\n').split('\t')
        if len(cols)>1 and cols[1].find('K')==0 and cols[0] in _set:
            _list.append(cols)
    proteinMappingPathway(_list, getKoMap(), folder+'/KEGG_Paths.txt', osas) 
    
#创建Domain富集背景
def createDomainBgByIPR(proteinList,folder,iprPath):
    data=pd.read_table(iprPath,header=-1,index_col=0,error_bad_lines=False)
    protein=data.groupby(level=0)
    fw=open(folder+'/Ipr_Domains.txt','w')
    _allProtein=set(proteinList)
    for pro in protein.groups:
        if pro in _allProtein:
            group=protein.get_group(pro)
            dt=group.loc[group[11]>0,[11,12]]
            iprs=''
            iprsDesc=''
            for i in range(len(dt[11])):
                iprs=iprs+dt.iloc[i][11]+';'
                iprsDesc=iprsDesc+dt.iloc[i][12]+';'
            fw.write(pro+'\t'+iprs+'\t'+iprsDesc+'\n')
    fw.close()


#创建Domain富集背景
def createDomainBg(proteinList,folder,_path,header=True):
    f=open(_path,'r')
    if header:
        f.readline()
    line=f.readline()
    _map={}
    while line:
        cols=line.rstrip().lstrip('\n').split('\t')
        _listID=[]
        _listDesc=[]
        if len(cols)>1:
            _listID=cols[1].split(';')
            _listDesc=cols[2].split(';')
        if _map.has_key(cols[0]):
            _map[cols[0]][0].extend(_listID)
            _map[cols[0]][1].extend(_listDesc)
        else:
            _map[cols[0]]=[_listID,_listDesc]
        line=f.readline()
    fw=open(folder+'/Ipr_Domains.txt','w')
    _allProtein=set(proteinList)
    for pro in _map:
        if pro in _allProtein:
            group=_map[pro]
            fw.write(pro+'\t'+';'.join(group[0])+'\t'+';'.join(group[1])+'\n')
    fw.close()
    
def writeCategory(_frame,outPath):
    fw=open(outPath,'w')
    fw1=open(outPath+'.tmp','w')
    for i in _frame.index:
        if _frame['FisherExact'][i]<0.05:
            fw.write(_frame['Category'][i][0:_frame['Category'][i].find('~')]+'\t'+_frame['Category'][i][_frame['Category'][i].find('~')+1:len(_frame['Category'][i])]
                     +'\t'+str(_frame['Mapping'][i])+'\t'+str(_frame['Background'][i])+'\t')
            fw.write(str(_frame['AllMapping'][i])+'\t'+str(_frame['AllBackground'][i])+'\t'+str(_frame['FoldEnrichment'][i])+'\t')
            fw.write(str(_frame['FisherExact'][i])+'\t'+str(_frame['MappingProteinIDs'][i])+'\n')
        fw1.write(_frame['Category'][i][0:_frame['Category'][i].find('~')]+'\t'+_frame['Category'][i][_frame['Category'][i].find('~')+1:len(_frame['Category'][i])]
                     +'\t'+str(_frame['Mapping'][i])+'\t'+str(_frame['Background'][i])+'\t')
        fw1.write(str(_frame['AllMapping'][i])+'\t'+str(_frame['AllBackground'][i])+'\t'+str(_frame['FoldEnrichment'][i])+'\t')
        fw1.write(str(_frame['FisherExact'][i])+'\t'+str(_frame['MappingProteinIDs'][i])+'\n')
    fw.close()
    fw1.close()
    
    
    
def KEGGEnrichment(genesUp,genesDown,folder,outFolder,full=1):
    kpdt=getKEGGPathData(folder)
    _mapIterm=kpdt['iterms']
    dataLength=kpdt['Num']
    data=kpdt['data']
    allMappingAll=0
    allMappingUp=0
    allMappingDown=0
    _colorMap={}
    _setUP=set(genesUp)
    _setDown=set(genesDown)
    for pro in range(len(data[0])):
        if data[0][pro] in _setUP:
            allMappingUp=allMappingUp+1
            allMappingAll=allMappingAll+1
            _colorMap[data[1][pro]]='red'
        elif data[0][pro] in _setDown:
            allMappingAll=allMappingAll+1
            allMappingDown=allMappingDown+1
            _colorMap[data[1][pro]]='green'
        else:
            _colorMap[data[1][pro]]='blue'
    upFrame=getDataFrame(_mapIterm, _setUP, dataLength, allMappingUp, full)
    downFrame=getDataFrame(_mapIterm, _setDown, dataLength, allMappingDown, full)
    allFrame=getDataFrame(_mapIterm, _setUP | _setDown, dataLength, allMappingAll, full)
    try:
        os.makedirs(outFolder)
    except:
        pass
    writeCategory(upFrame.sort_values(['FisherExact']),outFolder+'/Up_KEGG_Enrich.txt')
    writeCategory(downFrame.sort_values(['FisherExact']),outFolder+'/Down_KEGG_Enrich.txt')
    writeCategory(allFrame.sort_values(['FisherExact']),outFolder+'/All_KEGG_Enrich.txt')
    plotPathway(upFrame, _colorMap, outFolder+'/UP_Regulated')
    plotPathway(downFrame, _colorMap, outFolder+'/Down_Regulated')
    plotPathway(allFrame, _colorMap, outFolder+'/All_Regulated')

def getDataFrame(_mapIterm,_set,dataLength,allMapping,full):
    bg=[]
    bgDtail=[]
    allBg=[]
    mpUp=[]
    mpDtailUp=[]
    allMpUp=[]
    fts=[]
    fes=[]
    its=[]
    
    for key in _mapIterm:
        upPro=[]
        for pro in set(_mapIterm[key]):
            if pro in _set:
                upPro.append(pro)
        if len(upPro)>1:
            ft=fisherTestPvalue([len(upPro),len(set(_mapIterm[key])),allMapping,dataLength], full)
            fe=1.0*len(upPro)*dataLength/(len(set(_mapIterm[key]))*allMapping)
            if key.rstrip().lstrip()!='~':
                bg.append(len(set(_mapIterm[key])))
                bgDtail.append(';'.join(_mapIterm[key]))
                allBg.append(dataLength)
                mpUp.append(len(upPro))
                mpDtailUp.append(';'.join(upPro))
                allMpUp.append(allMapping)
                fts.append(ft)
                fes.append(fe)
                its.append(key)
    return pd.DataFrame({
                  'Category':its,
                  'Mapping':mpUp,
                  'Background':bg,
                  'AllMapping':allMpUp,
                  'AllBackground':allBg,
                  'FoldEnrichment':fes,
                  'FisherExact':fts,
                  'IdentifyProteinIDs':bgDtail,
                  'MappingProteinIDs':mpDtailUp
                  })


def getKeyAndSites(_paths,header=True):
    _list=[]
    for _path in _paths:
        _list.extend(getKeyAndSite(_path, header))
    return _list    

if __name__ == '__main__':
    folder='E:/Work/MH/MH-B16072601/ClusterMethod3'
#     EnrichGO(folder)
#     EnrichKEGG(folder)    
#     _list=getKey(folder+'/allProtein.txt',True)
#     _keys1=getKey(folder+'/2Up.txt', True)
#     _keys2=getKey(folder+'/2Down.txt', True)
#     _keys1.extend(_keys2)
#     _keys=_keys1
#     GOEnrichment(_keys, folder+'/BP_GOs.txt', folder+'/2_BP_Enrich.txt', 0)
#     GOEnrichment(_keys, folder+'/CC_GOs.txt', folder+'/2_CC_Enrich.txt', 0)
#     GOEnrichment(_keys, folder+'/MF_GOs.txt', folder+'/2_MF_Enrich.txt', 0)
#     DomainEnrichment(folder, _keys, folder+'/1_Domain.txt', 0)    
#     KEGGEnrichment(_keys1, _keys2, folder, folder+'/2KEGG', 0)
#     createGOBg(_list, None,None,folder)
#     createKEGGBg(_list, folder, folder+'/protein2ko.txt', 'hsa')
#     createDomainBg(_list, folder, folder+'/domain.txt', True)
#     print len(set(_list))
#     createGOBg(_list,folder+'/PTM20140924MI01/PTM_report_data/Annotation/GO_annotation.xls', 2,folder)




