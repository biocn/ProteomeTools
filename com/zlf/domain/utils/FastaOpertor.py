'''
Created on 2016-5-27

@author: Administrator
'''
##|proID|
##|proID 
##proID
def extractProteinID(line):
    _id=line
    if line.find(' ')>-1:
        _id=line[0:line.find(' ')]
    if _id.find('>')>-1:
        _id=line[_id.find('>')+1:len(_id)]
    if _id.count('|')>1:
        _id=_id.split('|')[1]
    elif _id.find('|')>-1:
        _id=_id[_id.find('|')+1:len(_id)]
    return _id    
    
def outFastaByKey(_keys,_fastaPath,outPath):
    f=open(_fastaPath,'r')
    line=f.readline()
    fw=open(outPath,'w')
    flag=False
    while line:
        if line.find('>')==0:
            proID=extractProteinID(line)
            if proID in _keys:
                fw.write(line)
                flag=True
            else:
                flag=False
        else:
            if flag:
                fw.write(line)
        line=f.readline()
    f.close()
    fw.close()
def readFasta(_path):
    f=open(_path,'r')
    line=f.readline()
    _map={}
    key=None
    seq=None
    while line:
        line=line.rstrip().lstrip('\n')
        if line.find('>')==0:
            if key:
                _map[key]=seq
            key=line[line.find('|')+1:len(line)]
            key=key[0:key.find('|')]
            seq=''
        else:
            seq+=line
        line=f.readline()
    f.close()
    if key:
        _map[key]=seq
    return _map

if __name__ == '__main__':
    folder='E:/Work/P1/MG005/Proteome'
    _fastaPath=folder+'/uniprot-organism_4081.fasta'
    f=open(folder+'/MergeAll.txt','r')
    f.readline()
    line=f.readline()
    _list=[]
    while line:
        _list.append(line.lstrip().rstrip('\n').split('\t')[0])
        line=f.readline()
    f.close()
    outFastaByKey(set(_list), _fastaPath, folder+'/identify.fasta')
    
    pass