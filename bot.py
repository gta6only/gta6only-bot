import discord
from discord.ext import commands, tasks
import aiohttp, asyncio, json, os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
CHANNEL_TWITTER_ID = int(os.getenv("CHANNEL_TWITTER_ID","0"))
CHANNEL_INSTAGRAM_ID = int(os.getenv("CHANNEL_INSTAGRAM_ID","0"))
TWITTER_ACCOUNTS = ["RockstarGames","GTAVI","RockstarSupport"]
INSTAGRAM_ACCOUNTS = ["rockstargames", "gtacommunity", "gtaleaks", "gta6only.game", "gta6france_officiel"]
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
seen_tweets = set()
seen_instagram = set()

def load_seen():
        global seen_tweets,seen_instagram
        try:
                    with open("seen.json") as f:
                                    d=json.load(f);seen_tweets=set(d.get("tweets",[]));seen_instagram=set(d.get("instagram",[]))
                            except: pass

    def save_seen():
            with open("seen.json","w") as f:
                        json.dump({"tweets":list(seen_tweets)[-200:],"instagram":list(seen_instagram)[-200:]},f)

        async def fetch_tweets(s,u):
                if not TWITTER_BEARER_TOKEN:return []
                        h={"Authorization":f"Bearer {TWITTER_BEARER_TOKEN}"}
    async with s.get(f"https://api.twitter.com/2/users/by/username/{u}",headers=h) as r:
                if r.status!=200:return []
                            uid=(await r.json()).get("data",{}).get("id")
        if not uid:return []
                async with s.get(f"https://api.twitter.com/2/users/{uid}/tweets?max_results=5&tweet.fields=created_at,attachments&expansions=attachments.media_keys&media.fields=url,preview_image_url,type",headers=h) as r:
                            if r.status!=200:return []
                                        data=await r.json()
        return data if isinstance(data,dict) else []

def tweet_embed(t,u,img=None):
        e=discord.Embed(description=t.get("text",""),color=0x1DA1F2,timestamp=datetime.now(timezone.utc))
    e.set_author(name=f"@{u} sur X",url=f"https://twitter.com/{u}/status/{t['id']}")
    e.add_field(name="Lien",value=f"[Tweet](https://twitter.com/{u}/status/{t['id']})")
    if img:e.set_image(url=img)
            e.set_footer(text="GTA6only Bot");return e

async def fetch_ig(s,u):
        try:
                    async with s.get(f"https://rsshub.app/instagram/user/{u}",timeout=aiohttp.ClientTimeout(total=10)) as r:
                                    return parse_rss(await r.text(),u) if r.status==200 else []
                            except:return []

    def parse_rss(x,u):
            import xml.etree.ElementTree as ET
            items=[]
            try:
                        root=ET.fromstring(x);ch=root.find("channel")
                        for item in (ch.findall("item")[:5] if ch else []):
                                        l=item.findtext("link","");d=item.findtext("description","")
                                        img=None
                                        if 'src="' in d:
                                                            s2=d.find('src="')+5;img=d[s2:d.find('"',s2)]
                                                        items.append({"id":l,"title":item.findtext("title",""),"link":l,"img_url":img,"username":u})
                                except:passi
                                    m p o r tr edtiusrcno ridt
efmrso
m
 ddeifs ciogr_de.mebxetd (ipm)p:o
r t   c oem=mdainsdcso,r dt.aEsmkbse
di(mtpiotrlte =api[o"httittpl,e "a]s[y:n2c5i6o],  ojrs o"nP,o sots 
Ifnrsotma gdraatme"t,icmoel oirm=p0oxrEt1 3d0a6tCe,ttiimmee,s ttaimmpe=zdoantee
tfirmoem. ndoowt(etnivm eizmopnoer.tu tlco)a)d
_ d o t een.vs
e
tl_oaaudt_hdoort(ennavm(e)=
fD"I@S{CpO[R'Du_sTeOrKnEaNm e=' ]o}s .Ignestteangvr(a"mD"I,SuCrOlR=Dp_[T"OlKiEnNk"")]
)T
W I T T EeR._aBdEdA_RfEiRe_lTdO(KnEaNm e== "oLsi.egne"t,evnavl(u"eT=WfI"T[TPEoRs_tB]E(A{RpE[R'_lTiOnKkE'N]"}))
"C)H
A N N E Li_fT WpI.TgTeEtR(_"IiDm g=_ uirnlt"()o:se..gseette_nivm(a"gCeH(AuNrNlE=Lp_[T"WiImTgT_EuRr_lI"D]"),
" 0 " ) )e
.CsHeAtN_NfEoLo_tIeNrS(TtAeGxRtA=M"_GITDA 6=o nilnyt (Boost."g)e;treentvu(r"nC HeA
N
N@EtLa_sIkNsS.TlAoGoRpA(Mm_iInDu"t,e"s0="1)5))

TaWsIyTnTcE Rd_eAfC CcOhUeNcTkS_ t=w i[t"tReorc(k)s:t
a r G a mcehs="b,o"tG.TgAeVtI_"c,h"aRnoncekls(tCaHrASNuNpEpLo_rTtW"I]T
TIENRS_TIADG)R
A M _ A CiCfO UnNoTtS  c=h :[r"ertoucrkns
t a r g aamseysn"c,  w"igttha caoimomhutntipt.yC"l,i e"ngttSaelsesaikosn"(,)  "agst as6:o
n l y . g a m e "f,o r" gut ai6nf rTaWnIcTeT_EoRf_fAiCcCiOeUlN"T]S
:i
n t e n t s   =   d i s ctorryd:.
I n t e n t s . d e f a u l t ( )d
aitnat=eanwtasi.tm efsestacghe__tcwoenettesn(ts ,=u )T
r u e 
 b o t   =   c o m m a n disf. Bnoott( cdoamtmaa:ncdo_nptrienfuiex
 = " ! " ,   i n t e n t s = i n ttewnetest)s
 =sdeaetna_.tgweete(t"sd a=t as"e,t[(]))
  soere n[_]i
  n s t a g r a m   =   s e t ( ) 
  m
  eddeifa sl=o{amd[_"smeeedni(a)_:k
  e y " ] :gml ofboarl  ms eienn _dtawteae.tgse,ts(e"einn_cilnusdteasg"r,a{m}
  ) . g e tt(r"ym:e
  d i a " , [ ] ) }w
  i t h   o p e n ( " s e e n . j sfoonr" )t  aisn  fr:e
  v e r s e d ( t w e e t sd)=:j
  s o n . l o a d ( f ) ; s e e n _ t w e eitfs =ts[e"ti(dd".]g eitn( "steweene_ttsw"e,e[t]s):)c;osneteinn_uien
  s t a g r a m = s e t ( d . g e t ( " i nsseteang_rtawme"e,t[s].)a)d
  d ( t [ "eixdc"e]p)t;:i mpga=sNso
  n
  ed
  e f   s a v e _ s e e n ( ) : 
           wfiotrh  ko pienn (t".sgeeetn(."jastotna"c,h"mwe"n)t sa"s, {f}:)
           . g e t ( " m e djisao_nk.edyusm"p,([{]")t:w
           e e t s " : l i s t ( s e e n _ t w e e t s ) [ -m2=0m0e:d]i,a"si.ngsetta(gkr)a
           m " : l i s t ( s e e n _ i n s t a g r a m ) [ -i2f0 0m::]i}m,gf=)m
           .
           gaesty(n"cu rdle"f)  foert cmh._gtewte(e"tpsr(esv,iue)w:_
           i m a g ei_fu rnlo"t) ;TbWrIeTaTkE
           R _ B E A R E R _ T O K E N : r e t u r na w[a]i
           t   c h .hs=e{n"dA(u"t@heovreirzyaotnieo n🚨" :Nfo"uBveealrleer  n{eTwWsI TGTTEAR6_ B!E"A,ReEmRb_eTdO=KtEwNe}e"t}_
           e m b e da(sty,nuc, iwmigt)h) ;sa.wgaeitt( fa"shytntcpiso:./s/laepeip.(t1w)i
           t t e r . c o m / 2 / u seexrcse/pbty /Euxsceerpntaimoen/ {aus} "e,:hperaidnetr(sf="h[)T Wa]s{ ur}::
           { e } " ) 
                 i fs arv.es_tsaeteuns(!)=
                 2
                 0@0t:arsektsu.rlno o[p](
                 m i n u t e s = 3u0i)d
                 =a(saywnaci td erf. jcshoenc(k)_)i.ngsetta(g"rdaamt(a)":,
                 { } ) . gceht=(b"oitd."g)e
                 t _ c h a n n e li(fC HnAoNtN EuLi_dI:NrSeTtAuGrRnA M[_]I
                 D ) 
                     a s yinfc  nwoitt hc hs:.rgeettu(rfn"
                     h t t p sa:s/y/nacp iw.ittwhi tatieorh.tctopm./C2l/iuesnetrSse/s{suiiodn}(/)t waese tss:?
                     m a x _ r e s u lftosr= 5u& tiwne eItN.SfTiAeGlRdAsM=_cArCeCaOtUeNdT_Sa:t
                     , a t t a c h m e n t s &terxyp:a
                     n s i o n s = a t t a c h m e n tfso.rm epd iian_ kreeyvse&rmseeddi(aa.wfaiietl dfse=tucrhl_,ipgr(esv,iue)w)_:i
                     m a g e _ u r l , t y p e " , h e a d e risf= hp)[ "aisd "r]: 
                     i n   s e e n _ iinfs tra.gsrtaamt:ucso!n=t2i0n0u:er
                     e t u r n   [ ] 
                                      d a t as=eaewna_iitn srt.ajgsroanm(.)a
                                      d d ( p [ " i d "r]e)t;uarwna idta tcah .isfe nids(i"n@setvaenrcyeo(ndea t🚨 aN,oduivcetl)l ee lnseew s[ ]G
                                      T
                                      Ad6e f! "t,weemebte_de=mibge_de(mtb,eud,(ipm)g)=;Naownaei)t: 
                                      a s y n cei=od.isslceoerpd(.1E)m
                                      b e d ( d e s c r i p t ieoxnc=etp.tg eEtx(c"etpetxito"n, "a"s) ,ec:oplroirn=t0(xf1"D[AI1GF]2{,ut}i:m{ees}t"a)m
                                      p = d a tseatviem_es.eneonw(()t
                                      i
                                      m@ebzootn.ec.oumtmca)n)d
                                      ( ) 
                                       a sey.nsce td_eafu tshtoart(unsa(mcet=xf)":@
                                       { u }   seu=rd iXs"c,ourrdl.=Efm"bhetdt(ptsi:t/l/et=w"iGtTtAe6ro.ncloym /B{out}"/,sctoaltours=/0{xt0[0'FiFd8'8])}
                                       " ) 
                                           e . aed.da_dfdi_eflide(lnda(mnea=m"eT=w"iLtiteenr"",,vvaalluuee==fs"t[rT(wTeWeItT]T(EhRt_tApCsC:O/U/NtTwSi)t)t;eer..acdodm_/f{iue}l/ds(tnaatmues=/"{Itn[s'tiadg'r]a}m)"",)v
                                           a l u e =isft ri(mIgN:SeT.AsGeRtA_Mi_mAaCgCeO(UuNrTlS=)i)m
                                           g ) 
                                               a w aei.ts ectt_xf.osoetnedr((etmebxetd=="eG)T
                                               A
                                               6@obnolty. cBoomtm"a)n;dr(e)t
                                               u@rcno mem
                                               a
                                               nadssy.nhca sd_epfe rfmeitscshi_oings((sa,dum)i:n
                                               i s t r attroyr:=
                                               T r u e ) 
                                                a s yanscy ndce fw iftohr cse.fgeettc(hf("chttxt)p:s
                                                : / / r saswhauibt. acptpx/.isnesntda(g"rCahme/cuks.e.r./"{)u;}a"w,atiitm ecohuetc=ka_itowhittttpe.rC(l)i;eanwtaTiitm ecohuetc(kt_oitnaslt=a1g0r)a)m (a)s; arw:a
                                                i t   c t x . s e n d ( "rOeKt!u"r)n

                                                 p@abroste._ervsesn(ta
                                                 waasiytn cr .dteefx to(n)_,rue)a diyf( )r:.
                                                 s t a t ulso=a=d2_0s0e eenl(s)e; p[r]i
                                                 n t ( f "eOxKc:e{pbto:tr.eutsuerrn} "[)];
                                                 c
                                                 hdeecfk _ptawristet_errs.ss(txa,rut)(:)
                                                 ; c h e cikm_pionrstt axgmrla.me.tsrteaer.tE(l)e
                                                 m e n t Tarweaei ta sb oEtT.
                                                 c h a n giet_epmrse=s[e]n
                                                 c e ( a cttriyv:i
                                                 t y = d i s c o rrdo.oGta=mEeT(.nfarmoem=s"tGrTiAn gV(Ix"));)c
                                                 h
                                                 =brooto.tr.ufni(nDdI(S"CcOhRaDn_nTeOlK"E)N
                                                 )        for item in (ch.findall("item")[:5] if ch else []):
                                                             l=item.findtext("link","");d=item.findtext("description","")
                                                                         img=None
                                                                                     if 'src="' in d:
                                                                                                     s2=d.find('src="')+5;img=d[s2:d.find('"',s2)]
                                                                                                                 items.append({"id":l,"title":item.findtext("title",""),"link":l,"img_url":img,"username":u})
                                                                                                                     except:pass
                                                                                                                         return items
                                                                                                                         
                                                                                                                         def ig_embed(p):
                                                                                                                             e=discord.Embed(title=p["title"][:256] or "Post Instagram",color=0xE1306C,timestamp=datetime.now(timezone.utc))
                                                                                                                                 e.set_author(name=f"@{p['username']} Instagram",url=p["link"])
                                                                                                                                     e.add_field(name="Lien",value=f"[Post]({p['link']})")
                                                                                                                                         if p.get("img_url"):e.set_image(url=p["img_url"])
                                                                                                                                             e.set_footer(text="GTA6only Bot");return e
                                                                                                                                             
                                                                                                                                             @tasks.loop(minutes=15)
                                                                                                                                             async def check_twitter():
                                                                                                                                                 ch=bot.get_channel(CHANNEL_TWITTER_ID)
                                                                                                                                                     if not ch:return
                                                                                                                                                         async with aiohttp.ClientSession() as s:
                                                                                                                                                                 for u in TWITTER_ACCOUNTS:
                                                                                                                                                                             try:
                                                                                                                                                                                             data=await fetch_tweets(s,u)
                                                                                                                                                                                                             if not data:continue
                                                                                                                                                                                                                             tweets=data.get("data",[]) or []
                                                                                                                                                                                                                                             medias={m["media_key"]:m for m in data.get("includes",{}).get("media",[])}
                                                                                                                                                                                                                                                             for t in reversed(tweets):
                                                                                                                                                                                                                                                                                 if t["id"] in seen_tweets:continue
                                                                                                                                                                                                                                                                                                     seen_tweets.add(t["id"]);img=None
                                                                                                                                                                                                                                                                                                                         for k in t.get("attachments",{}).get("media_keys",[]):
                                                                                                                                                                                                                                                                                                                                                 m=medias.get(k)
                                                                                                                                                                                                                                                                                                                                                                         if m:img=m.get("url") or m.get("preview_image_url");break
                                                                                                                                                                                                                                                                                                                                                                                             await ch.send("@everyone 🚨 Nouvelle news GTA6 !",embed=tweet_embed(t,u,img));await asyncio.sleep(1)
                                                                                                                                                                                                                                                                                                                                                                                                         except Exception as e:print(f"[TW]{u}:{e}")
                                                                                                                                                                                                                                                                                                                                                                                                             save_seen()
                                                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                                             @tasks.loop(minutes=30)
                                                                                                                                                                                                                                                                                                                                                                                                             async def check_instagram():
                                                                                                                                                                                                                                                                                                                                                                                                                 ch=bot.get_channel(CHANNEL_INSTAGRAM_ID)
                                                                                                                                                                                                                                                                                                                                                                                                                     if not ch:return
                                                                                                                                                                                                                                                                                                                                                                                                                         async with aiohttp.ClientSession() as s:
                                                                                                                                                                                                                                                                                                                                                                                                                                 for u in INSTAGRAM_ACCOUNTS:
                                                                                                                                                                                                                                                                                                                                                                                                                                             try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                             for p in reversed(await fetch_ig(s,u)):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 if p["id"] in seen_instagram:continue
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     seen_instagram.add(p["id"]);await ch.send("@everyone 🚨 Nouvelle news GTA6 !",embed=ig_embed(p));await asyncio.sleep(1)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 except Exception as e:print(f"[IG]{u}:{e}")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     save_seen()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     @bot.command()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     async def status(ctx):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         e=discord.Embed(title="GTA6only Bot",color=0x00FF88)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             e.add_field(name="Twitter",value=str(TWITTER_ACCOUNTS));e.add_field(name="Instagram",value=str(INSTAGRAM_ACCOUNTS))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 await ctx.send(embed=e)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 @bot.command()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 @commands.has_permissions(administrator=True)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 async def forcefetch(ctx):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     await ctx.send("Check...");await check_twitter();await check_instagram();await ctx.send("OK!")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     @bot.event
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     async def on_ready():
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         load_seen();print(f"OK:{bot.user}");check_twitter.start();check_instagram.start()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             await bot.change_presence(activity=discord.Game(name="GTA VI"))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             bot.run(DISCORD_TOKEN)
