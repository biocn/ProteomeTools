'''
Created on 2016-5-19

@author: Administrator
'''
from os.path import os
import shutil

from PIL import Image

from com.zlf.domain.net.KeggDownload import getPathwayList
import pandas as pd
from com.zlf.beans.Global import _KEGGFolder



def getConf(path):
    f=open(path,'r')
    _all=f.readlines()
    f.close()
    
    _koPois={}
    for line in _all:
        cols=line.rstrip().lstrip('\n').split('\t')
        if(cols[0]=='rect'):
            _koPois[cols[1]]=cols[2]
    return _koPois

def getColor(kos,colors):
    _kos=kos.split(',')
    _color={}
    _red=None
    _green=None
    _blue=None
    _yellow=None
    for ko in _kos:
        if colors.has_key(ko):
            if colors[ko]=='yellow':
                _yellow=colors[ko]
            elif colors[ko]!='blue':
                if not _red and (not _green or _green!=colors[ko]):
                    _red=colors[ko]
                elif _red and not _green and _red!=colors[ko]:
                    _green=colors[ko]
            else:
                _blue=colors[ko]
    if _yellow:
        return ['red','green']
    if _red:
        if _green:
            return [_red,_green]
        else:
            return [_red]
    elif _green:
        return [_green]
    elif _blue:
        return [_blue]
    return None

def plotPathway(_frame,_colorMap,folder):
    for i in _frame.index:
        if _frame['FisherExact'][i]<0.05:
            koPath=_frame['Category'][i][0:_frame['Category'][i].find('~')]
            _frame['IdentifyProteinIDs'][i]
            _frame['MappingProteinIDs'][i]
            try:
                os.makedirs(folder+'/img')
            except:
                pass
            copyPathwayHtml(koPath,folder)
            saveImg(koPath, _colorMap,folder+"/img/"+koPath+'.png')
            
            
def parseColor(color):
    if color=='red':
        return (255,0,0)
    if color=='green':
        return (0,255,0)
    if color=='blue':
        return (0,0,255)
    return (255,255,255)

def plotLine(x1,y1,x2,y2,_im,_color):
    if x1==x2:
        for i in range(y1,y2):
            _im.putpixel((x1,i),parseColor(_color))
    elif y1==y2:
        for i in range(x1,x2):
            _im.putpixel((i,y1),parseColor(_color))
    else:
        for i in range(x1,x2):
            _im.putpixel((i,(x2-x1)*i/(y2-y1)),parseColor(_color))    
    
def saveImg(koMap,colors,outPath):
    _koPois=getConf(_KEGGFolder+'/conf/'+koMap+'.conf')
    _im=Image.open(_KEGGFolder+'/img/'+koMap+'.png')
    for _kop in _koPois:
        _pos=_kop.split(',')
        x1=int(_pos[0])
        y1=int(_pos[1])
        x2=int(_pos[2])
        y2=int(_pos[3])
        if colors:
            _cors=getColor(_koPois[_kop], colors)
            if _cors and len(_cors)>1:
                plotLine(x1, y1, x2, y1, _im, _cors[0])
                plotLine(x1, y1+1, x2, y1+1, _im, _cors[0])
                
                plotLine(x1, y1, x1, (y1+y2)/2, _im, _cors[0])
                plotLine(x1+1, y1, x1+1, (y1+y2)/2, _im, _cors[0])

                plotLine(x2, y1, x2, (y1+y2)/2, _im, _cors[0])
                plotLine(x2-1, y1, x2-1, (y1+y2)/2, _im, _cors[0])
 
                plotLine(x1, y2, x2+1, y2, _im, _cors[1])
                plotLine(x1, y2-1, x2+1, y2-1, _im, _cors[1])
                
                plotLine(x1+1, (y1+y2)/2, x1+1, y2, _im, _cors[1])
                plotLine(x1, (y1+y2)/2, x1, y2, _im, _cors[1])
                
                plotLine(x2, (y1+y2)/2, x2, y2, _im, _cors[1])
                plotLine(x2-1, (y1+y2)/2, x2-1, y2, _im, _cors[1])
            elif _cors:
                plotLine(x1, y1, x2, y1, _im, _cors[0])
                plotLine(x1, y1, x1, y2, _im, _cors[0])
                plotLine(x1, y2, x2+1, y2, _im, _cors[0])
                plotLine(x2, y1, x2, y2, _im, _cors[0])  
                
                plotLine(x1, y1+1, x2, y1+1, _im, _cors[0])
                plotLine(x1+1, y1, x1+1, y2, _im, _cors[0])
                plotLine(x1, y2-1, x2+1, y2-1, _im, _cors[0])
                plotLine(x2-1, y1, x2-1, y2, _im, _cors[0])  
        else:
            plotLine(x1, y1, x2, y1, _im, 'blue')
            plotLine(x1, y1, x1, y2, _im, 'blue')
            plotLine(x1, y2, x2+1, y2, _im, 'blue')
            plotLine(x2, y1, x2, y2, _im, 'blue')
            
            plotLine(x1, y1+1, x2, y1+1, _im, 'blue')
            plotLine(x1+1, y1, x1+1, y2, _im, 'blue')
            plotLine(x1, y2-1, x2+1, y2-1, _im, 'blue')
            plotLine(x2-1, y1, x2-1, y2, _im, 'blue')
    _im.save(outPath,"png")        

def getKoMap():
    f=open(_KEGGFolder+'/KO2Map.txt','r')
    lines=f.readlines()
    f.close()
    _map={}
    for line in lines:
        cols=line.lstrip().rstrip('\n').split('\t')
        _map[cols[0]]=cols[1]
    return _map

def getInterceptedPathway(osas):
    _list=osas.split(',')
    allPathWays=[]
    for osa in _list:
        allPathWays=allPathWays+getPathwayList(osa)
    return set(allPathWays)

def getPathwayDesc():
    f=open(_KEGGFolder+'/pathway.txt','r')
    lines=f.readlines()
    f.close()
    _map={}
    for line in lines:
        cols=line.rstrip().lstrip('\n').split('\t')
        _map[cols[0]]=cols[1]
    return _map

def proteinMappingPathway(prot_koList,koMap,outPath,osas=None):
    fter=None
    if osas:
        fter=getInterceptedPathway(osas);
    fw=open(outPath,'w')
    _pathDescMap=getPathwayDesc()
    for cols in prot_koList:
        fw.write(cols[0]+'\t'+cols[1])
        if koMap.has_key(cols[1]):
            _pathways=koMap[cols[1]].rstrip(';').lstrip(';').split(';')
            _list=[]
            if fter:
                for pathway in _pathways:
                    if pathway[3:len(pathway)] in fter:
                        _list.append(pathway)
            else:
                _list=_pathways
            pathAll=''
            pathDescAll=''
            for m in _list:
                pathAll=pathAll+m+';'
#                 print m
                pathDescAll=pathDescAll+_pathDescMap[m]+';'
            fw.write('\t'+pathAll+'\t'+pathDescAll+'\n')
        else:
            fw.write('\n')
    fw.close()

def copyPathwayHtml(_koName,_outFolder):
    shutil.copy(_KEGGFolder+'/'+_koName+'.html',_outFolder+'/'+_koName+'.html')  


def getKEGGPathData(folder):
    data=pd.read_table(folder+'/KEGG_Paths.txt',header=-1,error_bad_lines=False)
    data=data.fillna('NA')
#     print data[3]
    data=data[(data[3]!='NA')]
    _mapIterm={}
    dataLength=0
    for i in range(len(data[0:len(data)])):
        if data.iloc[i][2]>0:
            dataLength=dataLength+1
            gos=data.iloc[i][2].split(';')
            goDescs=data.iloc[i][3].split(';')
            for j in range(len(gos)):
                iterm=(gos[j]+'~'+goDescs[j].lstrip('"').rstrip('"'))
                if _mapIterm.has_key(iterm):
                    _mapIterm[iterm].append(data.iloc[i][0])
                else:
                    _mapIterm[iterm]=[data.iloc[i][0]]
    return {'data':data,'Num':dataLength,'iterms':_mapIterm}

# def postKAAS(_path):
    
                    
if __name__ == '__main__':
#     _colors={}
#     _colors['K00658']='blue'
#     _colors['K00164']='green'
#     _colors['K00382']='red'
#     _colors['K01899']='green'
#     _colors['K01900']='red'
#     saveImg("map00020", _colors, keggPathFolder+"test/map00020_1.png")
    folder='E:/Work/MH/MH-T16052203/New'
#     proteinMappingPathway(folder+'/query.ko.txt',getKoMap(), folder+'/KEGG_Paths.txt', 'mmu') 
    pass


