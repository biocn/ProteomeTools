# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��11��28��

@author: Administrator
'''
from com.zlf.domain.net.KeggDownload import getImg
from com.zlf.domain.report.PartTemplate import getProjectInfo, \
    getProjectWorkFlow, getProjectGOAnnotation, getAnnoPart, \
    getSampleRegulatedEnrichReport, getSampleRegulatedClassFunctionReport, \
    getIpath2Report
from com.zlf.domain.report.ReportLabels import _AnnoFunTableHeader, _COGTxt, \
    _KEGGTxt, _DomainTxt, _SubCelurTxt
from com.zlf.domain.report.ReportTemplate import getTxtHtml, getImageHtml, \
    getFigureLabelHtml, getTitleMHtml, getTitleHHtml, Nav, getTableHtml, \
    getImagesHtml, getA_Bank, getTitleHtml, getFigureTxtHtml
from com.zlf.domain.utils.FileOpertor import getDataMatrix


def writePjectInfo(folder,_quant,levels,clusters):
    tables=getDataMatrix(folder+'/samplesInfo.xls')[0]
    summary='蛋白质是生命功能的执行者，其含量的变化在生物体的生长发育、环境应激、疾病发生发展等过程中发挥着重要的作用。从DNA、mRNA到蛋白质的过程中涉及到一整套精细的表达调控机制，如转录调控、转录后调控、翻译调控、翻译后调控等。因此，要全面探究生物体疾病机理、环境应激机制，精准描绘关键基因的表达模式，同步检测mRNA和蛋白质的表达量并进行联合分析已成为当前研究的必然趋势。本项目共分析了'+str(len(_quant))+'个比较组,分别从样本上下调状态关联('+','.join(levels)+')和表达谱聚类关联('+','.join(clusters)+')进行关联分析。'
    summary=summary+''
    return '<section>'+getProjectInfo('1、项目摘要',summary , tables)+getTxtHtml('蛋白组和转录组关联摘要如下：')+getImageHtml('蛋白组与转录组关联文氏图', '蛋白组与转录组关联文氏图#PDF', 'Data/Venn.jpg')+getFigureLabelHtml('蛋白组与转录组关联文氏图')+'</section>'

def writeWorkFlow():
    summary='将转录组和蛋白组数据进行整合关联，分析在不同样本转录水平和蛋白表达水平不同模式下的蛋白的功能注释和功能富集等表达水平分析。'
    return '<section>'+getProjectWorkFlow('2、信息分析流程：', summary, 'workflow_trans_pro.jpg')+'</section>'

def getTableUp2DownHtml():
    line='<div class="table-responsive">'
    line=line+'<table class="table table-bordered table-hover table-striped"><thead>'
    line=line+'<tr class="bg-info" ><td colspan="2" rowspan="2"></td><td colspan="3" align="center">Transcriptome</td></tr><tr class="bg-info"><td>up</td><td>down</td><td>constant</td></tr></thead>'
    line=line+'<tbody>'
    line=line+'<tr><td rowspan="3" class="bg-info" align="center">Proteome</td><td class="bg-info">up</td><td style="background-color:#CC3300">UU</td><td style="background-color:#996600">UD</td><td style="background-color:#9999FF">UN</td></tr>'
    line=line+'<tr><td class="bg-info">down</td><td style="background-color:#0066CC">DU</td><td style="background-color:#339933">DD</td><td style="background-color:#663366">DN</td></tr>'
    line=line+'<tr><td class="bg-info">constant</td><td style="background-color:#FFCC99">NU</td><td style="background-color:#99CC00">ND</td><td style="background-color:#333333">NN</td></tr>'
    line=line+'</tbody></table></div>'
    return line

def writeClusterLink(fw,folder,_quant,clusters):
    fw.write('<section>')
    fw.write(getTitleHHtml('4、表达模式关联分析', 'ClusterLnk'))
    nav=Nav('4、表达模式关联分析','ClusterLnk',None,True)
    fw.write(getTxtHtml('根据蛋白在样本转录组水平和蛋白组水平的表达水平进行聚类关联，筛选出具有代表性的'+str(len(clusters))+'类模式。'))
    fw.write(getTitleMHtml('4.1、关联摘要', 'ClusterLnk1'))
    nav.addC(Nav('4.1、关联摘要','ClusterLnk1',True))
    fw.write(getTxtHtml('各样本比较组关联的'+str(len(clusters))+'种模式下蛋白统计如下：'))
    _list=getDataMatrix(folder+'/Report/Data/commonCluster.stat.txt')[0]
    fw.write(getTableHtml(_list[0], _list[1:len(_list)]))
    fw.write(getTxtHtml('各样本比较组蛋白组与转录组表达聚类分析如下：'))
    imgs=[]
    for q in _quant:
        imgs.append([q+' 转录组与蛋白组聚类分析','Data/'+q+'_HeatMap.jpg',q+' 转录组与蛋白组聚类分析#PDF'])
    fw.write(getImagesHtml(imgs))
    fw.write(getFigureLabelHtml('蛋白组与转录组聚类分析'))
    fw.write(getTitleMHtml('4.2、关联蛋白功能富集分析','ClusterLnk2'))
    nav2=Nav('4.2、功能富集分析','ClusterLnk2',True)
    fw.write(getTxtHtml('对目标蛋白进行 GO、KEGG、Pathway功能显著性富集分析，可以说明目标蛋白的功能富集情况，在功能水平阐明样本间的差异。本分析使用软件 DAVID(https://david-d.ncifcrf.gov/)软件进行富集分析，使用方法为 Fisher 精确检验。 通常情况下，p 值≤0.05 了时，认为此功能节点存在显著富集情况，计算方法如下：'))
    fw.write(getTableHtml(['','目标蛋白数量','非目标蛋白数量','总和'], [['功能A','a','b','a+b'],['A以外的功能','c','d','c+d'],['总和','a+c','b+d','a+b+c+d(=n)']]))
    fw.write(getTxtHtml('Fisher 精确检验理论指出得到这一组数据的概率可以由超几何分布计算，公式如下：'))
    fw.write(getImageHtml('Fisher 精确检验公式','Fisher 精确检验公式', 'src/imgs/FisherTest.png'))
    for i in range(len(_quant)):
        nav2.addC(writeSampleEnrichment(fw, folder+'/Report', 'Cluster_'+_quant[i], clusters, '4.2.'+str(i+1)+''))
        
    nav3=Nav('4.3、功能分类分析','ClusterLnk3',True)
    fw.write(getTitleMHtml('4.3、关联蛋白功能分类','ClusterLnk3'))
    fw.write(getTxtHtml('对目标蛋白进行 GO Level、COG及亚细胞结构分类统计,分别从功能、进化、空间上说明目标蛋白的功能聚集情况'))
    for i in range(len(_quant)):
        nav3.addC(writeSampleClassFunction(fw, folder+'/Report', 'Cluster_'+_quant[i], clusters, '4.3.'+str(i+1)))
    fw.write('</section>')
    nav.addC(nav2)
    nav.addC(nav3)
    return nav


def writeUp2DownLink(fw,folder,_quant,levels):
    fw.write('<section>')
    fw.write(getTitleHHtml('3、调控关系关联分析', 'up2Down'))
    nav=Nav('3、调控关系关联分析','up2Down',None,True)
    fw.write(getTxtHtml('根据蛋白在样本转录组水平和蛋白组水平上下调状态进行关联，共计八种模式。'))
    fw.write(getTxtHtml('八种模式如下：'))
    fw.write(getTableUp2DownHtml())
    fw.write(getTitleMHtml('3.1、关联摘要', 'up2Down1'))
    nav.addC(Nav('3.1、关联摘要','up2Down1',True))
    fw.write(getTxtHtml('各样本比较组关联的八种模式下蛋白统计如下：'))
    _list=getDataMatrix(folder+'/Report/Data/commonUpDown.stat.txt')[0]
    fw.write(getTableHtml(_list[0], _list[1:len(_list)]))
    fw.write(getTxtHtml('各样本比较组蛋白组与转录组相关性分析如下：'))
    imgs=[]
    for q in _quant:
        imgs.append([q+' 转录组与蛋白组相关性','Data/'+q+'_Correlation.jpg',q+' 转录组与蛋白组相关性#PDF'])
    fw.write(getImagesHtml(imgs))
    fw.write(getFigureLabelHtml('蛋白组与转录组相关性分析'))
    fw.write(getTitleMHtml('3.2、功能注释分析', 'up2Down2'))
    nav1=Nav('3.2、关联蛋白功能注释分析','up2Down2',True)
    nav.addC(nav1)
    fw.write(getTxtHtml('将定量得到的全部蛋白进行功能注释，探究这些蛋白的生物学功能。 包括 GO、 KEGG、 Domain、 COG、 亚细胞结构定位从不同的角度对每一个蛋白进行功能注解。'))
    fw.write(getTxtHtml('完整的所有蛋白注释表如：'+getA_Bank('Data/CombineAnnotation.xls','蛋白功能注释表')))
    fw.write(getTxtHtml('表头信息如下：<br/>'+_AnnoFunTableHeader))
    tablesBP=getDataMatrix(folder+'/BP_GOs.txt')[0]
    tablesCC=getDataMatrix(folder+'/CC_GOs.txt')[0]
    tablesMF=getDataMatrix(folder+'/MF_GOs.txt')[0]
    headerBP=['Protein ID','GO_BP_IDs','GO_BP_Descs','GO_BP_Levels']
    headerCC=['Protein ID','GO_CC_IDs','GO_CC_Descs','GO_CC_Levels']
    headerMF=['Protein ID','GO_MF_IDs','GO_MF_Descs','GO_MF_Levels']
    fw.write(getProjectGOAnnotation('3.2.1 GO 功能注释', 'up2Down21', tablesBP, tablesCC, tablesMF, headerBP, headerCC, headerMF,folder+'/Report'))
    nav1.addC(Nav('3.2.1、GO 功能注释','up2Down21',True))
    fw.write(getTitleMHtml('3.2.2、COG 功能注释','up2Down22'))
    fw.write(getTxtHtml('COG，全称是 Cluster of Orthologous Groups of proteins，由 NCBI 创建并维护的蛋白数据库，根据细菌、藻类和真核生物完整基因组的编码蛋白系统进化关系分类构建而成。通过比对可以将某个蛋白序列注释到某一个 COG 中，每一簇COG 由直系同源序列构成，从而可以推测该序列的功能。'))
    fw.write(getTxtHtml('COG 分为两类，一类是原核生物的，另一类是真核生物。原核生物的一般称为 COG 数据库；真核生物的一般称为KOG 数据库。'))
    fw.write(getTxtHtml('首先根据 Uniprot 数据库中 idmapping，根据本次鉴定到的蛋白 uniprot 编号获得相应 COG/KOG 编号，然后根据COG/KOG 数据库进行注释。 对于 idmapping 中数据不全的蛋白使用 blast 进行序列比对获得蛋白对应的 COG/KOG 编号。'))
    fw.write(getAnnoPart(getDataMatrix(folder+'/COG_ClassFuns.txt')[0], ['Protein ID','COG_Gene','BlastScore','COG_Code','COG_Desc'],folder+'/Report', 'COG', _COGTxt))
    nav1.addC(Nav('3.2.2、COG 功能注释','up2Down22',True))
    fw.write(getTitleMHtml('3.2.3、KEGG 功能注释','up2Down23'))
    fw.write(getTxtHtml('KEGG（Kyoto Encyclopedia of Genes and Genomes，京都基因和基因组百科全书，http://www.genome.jp/kegg/）是基因组破译方面的公共数据库。该数据库是系统分析基因功能、联系基因组信息和功能信息的大型知识库，其中的基因组信息主要是从 NCBI 等数据库中获得的，包括完整和部分测序的基因组序列，存储于 KEGG GENES 数据库中；更高级的功能信息包括图形化的细胞过程如代谢、膜转运、信号传递、细胞周期等，还包括同系保守的子通路等信息，存储于 KEGG PATHWAY 数据库中；此外，关于化学物质、酶分子、酶化反应等相关的信息存储于 KEGG LIGAND 数据库中。'))
    fw.write(getTxtHtml('在生物体内，基因产物并不是孤立存在地作用的，不同基因产物之间通过有序的相互协调来行使其具体的生物学功能。因此，KEGG 数据库中丰富的通路信息将有助于我们从系统水平去了解基因的生物学功能，例如代谢途径、遗传信息传递以及细胞过程等一些复杂的生物功能，这大大提高了该数据库在实际生产和应用中的价值。'))
    fw.write(getTxtHtml('首先,使用 KEGG 在线服务工具 KAAS 注释蛋白得到蛋白对应于 KEGG 数据库的 KO 编号。然后使用 KEGG 在线服务工具 KEGG mapper 将 KO 号映射到具体的代谢通路上。'))
    fw.write(getAnnoPart(getDataMatrix(folder+'/KEGG_Paths.txt')[0], ['Protein ID','KO_ID','Pathway ID','Pathway Desc'],folder+'/Report', 'KEGG', _KEGGTxt))
    nav1.addC(Nav('3.2.3、KEGG 功能注释','up2Down23',True))

    fw.write(getTitleMHtml('3.2.4、Domain 功能注释','up2Down24'))
    fw.write(getTxtHtml(_DomainTxt))
    fw.write(getTxtHtml('我们使用基 于 序 列 比 对 搜 索 InterPro 数 据 库 的 软 件 InterProScan 来 用 于 蛋 白 的 结 构 域 注 释 。InterPro(http://www.ebi.ac.uk/interpro/)是一个集成了不同蛋白质结构域和功能的数据库网站。'))
    fw.write(getAnnoPart(getDataMatrix(folder+'/Ipr_Domains.txt')[0], ['Protein ID','IPR_IDs','Domain Desc'],folder+'/Report', 'Domain',_DomainTxt ))
    nav1.addC(Nav('3.2.4、Domain 功能注释','up2Down24',True))
    
    fw.write(getTitleMHtml('3.2.5、SubcellurLocation 功能注释','up2Down25'))
    fw.write(getTxtHtml(_SubCelurTxt))
    fw.write(getTxtHtml('首先使用 worfpsort/Cello 软件对蛋白进行分析，获得每个蛋白在亚细胞水平的位置。'))
    fw.write(getAnnoPart(getDataMatrix(folder+'/SubCellur_loactions.txt')[0], ['Protein ID','SubcellurLocation'],folder+'/Report', 'SubcellurLocation', _SubCelurTxt))
    nav1.addC(Nav('3.2.5、SubcellurLocation 功能注释','up2Down25',True))
    fw.write(getTitleMHtml('3.3、关联蛋白功能富集分析','up2Down3'))
    nav2=Nav('3.3、功能富集分析','up2Down3',True)
    fw.write(getTxtHtml('对目标蛋白进行 GO、KEGG、Pathway功能显著性富集分析，可以说明目标蛋白的功能富集情况，在功能水平阐明样本间的差异。本分析使用软件 DAVID(https://david-d.ncifcrf.gov/)软件进行富集分析，使用方法为 Fisher 精确检验。 通常情况下，p 值≤0.05 了时，认为此功能节点存在显著富集情况，计算方法如下：'))
    fw.write(getTableHtml(['','目标蛋白数量','非目标蛋白数量','总和'], [['功能A','a','b','a+b'],['A以外的功能','c','d','c+d'],['总和','a+c','b+d','a+b+c+d(=n)']]))
    fw.write(getTxtHtml('Fisher 精确检验理论指出得到这一组数据的概率可以由超几何分布计算，公式如下：'))
    fw.write(getImageHtml('Fisher 精确检验公式','Fisher 精确检验公式', 'src/imgs/FisherTest.png'))
    for i in range(len(_quant)):
        nav2.addC(writeSampleEnrichment(fw, folder+'/Report', _quant[i], levels, '3.3.'+str(i+1)+''))
    nav3=Nav('3.4、功能分类分析','up2Down4',True)
    fw.write(getTitleMHtml('3.4、关联蛋白功能分类','up2Down4'))
    fw.write(getTxtHtml('对目标蛋白进行 GO Level、COG及亚细胞结构分类统计,分别从功能、进化、空间上说明目标蛋白的功能聚集情况'))
    for i in range(len(_quant)):
        nav3.addC(writeSampleClassFunction(fw, folder+'/Report', _quant[i], levels, '3.4.'+str(i+1)))
    nav4=Nav('3.5、代谢通路整合分析','up2Down5',True)
    fw.write(getTitleMHtml('3.5、代谢通路整合分析','up2Down5'))
    fw.write(getTxtHtml('当得到了很多的代谢通路时，可以从系统生物学的角度对各个代谢通路整合分析用来观察感兴趣的蛋白在整个系统的代谢途径的变化'))
    fw.write(getTxtHtml('图中颜色分别与各个状态的字体颜色对应如：<strong style="color:#CC3300">UU</strong>,<strong style="color:#996600">UD</strong>,<strong style="color:#9999FF">UN</strong>,<strong style="color:#0066CC">DU</strong>,<strong style="color:#339933">DD</strong>,<strong style="color:#663366">DN</strong>,<strong style="color:#FFCC99">NU</strong>,<strong style="color:#99CC00">ND</strong>'))
    for i in range(len(_quant)):
        nav4.addC(Nav('3.5.'+str(i+1)+'、'+_quant[i],'up2Down5'+str(i+1),True))
        fw.write(getTitleHtml('3.5.'+str(i+1)+'、'+_quant[i]+'代谢通路整合分析', 'up2Down5'+str(i+1)))
        fw.write(getIpath2Report('Data/'+_quant[i]+'/iPath2'))
    fw.write('</section>')
    nav.addC(nav2)
    nav.addC(nav3)
    nav.addC(nav4)
    return nav

def writeSampleClassFunction(fw,folder,sample,levels,_id):
    fw.write(getTitleMHtml(_id+'、'+sample+'功能分类统计','up2Down'+_id.replace('.','',100)))
    nav=Nav(_id+'、'+sample+'','up2Down'+_id.replace('.','',100),True)
    for l in range(len(levels)):
        nav1=Nav(_id+'.'+str(l+1)+'、'+levels[l]+'', (_id+'.'+str(l+1)).replace('.','',100),True)
        fw.write(getSampleRegulatedClassFunctionReport(folder, sample, levels[l],_id+'.'+str(l+1)))
        nav.addC(nav1)
    return nav    
    
def writeSampleEnrichment(fw,folder,sample,levels,_id):
    fw.write(getTitleMHtml(_id+'、'+sample+'功能富集分析','up2Down'+_id.replace('.','',100)))
    nav=Nav(_id+'、'+sample+'','up2Down'+_id.replace('.','',100),True)
    for l in range(len(levels)):
        nav1=Nav(_id+'.'+str(l+1)+'、'+levels[l]+'', (_id+'.'+str(l+1)).replace('.','',100),True)
        fw.write(getSampleRegulatedEnrichReport(folder, sample, levels[l],_id+'.'+str(l+1)))
        nav.addC(nav1)
    nav1=Nav(_id+'.'+str(len(levels)+1)+'、富集聚类分析', (_id+'.'+str(len(levels)+1)).replace('.','',100),True)
    fw.write(getTitleHtml(_id+'.'+str(len(levels)+1)+'、富集聚类分析', (_id+'.'+str(len(levels)+1)).replace('.','',100)))
    fw.write(getTxtHtml('在不同组别或者不同样品处理得到了不同的差异蛋白，富集到了许多的生物学途径或者通路中，为了进一步比较不同处理的样本在生物学途径或通路中的异同，使用差异蛋白的富集结果进行整合，使用 hcluster 进行聚类分析，观察不同实验处理条件下，差异表达蛋白相关功能的相同与不同之处。将所有类目下的富集分析结果进行合并做功能富集聚类分析，结果如下：'))
    _imgs=[]
    for c in ['KEGG','Domain','GO_CC','GO_BP','GO_MF']:    
        _imgs.append([c+'富集功能聚类','Data/'+sample+'/'+c+'_Cluster.jpg',c+'富集功能聚类#PDF'])
    fw.write(getImagesHtml(_imgs))
    fw.write(getFigureTxtHtml('注：图中使用的是显著性p值作为聚类矩阵的数值，并做了-log10转换，灰色区域为目标蛋白在该功能节点上未富集到'))
    nav.addC(nav1)
    return nav
if __name__ == '__main__':
    pass