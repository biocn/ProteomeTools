# -*- coding:utf-8 -*-
'''
Created on 2016-10-23

@author: Administrator
'''
from com.zlf.beans.Global import _ReportRootPath

class Nav:
    def __init__(self,key,value,title=None,root=None):
        self.key=key
        self.value=value
        self.title=title
        self.root=root
        self.cList=[]
    def addC(self,nav):
        self.cList.append(nav)
    def setP(self,nav):
        self.pNav=nav
    def getHtml(self):
        if len(self.cList)==0:
            if self.title:
                return '<li><a href="#'+self.value+'" class="js-active-bg">'+self.key+'</a><ul class="nav"></ul></li>'
            return '<li><a href="#'+self.value+'" class="js-active-bg">'+self.key+'</a></li>\n'
        else:
            line='<li><a href="#'+self.value+'" class="js-active-bg">'+self.key+'</a><ul class="nav">\n'
            if self.root:
                line='<li><a href="#'+self.value+'">'+self.key+'</a><ul class="nav">\n'
            for nav in self.cList:
                line=line+nav.getHtml()
            line=line+'</ul></li>\n'
            return line

def getTextCenter(txt):
    return '<p class="text-center">'+txt+'</p>'
            
#获取导航栏
def getNavHtml(navs):
    line='<div role="complementary" class="col-md-3"><nav class="bs-docs-sidebar hidden-print hidden-xs hidden-sm affix-top">'
    line=line+'<ul class="nav bs-docs-sidenav">'
    for nav in navs:
        line=line+nav.getHtml()
    line=line+'</ul></nav></div>'
    return line

#获取报告尾部文件
def getHtmlFooter():
    line='</div><footer>'
    line=line+'<div class="text-center"><p>版权所有：牟合（上海）生物科技有限公司</p>'
    line=line+'<p>公司地址：上海市横泰经济开发区富民支路58号</p>'
    line=line+'<ul class="list-inline list-unstyled">'
#     line=line+'<li>Tel:400-600-3186</li>'
    line=line+'<li>Fax:021-50610115</li>'
    #line=line+'<li>Tel:400-600-3186</li>'
    line=line+'<li>E-mail:<a href="mailto:tech@mhelix.cn">tech@mhelix.cn</a></li>'
#    line=line+'<li>微信:biomarker_tech</li>'
#    line=line+'<li><a href="http://www.biocloud.cn/external/login/toLogin" target="_blank">百迈客生物云平台</a></li>'
    line=line+'<li><a href="http://www.mhelix.cn/" target="_blank">关于我们</a></li>'
    line=line+'</ul>'
    line=line+'</div>'
    line=line+'</footer>'
    line=line+'<div id="goTop"><a title="Top" class="backtotop"><img src="src/imgs/goTop.png" class="back-tip" />'
    line=line+'</a>'
    line=line+'</div>'
    line=line+'</div>'
    line=line+'</body>'
    line=line+'</html>'
    return line

#获取报告头部文件
def getHtmlHeader(title):
    line='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
    line=line+'<html lang="zh_CN" xmlns="http://www.w3.org/1999/xhtml"><head><title>'+title+'</title>'
    line=line+'<meta charset="UTF-8"></meta>'
    line=line+'<!--[if lt IE 9]>'
    line=line+'<script src="src/js/html5shiv.min.js"></script><script src="src/js/respond.min.js"></script>'
    line=line+'<![endif]-->'
    line=line+'<meta author="biocc"></meta>'
    line=line+'<meta content="IE=edge" http-equiv="X-UA-Compatible"></meta>'
    line=line+'<meta content="width=device-width, initial-scale=1" name="viewport"></meta>'
    line=line+'<link href="src/css/bootstrap.min.css" type="text/css" rel="stylesheet" />'
    line=line+'<link href="src/css/index.css" type="text/css" rel="stylesheet" />'
    line=line+'<link href="src/js/fancyBox/jquery.fancybox.css" type="text/css" rel="stylesheet" />'
    line=line+'<link href="src/css/nav.css" type="text/css" rel="stylesheet" />'
    line=line+'<link href="src/css/raxus.css" type="text/css" rel="stylesheet" />'
    line=line+'<script src="src/js/jquery-1.11.3.min.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/nav.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/raxus-slider.min.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/fancyBox/jquery.fancybox.pack.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/fancyBox/jquery.mousewheel-3.0.6.pack.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/bootstrap.min.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/ready.js" type="text/javascript"></script>'
    line=line+'<script src="src/js/scrolltop.js" type="text/javascript"></script>'
    line=line+'</head>'
    line=line+'<body><title>'+title+'</title>'
    line=line+'<div class="container shadow"><header><img src="src/imgs/logo.jpg" class="pull-right" />'
    line=line+'</header>'
    line=line+'<div class="row"><div role="main" class="col-md-9"><header><h2 id="title" class="text-center">'+title+'</h2>'
    line=line+'</header>'
    return line
#获取跳转内部的链接html
def getA_In(url,label):
    return '<a href="'+url+'">'+label+'</a>'
#获取跳转外部的链接html
def getA_Bank(url,label,_id=None):
    if _id:
        return '<a id="'+_id+'"  href="'+url+'" title="click" target="_blank">'+label+'</a>'
    return '<a href="'+url+'" title="click" class="mylink" target="_blank">'+label+'</a>'
#获取超大标题
def getTitleBigHtml(txt,_id='title'):
    return '<h2 id="'+_id+'" class="text-center">'+txt+'</h2>'
#获取大标题
def getTitleHHtml(txt,_id):
    return '<h3 id="'+_id+'">'+txt+'</h3>'
#获取中标题
def getTitleMHtml(txt,_id):
    return '<h4 id="'+_id+'" class="title-h4">'+txt+'</h4>'
#获取小标题的Html
def getTitleHtml(txt,_id):
    return '<h5 id="'+_id+'" class="title-h5">'+txt+'</h5>'
#获取文本的html
def getTxtHtml(txt):
    return '<p class="paragraph">'+txt+'</p>'
#获取图注释文本的html
def getFigureTxtHtml(txt):
    return '<p class="paragraph-mark center-block small img-width-max">'+txt+'</p>'
#获取图注的html
def getFigureLabelHtml(txt):
    return '<p class="img-mark text-center small">'+txt+'</p>'
#获取表注的html
def getTableLabelHtml(txt):
    return '<p class="table-mark small">'+txt+'</p>'
#生成图片幻灯的Html,imgs=[(title,url)]
def getImagesHtml(imgs):
    line='<div data-thumbnail="bottom" data-keypress="true" data-autoplay="3000" data-arrows="show" class="raxus-slider">'
    line=line+'<ul class="slider-relative">'
    for img in imgs:
        line=line+'<li class="slide"><a title="'+img[0]+'" href="'+img[1]+'" class="img-toggle">'
        line=line+'<img src="'+img[1]+'" alt="'+img[2]+'"/>'
        line=line+'</a>'
        line=line+'</li>'
    line=line+'</ul>'
    line=line+'</div>'
    return line

#生成图片的html
def getImageHtml(title,alt,url):
    line='<p class="text-center">'
    line=line+'<a title="'+title+'" href="'+url+'" class="img-toggle">'
    line=line+'<img src="'+url+'" alt="'+alt+'" class="img-width-max" />'
    line=line+'</a>'
    line=line+'</p>'
    
    return line

#生成表格的html
def getTableHtml(header,tables):
    line='<div class="table-responsive">'
    line=line+'<table class="table table-bordered table-hover table-striped"><thead>'
    line=line+'<tr class="tbHeader"><th>'+'</th><th>'.join(header)+'</th></tr></thead>'
    line=line+'<tbody style="word-break: break-all;">'
    for i in range(len(tables)):
        tr=tables[i]
        if i%2==1:
            line=line+'<tr style="word-break: break-all;" class="tbFlow"><td>'+'</td><td>'.join(tr[0:len(header)])+'</td></tr>'
        else:
            line=line+'<tr style="word-break: break-all;"><td>'+'</td><td>'.join(tr[0:len(header)])+'</td></tr>'
    line=line+'</tbody></table></div>'
    return line

#生成表格页面的html
def getTableTemplateHtml(title,tableResponsive,table,header=None):
    f=open(_ReportRootPath+'/table.template.html','r')
    lines=f.readlines()
    f.close()
    _list=[]
    for line in lines:
        line=line.replace('BioccTitle',title)
        line=line.replace('BioccResponsive',tableResponsive)
        _list.append(line)
    if header:
        _list.append('<thead><tr class="tbHeader"><th>'+'</th><th>'.join(header)+'</th></tr></thead>')
    _list.append('<tbody style="word-break: break-all;">')
    for i in range(len(table)):
        cols=table[i]
        if i%2==1:
            _list.append('<tr style="word-break: break-all;" class="tbFlow"><td>'+'</td><td>'.join(cols)+'</td></tr>')
        else:
            _list.append('<tr style="word-break: break-all;"><td>'+'</td><td>'.join(cols)+'</td></tr>')
    _list.append('</tbody></table></body></html>')
    return '\n'.join(_list)

if __name__ == '__main__':
    nav1=Nav('---1','123',None,True)
    nav11=Nav('---1.1','123',True)
    nav12=Nav('---1.2','123',True)
    nav13=Nav('---1.3','123',True)
    nav111=Nav('---1.1.1','123')
    nav112=Nav('---1.1.2','123')
    nav121=Nav('---1.2.1','123')
    nav11.addC(nav111)
    nav11.addC(nav112)
    nav12.addC(nav121)
    nav1.addC(nav11)
    nav1.addC(nav12)
    nav1.addC(nav13)
    print getNavHtml([nav1,nav1])
    
    
    pass