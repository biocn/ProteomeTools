# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��12��2��

@author: Administrator
'''
from math import radians
import math

from reportlab.graphics import renderPDF, renderPM
from svg2rlg import svg2rlg
import svgwrite

from com.zlf.domain.utils.FileOpertor import getDataMatrix


class EnrichBarGO(object):
    #data={'BP':[[]],'MF':[[]],'CC':[[]]}
    def __init__(self,data,header):
        self._range=30
        self.data=data
        self.colors=['#996600','#9999FF','#339933']
        self.tNum=len(self.data['BP'])+len(self.data['CC'])+len(self.data['MF'])
        self.header=header
        self.span=5
        self.span1=3
    
    def formatData(self):
        _list=[]
        _list.extend(self.data['CC'])
        _list.extend(self.data['MF'])
        _list.extend(self.data['BP'])
        return _list
    
    def xAxisPlot(self,dwg,x,y,y1,w,_list):
        dwg.add(dwg.line((x, y), (x+w, y), stroke=svgwrite.rgb(10, 10, 16, '%')))
        dwg.add(dwg.line((x, y1), (x+w, y1), stroke=svgwrite.rgb(10, 10, 16, '%')))
        binW=w*1.0/len(_list)
        rec=self._range
        _inds=[0,len(self.data['CC'])-1,len(self.data['CC']),len(self.data['CC'])+len(self.data['MF'])-1,len(self.data['CC'])+len(self.data['MF']),len(_list)-1]
        lines=[]
        for i in range(len(_list)):
            dwg.add(dwg.line((x+binW+i*binW, y1), (x+binW+i*binW, y1+5), stroke=svgwrite.rgb(10, 10, 16, '%')))
            label=_list[i][0]
            if len(label)>40:
                label=label[0:37]+'...'
            txt=dwg.text(label, insert=(x+binW/2+i*binW, y+10),text_anchor='end',font_family='Times New Roman',font_size=8)
            txt.rotate(rec-90,(x+binW/2+i*binW, y+10))
            dwg.add(txt)
            if i in set(_inds):
                h=len(label)*4.5
                if len(label)<30:
                    h=len(label)*5
                if len(label)<20:
                    h=len(label)*5.5
                if len(label)<10:
                    h=len(label)*8
                dwg.add(dwg.line((x+binW/2+i*binW+3-math.tan(radians(rec))*h, y+h), (x+binW/2+i*binW+3-math.tan(radians(rec))*183, y+183), stroke=svgwrite.rgb(10, 10, 16, '%')))
                lines.append((x+binW/2+i*binW+3-math.tan(radians(rec))*183, y+183))
        txts=[]
        if len(self.data['CC'])>0:
            txts.append('Cellular Component')
        if len(self.data['MF'])>0:
            txts.append('Molecular Function')
        if len(self.data['BP'])>0:
            txts.append('Biological Process')
        for i in range(0,len(lines),2):
            dwg.add(dwg.line((lines[i][0], lines[i][1]), (lines[i+1][0], lines[i+1][1]), stroke=svgwrite.rgb(10, 10, 16, '%')))
            dwg.add(dwg.text(txts[i/2], insert=((lines[i][0]+lines[i+1][0])/2, lines[i][1]+20),text_anchor='middle'))
            
    def yAxis1Plot(self,dwg,x,y1,y2,_max=100):
        span=(y2-y1)/4.0
        sp=_max/4.0
        dwg.add(dwg.line((x, y1), (x, y2), stroke=svgwrite.rgb(10, 10, 16, '%')))
        for i in range(5):
            dwg.add(dwg.line((x-5, y1+span*i), (x, y1+ span*i), stroke=svgwrite.rgb(10, 10, 16, '%')))
            dwg.add(dwg.text(str(int(_max-sp*i))+'%', insert=(x-5, y1+span*i+5),text_anchor='end')) # settings are valid for all text added to 'g'
    def yAxis2Plot(self,dwg,x,y1,y2,maxs):
        span=(y2-y1)/4.0
        dwg.add(dwg.line((x, y1), (x, y2), stroke=svgwrite.rgb(10, 10, 16, '%')))
        for i in range(5):
            dwg.add(dwg.line((x+5, y1+span*i), (x, y1+ span*i), stroke=svgwrite.rgb(10, 10, 16, '%')))
            if len(maxs)==1:
                dwg.add(dwg.text(str(int(maxs[0]*(1-0.25*i))), insert=(x+5, y1+span*i+5)))
            elif len(maxs)==2:
                dwg.add(dwg.text(str(int(maxs[0]*(1-0.25*i))), insert=(x+5, y1+span*i),fill=self.colors[0],font_size=8))
                dwg.add(dwg.text(str(int(maxs[1]*(1-0.25*i))), insert=(x+5, y1+span*i+10),fill=self.colors[1],font_size=8))
            elif len(maxs)==3:
                dwg.add(dwg.text(str(int(maxs[0]*(1-0.25*i))), insert=(x+5, y1+span*i-5),fill=self.colors[0],font_size=8))
                dwg.add(dwg.text(str(int(maxs[1]*(1-0.25*i))), insert=(x+5, y1+span*i+5),fill=self.colors[1],font_size=8))
                dwg.add(dwg.text(str(int(maxs[2]*(1-0.25*i))), insert=(x+5, y1+span*i+15),fill=self.colors[2],font_size=8))
        if len(maxs)>1:
            w=0
            for i in range(len(maxs)):
                l=len(self.header[i])*8
                if len(self.header[i])>5:
                    l=len(self.header[i])*7
                if len(self.header[i])>10:
                    l=len(self.header[i])*6
                if len(self.header[i])>15:
                    l=len(self.header[i])*5
                if len(self.header[i])>20:
                    l=len(self.header[i])*4.5
                if w<l:
                    w=l
            for i in range(len(maxs)):
                dwg.add(dwg.rect(insert=(x-w-20, y1+10+15*i),size=(10,10),fill=self.colors[i]))
                dwg.add(dwg.text(self.header[i], insert=(x-w-7, y1+20+15*i),fill=self.colors[i],font_size=8))
                    
    def barPlot(self,dwg,x,y1,y2,w,_list,maxs):
        binW=w*1.0/len(_list)
        width=binW-self.span1*2
        _inds=[0,len(self.data['CC'])-1,len(self.data['CC']),len(self.data['CC'])+len(self.data['MF'])-1,len(self.data['CC'])+len(self.data['MF']),len(_list)-1]
        for i in range(len(_list)):
            start=x+i*binW
            if len(maxs)==1:
                h=_list[i][1]*(y2-y1)/maxs[0]
                color=self.colors[0]
                if i>=len(self.data['CC']) and i<(len(self.data['CC'])+len(self.data['MF'])):
                    color=self.colors[1]
                elif i>=(len(self.data['CC'])+len(self.data['MF'])):
                    color=self.colors[2]
                else:
                    color=self.colors[0]
                dwg.add(dwg.rect(insert=(start+self.span1, y2-h),size=(width,h),fill=color))
            else:
                bw=width*1.0/len(maxs)
                for j in range(len(maxs)):
                    h=_list[i][1+j]*(y2-y1)/maxs[j]
                    dwg.add(dwg.rect(insert=(start+self.span1+bw*j, y2-h),size=(bw,h),fill=self.colors[j]))
                
    def writeBar(self,title,outPath,maxs):
        x1=120
        y1=40
        y2=320
        _width=800.0
        _height=550
        _list=self.formatData()
        if _width/len(_list)>50:
            x2=x1+len(_list)*50
        elif _width/len(_list)<10:
            x2=x1+len(_list)*10
        else:
            x2=x1+_width
        _max=0
        for cols in _list:
            for i in range(1,len(cols)):
                if _max<cols[i]*100.0/maxs[i-1]:
                    _max=cols[i]*100.0/maxs[i-1]
        if _max+10<100:
            _max=_max+10
        for i in range(len(maxs)):
            maxs[i]=maxs[i]*_max/100
        dwg=svgwrite.Drawing(outPath+'.svg', profile='tiny',size=(x2+100,_height))
        self.yAxis1Plot(dwg,x1,y1,y2,_max)
        self.xAxisPlot(dwg, x1, y2,y1,x2-x1,_list)
        self.yAxis2Plot(dwg, x2, y1, y2, maxs)
        self.barPlot(dwg, x1, y1, y2, x2-x1, _list, maxs)
        dwg.add(dwg.text(title, insert=((x1+x2)/2, y1-5),text_anchor='middle'))
        dwg.save()
        drawing = svg2rlg(outPath+'.svg')
        renderPDF.drawToFile(drawing, outPath+".pdf")
        renderPM.drawToFile(drawing, outPath+".jpg",'JPG')
        return (x2+100,_height)

def getLevelData(path):
    data=getDataMatrix(path)[0]
    _list=[]
    for cols in data:
        _list.append([cols[1],int(cols[2])])
    _list1=sorted(_list,key=lambda a_tuple:a_tuple[1],reverse=True)
    return _list1

def appendLevelData(_list,data):
    _map={}
    _keys=[]
    l=None
    for cols in _list:
        _map[cols[0]]=cols[1:len(cols)]
        _keys.append(cols[0])
        if not l:
            l=len(cols)-1
    for cols in data:
        if _map.has_key(cols[0]):
            _map[cols[0]].append(cols[1])
        else:
            _map[cols[0]]=[]
            for i in range(l):
                _map[cols[0]].append(0)
            _map[cols[0]].append(cols[1])
            _keys.append(cols[0])
    _list=[]
    for key in _keys:
        _lis=_map[key]
        if len(_lis)==l:
            _lis.append(0)
        _lis.insert(0,key)
        _list.append(_lis)
    return _list

def test3():
    folder='E:/Work/P1/MG005/Proteome'


def test2():
    folder='E:/Work/P1/MG005/Proteome'


def test1():
    folder='E:/Work/P1/MG005/Proteome'

    
if __name__ == '__main__':
    test1()
    folder='E:/Work/P1/MG005/Proteome'
    
#     drawing = svg2rlg(folder+'/Metabolic.svg')
#     renderPDF.drawToFile(drawing, folder+'/Metabolic.pdf')
#     renderPM.drawToFile(drawing, folder+'/Metabolic.jpg','JPG')
    pass






