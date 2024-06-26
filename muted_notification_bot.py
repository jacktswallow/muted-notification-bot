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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=False)

#helper function to retrieve path
def get_path(path):
    return os.path.join(os.path.dirname(__file__), path)

#play chosen notification sound in voice channel
async def play(voice_client, member, status):   
    if str(member.id) in custom_sounds:
        sound_path = get_path(custom_sounds[str(member.id)][status])
    else:
        sound_path = get_path(DEFAULT_SOUND_PATH)
    audio_source = discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=sound_path)
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)
    else:
        print('already playing audio, retrying...')
        time.sleep(2)
        await play(voice_client, member, status)

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

    #check if bot is connected to voice
    def is_connected():
        return voice_client and voice_client.is_connected()
    
    #on user mute, if user is in the same voice channel as the bot, play mute sound and send message with their username and status eg 'username muted'
    async def muted(mute_type):
        if is_connected() and voice_client.channel == after.channel:
            await play(voice_client, member, 'mute')
            message = f'{member} {mute_type}'
            await after.channel.send(message)
            print(message)

    if member.id != BOT_USER_ID:
        #if user has deafened themselves
        if before.self_deaf == False and after.self_deaf == True:
            await muted('deafened')

        #if user has muted themselves
        elif before.self_mute == False and after.self_mute == True:
            await muted('muted')
        
        #if a user joins the channel that the bot is in, play join sound
        elif voice_client and after.channel and after.channel == voice_client.channel and before.channel != after.channel:
            await play(voice_client, member, 'join')
            print(str(member) + " joined")

        #if a member joins a channel and the bot has not already joined any channel, join channel
        elif not voice_client and after.channel:
            await after.channel.connect()
            print('connected to vc')
        
        #if a member moves from one channel to another and the new channel has more members, the bot will follow
        elif voice_client and after.channel and before.channel != after.channel and len(after.channel.members) >= len(voice_client.channel.members):
            await voice_client.move_to(after.channel)
            print('changed vc')
        
        #if the bot is the sole remaining member in a channel, disconnect 
        elif voice_client and len(voice_client.channel.members) == 1:
            await voice_client.disconnect()
            print('disconnected from vc')
        
        #if a user leaves the channel that the bot is in, play leave sound
        elif voice_client and before.channel and before.channel == voice_client.channel and after.channel != voice_client.channel:
            await play(voice_client, member, 'leave')
            print(str(member) + " left")
    else:
        #if bot has just disconnected from a channel, check if any other channels have members and join the most populous
        if not voice_client:
            print('checking for active vc...')
            most_pop_vc = member.guild.voice_channels[0]
            for vc in member.guild.voice_channels:
                if len(vc.members) > len(most_pop_vc.members):
                    most_pop_vc = vc
            if len(most_pop_vc.members) > 0:
                await most_pop_vc.connect()
                print('reconnected to vc')
            else:
                print('no active vc')

#custom sound paths for certain Discord members are stored in a .json file
custom_sounds = json.load(open(get_path(CUSTOM_SOUNDS_PATH)))

bot.run(BOT_TOKEN)