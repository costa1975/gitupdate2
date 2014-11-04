import urllib,re,string,sys,os
import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
prettyName = 'PFTV'

BASE_URL='http://free-tv-video-online.me/internet/'

def MAINPFTV():
        main.addDir('Search','s',468,art+'/search.png')
        main.addDir('A-Z','s',463,art+'/az.png')
        main.addDir('Yesterdays Episodes','http://www.free-tv-video-online.me/internet/index_last_3_days.html',460,art+'/yesepi.png')
        main.addDir('Todays Episodes','http://www.free-tv-video-online.me/internet/index_last.html',460,art+'/toepi2.png')
        main.addDir('Popular Shows','shows',467,art+'/popshowsws.png')
        main.addDir('This Weeks Popular Episodes','season',467,art+'/thisweek.png')
        main.GA("Plugin",prettyName)
        main.VIEWSB()



def SearchhistoryPFTV(index=False):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            SEARCHWS(index=index)
        else:
            main.addDir('Search','###',469,art+'/search.png',index=index)
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,469,thumb,index=index)

def superSearch(encode,type):
    try:
        returnList=[]
        epi = re.search('(?i)s(\d+?)e(\d+?)$',encode)
        if epi:
            epistring = encode.rpartition('%20')[2].upper()
            e = int(epi.group(2))
            s = int(epi.group(1))
            ss=str(s)
            encodewithoutepi = urllib.quote(re.sub('(?i)(\ss(\d+)e(\d+))|(Season(.+?)Episode)|(\d+)x(\d+)','',urllib.unquote(encode)).strip())
            surl='http://www.free-tv-video-online.me/search/?q='+encodewithoutepi+'&md=shows'
            link=main.OPENURL(surl,verbose=False)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
            match=re.compile(' class="mnlcategorylist"><a href="([^"]+)"><b>([^<]+)</b>',re.DOTALL).findall(link)
            for url,nameds in match:
                url = 'http://www.free-tv-video-online.me' + url+'/season_'+ss+'.html'
            if(len(str(e))==1): e = "0" + str(e)
            if len(str(s))==1: s= "0" + str(s)
            name=nameds+' S'+str(s)+'E'+str(e)
            returnList.append((name,prettyName,url,'',461,True))
            return returnList
        surl='http://www.free-tv-video-online.me/search/?q='+encode+'&md=shows'
        link=main.OPENURL(surl,verbose=False)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile(' class="mnlcategorylist"><a href="([^"]+)"><b>([^<]+)</b>',re.DOTALL).findall(link)
        for url,name in match:
            url = 'http://www.free-tv-video-online.me' + url
            returnList.append((name,prettyName,url,'',461,True))
        return returnList
    except: return []
            
def SEARCHPFTV(murl = '',index=False):
        encode = main.updateSearchFile(murl,'TV')
        if not encode: return False   
        surl='http://www.free-tv-video-online.me/search/?q='+encode+'&md=shows'
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile(' class="mnlcategorylist"><a href="([^"]+)"><b>([^<]+)</b>',re.DOTALL).findall(link)
        for url,name in match:
                main.addDirT(name,'http://free-tv-video-online.me'+url,465,'','','','','','',index=index)
        main.GA(prettyName,"Search")
def AtoZPFTV():
    main.addDir('0-9','#',464,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,(chr(ord(i)+1)),464,art+'/'+i.lower()+'.png')
    main.GA(prettyName,"A-Z")
    main.VIEWSB()

def LISTSHOW(mname,murl):
    link=main.OPENURL(BASE_URL)
    link=link.replace('\r','').replace('\n','').replace('\t','')
    if 'Z' in mname:
        links = re.search('<a name="Z">(.+?)<!-- End of the page footer -->', link)
    elif '0-9' in mname:
        links = re.search('<a name="#">(.+?)<a name="A">', link)
    else:
        links = re.search('<a name="'+mname+'">(.+?)<a name="'+murl+'">', link)
    if links:
        links = links.group(1)
        match=re.compile('''class="mnlcategorylist"><a href="([^"]+?)"><b>([^<]+?)</b></a>''', re.DOTALL).findall(links)
        for url, name in match:
            main.addDirT(name,BASE_URL+url,465,'','','','','','')

def POPULARPFTV(murl):
        link=main.OPENURL('http://www.free-tv-video-online.me/')
        link=link.replace('\r','').replace('\n','').replace('\t','')
        if 'season' in murl:
                match=re.compile('(?sim)<td class="tleft" style="text-align:center"><a href="([^"]+?)">([^<]+?)</a>').findall(link)
        else:
                match=re.compile('(?sim)<td class="tleft" style="text-align:center;"><a href="([^"]+?)">([^<]+?)</a>').findall(link)
        for url,name in match:
            if 'season' in murl:
                    sepi=re.findall('(?sim)(\(s(\d+)e(\d+)\))',name)
                    if sepi:
                            name=re.sub('(?sim)(\(s(\d+)e(\d+)\))','',name)
                            fname = re.sub('-',sepi[0],name).replace('(','').replace(')','')
                    main.addDirTE(fname,'http://free-tv-video-online.me'+url,461,'','','','','','')
            else:
                    main.addDirT(name,url,465,'','','','','','')
            #main.addDir(name,murl,461,thumb)
        
            
def LISTSEASON(mname,murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        thumb=art+'/folder.png'
        match=re.compile('class="mnlcategorylist"><a href="([^"]+?)"><b>([^<]+?)</b></a>([^<]+?)</td>').findall(link)
        for url, name, count in reversed(match):
            main.addDir(mname+' [COLOR red]'+name+'[/COLOR] '+count,murl+url,466,thumb)

def LISTEPISODE(mname,murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('(?sim)<td class="episode"><a name=".+?"></a><b>([^<]+?)</b></td><td class="mnllinklist" align="right"><div class="right">(s\d+e\d+).+?</div>').findall(link)
        for name,epi in reversed(match):
            mname=re.sub('(\(.+?\))','[COLOR red]Episode[/COLOR]',mname)
            name=mname+' [COLOR red]'+name.strip().replace('.','')+'[/COLOR]'
            name = re.sub('Seas(on)?\.? (\d+).*?Ep(isode)?\.? (\d+)',epi,main.removeColorTags(name),re.I)
            #name=name.encode('utf-8')
            name = name.decode("utf-8", "ignore")
            main.addDirTE(name,murl,461,'','','','','','')
    
def LISTPFTV(murl):
        main.GA(prettyName,"List")
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('''class="mnlcategorylist"><a href="([^"]+?)"><b>([^<]+?)<span style='.+?'>\((.+?)\)''').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url, name, count in match:
            name=re.sub('\((\d+)x(\d+)\)','',name,re.I)
            episode = re.search('Seas(on)?\.? (\d+).*?Ep(isode)?\.? (\d+)',name, re.I)
            if(episode):
                e = str(episode.group(4))
                if(len(e)==1): e = "0" + e
                s = episode.group(2)
                if(len(s)==1): s = "0" + s
                name = re.sub('Seas(on)?\.? (\d+).*?Ep(isode)?\.? (\d+)','',name,re.I)
                name = name.strip() + " " + "S" + s + "E" + e
                main.addDirTE(name,BASE_URL+url,461,'','','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait

def LISTHOST(mname,murl,thumb):
    epi = re.findall('\ss(\d+)e(\d+)\s',mname + " ",re.I)
    for s,e in epi:
        pass
    if e[0:1]=='0':
        epis=e[1:]
    else:
        epis=e
    CheckNextEpi= int(epis)+1
    if(len(str(CheckNextEpi))==1): CheckNextEpi = "0" + str(CheckNextEpi)
    CheckNextEpi ="S" + str(s) + "E" + str(CheckNextEpi)
    CurrentEpi = re.search('(?i)(s\d+e\d+)',mname)
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','')
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    if CheckNextEpi in link:
        links = re.search('<td class="mnllinklist" align="right"><div class="right">'+CurrentEpi.group(1)+'.+?</div>(.+?)<div class="right">'+CheckNextEpi+'.+?</div>', link)
    else:
        links = re.search('<td class="mnllinklist" align="right"><div class="right">'+CurrentEpi.group(1)+'.+?</div>(.+?)<!-- End of the page footer -->', link)
    if links:
        links = links.group(1)
        match=re.compile('''<a onclick='.+?href="([^"]+?)" target=".+?"><div>.+?</div><span>Loading Time: <span class='.+?'>([^<]+?)</span><br/>Host:(.+?)<br/>''', re.DOTALL).findall(links)
        for url, loadtime, name in match:
            domain=name    
            name=name.replace(' ','')
            if name[0:1]=='.':
                name=name[1:]
            name=name.split('.')[0]
            if main.supportedHost(name.strip().lower()):
                try:mediaID=url.split('?id=')[1]
                except:mediaID=url.split('http://')[1].split('/')[1]
                main.addDown2(mname+' [COLOR red](Loading Time: '+loadtime+')[/COLOR]'+' [COLOR blue]'+name.upper()+'[/COLOR]',name.lower().strip()+'x1x8x'+mediaID,462,art+'/hosts/'+name.lower()+'.png',art+'/hosts/'+name.lower()+'.png')

        
        

def PLAYPFTV(mname,murl):
    host=murl.split('x1x8x')[0]
    media_id=murl.split('x1x8x')[1]
    main.GA(prettyName,"Watched")
    ok=True
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Checking Link,3000)")
    #furl=geturl(murl)
    infoLabels =main.GETMETAEpiT(mname,'','')
    video_type='episode'
    season=infoLabels['season']
    episode=infoLabels['episode']
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
    try:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        
        import urlresolver
        source = urlresolver.HostedMediaFile(host=host, media_id=media_id)
        if source:
                stream_url = source.resolve()
        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory('plugin.video.movie25')
            wh.add_item(mname+' '+'[COLOR green]PFTV[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=img, fanart='', is_folder=False)
            player.KeepAlive()
            return ok
    except Exception, e:
            if stream_url != False:
                main.ErrorReport(e)
            return ok
#<td class="mnllinklist" align="right"><div class="right">S01E04.+?</div>