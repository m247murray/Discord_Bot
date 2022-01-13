#py DiscordBot.py

import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import youtube_dl
import asyncio
load_dotenv()
import time
#todo put your bot token here
token = 
TOKEN = os.getenv(token)


global mes 
mes =''



bot = commands.Bot(command_prefix='`')#prefix to call bot commands (`)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'

    
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
   

@bot.command(name = 'search')
async def S (ctx, message):
    destination = ctx.author.voice.channel
        
    vc = await destination.connect()
    s = message
    
    player = await YTDLSource.from_url(s, loop=False)#gets source from link to play
    vc.play(player, after=lambda e: print('player error: %s' % e) if e else None)#plays source
    print(player.data)
    while vc.is_playing():# if the bot is playing loop
        await asyncio.sleep(1)
    await vc.disconnect()# when no longer playing disconect bot so when someone new is added it will restart properly


@bot.command(name='BASS')
async def bass(ctx,message):
        destination = ctx.author.voice.channel
        
        vc = await destination.connect()
        

        await ctx.author.create_dm()
        id = ctx.author.dm_channel.id
        b = bot.get_channel(id)
        
        for i in range(31,40):
            b.send('Hello There')

            time.sleep(0.2)

        if message != '' :
            mes = message
        else:
            message = mes

        player = await YTDLSource.from_url(message, loop=False)#gets source from link to play
       
        vc.play(player, after=lambda e: print('player error: %s' % e) if e else None)#plays source
        vc.source = discord.PCMVolumeTransformer(vc.source, volume = 200.0)
        for i in range(10):# if the bot is playing loop
            await asyncio.sleep(100)
        await vc.disconnect()
        

@bot.command(name='b')
async def dis(ctx):
        print('BRUH MOMENT') 
        await ctx.voice_client.disconnect()

@bot.command(name='a')
async def conn(ctx):
        print('BRUH MOMENT') 
        conn =  ctx.author.voice.channel
        await conn.connect()
 


        

@bot.event #on voice state update event run code
async def on_voice_state_update (member,before,after):
            #check if member is the bot or user is leaving channel
            TWZONE = 802430025982803968
            if(after.channel is None or member.id == 803461671272185873 ): #if member is bot or user is leaving then return
                return
            destination = member.voice.channel
            user_list=destination.members
             #check if bot is already connected to channel   
            for x in user_list:
                if(x.id==803461671272185873):# if bot is already conected to channel return
                    return
            if(after.channel.id==TWZONE ):
                vc = await destination.connect() #if user is connecting to the channel connect the bot to voice channel
            if(member.voice.channel.id == TWZONE):#if user is joining the right channel run Commands
                role = discord.utils.get(member.guild.roles, id=803082472392097833)#gets role
                await member.add_roles(role,reason = None, atomic=True)#adds role to user
                id = 803454043057422376 
                channel = bot.get_channel(id) #uses channel id to get channel object
                name = member.name # gets name of the member
                await channel.send(f' {name} has entered the Twilight zone') # send message on arival of user in text channel
                player = await YTDLSource.from_url('https://www.youtube.com/watch?v=cxf_Dvy0VLs', loop=False)#gets source from link to play
                vc.play(player, after=lambda e: print('player error: %s' % e) if e else None)#plays source
                while vc.is_playing():# if the bot is playing loop
                    await asyncio.sleep(1)
                await vc.disconnect()# when no longer playing disconect bot so when someone new is added it will restart properly


# @bot.command(aka='f1')
# async def Formula1(ctx):
#     link = 'https://ergast.com/api/f1/2021/last/Qualifying'
#     f = urllib.urlopen(link)           
#     myfile = f.open()  
#     json.load(myfile)

        

#todo put your bot token here
bot.run(token)
