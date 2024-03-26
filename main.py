import discord
from discord import app_commands

import pykakasi
from pyokaka import okaka
import re

import os

debug = True

if debug:
    print("デバッグモードがオンですわ！")
    
#ファイル確認
needfiles = ["token","words.txt","dispwords.txt"]

for i in needfiles:
    if not os.path.isfile(f"./{i}"):
        raise Exception(f'エラー 必須ファイル"{i}"が存在しません')

TOKEN = open('token', 'r').read()

intents = discord.Intents.default()
intents.message_content=True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

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

def load():
    global words, dispwords
    words = open('words.txt', 'r', encoding='utf-8').read().split("\n")
    dispwords = open('dispwords.txt', 'r', encoding='utf-8').read().split("\n")

def tohira(text):
    kakasi = pykakasi.kakasi()
    return "".join([i["hira"] for i in kakasi.convert(okaka.convert(text))])

def is_hiragana(text):
    # ひらがなのUnicode範囲: \u3040-\u309F
    hiragana_pattern = re.compile(r'^[\u3040-\u309F]+$')
    return bool(hiragana_pattern.match(text))

load()

@client.event
async def on_ready():
    print("discordに接続しました")
    await tree.sync()#スラッシュコマンドを同期

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
        print(f"破廉恥な言葉を{len(hitlist)}個検出しました！えっち！！")
        await message.reply(rpmsg)

@tree.command(name="ping",description="botが正しく動いているか確認します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("botは正常に動いてます",ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」

@tree.command(name="addword",description="語録を監視リストに追加します")
@app_commands.describe(hira="ひらがなで語録を書いてください",disp="語録を表示するときのやつを書いてください")
async def addword(interaction: discord.Interaction,hira:str,disp:str):
    global words, dispwords
    if not hira in words:
        if not disp in dispwords:
            if is_hiragana(hira):
                words += hira
                dispwords += disp
                open("./words.txt", 'a', encoding='utf-8').write(f"\n{hira}")
                open("./dispwords.txt", 'a', encoding='utf-8').write(f"\n{disp}")
                await interaction.response.send_message(f'単語`{disp}`(`{hira}`)は正しく語録リストに追加されました',ephemeral=True)
            else:
                await interaction.response.send_message(f'第1引数として指定された文字列`{hira}`はひらがなではないですわよ！',ephemeral=True)
        else:
            await interaction.response.send_message(f'表示名`{disp}`はすでに語録リストに存在しますわよ',ephemeral=True)
    else:
        await interaction.response.send_message(f'ひらがな`{hira}`はすでに語録リストに存在しますわよ',ephemeral=True)

@tree.command(name="wordlist",description="語録一覧を出力します")
async def wordlist(interaction: discord.Interaction):
    msg = ""
    msg += "`表示名`,`ひらがな`\nのような形式で出力します"
    for i in range(len(words)):
        msg += f"\n`{dispwords[i]}`,`{words[i]}`"
    await interaction.response.send_message(msg,ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」


if debug:
    client.run(TOKEN)
else:
    client.run(TOKEN, log_handler=None) #初期値がわからない