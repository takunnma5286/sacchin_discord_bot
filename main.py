import discord

TOKEN = 'THi5IsDuMMyaCCesSTOK3n00.Cl2FMQ.ThIsi5DUMMyAcc3s5ToKen0000'

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content == '/neko':
        await message.channel.send('にゃーん')

client.run(TOKEN)
