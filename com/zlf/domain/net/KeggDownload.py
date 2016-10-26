'''
Created on 2016-5-16

@author: Administrator
'''

import cookielib
import re
import urllib
import urllib2

from com.zlf.beans.Global import _KEGGFolder

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImageMapConf(html,confOutFile):
    _map= html[html.find('<map'):html.find('</map>')]
    _list=_map.split("/>")
    f=open(confOutFile,'w')
    num=0
    for line in _list:
        _aera=line[line.find('<area')+6:len(line)]
        _coords=_aera[_aera.find('coords=')+7:_aera.find('href=')].rstrip().lstrip().lstrip('    ')
        _shape=_aera[_aera.find('shape=')+6:_aera.find('coords=')].rstrip().lstrip().lstrip('    ')
        _href=_aera[_aera.find('href="')+6:_aera.find('title=')].rstrip().lstrip().lstrip('    ').lstrip('"')
        _hrefs=_href[_href.find('?')+1:_href.find('"')].split('+')
        _kos=[]
        for _hr in _hrefs:
            if _hr.find('K')==0:
                _kos.append(_hr)
        if len(_kos)>0:        
            f.write(_shape+'\t'+_coords+'\t'+str(','.join(_kos))+'\n')
            num=num+1
    f.close()
    if num==0:
        print confOutFile
    
def parseMapPathway():
    html = getHtml("http://rest.kegg.jp/list/pathway")
    _maps=html.split('path:')
    _list=[]
    for _map in _maps:
        if _map.find('map')==0:
            _list.append(_map[0:8])        
    return _list
    
def getImg(html):  
    reg = r'src="(.+?\.png)" pic_ext'  
    imgre = re.compile(reg)  
    imglist = imgre.findall(html)  
    x = 0  
    print imglist
    for imgurl in imglist:  
        urllib.urlretrieve(imgurl,'%s.png' % x)  
        x = x + 1    
def downloadImg(_url,outPath):
    cj=cookielib.LWPCookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    req=urllib2.Request(_url)
    operate=opener.open(req)
    data=operate.read()
    f=open(outPath, "wb")
    f.write(data)
    f.flush()
    f.close()

def downPathwayHtml(html,outPath):
    html=html.replace('/Fig/bget/kegg3.gif','http://www.kegg.jp/Fig/bget/kegg3.gif')
#     html=html.replace('/Fig/bget/button_Hb.gif','http://www.kegg.jp/Fig/bget/button_Hb.gif')
    
    html=html.replace('/js/dhtml.js','http://www.kegg.jp/js/dhtml.js')
    html=html.replace('/Fig/bget/button','http://www.kegg.jp/Fig/bget/button',10)
    
    html=html.replace('href="/','href="http://www.kegg.jp/',100)
    html=html.replace("'/kegg","'http://www.kegg.jp/kegg",100)
    html=html.replace('"/kegg','"http://www.kegg.jp/kegg',100)
    
    html=html.replace('href="/dbget-bin','href="http://www.kegg.jp/dbget-bin',10000)
    html=html.replace('http://www.kegg.jp/kegg/pathway/map/','img/')
    
    f=open(outPath,'w')
    f.write(html)
    f.close()

def downLoadKO(html,_path):    
    f=open(_path,'w')
    for line in html.split('\n'):
        if line.find('ko:')>0:
            f.write(line[line.find('ko:')+3:len(line)]+'\n')
    f.close()
def getKOList(html):
    _list=[]
    for line in html.split('\n'):
        if line.find('ko:')>0:
            _list.append(line[line.find('ko:')+3:len(line)])
    return _list

def getPathwayList(osa):
    html = getHtml("http://rest.kegg.jp/list/pathway/"+osa)
    _list=[]
    for line in html.split('\n'):
        if line.find('path')==0:
            _list.append(line[line.find(osa)+len(osa):line.find(osa)+len(osa)+5])
    return _list
        
if __name__ == '__main__':
    _maps=parseMapPathway()
    flag=None
    _mapKO={}
    for _map in _maps:
        html = getHtml("http://rest.kegg.jp/link/ko/"+_map)
        _list=getKOList(html)
        for ko in _list:
            if _mapKO.has_key(ko):
                _mapKO[ko].append(_map)
            else:
                _mapKO[ko]=[_map]
    f=open(_KEGGFolder+'/KO2Map.txt','w')
    for key in _mapKO:
        f.write(key+'\t')
        for pathway in _mapKO[key]:
            f.write(pathway+';')
        f.write('\n')
    f.close()
    
    
    
    