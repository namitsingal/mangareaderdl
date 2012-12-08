#!usr/bin/python2.7
from urllib import urlopen
import re
import os
import sys
import urllib2

BASE_DIR=''
names=''

def checkend(link1,link2):  
    flag=0
    for i in link1:
        if(i=='.'):
            flag=1
            break
    if(flag==1):
        if(link1.split('/')[-1]==link2.split('/')[-1]):
            return False
        else:
            return True
    else:
        if(link1.split('/')[-1]==link2.split('/')[-2]):
            return False
        else:
            return True

def getname(name):
    try:
        url='http://www.mangareader.net/alphabetical'
        webpage=urlopen(url).read()
        k='<a hr.*>'+name+'</a>'
        exp=re.compile(k,flags=re.IGNORECASE)
        res=re.findall(exp,webpage)
        #for i in res:
        #    if(i.split('>')[-2].split('<')[0].lower()==name.lower()):
        return res[0].split('"')[1]
    except(IOError):
        print 'Internet Not working'
        sys.exit()
    
def findurl(name,chapter,x1):
    try:
        urls='http://www.mangareader.net'+str(name)
        webpage=urlopen(urls).read()
        p=re.compile('<img.*src="(.*)"')
        #x=re.compile('[<a href="(.*)">\na href="(.*)">')
        x=re.compile('<div class="chi.*>\n<a href="(.*)">')
        img=re.findall(x,webpage)
        try:
            length=len(img)
            #print length
            if(length>12 and chapter<=length):
                dlchapter(img[chapter+5],chapter,name,x1,p)
            elif(chapter<=length/2):
                dlchapter(img[length/2-chapter],chapter,name,x1,p)
            else:
                print 'Chapter',chapter,'does not exist'
                sys.exit()
        except(IndexError):
                print 'Chapter',chapter,'does not exist'
                sys.exit()
    except(IOError):
        print 'Internet Not Working'
        sys.exit()
        
def dlchapter(url,chapter,name,x1,p):
    global names
    k=BASE_DIR+str(names)
    if(os.path.isdir(k)==False):
        os.mkdir(k)
    z=k+'/'+str(chapter)
    if(os.path.isdir(z)==False):
        os.mkdir(z)
    #print z
    x='http://www.mangareader.net'+url
    i=1
    while(True):
        print 'saving chapter '+str(chapter)+' page '+str(i)
        x= str(downloader(x,i,chapter,name,x1,p))
        i=i+1
        y=x
        z=''
        x='http://www.mangareader.net'
        for k in y:
            if(k!="["and k!="'"and k!="]"):
                z=z+k
                x+=k
        
        if(checkend(url,z)):
            break
    return
    
def downloader(urls,i,chapter,name,x,p):
    try:
        webpage=urlopen(urls).read()
        #print webpage
        #print p
        img= ''.join(re.findall(p,webpage))
        img=img[0:img.index('"')]
        #print img
        s=str(re.findall(x,webpage))
        kk=str(s)
        #print kk
        global names
        loc=BASE_DIR+str(names)+'/'+str(chapter)+'/'+str(i)+'.jpg'
        reqs = urllib2.Request(img)
        output = open(loc,'wb')
        output.write(urllib2.urlopen(reqs).read())
        output.close()
        #urlretrieve(img,loc)
        #print 'done'
        return kk
        #print img
    except(IOError):
        print 'Internet Not Working'
        sys.exit()
        
def main():
    try:
        global names
        name=''
        if(os.path.isfile(os.getcwd()+'/manga.conf')==False):
            #print os.getcwd()+'/manga.conf'
            var = raw_input("Enter Source Directory(Complete Path): ")
            if(os.path.isdir(var)==False):
                print "Entered Directory Does not exist aborting"
                sys.exit()
            else:
                k=open(os.getcwd()+'/manga.conf','w+')
                k.write('path='+var)
                k.close()
                global BASE_DIR
                BASE_DIR=var + '/'
        else:
            k=open('manga.conf').read()
            fil=k[k.index('path=')+5:-2]
            print fil
            if(os.path.isdir(fil)==False):
                os.unlink('manga.conf')
                var = raw_input("Enter Source Directory(Complete Path): ")
                if(os.path.isdir(var)==False):
                    print "Entered Directory Does not exist aborting"
                    sys.exit()    
            else:
                global BASE_DIR
                BASE_DIR=fil + '/'




        x=re.compile('<a href="(.*)"><img id')
        k=int(sys.argv[3])
        l=int(sys.argv[2])
        names=str(sys.argv[1])
        name= getname(names)
        i=l
        while(i<=k):
            findurl(name,i,x)
            i=i+1
    except(IndexError):
        try:
            l=int(sys.argv[2])
            names=str(sys.argv[1])
            name= getname(names)
            findurl(name,l,x)
            print 1
        except(IndexError):
            print 'Please Enter a Chapter'
            sys.exit()
        
        
if __name__=='__main__':main()