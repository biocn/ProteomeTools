# -*- coding:utf-8 -*-
from __main__ import time
from os.path import os
import sys

import requests


reload(sys)
sys.setdefaultencoding('utf-8')
'''
Created on 2016-10-16

@author: Administrator
'''
#In order to make the functional categories more understandable, 
#terms were clustered according to their functional similarity using REVIGO

def getPostHeader(_path):
    f=open(_path,'r')
    lines=f.readlines()
    f.close()
    text=''
    for line in lines:
        cols=line.rstrip('\n').split('\t')
        text=text+cols[0]+'\t'+cols[7]+'\n'
    if len(lines)>3:
        return {'goList':text,'cutoff':0.7,'isPValue':'yes','goSizes':0,'measure':'SIMREL'}   
    else:
        return None
    #return {'outputListSize':'medium','isPValue':'yes','goSizes':'UniProt','measure':'SIMREL','inputGoList':text,'whatIsBetter':'higher'}

#获取R数据集合
def getRData(text):
    text=text[text.find('rbind(c("')+8:len(text)]
    text=text[0:text.find(');')+1]
    lines=text.lstrip().rstrip().split('\n')
    txt=''
    for line in lines:
        if line.lstrip().rstrip('\n').find('GO:')>0:
            line=line.lstrip('c(').rstrip('\n').rstrip(',').rstrip('\n').rstrip('\r')
#             print line
            start=False
            l=[]
            col=''
            for i in range(len(line)):
                if not start and line[i:i+1]==',':
                    if col.find('(')==-1 and col.find(')')>0:
                        col=col[0:col.find(')')]
                    l.append(col.rstrip('"').lstrip('"').rstrip('\n').rstrip('\r'))
                    col=''
                else:
                    col=col+line[i:i+1]
                if line[i:i+1]=='"' and not start:
                    start=True
                elif line[i:i+1]=='"' and start:
                    start=False
            if col!='' and col!='\n' and col!='\r':
                if col.find('(')==-1 and col.find(')')>0:
                    col=col[0:col.find(')')]
                l.append(col.rstrip('"').lstrip('"').rstrip('\n').rstrip('\r'))
            txt=txt+'\t'.join(l)+'\n'
    return txt

#提交数据到REVIGO
def postAndSaveR(folder,enricName):
    if os.path.exists(folder+'/'+enricName+'.treemap.txt') and os.path.exists(folder+'/'+enricName+'.base.txt') and os.path.exists(folder+'/'+enricName+'.xgmml'):
        return
    postData=getPostHeader(folder+'/'+enricName+'.txt')
    if postData:
        _session = requests.Session()
        r = _session.post("http://revigo.irb.hr/revigo.jsp", data=postData)
        print '-----------------1'
        time.sleep(10)
        r1=_session.get('http://revigo.irb.hr/toR_treemap.jsp?table=1')
        fw=open(folder+'/'+enricName+'.treemap.txt','w')
        fw.write("term_ID\tdescription\tfreqInDbPercent\tabslog10pvalue\tuniqueness\tdispensability\trepresentative\n")
        fw.write(getRData(r1.text))
        fw.close();
        print '-----------------2'
        time.sleep(10)
        r2=_session.get('http://revigo.irb.hr/toR.jsp?table=1')
        fw=open(folder+'/'+enricName+'.base.txt','w')
        fw.write("term_ID\tdescription\tfrequency_%\tplot_X\tplot_Y\tplot_size\tlog10_p_value\tuniqueness\tdispensability\n")
        fw.write(getRData(r2.text))
        fw.close()
        print '-----------------3'
        html=r.text
        html=html[html.find('href="download.jsp?filename=')+6:len(html)]
        html=html[0:html.find('">')]
        time.sleep(10)
        r3=_session.get('http://revigo.irb.hr/'+html)
        fw1=open(folder+'/'+enricName+'.xgmml','w')
        fw1.write(r3.text)
        fw1.close()
        print '-----------------4end'

def postAll(folder,quant):
    for q in quant:
        lev=q.replace('/','-vs-') 
        postAndSaveR(folder+'/'+lev, 'All_GO_BP_Enrich')
        postAndSaveR(folder+'/'+lev, 'Up_GO_BP_Enrich')
        postAndSaveR(folder+'/'+lev, 'Down_GO_BP_Enrich')
        postAndSaveR(folder+'/'+lev, 'All_GO_CC_Enrich')
        postAndSaveR(folder+'/'+lev, 'Up_GO_CC_Enrich')
        postAndSaveR(folder+'/'+lev, 'Down_GO_CC_Enrich')
        postAndSaveR(folder+'/'+lev, 'All_GO_MF_Enrich')
        postAndSaveR(folder+'/'+lev, 'Up_GO_MF_Enrich')
        postAndSaveR(folder+'/'+lev, 'Down_GO_MF_Enrich')
        
if __name__ == '__main__':
#     _session = requests.Session()
    
    folder='E:/Work/MH/MHT12A/Result2/UBE2V2-vs-NC1'
#     postAndSaveR(folder,'Up_GO_CC_Enrich')
#     r = _session.post("http://revigo.irb.hr/revigo.jsp", data=getPostHeader(folder+'/Up_GO_CC_Enrich.txt'))
#     html=r.text
#     fw=open(folder+'/0A_REVIGO.html','w')
#     fw.write(html)
#     fw.close()
#     print '-----------------'
#     r1=_session.get('http://revigo.irb.hr/toR_treemap.jsp?table=1')
#     print r1.text
    

    
    
    
    