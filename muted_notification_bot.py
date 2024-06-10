import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USER_ID = int(os.getenv("BOT_USER_ID"))
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=False)

#message test channel on launch
@bot.event
async def on_ready():
    print('running...')
    channel = bot.get_channel(TEST_CHANNEL_ID)
    await channel.send('running...')

#handle voice state changes 
@bot.event
async def on_voice_state_update(member, before, after):
    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

    #if a member joins a channel and the bot has not already joined any channel
    if after.channel and not voice_client:
        await after.channel.connect()
        print("connected to vc")
    
    #if a member moves from one channel to another and the new channel has more members, the bot will follow
    elif voice_client and before.channel and after.channel and after.channel != before.channel and len(after.channel.members) >= len(before.channel.members):
        await voice_client.disconnect()
        await after.channel.connect()
        print("changed vc")

    #if the bot is the sole remaining member in a channel, disconnect 
    elif voice_client and len(voice_client.channel.members) == 1:
        await voice_client.disconnect()
        print("disconnected from vc")
    
    #if bot has just disconnected from a channel, check if any other channels have members and join the most populous
    elif member.id == BOT_USER_ID and not voice_client:
        print("checking for active vc...")
        if not member.guild.voice_channels:
            print("no vc found") #works for now, axpand to notify the user later
            return
        most_pop_vc = member.guild.voice_channels[0]
        for vc in member.guild.voice_channels:
            if len(vc.members) > len(most_pop_vc.members):
                most_pop_vc = vc
        if len(most_pop_vc.members) > 0:
            await most_pop_vc.connect()
            print("reconnected to vc")
        else:
            print("no active vc")

    #if user has deafened themselves message user's current voice channel with their username and status eg 'username deafened'
    if before.self_deaf == False and after.self_deaf == True:
        await after.channel.send(str(member) + " deafened")
        print(str(member) + " deafened")

    #if user has muted themselves message user's current voice channel with their username and status eg 'username muted'
    elif before.self_mute == False and after.self_mute == True:
        await after.channel.send(str(member) + " muted")
        print(str(member) + " muted")

bot.run(BOT_TOKEN)
