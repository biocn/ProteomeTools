# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��10��24��

@author: Administrator
'''
from HTMLParser import HTMLParser

import requests

from com.zlf.beans.Global import _AminoSet, _NucleSet
from com.zlf.domain.utils.FastaOpertor import extractProteinID
from com.zlf.domain.utils.FileOpertor import getLines


#解析Cello结果页面
class MyHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.isTable=''
        self.isTR=''
        self.isTD=''
        self._list=[]
        self._lines=[]
        self._cello=[]
        self.title=''
    def handle_starttag(self,tag,attrs):
        if tag=='table':
            for name,value in attrs:
                if name=='border' and value=='0':
                    self.isTable=1
        if tag=='td' and self.isTable==1:
                self.isTD=1
        if tag=='tr' and self.isTable==1:
            self.isTR=1
            
            
    def handle_endtag(self, tag):
        if tag=='table' and self.isTable==1:
            self.isTable=''
            self.isTR=''
            self.isTD=''
        if self.isTR==1 and tag=='tr':
            if self._cello==1 and len(self._list)==3:
                if self._list[-1].find('*')>-1:
                    self._lines.append((self._list,self.title))
            self._list=[]
        if self.isTD==1 and tag=='td':
            if len(self._list)>0:
                if self._list[-1].find('CELLO Prediction:')!=-1:
                    self._cello=1
                elif self._list[-1].find('**************************')!=-1:
                    self.title=''
                    self._cello=''
                elif self._list[-1].find('SeqID:')!=-1:
                    self.title=self._list[-1]
            self.isTD=''
             
    def handle_data(self, data):
        if self.isTable==1 and self.isTR and self.isTD:
            self._list.append(data.rstrip(' ').lstrip(' ').rstrip('\n').lstrip('\n').rstrip('\t').lstrip('\t').rstrip(' ').lstrip(' '))
    
    def getLines(self):
        _lines=[]
        _map={}
        for line in self._lines:
            txt=line[1][line[1].find('SeqID:')+6:len(line[1])].lstrip().rstrip()
            txt=txt[0:txt.find(' ')].lstrip().rstrip()
            if _map.has_key(extractProteinID(txt)):
                _map[extractProteinID(txt)]=_map[extractProteinID(txt)]+','+line[0][0]
            else:
                _map[extractProteinID(txt)]=line[0][0]
        for key in _map:
            _lines.append(key+'\t'+_map[key])
        return _lines

#原核使用该方法进行亚细胞结构定位预测,gram为True则革兰仕阳性，阴性则为false
def getPostHeaders(_fasta,gram=True):
    lines=getLines(_fasta)
    text=''
    pro=False
    ii=1
    _lis=[]
    for line in lines:
        if line.find('>')==-1 and not pro:
            for i in range(len(line.rstrip('\n').rstrip('\r'))):
                if line[i:i+1] in _AminoSet and line[i:i+1] not in _NucleSet:
                    pro=True
                    break
        if line.find('>')==0:
            ii=ii+1
            if ii%101==0:
                _lis.append(text)
                text=''
        text=text+line
    if text!='':
        _lis.append(text)
    _maps=[]
    for txt in _lis:
        _map={'fasta':txt}
        _map['Submit']='Submit'
        if pro:
            _map['seqtype']='prot'
        else:
            _map['seqtype']='dna'
        if gram:
            _map['species']='gramp'
        else:
            _map['species']='pro'
        _maps.append(_map)
    return _maps

#向Cello提交数据
def postCello(_fasta,gram):
    postDatas=getPostHeaders(_fasta,gram)
    _lines=[]
    for postData in postDatas:
        _session = requests.Session()
        r = _session.post("http://cello.life.nctu.edu.tw/cgi/main.cgi", data=postData)
        parser=MyHTMLParser()
        parser.feed(r.text)
        _query=parser.getLines()
        _lines.extend(_query)
        print 'successful:'+str(len(_lines))
    return _lines
#http://cello.life.nctu.edu.tw/cgi/main.cgi
if __name__ == '__main__':
    _lines=postCello('E:/Work/MH/MH-B16061603/ProteinTrans/identify.fasta', False)
    fw=open('E:/Work/MH/MH-B16061603/ProteinTrans/worf.clear','w')
    fw.write('\n'.join(_lines))
    fw.close()

