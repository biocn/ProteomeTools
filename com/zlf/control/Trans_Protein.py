# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��10��27��

@author: Administrator
转录组与蛋白组关联分析
准备条件：
1、关联的ID文件，分为两列，名字为trans_protein.txt
    第一列为蛋白ID，第二列为基因ID
2、蛋白表达谱文件
3、转录组差异表达文件及表达谱文件
步骤：
1、先合并转录组和蛋白组表达谱，根据trans_protein.txt，取交集
2、合并后对各个蛋白进行功能注释
3、安装上下调反式进行合并差异比较组，蛋白差异阈值可适当调整
4、对各个差异比较组进行富集分析
5、聚类分析
6、取上下调蛋白与转录组交集做聚类分析，找相关表达模式
7、富集分析
8、聚类
'''
from os.path import os

from com.zlf.beans.Global import _ReportRootPath
from com.zlf.control.TransProteinReport import writePjectInfo, writeWorkFlow, \
    writeUp2DownLink, writeClusterLink
from com.zlf.domain.ClassFunction import outClassFuncionGO, \
    getMapItermGO, getMapItermCOG, outClassFuncionCOG, getMapItermSubCellur, \
    outClassFuncionSubCelur
from com.zlf.domain.EnrichmentOpertor import GOEnrichment, getDataFrame, \
    writeCategory, KEGGEnrichment, DomainEnrichment, getEnrichmenResultData, \
    mergeEnrichmentResultData
from com.zlf.domain.FunAnnotation import goAnnotation, keggAnnotation, \
    domainAnnotation, cogAnnotation, subCellurAnnotation, mergeAnnotation, \
    mergeRegulatedAnnation
from com.zlf.domain.KeggOpertor import getKEGGPathData, plotPathway, \
    getKO2Protein
from com.zlf.domain.net.Cello import postCello
from com.zlf.domain.net.KAAS import postKAAS
from com.zlf.domain.net.REVIGO import postAndSaveR
from com.zlf.domain.report.ReportTemplate import getHtmlHeader, Nav, getNavHtml, \
    getHtmlFooter
from com.zlf.domain.utils.Blast import parseM8
from com.zlf.domain.utils.FastaOpertor import outFastaByKey, extractProteinID
from com.zlf.domain.utils.FileOpertor import getDataMatrix, getLines, \
    getCommonList, writeLines, writeMatrix, getLineDatas, mkdir, copyFile, \
    copyImage, copyFolder


#通过blast进行关联ID,去除ID重复
def formatTrans_protein(_path,folder):
    _map=parseM8(_path)
    fw=open(folder+'/trans_protein.txt','w')
    _map1={}
    for key in _map:
        if _map[key][1]>90:
            if not _map1.has_key(_map[key][0]) or (_map1.has_key(_map[key][0]) and _map1[_map[key][0]][1]<_map[key][2]):
                _map1[_map[key][0]]=(key,_map[key][2],_map[key][1])
    for key in _map1:
        fw.write(_map1[key][0]+'\t'+key+'\t'+str(_map1[key][2])+'\n')
    fw.close()

def getTransProteinMap(folder,rev=False):
    data1=getDataMatrix(folder+'/trans_protein.txt')
    _map={}
    for cols in data1[0]:
        if rev:
            _map[cols[1]]=cols[0]
        else:
            _map[cols[0]]=cols[1]
    return _map

#输出最终共同的蛋白序列
def writeBgFasta(folder,bgPath):
    matrix=getTransProteinMap(folder)
    outFastaByKey(set(list(matrix.iterkeys())), bgPath,folder+'/identify.fasta')


#格式化输出转录组和蛋白组表达数据以及合并两个表达谱数据
def formatProTransExpro(_proExproPath,_tranExproPath,folder):
    _map=getTransProteinMap(folder)
    _map1=clearExpro(_proExproPath, _map, folder, 'ProteinExprossion.txt')
    _map2=clearExpro(_tranExproPath, getTransProteinMap(folder,True), folder, 'TransExprossion.txt')
    fw=open(folder+'/ProteinTransExprossion.txt','w')
    fw.write('Protein\tGene\t'+'\t'.join(_map1['header'])+'\t'+'\t'.join(_map2['header'])+'\n')
    for key in _map:
        fw.write(key+'\t'+_map[key]+'\t'+'\t'.join(_map1[key])+'\t'+'\t'.join(_map2[_map[key]])+'\n')
    fw.close()
    
def clearExpro(_exproPath,_keyMap,folder,outName):
    data1=getDataMatrix(_exproPath)
    fw=open(folder+'/'+outName,'w')
    fw.write('\t'.join(data1[0][0])+'\n')
    _map={}
    _map['header']=data1[0][0][1:len(data1[0][0])]
    for i in range(1,len(data1[0])):
        if _keyMap.has_key(data1[0][i][0]):
            fw.write('\t'.join(data1[0][i])+'\n')
            _map[data1[0][i][0]]=data1[0][i][1:len(data1[0][i])]
    fw.close()
    return _map
def annotationByGO(folder,iprPath=None, merge=None):
    _map=getTransProteinMap(folder)
    goAnnotation(list(_map.iterkeys()), folder, iprPath, merge)
def annotationByKEGG(folder,osas):
    _map=getTransProteinMap(folder)
    keggAnnotation(folder, list(_map.iterkeys()), osas)    
def annotationByDomain(iprPath,folder):
    _map=getTransProteinMap(folder)
    domainAnnotation(iprPath, folder,list(_map.iterkeys()))
def annotationByCOG(folder,m8Path,kog=None):
    _map=getTransProteinMap(folder)
    cogAnnotation(m8Path, list(_map.iterkeys()),folder,kog)    
def annotationBySub(folder,subPath):
    _map=getTransProteinMap(folder)
    subCellurAnnotation(folder,list(_map.iterkeys()),subPath)    

#gram 格兰仕阴性为False
def subCellurCello(folder,gram):
    _lines=postCello(folder+'/identify.fasta', False)
    fw=open(folder+'/worf.tab','w')
    fw.write('\n'.join(_lines))
    fw.close()

        
#    
def outUpDownCommon(_path1,_path2,folder,outName,regulated1=1,regulated2=1):
    keyMap1=getTransProteinMap(folder)
    pro=parseDiff(_path1, regulated1, keyMap1)
    keyMap2=getTransProteinMap(folder,True)
    tran=parseDiff(_path2, regulated2, keyMap2,True)            
    try:
        os.mkdir(folder+'/'+outName)
    except:
        pass
    tranDif=set(tran[0]).union(set(tran[1]))
    proDif=set(pro[0]).union(set(pro[1]))
    _uu=getCommonList(pro[0], tran[0])
    _ud=getCommonList(pro[0], tran[1])
    _un=list(set(pro[0]).difference(tranDif))
    _nu=list(set(tran[0]).difference(proDif))
    _dd=getCommonList(pro[1], tran[1])
    _du=getCommonList(pro[1], tran[0])
    _dn=list(set(pro[1]).difference(tranDif))
    _nd=list(set(tran[1]).difference(proDif))
    writeLines(_uu, folder+'/'+outName+'/UU.txt')
    writeLines(_ud, folder+'/'+outName+'/UD.txt')
    writeLines(_un, folder+'/'+outName+'/UN.txt')
    writeLines(_nu, folder+'/'+outName+'/NU.txt')
    writeLines(_du, folder+'/'+outName+'/DU.txt')
    writeLines(_dd, folder+'/'+outName+'/DD.txt')
    writeLines(_dn, folder+'/'+outName+'/DN.txt')
    writeLines(_nd, folder+'/'+outName+'/ND.txt')
    return [len(_uu),len(_ud),len(_un),len(_nu),len(_du),len(_dd),len(_dn),len(_nd)]
    
    
def parseDiff(_path,regulated,keyMap,rev=False):
    _data=getDataMatrix(_path)[0]
    up=[]
    down=[]
    for cols in _data:
        if keyMap.has_key(cols[0]):
            if cols[regulated]=='down' or cols[regulated]=='Down' or cols[regulated]=='DOWN':
                if rev:
                    down.append(keyMap[cols[0]])
                else:
                    down.append(cols[0])
            elif cols[regulated]=='up' or cols[regulated]=='Up' or cols[regulated]=='UP':
                if rev:
                    up.append(keyMap[cols[0]])
                else:
                    up.append(cols[0])
    return (up,down)

def crosslink(folder,_quant):
    diffCount=[]
    diffCount.append(['sample','UU','UD','UN','NU','DU','DD','DN','ND'])
    for q in _quant:
        _st=outUpDownCommon(folder+'/'+q+'.diff.exp.xls',folder+'/DiffExp_Analysis/'+q+'.diff.exp.xls.annot.xls', folder,q,7,19)
        _st.insert(0, q)
        diffCount.append(_st)
    writeMatrix(diffCount, folder+'/commonUpDown.stat.txt')
    
    
def outGOEnrichment(folder, quant,levels,full=0):
    for q in quant:
        for level in levels:
#             print getLineDatas(folder+'/'+q+'/'+level+'.txt')
            GOEnrichment(getLineDatas(folder+'/'+q+'/'+level+'.txt'), folder+'/BP_GOs.txt',folder+'/'+q+'/'+level+'_GO_BP_Enrich.txt', full)
            GOEnrichment(getLineDatas(folder+'/'+q+'/'+level+'.txt'), folder+'/CC_GOs.txt',folder+'/'+q+'/'+level+'_GO_CC_Enrich.txt', full)
            GOEnrichment(getLineDatas(folder+'/'+q+'/'+level+'.txt'), folder+'/MF_GOs.txt',folder+'/'+q+'/'+level+'_GO_MF_Enrich.txt', full)

def postREVIGO(folder,_quant,levels):
    if _quant:
        for q in _quant:
            fold1=folder+'/'+q
            for level in levels:
                print 'post:'+q+'-MF-'+level
                postAndSaveR(fold1,level+'_GO_MF_Enrich')
                print 'post:'+q+'-CC-'+level
                postAndSaveR(fold1,level+'_GO_CC_Enrich')
                print 'post:'+q+'-BP-'+level
                postAndSaveR(fold1,level+'_GO_BP_Enrich')

def outKEGGEnrichment(folder,quant,levels,full=0):
    for q in quant:
        for level in levels:
            KEGGEnrichment(getLineDatas(folder+'/'+q+'/'+level+'.txt'), folder+'/KEGG_Paths.txt', folder+'/'+q+'/'+level,0)

def outDomainEnrichment(folder,quant,levels,full=0):
    for q in quant:
        for level in levels:
            DomainEnrichment(getLineDatas(folder+'/'+q+'/'+level+'.txt'), folder+'/Ipr_Domains.txt', folder+'/'+q+'/'+level+'_Domain_Enrich.txt',0)

def enrichment(folder, quant,levels,full=0):
    outGOEnrichment(folder, quant,levels,full)
    outKEGGEnrichment(folder,quant,levels,full)
    outDomainEnrichment(folder,quant,levels,full)

def classFunctionGO(folder, quant,levels):
    for i in range(2,8):
        bp=getMapItermGO(folder+'/BP_GOs.txt', i)
        cc=getMapItermGO(folder+'/CC_GOs.txt', i)
        mf=getMapItermGO(folder+'/MF_GOs.txt', i)
        for q in quant:
            for level in levels:
                outClassFuncionGO(bp,set(getLineDatas(folder+'/'+q+'/'+level+'.txt')),folder+'/'+q+'/'+level+'_BP_level'+str(i)+'_classFun.txt')
                outClassFuncionGO(cc,set(getLineDatas(folder+'/'+q+'/'+level+'.txt')),folder+'/'+q+'/'+level+'_CC_level'+str(i)+'_classFun.txt')
                outClassFuncionGO(mf,set(getLineDatas(folder+'/'+q+'/'+level+'.txt')),folder+'/'+q+'/'+level+'_MF_level'+str(i)+'_classFun.txt')
def classFunctionCOG(folder, quant,levels):
    bg=getMapItermCOG(folder+'/COG_ClassFuns.txt')
    for q in quant:
        for level in levels:
            outClassFuncionCOG(bg,set(getLineDatas(folder+'/'+q+'/'+level+'.txt')),folder+'/'+q+'/'+level+'_COG_classFun.txt')

def classFunctionSubCelurLocation(folder, quant,levels):
    bg=getMapItermSubCellur(folder+'/SubCellur_loactions.txt')
    for q in quant:
        for level in levels:
            outClassFuncionSubCelur(bg,set(getLineDatas(folder+'/'+q+'/'+level+'.txt')),folder+'/'+q+'/'+level+'_SubCelur_classFun.txt')

            
def classFunction(folder, quant,levels):
    classFunctionGO(folder, quant,levels)
    classFunctionCOG(folder, quant,levels)
    classFunctionSubCelurLocation(folder, quant,levels)

def enrichMerge(folder,quant,levels):
    stages=['GO_CC','GO_MF','GO_BP','Domain','KEGG']
    for q in quant:
        for stage in stages: 
            _list=[]
            for level in levels:
                _map1=getEnrichmenResultData(folder+'/'+q+'/'+level+'_'+stage+'_Enrich.txt.tmp')
                _list.append(_map1)
            _mergeMap=mergeEnrichmentResultData(_list)
            fw=open(folder+'/'+q+'/merge_'+stage+'_Enrich.txt','w')
            fw.write('CategorieID\tCategorieName\t'+'\t'.join(levels)+'\n')
            for key in _mergeMap:
                fw.write(key+'\t'+'\t'.join(_mergeMap[key])+'\n')
            fw.close()

def iPath2(folder,quant,levels):
    colors=["#CC3300", "#996600",'#9999FF','#FFCC99','#0066CC',"#339933",'#663366','#99CC00',"#333333"]
    _map=getKO2Protein(folder+'/query.ko')
    _exproMap=getTransProteinMap(folder)
    for q in quant:
        try:
            os.makedirs(folder+'/'+q+'/iPath2')
        except:
            pass
        _list=[]
        for _l in levels:
            _list.append(set(getLineDatas(folder+'/'+q+'/'+_l+'.txt')))
        fw=open(folder+'/'+q+'/iPath2/queryList.txt','w')
        for pro in _exproMap:
            if _map.has_key(pro):
                diff=False
                for i in range(len(levels)):
                    if pro in _list[i]:
                        diff=True
                        fw.write(_map[pro]+' W8 '+colors[i]+'\n')
                        break
                if not diff:
                    fw.write(_map[pro]+' W6 '+colors[-1]+'\n')#green
        fw.close()
def crossCluster(folder,quant):
    diffCount=[]
    diffCount.append(['sample','Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7','Cluster8','Cluster9','Cluster10'])
    for q in _quant:
        try:
            os.mkdir(folder+'/Cluster_'+q)
        except:
            pass
        dt=getDataMatrix(folder+'/'+q+'_Cluster.txt')[0]
        _map={}
        for cols in dt:
            if _map.has_key(cols[1]):
                _map[cols[1]].append(cols[0].rstrip('"').lstrip('"'))
            else:
                _map[cols[1]]=[cols[0].rstrip('"').lstrip('"')]
        _st=[q]
        for i in range(10):
            cl=_map[str(i+1)]
            writeLines(cl, folder+'/Cluster_'+q+'/Cluster'+str(i+1)+'.txt')
            _st.append(len(cl))
        diffCount.append(_st)
    writeMatrix(diffCount, folder+'/commonCluster.stat.txt')    

def formatRegulatedReport(folder,rootFolder,sample,stage):
    fd=folder+'/'+sample+'/'
    rf=rootFolder+'/'+sample+'/'+stage+'/'
    mergeRegulatedAnnation(rootFolder+'/CombineAnnotation.xls', set(getLineDatas(fd+stage+'.txt')), rf+'RegulatedCombineAnnotation.xls')
    for g in ['Domain','KEGG','GO_CC','GO_BP','GO_MF']:
        copyImage(fd+stage+'_'+g+'_Enrich', rf+g+'_Enrich')
        copyFile(fd+stage+'_'+g+'_Enrich.txt', rf+g+'_Enrich.txt')
    copyImage(fd+stage+'_GO_CC_topGO', rf+'GO_CC_Enrich_topGO')
    copyImage(fd+stage+'_GO_BP_topGO', rf+'GO_BP_Enrich_topGO')
    copyImage(fd+stage+'_GO_MF_topGO', rf+'GO_MF_Enrich_topGO')
    copyImage(fd+stage+'_GO_CC_Enrich_Scatter', rf+'GO_CC_Enrich_Scatter')
    copyImage(fd+stage+'_GO_BP_Enrich_Scatter', rf+'GO_BP_Enrich_Scatter')
    copyImage(fd+stage+'_GO_MF_Enrich_Scatter', rf+'GO_MF_Enrich_Scatter')
    copyImage(fd+stage+'_GO_CC_Enrich_Treemap', rf+'GO_CC_Enrich_Treemap')
    copyImage(fd+stage+'_GO_BP_Enrich_Treemap', rf+'GO_BP_Enrich_Treemap')
    copyImage(fd+stage+'_GO_MF_Enrich_Treemap', rf+'GO_MF_Enrich_Treemap')
    for i in range(1,6):
        copyImage(fd+stage+'_level'+str(i)+'_Classfun', rf+'GO_Level'+str(i)+'_Classfun')
        for g in ['BP','CC','MF']:
            copyFile(fd+stage+'_'+g+'_level'+str(i)+'_classFun.txt', rf+g+'_Level'+str(i)+'_Classfun.txt')
    for g in ['COG','SubCelur']:
        copyImage(fd+stage+'_'+g+'_ClassFun', rf+g+'_ClassFun')
        copyFile(fd+stage+'_'+g+'_classFun.txt', rf+g+'_ClassFun.txt')
    copyFolder(fd+stage+'_KEGG_PATH', rf+'KEGG_PATH')            
    
    
def formatReport(folder,_quant,levels,clusters):
    rootFolder=folder+'/Report/Data'
    mkdir(rootFolder)
    copyImage(folder+'/Venn', rootFolder+'/Venn')
    copyFile(folder+'/commonCluster.stat.txt', rootFolder+'/commonCluster.stat.txt')
    copyFile(folder+'/commonUpDown.stat.txt', rootFolder+'/commonUpDown.stat.txt')
    mergeAnnotation(folder, folder+'/ProteinTransExprossion.txt', rootFolder+'/CombineAnnotation.xls')
    for q in _quant:
        copyImage(folder+'/'+q+'_HeatMap',rootFolder+'/'+q+'_HeatMap')
        copyImage(folder+'/'+q+'_Correlation',rootFolder+'/'+q+'_Correlation')
        for l in levels:
            mkdir(rootFolder+'/'+q+'/'+l)
            formatRegulatedReport(folder, rootFolder, q, l)
        for l in clusters:
            mkdir(rootFolder+'/Cluster_'+q+'/'+l)
            formatRegulatedReport(folder, rootFolder, 'Cluster_'+q, l)
        copyFolder(folder+'/'+q+'/iPath2', rootFolder+'/'+q+'/iPath2')
        for c in ['KEGG','Domain','GO_CC','GO_BP','GO_MF']:
            copyImage(folder+'/'+q+'/'+c+'_Cluster', rootFolder+'/'+q+'/'+c+'_Cluster')
            copyImage(folder+'/Cluster_'+q+'/'+c+'_Cluster', rootFolder+'/Cluster_'+q+'/'+c+'_Cluster')
        
        
def createReport(folder,_quant,levels,clusters):
    rootFolder=folder+'/Report/Data'
    mkdir(folder+'/Report/Tables')
    if not os.path.exists(rootFolder):
        formatReport(folder, _quant, levels, clusters)
    copyFolder(_ReportRootPath+'/src/js', folder+'/Report/src/js')
    copyFolder(_ReportRootPath+'/src/css', folder+'/Report/src/css')
    copyFolder(_ReportRootPath+'/src/imgs', folder+'/Report/src/imgs')
    fw=open(folder+'/Report/Report.html','w')
    fw.write(getHtmlHeader('蛋白组与转录组关联分析报告'))
    fw.write(writePjectInfo(folder, _quant, levels, clusters))
    nav1=Nav('1、样本信息','sampleInfo',None,True)
    fw.write(writeWorkFlow())
    nav2=Nav('2、分析流程','workflow',None,True)
    nav3=writeUp2DownLink(fw, folder, _quant, levels)
    nav4=writeClusterLink(fw, folder, _quant, clusters)
    navs=[nav1,nav2,nav3,nav4]
    fw.write('</div>')
    fw.write(getNavHtml(navs))
    fw.write(getHtmlFooter())
    fw.close()

if __name__ == '__main__':
    folder='E:/Work/P1/MG005/Proteome'
#     formatTrans_protein(folder+'/seq.m8', folder)
#     formatProTransExpro(folder+'/MergeAll.txt', folder+'/DiffExp_Analysis/genes.fpkm_table', folder)
#     writeBgFasta(folder, folder+'/uniprot-organism_4081.fasta')
#     annotationByGO(folder)  
#     postKAAS(folder+'/identify.fasta', 'sly')
#     annotationByKEGG(folder, 'sly')
#     annotationByDomain(folder+'/inter.domain',folder)
#     annotationByCOG(folder, folder+'/seq.m8', 'kog')
#     subCellurCello(folder,False)
#     annotationBySub(folder, folder+'/worf.tab')
    _quant=['gib-3-0d_vs_WT-0d','WT-14d_vs_WT-0d']#,'gib-3-14d_vs_gib-3-0d','gib-3-14d_vs_WT-14d'
#     crosslink(folder, _quant)
    _levels=['UU','UD','UN','NU','DU','DD','DN','ND']
#     enrichment(folder, _quant, _levels, 0)
#     postREVIGO(_quant, _levels)
#     classFunction(folder, _quant, _levels)
#     enrichMerge(folder, _quant, _levels)
#     iPath2(folder, _quant, _levels)
    ###############Cluster Analysis############################
#     crossCluster(folder,_quant)
    _clusters=['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5','Cluster6','Cluster7','Cluster8','Cluster9','Cluster10']
    _cQuant=[]
    for _q in _quant:
        _cQuant.append('Cluster_'+_q)
#     enrichment(folder, _cQuant, _clusters, 0)
#     postREVIGO(_cQuant, _clusters)
#     classFunction(folder, _cQuant, _clusters)
#     enrichMerge(folder, _cQuant, _clusters)
    #################Create Report###########################
#     formatReport(folder, _quant, _levels, _clusters)
    createReport(folder, _quant, _levels, _clusters)
    
    
    
    
    