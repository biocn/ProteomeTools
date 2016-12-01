# -*- coding:utf-8 -*-
'''
Created on 2016��10��26��

@author: Administrator
'''
_GOTxt='GO数据库是GO组织（Gene Ontology Consortium）于2000年构建的一个结构化的标准生物学注释系统，旨在建立基因及其产物知识的标准词汇体系，适用于各个物种。GO注释系统是一个有向无环图，包含三个主要分支，即：生物学过程（Biological Process），分子功能（Molecular Function）和细胞组分（Cellular Component）。'
_GOTxtMathodP1='利用 GO 数据库，可以将基因按照其参与的生物过程（Biological Process, BP）、细胞组分（Cellular Component,CC），分子功能（Molecular Function, MF）三个方面进行分类注释。在这三个大分支下面又分很多小层级（level），level级别数字越大，功能越细致。最顶层的三大分支视为 level1，之后的分级依次为 level2，level3 和 level4。因此 GO 注释有助于了解基因背后所代表的生物学意义。通过 GO 分类图，可以大致了解某个物种的全部基因产物的分类情况。'
_GOTxtMathodP2='蛋白的 GO 注释信息主要来源于 UniProt-GOA 数据库(www. http://www.ebi.ac.uk/GOA/). 首先, 将蛋白的 ID 转换为 UniProtKB 数据库的 ID 然后根据 UniProKB 的 ID 在 UniProt-GOA 中找到对用的 GO 注释信息。如果有一些鉴定的蛋白在数据库中没有被注释到，将使用 InterProScan 同序列比对的方法去注释蛋白的 GO 分类。'
_TopGOTxt='对样品间差异基因进行富集分析，富集到的Term做topGO有向无环图。topGO有向无环图能直观展示差异表达蛋白富集的GO节点（Term）及其层级关系，是差异表达蛋白GO富集分析的结果图形化展示，分支代表包含关系，从上至下所定义的功能描述范围越来越具体。差异表达蛋白的topGO有向无环图如下：'
_TopGOLabel='注：对每个GO节点进行富集，最显著的前20个（显著的少于20个则全部列出）节点在图中用方框表示，图中还包含其各层对应关系。每个方框（或椭圆）内给出了该GO节点的内容描述和富集显著性值。不同颜色代表不同的富集显著性，颜色越深，显著性越高。'
_COGTxt='COG（Cluster of Orthologous Groups of proteins）数据库是基于细菌、藻类、真核生物的系统进化关系构建得到的，利用COG数据库可以对基因产物进行直系同源分类。'
_COGLabel='注：横坐标为COG各分类内容，纵坐标为蛋白数目。在不同的功能类中，蛋白所占多少反映对应时期和环境下代谢或者生理偏向等内容，可以结合研究对象在各个功能类的分布做出科学的解释。'
_KEGGTxt='在生物体内，不同的基因产物相互协调来行使生物学功能，对差异表达蛋白的通路（Pathway）注释分析有助于进一步解读蛋白的功能。KEGG（Kyoto Encyclopedia of Genes and Genomes）是系统分析基因功能、基因组信息数据库，它有助于研究者把基因及表达信息作为一个整体网络进行研究。作为是有关Pathway的主要公共数据库(Kanehisa,2008），KEGG提供的整合代谢途径 (pathway)查询，包括碳水化合物、核苷、氨基酸等的代谢及有机物的生物降解，不仅提供了所有可能的代谢途径，而且对催化各步反应的酶进行了全面的注解，包含有氨基酸序列、PDB库的链接等等，是进行生物体内代谢分析、代谢网络研究的强有力工具。'
_KEGGLabel='注：相对于对照组来说，红色框标记的酶与目标蛋白（上下调富集分析中则为上调蛋白）有关，上下调富集分析中绿色框标记的酶与下调蛋白有关。一半绿色一半红色框标记的酶与上调和下调蛋白均有关，蓝色框标记的酶表示在本次实验中被鉴定到，框内的数字代表酶的编号（EC number），而整个通路由多种酶催化的复杂生化反应构成，此通路图中与差异表达蛋白相关的酶均用不同的颜色标出，根据研究对象间的差异，重点研究某些代谢通路相关的差异表达情况，通过通路解释表型差异的根源。'
_VocanoLabel='注：差异表达火山图中的每一个点表示一个蛋白，横坐标表示某一个蛋白在两样品中表达量差异倍数的对数值；纵坐标表示蛋白表达量变化的统计学显著性的负对数值。横坐标绝对值越大，说明表达量在两样品间的表达量倍数差异越大；纵坐标值越大，表明差异表达越显著，筛选得到的差异表达蛋白越可靠。图中蓝色的点代表差异表达蛋白，红色的点代表非差异表达蛋白。'
_GoEnrichmentLebel=''
_AnnoFunTableHeader='BP_GO_ID=Biological Process GO ID<br/>BP_GO_Desc=Biological Process GO 描述<br/>BP_GO_Level=Biological Process GO 层次<br/>CC_GO_ID=Cellular Component GO ID<br/>CC_GO_Desc=Cellular Component 描述<br/>CC_GO_Level=Cellular Component 层次<br/>MF_GO_ID=Molecular Function GO ID<br/>MF_GO_Desc=Molecular Function 描述<br/>MF_GO_Level=Molecular Function 层次<br/>KEGG_KO=KEGG KO数据库ID<br/>KEGG_Pathway_ID=KEGG Pathway ID<br/>KEGG_Pathway_Desc=KEGG Pathway 描述<br/>Domain_ID=IPR 结构域数据库ID<br/>Domain_Desc==IPR 结构域描述<br/>SubcellurLocation=亚细胞结构<br/>COG_Gene=COG/KOG基因ID<br/>BlastScore=蛋白与该COG/KOG的比对得分<br/>COG_Code=COG/KOG的编码<br/>COG_Desc=COG/KOG 描述'
_DomainTxt='蛋白质结构域是在进化上非常保守的一段蛋白序列、结构或者功能独立存在的其他蛋白质链。每个结构域形成一个紧凑的三维结构,通常可以独立稳定和折叠。许多蛋白质包含多个结构域。一个结构域可能出现在各种不同的蛋白质。分子进化使用结构域作为构建块,这些可能在不同的排列来创建重组蛋白与不同的功能。域的长度约在 25 个氨基酸和 500 个氨基酸长度之间。'
_SubCelurTxt='亚细胞结构定位分析是指某种蛋白或表达产物在细胞内的具体存在部位，从蛋白质在空间上的位置来分析系统生物学功能为实验设计提供参考。'
_EnrichTabelTxt='表中Category_ID为相关功能ID,Category_Name为相关功能描述，DiffMapping为目标蛋白在该功能分类中的数目，ProteinMapping为鉴定到的蛋白在该分类中的数目，DiffNum为目标蛋白在该所有功能分类中的数目，ProteinNum为鉴定到的蛋白在所有分类中的数目，FoldEnrichment为目标蛋白在该功能分类中的比例与所有鉴定到的蛋白在该分类上的比例，Fisher\'s exact text p value为Fisher精确检验p值'
_EnrichPlotTxt='注：图中每个实心圈为一个 功能 term，横坐标表示term富集的显著性 p 值，该值取了-log10，值越大表示越富集；纵坐标表示 Term的名称。实心圈的大小表示该 Term下的目标蛋白个数，圈越大表示包含目标蛋白个数越多；实心圈的颜色表示该 Term的富集倍数（算法如下：如果DiffMapping=a; ProteinMapping=b; DiffNum=c; ProteinNum=d; 那么 fold enrichment = (a/c)/(b/d)）,颜色越红表示富集倍数越大；图中可以从三个方面来对比每一个 功能Term的重要性。'
if __name__ == '__main__':
    pass