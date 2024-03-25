import discord
import pykakasi
from pyokaka import okaka
import logging

debug = False

if debug:
    print("デバッグモードがオンです！")
    

TOKEN = open('token', 'r').read()

intents = discord.Intents.default()
intents.message_content=True

client = discord.Client(intents=intents)

AA = r"""
   _____                _ _   _                                   _           
  / ____|              (_) | (_)                                 | |          
 | (___   ___ _ __  ___ _| |_ ___   _____  __      _____  _ __ __| |          
  \___ \ / _ \ '_ \/ __| | __| \ \ / / _ \ \ \ /\ / / _ \| '__/ _` |          
  ____) |  __/ | | \__ \ | |_| |\ V /  __/  \ V  V / (_) | | | (_| |          
 |_____/ \___|_| |_|___/_|\__|_| \_/ \___|   \_/\_/ \___/|_|_ \__,_|          
     | |    | |          | | (_)                           | |                
   __| | ___| |_ ___  ___| |_ _  ___  _ __    ___ _   _ ___| |_ ___ _ __ ___  
  / _` |/ _ \ __/ _ \/ __| __| |/ _ \| '_ \  / __| | | / __| __/ _ \ '_ ` _ \ 
 | (_| |  __/ ||  __/ (__| |_| | (_) | | | | \__ \ |_| \__ \ ||  __/ | | | | |
  \__,_|\___|\__\___|\___|\__|_|\___/|_| |_| |___/\__, |___/\__\___|_| |_| |_|
                                                   __/ |                      
                                                  |___/                       
"""

skiplist = ["\n", "、", "。", " ", "　"]

print(AA)

words = open('words.txt', 'r', encoding='utf-8').read().split("\n")
dispwords = open('dispwords.txt', 'r', encoding='utf-8').read().split("\n")

def tohira(text):
    kakasi = pykakasi.kakasi()
    return "".join([i["hira"] for i in kakasi.convert(okaka.convert(text))])


@client.event
async def on_ready():
    print("discordに接続しました")

@client.event
async def on_message(message):
    msg = message.content
    msg = tohira(msg)
    for i in range(len(skiplist)):
        msg = msg.replace(skiplist[i],"")
    
    if message.author.bot:
        return
    
    if any([msg.find(i) != -1 for i in words]):
        hitlist = [dispwords[i] for i in range(len(words)) if msg.find(words[i]) != -1]
        hitcontent = "".join([f"`{i}`、" for i in hitlist])[0:-1]
        rpmsg = f"あなたのメッセージには破廉恥な言葉、{hitcontent}が含まれていますわ"
        print(f"破廉恥な言葉を{len(hitlist)}")
        await message.reply(rpmsg)

if debug:
    client.run(TOKEN)
else:
    client.run(TOKEN, log_handler=None) #初期値がわからない