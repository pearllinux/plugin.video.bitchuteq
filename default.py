# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmcaddon
import sys

# Set default encoding to 'UTF-8' instead of 'ascii'
reload(sys)
sys.setdefaultencoding("UTF8")


addon = xbmcaddon.Addon('plugin.video.bitchuteq')
__language__  = addon.getLocalizedString
__icon__ = addon.getAddonInfo('icon')
__fanart__ = addon.getAddonInfo('fanart')

#headers = ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
headers = [['User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0 SeaMonkey/2.46'],
    ['Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8']]

def CATEGORIES():

#Video categories on Main Page
    req = urllib2.Request("http://www.bitchute.com/")
    for header in headers:
        req.add_header(*header)
    url = urllib2.urlopen(req)
    body = url.read()

    soup = BeautifulSoup(body, "html.parser")
    
    links = {}
    
    for link in soup.find_all('li'):
        for link2 in link.find_all('a'):
             href = link2.get('href')
             if not href: continue
             href = ("https://www.bitchute.com"+href if href[0] == "/" else href)
             if "/category/" in href:
                 links[href] = {}

    iconImage='DefaultVideo.png'
    for link in links:
        addDir(link[link.index("/category/")+10:].title(),link,1,iconImage)
#
#Latest Videos on Main Page
    req = urllib2.Request("https://www.bitchute.com/profile/jczKgfJKWJEJ/")
    for header in headers:
        req.add_header(*header)
    urlx = urllib2.urlopen(req)
    bodyx = urlx.read()
    soup = BeautifulSoup(bodyx, "html.parser")

    links = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        className = link.get('class')
        if href and href.startswith('/video'):
            if className and 'btn' in className:
                continue
            children = link.find_all('img',{'class':'img-responsive'})
            if link.parent.name.lower() == "img":
                if "img-responsive" in link.parent.get('class'):
                    children += link.parent.parent.find_all('img',{'class':'img-responsive'})
            for child in children:
                if href not in links:
                    links[href] = {}
                child_data_src = child.get("data-src")
                if child_data_src and "play-button" not in child_data_src and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = child_data_src
                childsrc = child.get("src")
                if "play-button.png" not in childsrc and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = childsrc
            if len(children) == 0:
                if href not in links:
                    links[href] = {}
                links[href]["name"] = link.contents[0].strip("\n").strip()
    links2 = []
    for link in links.iteritems():
        thumbnail = None if "thumbnail" not in link[1] else link[1]["thumbnail"]
        if thumbnail != None and thumbnail[0] == "/":
            thumbnail = "https://www.bitchute.com"+thumbnail
        if thumbnail == None:
            thumbnail = __icon__
        linkToURL = link[0] if link[0][0] != "/" else "https://www.bitchute.com"+link[0]
        addDir(link[1]["name"].encode("utf8"),linkToURL.encode("utf8"),2,thumbnail)
              
def INDEX(url):
    req = urllib2.Request(url)
    for header in headers:
        req.add_header(*header)
    urlx = urllib2.urlopen(req)
    bodyx = urlx.read()
    soup = BeautifulSoup(bodyx, "html.parser")

    links = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        className = link.get('class')
        if href and href.startswith('/video'):
            if className and 'btn' in className:
                continue
            children = link.find_all('img',{'class':'img-responsive'})
            if link.parent.name.lower() == "img":
                if "img-responsive" in link.parent.get('class'):
                    children += link.parent.parent.find_all('img',{'class':'img-responsive'})
            for child in children:
                if href not in links:
                    links[href] = {}
                child_data_src = child.get("data-src")
                if child_data_src and "play-button" not in child_data_src and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = child_data_src
                childsrc = child.get("src")
                if "play-button.png" not in childsrc and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = childsrc
            if len(children) == 0:
                if href not in links:
                    links[href] = {}
                links[href]["name"] = link.contents[0].strip("\n").strip()
    links2 = []
    for link in links.iteritems():
        thumbnail = None if "thumbnail" not in link[1] else link[1]["thumbnail"]
        if thumbnail != None and thumbnail[0] == "/":
            thumbnail = "https://www.bitchute.com"+thumbnail
        if thumbnail == None:
            thumbnail = __icon__
        linkToURL = link[0] if link[0][0] != "/" else "https://www.bitchute.com"+link[0]
        addDir(link[1]["name"].encode("utf8"),linkToURL.encode("utf8"),2,thumbnail)


def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        for header in headers:
            req.add_header(*header)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=(re.compile("torrent.addWebSeed\('(.+?)'\)").findall(link)+re.compile('torrent.addWebSeed\("(.+?)"\)').findall(link))
        if len(match) == 0:
            match += re.compile(r'<source src="(.+?)"(?:\s*)\/?>').findall(link)
        for url in match:
                addLink(name,url,__icon__)
        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)       

elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

else:
        print ""+url
        CATEGORIES()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
