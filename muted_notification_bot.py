import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=False)

#message test channel on launch
@bot.event
async def on_ready():
    print('running...')
    channel = bot.get_channel(TEST_CHANNEL_ID)
    await channel.send('running...')

#message user's current voice channel upon deafen or mute with their username and status eg 'username muted'
@bot.event
async def on_voice_state_update(member, before, after):
    channel = after.channel
    if before.self_deaf == False and after.self_deaf == True:
        print(str(member) + " deafened")
        await channel.send(str(member) + " deafened")
    elif before.self_mute == False and after.self_mute == True:
        print(str(member) + " muted")
        await channel.send(str(member) + " muted")

bot.run(BOT_TOKEN)
