# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��11��26��

@author: Administrator
'''
from os.path import os

from com.zlf.domain.report.ReportLabels import _GOTxt, _GOTxtMathodP1, \
    _GOTxtMathodP2, _EnrichTabelTxt, _EnrichPlotTxt, _TopGOLabel, \
    _KEGGLabel
from com.zlf.domain.report.ReportTemplate import getTxtHtml, getImageHtml, \
    getTitleHHtml, getFigureLabelHtml, getTableHtml, getTitleMHtml, \
    getTableTemplateHtml, getTableLabelHtml, getA_Bank, getFigureTxtHtml, \
    getImagesHtml, getTitleHtml
from com.zlf.domain.utils.FileOpertor import getDataMatrix


def getProjectInfo(label,summary,tables):
    _line=getTitleHHtml(label, 'sampleInfo')
    _line=_line+getTxtHtml(summary)
    _line=_line+getTxtHtml('样本信息如下：')
    _line=_line+getTableHtml(tables[0], tables[1:len(tables)])
    return _line
def getProjectWorkFlow(label,summary,img):
    _line=getTitleHHtml(label, 'workflow')
    _line=_line+getTxtHtml(summary)
    _line=_line+getTxtHtml('生物信息分析流程见下图:')
    _line=_line+getImageHtml('信息分析流程图','信息分析流程图' , 'src/imgs/'+img)
    _line=_line+getFigureLabelHtml('生物信息分析流程图')
    return _line

def getAnnoGOPart(stage,shortLabel, tablesBP, headerBP,rootFolder):
    tableTxt=getTableTemplateHtml('蛋白的GO '+stage+'注释表'
                                  , _GOTxt+'<br/><strong>'+stage+':</strong>'
                                  , tablesBP, headerBP)
    f=open(rootFolder+'/Tables/GO_'+shortLabel+'_Function_Annotation.html','w')
    f.write(tableTxt)
    f.close()
    l=10
    if len(tablesBP)<10:
        l=len(tablesBP)
    lines=(getTxtHtml('展示前'+str(l)+'个蛋白的'+stage+'注释表如下：'))
    lines=lines+(getTableHtml(headerBP,tablesBP[0:l]))
    lines=lines+(getTableLabelHtml('GO功能注释表，更多详情请看'+getA_Bank('Tables/GO_'+shortLabel+'_Function_Annotation.html', '蛋白GO '+stage+'功能注释表')))
    return lines

def getAnnoPart(tables, header,rootFolder,stage,txt):
    tableTxt=getTableTemplateHtml('蛋白的GO '+stage+' 注释表'
                                  , txt
                                  , tables, header)
    f=open(rootFolder+'/Tables/'+stage+'_Function_Annotation.html','w')
    f.write(tableTxt)
    f.close()
    l=10
    if len(tables)<10:
        l=len(tables)
    lines=(getTxtHtml('展示前'+str(l)+'个蛋白的'+stage+'注释表如下：'))
    lines=lines+(getTableHtml(header,tables[0:l]))
    lines=lines+(getTableLabelHtml(stage+'功能注释表，更多详情请看'+getA_Bank('Tables/'+stage+'_Function_Annotation.html', '蛋白'+stage+'功能注释表')))
    return lines


def getProjectGOAnnotation(title,_id,tablesBP,tablesCC,tablesMF,headerBP,headerCC,headerMF,rootFolder):
    lines=getTitleMHtml(title,_id)
    lines=lines+getTxtHtml(_GOTxt)
    lines=lines+getTxtHtml(_GOTxtMathodP1)
    lines=lines+getTxtHtml(_GOTxtMathodP2)
    lines=lines+getAnnoGOPart('Biological Process', 'BP', tablesBP, headerBP, rootFolder)
    lines=lines+getAnnoGOPart('Cellular Component', 'CC', tablesCC, headerCC, rootFolder)
    lines=lines+getAnnoGOPart('Molecular Function', 'MF', tablesMF, headerMF, rootFolder)
    return lines


def writeEnrichmentTableTemplateHtml(folder,sampleName,regulatedName,tie,fileName):
    header=['Category_ID','Category_Name','DiffMapping','ProteinMapping','DiffNum','ProteinNum','FoldEnrichment','Fisher\'s exact test p value','DiffMapping Protein IDs']
    tb1=getDataMatrix(folder+'/Data/'+sampleName+'/'+regulatedName+'/'+fileName+'.txt')[0]
    l=10
    if len(tb1)>0:
        f=open(folder+'/Tables/'+sampleName+'_'+regulatedName+'_'+fileName+'.html','w')
        f.write(getTableTemplateHtml(regulatedName+'基因'+tie+'富集分析结果',_EnrichTabelTxt+'<strong>'+getA_Bank('../Data/'+sampleName+'/'+regulatedName+'/'+fileName+'.txt', '下载')+'</strong>', tb1,header))
        f.close()        
        if len(tb1)<10:
            l=len(tb1)
        if l==10:
            lines=getTxtHtml(regulatedName+'基因'+tie+'富集分析前10个结果如下：')
        else:
            lines=getTxtHtml(regulatedName+'基因'+tie+'富集分析结果如下：')
        lines=lines+getTableHtml(header[0:len(header)-1], tb1[0:l])
        lines=lines+getTableLabelHtml(_EnrichTabelTxt+getA_Bank('Tables/'+sampleName+'_'+regulatedName+'_'+fileName+'.html','查看更多详情'))
        if l>1:
            lines=lines+getEnrichmentPlotHtml(sampleName, regulatedName, tie, fileName)
    else:
        l=0
        lines=(getTxtHtml(regulatedName+'基因无显著富集的'+tie+'结果'))
    return (lines,l)

def getEnrichmentPlotHtml(sampleName, regulatedName,tie,fileName):
    lines=getTxtHtml(tie+'富集结果可视化如下：')
    lines=lines+getImageHtml(tie+'富集结果可视化', tie+'富集结果可视化#PDF', 'Data/'+sampleName+'/'+regulatedName+'/'+fileName+'.jpg')
    lines=lines+getFigureTxtHtml(_EnrichPlotTxt)
    return lines

def getTopGOAndTreeMap(sampleName, regulatedName,tie,fileName,folder):
    lines=getTxtHtml('显著性'+tie+'有向无环图:')
    lines=lines+getImageHtml('显著性'+tie+'有向无环图', '显著性'+tie+'有向无环图#PDF', 'Data/'+sampleName+'/'+regulatedName+'/'+fileName+'_topGO.jpg')
    lines=lines+getFigureTxtHtml(_TopGOLabel)
    if os.path.exists(folder+'/Data/'+sampleName+'/'+regulatedName+'/'+fileName+'_Scatter.jpg'):
        lines=lines+getTxtHtml('当得到了很多的 GO 富集结果时，面对大量报告的 GO 分类茫然无措，可以通过对每个 GO 分类进行相似性归类分析，总结出几个重要的类别显著性')
        lines=lines+getTxtHtml(tie+'语义相似性聚类分析:')
        lines=lines+getImageHtml('显著性'+tie+'语义相似性聚类分析', '显著性'+tie+'语义相似性聚类分析#PDF', 'Data/'+sampleName+'/'+regulatedName+'/'+fileName+'_Treemap.jpg')
        lines=lines+getImageHtml('显著性'+tie+'语义相似性聚类分析', '显著性'+tie+'语义相似性聚类分析#PDF', 'Data/'+sampleName+'/'+regulatedName+'/'+fileName+'_Scatter.jpg')
    return lines

def getKEGGPathway(folder, sampleName, regulatedName,tie,fileName):
    tb1=getDataMatrix(folder+'/Data/'+sampleName+'/'+regulatedName+'/'+fileName+'.txt')[0]
    lines=getTxtHtml('显著性'+tie+'通路图:')
    imgs=[]
    for p in tb1:
        imgs.append([p[1]+' ','Data/'+sampleName+'/'+regulatedName+'/KEGG_PATH/img/'+p[0]+'.png',p[1]+'#Pathway'])
    lines=lines+getImagesHtml(imgs)
    lines=lines+getFigureTxtHtml(_KEGGLabel)
    return lines

def getClassFunGO(folder,sampleName,regulatedName):
    imgs=[]
    lines=''
    for i in range(1,6):
        if os.path.exists(folder+'/Data/'+sampleName+'/'+regulatedName+'/GO_Level'+str(i)+'_Classfun.jpg'):
            imgs.append(['GO Level'+str(i)+' 分类统计','Data/'+sampleName+'/'+regulatedName+'/GO_Level'+str(i)+'_Classfun.jpg','GO Level'+str(i)+' 分类统计#PDF'])
            lines=lines+getTxtHtml(getA_Bank('Data/'+sampleName+'/'+regulatedName+'/GO_Level'+str(i)+'_Classfun.txt', 'GO Level'+str(i)+' 分类统计详细信息'))
    if len(imgs)>0:
        lines=getTxtHtml('GO Level 分类统计结果如下：')+lines
        lines=lines+getTxtHtml('GO Level 分类统计结果可视化如下：')
        lines=lines+getImagesHtml(imgs)
        lines=lines+getFigureTxtHtml('注：图中百分比为改GO Term下的目标蛋白个数占所有目标蛋白个数的比例，同一个蛋白可能会同时出现在多个GO Term中')
    else:
        lines=getTxtHtml('无GO Level 分类统计结果')
    return lines

def getIpath2Report(url):
    line=getTxtHtml('iPATH2代谢通路整合分析结果如下：')
    imgs=[['Metabolic pathways: constructed using 146 KEGG pathways, and gives an overview of the complete metabolism in biological systems',url+'/Metabolic.jpg','Metabolic#PDF']
          ,['22个 KEGG regulatory pathways整合分析',url+'/Regulatory.jpg','Regulatory#PDF']
          ,['Biosynthesis of secondary metabolites: contains 58 KEGG pathways involved in biosynthesis of secondary metabolites',url+'/Biosynthesis.jpg','Biosynthesis#PDF']]
    line=line+getImagesHtml(imgs)
    return line
    
def getSampleRegulatedClassFunctionReport(folder,sampleName,regulatedName,_id):
    lines=getTitleHtml(_id+'、'+regulatedName+'功能分类统计',_id.replace('.','',100))
    lines=lines+getTxtHtml('对'+regulatedName+'基因进行GO Level、COG、SubcellurLocation功能分类统计分析')
    lines=lines+getClassFunGO(folder, sampleName, regulatedName)
    lines=lines+getTxtHtml('COG 分类统计结果如下：')
    lines=lines+getTxtHtml(getA_Bank('Data/'+sampleName+'/'+regulatedName+'/COG_ClassFun.txt', 'COG 分类统计详细信息'))
    lines=lines+getTxtHtml('COG 分类统计结果可视化如下：')
    lines=lines+getImageHtml('COG 分类统计详细信息','COG 分类统计详细信息#PDF','Data/'+sampleName+'/'+regulatedName+'/COG_ClassFun.jpg')
    lines=lines+getTxtHtml('SubcellurLocation 分类统计结果如下：')
    lines=lines+getTxtHtml(getA_Bank('Data/'+sampleName+'/'+regulatedName+'/SubCelur_ClassFun.txt', 'SubcellurLocation 分类统计详细信息'))
    lines=lines+getTxtHtml('SubcellurLocation 分类统计结果可视化如下：')
    lines=lines+getImageHtml('SubcellurLocation 分类统计详细信息','SubcellurLocation 分类统计详细信息#PDF','Data/'+sampleName+'/'+regulatedName+'/SubCelur_ClassFun.jpg')
    return lines
    
def getSampleRegulatedEnrichReport(folder,sampleName,regulatedName,_id):
    lines=getTitleHtml(_id+'、'+regulatedName+'富集分析',_id.replace('.','',100))
    lines=lines+getTxtHtml('对'+regulatedName+'基因进行GO、KEGG、Domain功能富集分析')
    col=writeEnrichmentTableTemplateHtml(folder, sampleName, regulatedName, 'GO Biological Process', 'GO_BP_Enrich')
    lines=lines+col[0]
    if col[1]>0:
        lines=lines+getTopGOAndTreeMap(sampleName, regulatedName, 'GO Biological Process', 'GO_BP_Enrich',folder)
        
    col=writeEnrichmentTableTemplateHtml(folder, sampleName, regulatedName, 'GO Cellular Component', 'GO_CC_Enrich')
    lines=lines+col[0]
    if col[1]>0:
        lines=lines+getTopGOAndTreeMap(sampleName, regulatedName, 'GO Cellular Component', 'GO_CC_Enrich',folder)
        
    col=writeEnrichmentTableTemplateHtml(folder, sampleName, regulatedName, 'GO Molecular Function', 'GO_MF_Enrich')
    lines=lines+col[0]
    if col[1]>0:
        lines=lines+getTopGOAndTreeMap(sampleName, regulatedName, 'GO Molecular Function', 'GO_MF_Enrich',folder)
        
    col=writeEnrichmentTableTemplateHtml(folder, sampleName, regulatedName, 'KEGG Pathway', 'KEGG_Enrich')
    lines=lines+col[0]
    if col[1]>0:
        lines=lines+getKEGGPathway(folder, sampleName, regulatedName, 'KEGG Pathway', 'KEGG_Enrich')
    
    col=writeEnrichmentTableTemplateHtml(folder, sampleName, regulatedName, 'Domain', 'Domain_Enrich')
    lines=lines+col[0]
    
    
    
    return lines
    
if __name__ == '__main__':
    pass