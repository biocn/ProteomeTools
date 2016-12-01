# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��10��24��

@author: Administrator
'''
from HTMLParser import HTMLParser

import requests

from com.zlf.beans.Global import _AminoSet, _NucleSet
from com.zlf.domain.utils.FileOpertor import getLines
import urllib2
from os.path import os
from com.zlf.domain.utils.FastaOpertor import extractProteinID

#解析KAAS结果页面
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isTable=''
        self.isTR=''
        self._list=[]
        self._lines=[]
        self._as=[]
    def handle_starttag(self,tag,attrs):
        if tag=='table':
            for name,value in attrs:
                if name=='border' and value=='0':
                    self.isTable=1
        if tag=='a' and self.isTable==1:
            for name,value in attrs:
                if name=='href':
                    self._as.append(value)
        if tag=='tr' and self.isTable==1:
            self.isTR=1
            
            
    def handle_endtag(self, tag):
        if tag=='table' and self.isTable==1:
            self.isTable=''
            self.isTR=''
        if self.isTR==1 and tag=='tr':
            self._lines.append((self._list,self._as))
            self._list=[]
            self._as=[]
            
    def handle_data(self, data):
        if self.isTable==1:
            self._list.append(data.rstrip(' ').lstrip(' ').rstrip('\n').lstrip('\n').rstrip('\t').lstrip('\t').rstrip(' ').lstrip(' '))
    
    def getLines(self):
        _queryList=[]
        for line in self._lines:
            if len(line[1])==3 and line[1][2].find('query.ko')>0:
                _queryList.append(line[1][2])
            else:
                _queryList.append('None')
        return _queryList

#构造post 头信息
def getPostHeader(_path,orgs):
    lines=getLines(_path)
    text=''
    pro=False
    for line in lines:
        if line.find('>')==-1 and not pro:
            for i in range(len(line.rstrip('\n').rstrip('\r'))):
                if line[i:i+1] in _AminoSet and line[i:i+1] not in _NucleSet:
                    pro=True
                    break
        text=text+line
    _map={'continue':1,'prog':'BLAST','uptype':'q_text','text':text,'qname':'query','mail':'zhurangfei@126.com'
                ,'dbmode':'manual','org_list':orgs,'way':'b','mode':'compute'}   
    if not pro:
        _map['peptide1']='n'
    return _map

#获取对应KAAS结果的链接，未完成则返回None
def getStatus(reversedInd):
    _url='http://www.genome.jp/kaas-bin/kaas_main?mode=user&mail=zhurangfei@126.com'
    content = urllib2.urlopen(_url).read()
    parser=MyHTMLParser()
#     print content
    parser.feed(content)
    _query=parser.getLines()
    return _query[reversedInd]

#向KAAS获取数据，当前folder文件夹无query.ko则进行获取，reversedInd表示顺序第几个
def getQueryKO(folder,reversedInd):
    if os.path.exists(folder+'/query.ko'):
        return True    
    _url=getStatus(reversedInd)
    if _url!='None':
        _url='http://www.genome.jp'+_url
        content = urllib2.urlopen(_url).read()
        fw=open(folder+'/query.ko','w')
        for line in content.split('\n'):
            cols=line.split('\t')
            if len(cols)==2:
                cols[0]=extractProteinID(cols[0])
                fw.write(cols[0]+'\t'+cols[1]+'\n')
        fw.close()
        return True
    else:
        return None

#向KAAS提交数据
def postKAAS(_fasta,orgs='mmu,hsa'):
    postData=getPostHeader(_fasta,orgs)
    _session = requests.Session()
    r = _session.post("http://www.genome.jp/kaas-bin/kaas_main", data=postData)
    if r.text.find('Accepted</p>')>0:
        print 'post successful,please open:http://www.genome.jp/kaas-bin/kaas_main?mode=user&mail=zhurangfei@126.com'
    else:
        print 'post fail'

if __name__ == '__main__':
    
#     postKAAS('E:/Work/MH/MH-B16061603/ProteinTrans/identify.fasta', 'aha')
    pass



