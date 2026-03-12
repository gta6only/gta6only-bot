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
    h={"Authorization":f"Bearer {TWITTER_BEARER_TOKEN}"}
    async with s.get(f"https://api.twitter.com/2/users/by/username/{u}",headers=h) as r:
        if r.status!=200:return []
        uid=(await r.json()).get("data",{}).get("id")
        if not uid:return []
    async with s.get(f"https://api.twitter.com/2/users/{uid}/tweets?max_results=5&tweet.fields=created_at,attachments&expansions=attachments.media_keys&media.fields=url,preview_image_url,type",headers=h) as r:
        return await r.json() if r.status==200 else []

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
                data=await fetch_tweets(s,u);tweets=data.get("data",[]) or []
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
