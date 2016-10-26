# -*- coding:utf-8 -*-
'''
Created on 2016-9-9

@author: Administrator
'''
from math import isnan

from numpy.core.numeric import nan
from pandas.core.frame import DataFrame
from scipy.stats.stats import ttest_1samp

from com.zlf.domain.utils.FastaOpertor import readFasta
import pandas as pd


#_path=psm.txt
#_path1=proteinGroup.txt
def readProteomeBySequst(_path,_path1,_quant):
    data=pd.read_table(_path,header=0,index_col=0,error_bad_lines=False)
    data=data[(data['Quan Usage']=='Used')]
    _rData={}
    _rData['pep_seq']=data['Sequence']
    _rData['mass_error']=data[['Delta Mass [PPM]','SpScore']].drop_duplicates(['Delta Mass [PPM]','SpScore'])
    _rData['pep_seq']=data['Sequence']
    _pepQuantMap={}
    for q in _quant:
        _pepQuantMap[q]=data[q]
    _rData['pep_ratio']=_pepQuantMap
    _map={}
    for i in range(len(data['Protein Group Accessions'])):
        key=data['Protein Group Accessions'][i]
        _ratios=[]
        for q in _quant:
            _ratios.append(data[q][i])
        if _map.has_key(key):
            _map[key].append(_ratios)
        else:
            _map[key]=[_ratios]
    data1=pd.read_table(_path1,header=0,index_col=-1,error_bad_lines=False)
    _protRatio={}
    for j in range(len(data1['Accession'])):
#         print data1['Accession'].iloc[j]
        key=data1['Accession'].iloc[j]
        _ratios=[]
        for i in range(len(_quant)):
            if not isnan(data1[_quant[i]].iloc[j]):
                _pepList=_map[key]
                _r=[]
                for pep in _pepList:
                    if not isnan(pep[i]):
                        _r.append(pep[i])
                if len(_r)>1:
                    p=ttest_1samp(_r,popmean=1)[1]
                else:
                    p=1
                _ratios.append((data1[_quant[i]].iloc[j],p))
            else:
                _ratios.append(('NA','NA'))
        _protRatio[key]=(data1['Description'].iloc[j],_ratios)
    _rData['prot_ratio']=_protRatio
    return _rData

def writeModifyProtExproAndStatistics(_rData,_quant,folder):
    _map=_rData['prot_ratio']
    _mapModify=statisticsModifyInProtein(folder)
    f=open(folder+'/ProteinExprossion.txt','w')
    f.write('Protein\tProteinName\tNo. of ModifySites')
    for q in _quant:
        f.write('\t'+q.replace('/','-vs-')+'\t'+q.replace('/','-vs-')+'-p')
    f.write('\n')
    for key in _map:
        if _mapModify.has_key(key):
            f.write(key)
            _exproMap=_map[key]
            f.write('\t'+_exproMap[0])
            f.write('\t'+str(_mapModify[key]))
            for i in range(len(_quant)):
                f.write('\t'+str(_exproMap[1][i][0])+'\t'+str(_exproMap[1][i][1]))
            f.write('\n')
    f.close()

def writeProtExpro(_rData,_quant,folder):
    _map=_rData['prot_ratio']
    f=open(folder+'/ProteinExprossion.txt','w')
    f.write('Protein\tProteinName')
    for q in _quant:
        f.write('\t'+q.replace('/','-vs-')+'\t'+q.replace('/','-vs-')+'-p')
    f.write('\n')
    for key in _map:
        f.write(key)
        _exproMap=_map[key]
        f.write('\t'+_exproMap[0])
        for i in range(len(_quant)):
            f.write('\t'+str(_exproMap[1][i][0])+'\t'+str(_exproMap[1][i][1]))
        f.write('\n')
    f.close()

def readModifyBySequst(_path,modi,fasta,_quant):
    data=pd.read_table(_path,header=0,index_col=0,error_bad_lines=False)
#     data=data[(data['Quan Info']=='Unique')|(data['Quan Info']=='No Quan Values')|(data['Quan Info']=='Not Unique')|(data['Quan Info']=='Inconsistently Labeled')]
    _rData={}
    _rData['pep_seq']=data['Sequence']
    _rData['mass_error']=data[['Delta Mass [PPM]','SpScore']]
    _pepQuantMap={}
    for q in _quant:
        _pepQuantMap[q]=data[q]
    _rData['pep_ratio']=_pepQuantMap
    _modifyProteins={}
    for i in range(len(data['Sequence'])):
        ratios=[]
        for q in _quant:
            if data['Quan Usage'][i]=='Used':
                ratios.append(data[q][i])
            else:
                ratios.append(nan)
        modis=data['Modifications'][i].split(';')
        _mInds=[]
        for mod in modis:
            mod=mod.rstrip(' ').lstrip(' ')
            if mod.upper().find('('+modi.upper()+')')>-1:
                _mInds.append(int(mod[1:mod.upper().find('('+modi.upper()+')')]))
        seq=data['Sequence'][i].upper()
        if len(_mInds)>0 and str(data['Protein Group Accessions'][i])!='nan':
            protein=data['Protein Group Accessions'][i].split(';')[0].rstrip(' ').lstrip(' ')
            proteinDesc=data['Protein Descriptions'][i].split(';')[0].rstrip(' ').lstrip(' ')
            cnum=fasta[protein].count(seq)
            if cnum==1:
                basInd=fasta[protein].rstrip(' ').lstrip(' ').find(seq)
                for l in _mInds:
                    key=protein+'-'+str(basInd+l)
                    if _modifyProteins.has_key(key):
                        _modifyProteins[key].append((proteinDesc,seq,ratios))
                    else:
                        _modifyProteins[key]=[(proteinDesc,seq,ratios)]
            elif cnum>1:
                s=fasta[protein].rstrip(' ').lstrip(' ')
                inds=[]
                for f in range(cnum):
                    ind=s.find(seq)
                    s=s[ind+1:len(s)]
                    if f==0:
                        inds.append(ind)
                    else:
                        inds.append(ind+inds[f-1]+1)
                for l in _mInds:
                    key=protein+'-'
                    for ind in inds:
                        key=key+str(ind+l)+','
                    if _modifyProteins.has_key(key):
                        _modifyProteins[key].append((proteinDesc,seq,ratios))
                    else:
                        _modifyProteins[key]=[(proteinDesc,seq,ratios)]
    _modifyPepQuant={}
    for key in _modifyProteins:
        _qs=[]
        for m in range(len(_quant)):
            _q1=[]
            for c in _modifyProteins[key]:
                if not isnan(c[2][m]):
                    _q1.append(c[2][m])
            if len(_q1)>0:
                dt=DataFrame(_q1)
                ratio=dt.median()
                _qs.append(ratio[0])
            else:
                _qs.append('NA')
        _modifyPepQuant[key]=(_modifyProteins[key][0][0],_modifyProteins[key][0][1],_qs)    
    _rData['modifyPepQuant']=_modifyPepQuant
    return _rData
def writeMassError(_rData,folder):
    _map=_rData['mass_error']
    f=open(folder+'/MassError.txt','w')
    f.write('Delta Mass [PPM]\tSpScore\n')
    for i in range(len(_map['Delta Mass [PPM]'])):
        f.write(str(_map.iloc[i][0])+'\t'+str(_map.iloc[i][1])+'\n')
    f.close()

def writeModifyProtExpro(_rData,_quant,folder):
    _map=_rData['modifyPepQuant']
    f=open(folder+'/ModifyPeptideExprossion.txt','w')
    f.write('Protein\tProteinName\tSite\tpepSeq')
    for q in _quant:
        f.write('\t'+q.replace('/','-vs-'))
    f.write('\n')
    for key in _map:
        f.write(key[0:key.find('-')]+'\t'+_map[key][0]+'\t'+key[key.find('-')+1:len(key)]+'\t'+_map[key][1])
        for q in _map[key][2]:
            f.write('\t'+str(q))
        f.write('\n')
    f.close()
def writePepSeq(_rData,folder):
    f=open(folder+'/PeptideSeq.txt','w')
    f.write('seq\tseq_length\n')
    for r in set(_rData['pep_seq']):
        try:
            f.write(str(r)+'\t'+str(len(r))+'\n')
        except:
            pass
    f.close()

def writePepRatio(_rData,_quant,folder):
    _map=_rData['pep_ratio']
    for q in _quant:
        if _map.has_key(q):
            f=open(folder+'/'+q.replace('/','-vs-')+'.pepRatio','w')
            f.write('Ratio\n')
            for r in _map[q]:
                if r!='---' and r!='###' and float(r)>0 and float(r)<30:
                    f.write(str(r)+'\n')
            f.close()
            
def parseQuantDiffNotP(_quant,folder):
    data=pd.read_table(folder+'/ModifyPeptideExprossion.txt',header=0)
    _set=set(_quant)
    f=open(folder+'/diffStatistics.txt','w')
    f.write('Samples\tUP2\tDown2\tUP1.5\tDown1.5\tUP1.3\tDown1.3\tUP1.2\tDown1.2\n')
    for q in _quant:
        lev=q.replace('/','-vs-')
        Up1205=data.loc[(data[lev]>1.2),['Protein']]
        Dwon1205=data.loc[(data[lev]<1/1.2),['Protein']]
        Up1305=data.loc[(data[lev]>1.3),['Protein']]
        Dwon1305=data.loc[(data[lev]<1/1.3),['Protein']]
        Up1505=data.loc[(data[lev]>1.5),['Protein']]
        Dwon1505=data.loc[(data[lev]<1/1.5),['Protein']]
        Up205=data.loc[(data[lev]>2),['Protein']]  
        Dwon205=data.loc[(data[lev]<1.0/2),['Protein']]
        
        _list=[len(Up205),len(Dwon205)
               ,len(Up1505),len(Dwon1505)
               ,len(Up1305),len(Dwon1305)
               ,len(Up1205),len(Dwon1205)]
        _list1=[len(Up205.drop_duplicates()),len(Dwon205.drop_duplicates())
               ,len(Up1505.drop_duplicates()),len(Dwon1505.drop_duplicates())
               ,len(Up1305.drop_duplicates()),len(Dwon1305.drop_duplicates())
               ,len(Up1205.drop_duplicates()),len(Dwon1205.drop_duplicates())]
        f.write(lev)
        for l in range(len(_list)):
            f.write('\t'+str(_list[l])+'('+str(_list1[l])+')')
        f.write('\n')
    f.close()

def statisticsModifyInProtein(folder):
    data=pd.read_table(folder+'/ModifyPeptideExprossion.txt',index_col=0,header=0)
    protein=data.groupby(level=0)
#     fw=open(folder+'/StatisticsModify.txt','w')
#     fw.write('Protein\tNo. of ModiSites\n')
    _mapProtein={}
    for pro in protein.groups:
        group=protein.get_group(pro)
        _mapProtein[pro]=len(group)
#         fw.write(pro+'\t'+str(len(group))+'\n')
#     fw.close()
    return _mapProtein
    
def processSummary(folder,modi,_path,proteinPath,quant,fastaPath):
    print '---------Reading data---------'
    _rData=readModifyBySequst(_path,modi,readFasta(fastaPath),quant)
    print '---------Read data successful---------'
    writePepRatio(_rData, quant, folder)
    print '---------Write pepRatio successful---------'
    writePepSeq(_rData, folder)
    print '---------Write pepSeq successful---------'
    writeModifyProtExpro(_rData, quant, folder)
    print '---------Write protein expro successful---------'
    writeMassError(_rData, folder)
    print '---------Write mass error successful---------'
    parseQuantDiffNotP(quant,folder)
    print '---------Write protein diffstatistics successful---------'
    _rData1=readProteomeBySequst(_path, proteinPath, quant)    
    writeModifyProtExproAndStatistics(_rData1, quant, folder)
    print '---------write protein modify statistics successful------'

def processSummaryProtein(folder,_path1,_path2,quant):
    print '---------Reading data---------'
    _rData=readProteomeBySequst(_path1, _path2, quant)
    print '---------Read data successful---------'
    writePepRatio(_rData, quant, folder)
    print '---------Write pepRatio successful---------'
    writePepSeq(_rData, folder)
    print '---------Write pepSeq successful---------'
    writeProtExpro(_rData, quant, folder)
    print '---------Write protein expro successful---------'
    writeMassError(_rData, folder)
    print '---------Write mass error successful---------'
    #parseQuantDiff(quant,folder)
    #print '---------Write protein diffstatistics successful---------'
    

if __name__ == '__main__':
    folder='E:/Work/MH/MH-B16072001/SearchResult/Phos'
    _quant=['Heavy/Light','Light/Heavy']
#     Phospho,Acetyl
#     processSummaryProtein(folder, folder+'/SILAC_psms.txt', folder+'/SILAC_proteingroups.txt', _quant)
#     _rData=processSummary(folder,'Acetyl',folder+'/Ac_SILAC_psms.txt',_quant,folder+'/../uniprot-all.fasta')
    _rData=readProteomeBySequst(folder+'/Ph_SILAC_psms.txt', folder+'/Ph_SILAC_proteingroups.txt', _quant)    
    print '---------write protein modify statistics successful------'
    writeModifyProtExproAndStatistics(_rData, _quant, folder)
    
    
    
    
    


