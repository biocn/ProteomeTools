# -*- coding:utf-8 -*-
#!/usr/bin/python
'''
Created on 2016��12��5��
该流程图 保存png时存在一些问题，实现思路是使用webdriver进行网页截图，在部署到不同机器上需要注意一下下载chromedriver驱动到环境变量中
还有必须按照谷歌浏览器
@author: Administrator
'''
from math import radians
import math
from random import randint
import random

from svgpathtools.path import Path, Line, CubicBezier
import svgwrite

from com.zlf.domain.plot.Basic import _BasicColors
from selenium import webdriver
from PIL import Image

class WorkFlow(object):
    def __init__(self,dwg):
        self.dwg=dwg
        self.rad=1
    
    def getLine(self,x1,y1,x2,y2,width=None,color=None):
        if not color:
            color=svgwrite.rgb(10, 10, 16, '%')
        if width:
            line=self.dwg.line((x1, y1), (x2,y2), stroke=color,fill=color,stroke_width=width)
        else:
            line=self.dwg.line((x1, y1), (x2,y2), stroke=color,fill=color)
        return line
    def getRect(self,x1,y1,width,height,strokeWidth=None,color=None):
        if not color:
            color=svgwrite.rgb(10, 10, 16, '%')
        if len(color)>1:
            rect=self.dwg.rect(insert=(x1, y1),size=(width,height),fill=color[1],stroke=color[0])
        else:
            rect=self.dwg.rect(insert=(x1, y1),size=(width,height),stroke=color,stroke_width=strokeWidth)
        return rect 
       
    def getPolygon3(self,x1,y1,x2,y2,fillColor=None,rec=30):
        x=(y2-y1)*math.tan(radians(rec))
        y=(x2-x1)*math.tan(radians(rec))
        if not fillColor:
            fillColor=svgwrite.rgb(10, 10, 16, '%')
        ploy=self.dwg.polygon([(x1+x,y1-y),(x1-x,y1+y),(x2,y2)],fill=fillColor)
        return ploy
    
    def getLinePloygon(self,x1,y1,x2,y2,color=None,h=27,rec=30,width=5):
        L=math.sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1))
        x=h*(x2-x1)/L
        y=h*(y2-y1)/L
        g=self.dwg.g()
        g.add(self.getLine(x1, y1, x2-x, y2-y, width, color))
        g.add(self.getPolygon3(x2-x, y2-y, x2, y2,color,rec))
        return g
    
    def getTestTube(self,x1,y1,y2,r,color='red',pColor='blue',txt=None):
        l=2*r
        l1=r/2
        l2=r/2
        h=y2-y1-l
        ax=x1-r
        bx=x1+r
        ay=y1+h/2
        g=self.dwg.g()
        for i in range(random.randint(r, 2*r)):
            x=random.randint(ax, bx)
            y=random.randint(ay, y2-l)
            g.add(self.dwg.circle(center=(x, y), r=1, fill=pColor))
        path=Path(Line(complex(ax,ay),complex(bx,ay)),Line(complex(bx,ay),complex(bx,y2-l))
             ,CubicBezier(complex(bx,y2-l),complex(bx,y2),complex(ax,y2),complex(ax,y2-l))
             ,Line(complex(ax,y2-l),complex(ax,ay)))
        g.add(self.dwg.path(d=path.d(),fill=color,fill_opacity=0.1))
        path2=Path(Line(complex(ax,y1),complex(ax,y2-l))
             ,CubicBezier(complex(ax,y2-l),complex(ax,y2),complex(bx,y2),complex(bx,y2-l))
             ,Line(complex(bx,y2-l),complex(bx,y1))
            ,CubicBezier(complex(bx,y1),complex(bx,y1+l1),complex(ax,y1+l1),complex(ax,y1))
             ,CubicBezier(complex(ax,y1),complex(ax,y1-l2),complex(bx,y1-l2),complex(bx,y1)))
        g.add(self.dwg.path(d=path2.d(),stroke_width=2,fill='none',stroke='#000'))
        if txt:
            g.add(self.dwg.text(txt, insert=(x1, ay),font_family='Times New Roman',font_size=8,text_anchor='middle'))
        return g
    
    def getMedium(self,x1,y1,y2,r,color='red',pColor='blue'):
        l=r/8
        ax=x1-r
        bx=x1+r
        ay=y1+(y2-y1-l)/3
        g=self.dwg.g()
        for i in range(random.choice(range(r/4, r))):
            x=random.randint(ax, bx)
            y=random.randint(ay, y2-l)
            g.add(self.dwg.circle(center=(x, y), r=1, stroke=pColor))
        path=Path(Line(complex(ax,ay),complex(bx,ay)),Line(complex(bx,ay),complex(bx,y2-l))
             ,CubicBezier(complex(bx,y2-l),complex(bx,y2),complex(ax,y2),complex(ax,y2-l))
             ,Line(complex(ax,y2-l),complex(ax,ay)))
        g.add(self.dwg.path(d=path.d(),fill=color,fill_opacity=0.1))
        path2=Path(Line(complex(ax,y1),complex(ax,y2-l))
             ,CubicBezier(complex(ax,y2-l),complex(ax,y2),complex(bx,y2),complex(bx,y2-l))
             ,Line(complex(bx,y2-l),complex(bx,y1)))
        g.add(self.dwg.path(d=path2.d(),stroke_width=2,fill='none',stroke='#000'))
        return g
    def getMergeImg(self,x1,y1,x2,h=20,color='#000'):
        h=h/2
        path=Path(Line(complex(x1,y1),complex(x1,y1+h/2))
                 ,CubicBezier(complex(x1,y1+h/2),complex(x1,y1+h),complex(x1,y1+h),complex(x1+h/2,y1+h))
                 ,Line(complex(x1+h/2,y1+h),complex((x2+x1)/2-h,y1+h))
                 ,CubicBezier(complex((x2+x1)/2-h,y1+h),complex((x2+x1)/2-h/2,y1+h),complex((x2+x1)/2-h/2,y1+h),complex((x2+x1)/2,y1+2*h))
                 ,CubicBezier(complex((x2+x1)/2,y1+2*h),complex((x2+x1)/2+h/2,y1+h),complex((x2+x1)/2+h/2,y1+h),complex((x2+x1)/2+h,y1+h))
                 ,Line(complex((x2+x1)/2+h,y1+h),complex(x2-h/2,y1+h))
                 ,CubicBezier(complex(x2-h/2,y1+h),complex(x2,y1+h),complex(x2,y1+h),complex(x2,y1+h/2))
                 ,Line(complex(x2,y1+h/2),complex(x2,y1)))
        g=self.dwg.g()
        g.add(self.dwg.path(d=path.d(),stroke_width=2,fill='none',stroke=color))
        return g
    def getHPLC(self,x1,y1,h,r,sampleColors):
        rad_grad = self.dwg.linearGradient(("0%", "0%"), ("0%", "100%"), id="rad_grad"+str(self.rad))
        rad_grad.add_stop_color(0, 'blue',0.8)
        rad_grad.add_stop_color(1, '#fff')
        self.dwg.defs.add(rad_grad)
        g=self.dwg.g()
        for c in sampleColors:
            for m in range(randint(5,20)):
                x=random.randint(x1-r, x1+r)
                y=random.randint(y1+0.5*r, y1+h-r)
                g.add(self.dwg.circle(center=(x, y), r=1, stroke=c))
        ploy=self.dwg.polygon([(x1+r,y1+h-r),(x1-r,y1+h-r),(x1-2*r,y1+h),(x1+2*r,y1+h),(x1+r,y1+h-r)],fill='url(#rad_grad'+str(self.rad)+')')
        g.add(ploy)
        path=Path(Line(complex(x1-1.5*r,y1),complex(x1-r,y1+r/2))
                   ,Line(complex(x1-r,y1+r/2),complex(x1-r,y1+h-r))
                   ,Line(complex(x1-r,y1+h-r),complex(x1-2*r,y1+h))
                   ,Line(complex(x1+2*r,y1+h),complex(x1+r,y1+h-r))
                   ,Line(complex(x1+r,y1+h-r),complex(x1+r,y1+r/2))
                   ,Line(complex(x1+r,y1+r/2),complex(x1+1.5*r,y1))
                   ,Line(complex(x1+1.5*r,y1),complex(x1-1.5*r,y1)))
        g.add(self.dwg.path(d=path.d(),stroke_width=2,fill='none',stroke='#000'))
        s=(h-r)/4
        h1=3
        cs=['red','blue','yellow']
        for i in range(3):
            path2=Path(Line(complex(x1-r,y1+s+i*s-h1),complex(x1-r,y1+s+i*s+h1))
                 ,CubicBezier(complex(x1-r,y1+s+i*s+h1),complex(x1-r,y1+s+i*s+h1+8),complex(x1+r,y1+s+i*s+h1+8),complex(x1+r,y1+s+i*s+h1))
                 ,Line(complex(x1+r,y1+s+i*s+h1),complex(x1+r,y1+s+i*s-h1))
                 ,CubicBezier(complex(x1+r,y1+s+i*s-h1),complex(x1+r,y1+s+i*s-h1+8),complex(x1-r,y1+s+i*s-h1+8),complex(x1-r,y1+s+i*s-h1)))
            g.add(self.dwg.path(d=path2.d(),fill_opacity=0.7,fill=cs[i]))
        self.rad=self.rad+1
        return g
    def getMS_MS(self,x1,y1,x2,y2):
        span=(x2-x1)/9
        h=15
        g=self.dwg.g()
        for i in range(int(0.05*(x2-x1))):
            x=randint(x1+span,x2-span)
            g.add(self.getLine(x, randint(y1,(y1+y2)/2),x, y2-h))
        for i in range(int(0.15*(x2-x1))):
            x=randint(x1,x2)
            g.add(self.getLine(x, randint((y1+y2)/2,y2-h),x, y2-h))
        g.add(self.getLine(x1,y2-h ,x2, y2-h))
        for i in range(9):
            g.add(self.getLine(x1+(0.5+i)*span,y2-h ,x1+(0.5+i)*span, y2-h+3))
        g.add(self.dwg.text('m/z', insert=((x1+x2)/2,y2),font_family='Times New Roman',font_size=8,text_anchor='middle'))
        return g
    def getBoxTxt(self,x1,y1,x2,y2,txt,color='blue'):
        rad_grad = self.dwg.radialGradient(("50%", "50%"), "50%", id="rad_grad"+str(self.rad))
        rad_grad.add_stop_color(0, '#fff',0.3)
#         rad_grad.add_stop_color(0.6, '#fff')
        rad_grad.add_stop_color(1, color,0.3)
        self.dwg.defs.add(rad_grad)
        g=self.dwg.g()
        g.add(self.dwg.rect(insert=(x1, y1),size=(x2-x1,y2-y1),stroke=color,stroke_width=1,fill='url(#rad_grad'+str(self.rad)+')'))
        g.add(self.dwg.text(txt, insert=((x1+x2)/2,(y2+y1)/2+4),font_family='Times New Roman',font_size=12,text_anchor='middle'))
        self.rad=self.rad+1
        return g
    def getBoxDBTxt(self,x1,y1,x2,y2,txt,color='blue'):
        rad_grad = self.dwg.radialGradient(("50%", "50%"), "50%", id="rad_gradDB"+str(self.rad))
        rad_grad.add_stop_color(0, '#fff',0.3)
#         rad_grad.add_stop_color(0.6, '#fff')
        rad_grad.add_stop_color(1, color,0.3)
        self.dwg.defs.add(rad_grad)
        g=self.dwg.g()
        h=y2-y1
        path=Path(Line(complex(x1,y1),complex(x1,y2))
                  ,CubicBezier(complex(x1,y2),complex((x1+x2)/2,y2+h/10),complex((x1+x2)/2,y2+h/10),complex(x2,y2))
                  ,Line(complex(x2,y2),complex(x2,y1))
                  ,CubicBezier(complex(x2,y1),complex((x1+x2)/2,y1+h/10),complex((x1+x2)/2,y1+h/10),complex(x1,y1))
#                   ,CubicBezier(complex(x1,y1),complex((x1+x2)/2,y1-h/10),complex((x1+x2)/2,y1-h/10),complex(x2,y1))
                  )
        g.add(self.dwg.path(d=path.d(),stroke=color,stroke_width=1,fill='url(#rad_gradDB'+str(self.rad)+')'))        
        g.add(self.dwg.text(txt, insert=((x1+x2)/2,(y2+y1)/2+6),font_family='Times New Roman',font_size=14,text_anchor='middle'))
        self.rad=self.rad+1
        return g
    
    def getBoxRect(self,x1,y1,x2,y2,color,txt):
        g=self.dwg.g()
        g.add(self.dwg.rect(insert=(x1, y1),size=(x2-x1,y2-y1),stroke=color,stroke_width=1.5,fill='none'))
        g.add(self.dwg.text(txt, insert=((x1+x2)/2,(y2+y1)/2+4),font_family='Times New Roman',font_size=12,text_anchor='middle'))
        return g
    def getBioinfomatics(self,x1,y1):
        g=self.dwg.g()
        g.add(self.getLinePloygon(x1, y1, x1,y1+40, None, 15, 30, 3))
        g.add(self.getLinePloygon(x1-165, y1+15, x1-165,y1+40, None, 15, 30, 3))
        g.add(self.getLinePloygon(x1+165, y1+15, x1+165,y1+40, None, 15, 30, 3))
        g.add(self.getLine(x1-166, y1+15, x1+166, y1+15, 3, None))
        g.add(self.getBoxTxt(x1-80-165, y1+45, x1-85, y1+45+30, 'Qualitative Analysis', '#0a9775'))
        g.add(self.getBoxRect(x1-80-165, y1+80, x1-85, y1+80+30, '#0a9775', 'Function Annotation'))
        
        g.add(self.getBoxTxt(x1-80, y1+45, x1+80, y1+45+30, 'Quantitative Analysis', '#0b80b5'))
        g.add(self.getBoxRect(x1-80, y1+80, x1+80, y1+80+30, '#0b80b5', 'Differential Analysis'))

        g.add(self.getBoxTxt(x1+85, y1+45, x1+80+165, y1+45+30, 'Custom Analysis', '#543d8f'))
        g.add(self.getBoxRect(x1+85, y1+80, x1+80+165, y1+80+30, '#543d8f', 'Network Analysis'))
        
        return g
        
def testPath():
    dwg = svgwrite.Drawing('D:/test.svg')
    dwg.add(dwg.polyline(
        [(10, 10), (50, 20), (70, 50), (100, 30)],
        stroke='black', fill='none'))
    
    # create a new marker object
    path = Path(Line(0+0j, 0+6j),Line(0+6j, 9+3j),Line(9+3j, 0+0j))
    marker = dwg.marker(insert=(0,3), size=(10,10))
    marker.add(dwg.path(d=path.d(),fill='red'))
    dwg.defs.add(marker)
    line = dwg.add(dwg.line((50,50),(250,50),stroke="#000"))
    line.set_markers(('#','#','#'+marker['id']))
    dwg.save()    
'''
def convertSvgToPng(svgFilepath,pngFilepath,width):
    r=QSvgRenderer(svgFilepath)
    height=r.defaultSize().height()*width/r.defaultSize().width()
    i=QImage(width,height,QImage.Format_ARGB32)
    p=QPainter(i)
    r.render(p)
    i.save(pngFilepath)
    p.end()
'''
def plotWorkFlow(sampleNames,labelNames,outPath):
    _height=560
    _maxSample=0
    sampleColors=random.sample(_BasicColors,len(sampleNames))
    for i in range(len(sampleNames)):
        if _maxSample<len(sampleNames[i]):
            _maxSample=len(sampleNames[i])
    sw=_maxSample*6+4
    if sw<120:
        sw=120
    _width=sw*len(sampleNames)
    if _width<500:
        _width=500
    dwg = svgwrite.Drawing(outPath+'.svg', profile='tiny',size=(_width,_height))
    work=WorkFlow(dwg)
    g=dwg.g()
    y=20
    for i in range(len(sampleNames)):
        g.add(dwg.text(sampleNames[i], insert=(sw/2+(sw)*i, 17),font_family='Times New Roman',font_size=12,text_anchor='middle'))
        g.add(work.getMedium(sw/2+(sw)*i, y, 50, 50,'red',sampleColors[i]))
        g.add(work.getLinePloygon(sw/2+(sw)*i, 55, sw/2+(sw)*i, 85, sampleColors[i], 15, 26, 5))
        g.add(work.getTestTube(sw/2+(sw)*i, 95, 150, 10,'red',sampleColors[i],'126'))
    y=150
    g.add(dwg.text('Mix Sample', insert=((sw)*len(sampleNames)/2, y+12),font_family='Times New Roman',font_size=12,text_anchor='middle'))
    g.add(work.getMergeImg(sw/2, y+5, sw*len(sampleNames)-sw/2,20))
    y=175
    g.add(work.getHPLC((sw)*len(sampleNames)/2, y+5, 80, 20,sampleColors))
    g.add(dwg.text('HPLC', insert=((sw)*len(sampleNames)/2-30, y+5+40),font_family='Times New Roman',font_size=12,text_anchor='end'))
    y=y+5+80
    g.add(work.getLinePloygon((sw)*len(sampleNames)/2, y+5, (sw)*len(sampleNames)/2, y+5+30, None, 15, 30, 5))
    y=y+5+30
    g.add(work.getMS_MS((sw)*len(sampleNames)/2-80, y+3, (sw)*len(sampleNames)/2+80, y+50+3))
    g.add(dwg.text('MS/MS', insert=((sw)*len(sampleNames)/2-85, y+3+25),font_family='Times New Roman',font_size=12,text_anchor='end'))
    y=y+50+3
    g.add(work.getLinePloygon((sw)*len(sampleNames)/2, y+3, (sw)*len(sampleNames)/2, y+3+30, None, 15, 30, 5))
    y=y+33
    g.add(work.getBoxDBTxt((sw)*len(sampleNames)/2-100, y+3, (sw)*len(sampleNames)/2+100, y+3+47,'Bioinfomatics Analysis',_BasicColors[randint(0,len(_BasicColors)-1)]))
    y=y+50
    g.add(work.getBioinfomatics((sw)*len(sampleNames)/2, y+5))
    if (sw)*len(sampleNames)/2<250:
        g.translate(250-(sw)*len(sampleNames)/2)
    dwg.add(g)
    dwg.save()
    saveJpg(outPath, _width)
#     fileHandle = open(outPath+'.svg')
#     svg = fileHandle.read()
#     fileHandle.close()
#     cairosvg.svg2pdf(bytestring=svg, write_to='.pdf')
#     cairosvg.svg2png(bytestring=svg, write_to=outPath+'.jpg')
#     convertSvgToPng(outPath+'.svg', outPath+'.png', _width)
#     drawing = svg2rlg(outPath+'.svg')
#     renderPDF.drawToFile(drawing, outPath+".pdf")
#     renderPM.drawToFile(drawing, outPath+".jpg",'JPG')

def saveJpg(outPath,_width):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('file:///'+outPath+'.svg')
    driver.save_screenshot(outPath+'.png')
    i=Image.open(outPath+'.png') #打开截图
    frame4=i.crop((0, 0, _width, 550))  #使用Image的crop函数，从截图中再次截取流程图区域的区域
    frame4.save(outPath+'.png')
    driver.quit()

if __name__ == '__main__':
    sampleNames=['Sample1','Sample2','Sample3','Sample4','Sample5','Sample6','Sample7','Sample8']
    sampleNames=sampleNames[0:randint(2,8)]
    plotWorkFlow(sampleNames, sampleNames,'D:/test')




