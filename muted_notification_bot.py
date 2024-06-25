import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USER_ID = int(os.getenv('BOT_USER_ID'))
TEST_CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
FFMPEG_PATH = os.getenv('FFMPEG_PATH')
DEFAULT_SOUND_PATH = os.getenv('DEFAULT_SOUND_PATH')
CUSTOM_SOUNDS_PATH = os.getenv('CUSTOM_SOUNDS_PATH')

#custom sound paths for certain Discord members are stored in a .json file
custom_sounds = json.load(open(os.path.join(os.path.dirname(__file__), CUSTOM_SOUNDS_PATH)))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=False)

#play chosen notification sound in voice channel
async def play(voice_client, member):   
    if str(member.id) in custom_sounds:
        sound_path = os.path.join(os.path.dirname(__file__), custom_sounds[str(member.id)])
    else:
        sound_path = os.path.join(os.path.dirname(__file__), DEFAULT_SOUND_PATH)
    audio_source = discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=sound_path)
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)
    else:
        print('already playing audio, retrying...')
        time.sleep(2)
        await play(voice_client)

#message test channel on launch
@bot.event
async def on_ready():
    print('running...')
    channel = bot.get_channel(TEST_CHANNEL_ID)
    await channel.send('running...')

#handle voice state changes 
@bot.event
async def on_voice_state_update(member, before, after):
    voice_client = discord.utils.get(bot.voice_clients, guild = member.guild)

    def is_connected():
        return voice_client and voice_client.is_connected()

    if member.id != BOT_USER_ID:
        #if user has deafened themselves and is in the same vc as the bot, message user's current voice channel with their username and status eg 'username deafened'
        if is_connected() and before.self_deaf == False and after.self_deaf == True and voice_client.channel == after.channel:
            await play(voice_client, member)
            message = f'{member} deafened'
            await after.channel.send(message)
            print(message)

        #if user has muted themselves and is in the same vc as the bot, message user's current voice channel with their username and status eg 'username muted'
        elif is_connected() and before.self_mute == False and after.self_mute == True and voice_client.channel == after.channel:
            await play(voice_client, member)
            message = f'{member} muted'
            await after.channel.send(message)
            print(message)

        #if a member joins a channel and the bot has not already joined any channel, join channel
        elif not voice_client and after.channel:
            await after.channel.connect()
            print('connected to vc')
        
        #if a member moves from one channel to another and the new channel has more members, the bot will follow
        elif voice_client and after.channel and before.channel != after.channel and len(after.channel.members) >= len(voice_client.channel.members):
            # await member.guild.voice_client.move_to(after.channel)
            await voice_client.move_to(after.channel)
            print('changed vc')
        
        #if the bot is the sole remaining member in a channel, disconnect 
        elif voice_client and len(voice_client.channel.members) == 1:
            await voice_client.disconnect()
            print('disconnected from vc')
    else:
        #if bot has just disconnected from a channel, check if any other channels have members and join the most populous
        if not voice_client:
            print('checking for active vc...')
            if not member.guild.voice_channels:
                print('no vc found') #works for now, expand to notify the user later
                return
            most_pop_vc = member.guild.voice_channels[0]
            for vc in member.guild.voice_channels:
                if len(vc.members) > len(most_pop_vc.members):
                    most_pop_vc = vc
            if len(most_pop_vc.members) > 0:
                await most_pop_vc.connect()
                print('reconnected to vc')
            else:
                print('no active vc')

bot.run(BOT_TOKEN)