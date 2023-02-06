import discord
import functions
import asyncio
import datetime
import pytz
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
timerActive = False
hour = 0
minute = 0
duration = 10
load_dotenv()

@client.event
async def on_ready():
  print(f"{client.user} is now ready")
  while True:
    if timerActive:
      await send_problem_at_time(channel_id)
    await asyncio.sleep(duration)


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith(".prob"):
    difficulty = {"easy": 1, "medium": 2, "hard": 3}
    diff = message.content.split()[1]
    if diff not in difficulty.keys():
      await message.channel.send("please enter [easy-medium-hard]")
      return
    functions.get_problem(difficulty[diff])
    await message.channel.send(
      f'https://leetcode.com/problems/{functions.get_problem(difficulty[diff])}'
    )

  if message.content.startswith('.timerON'):
    global channel_id,timerActive,hour,minute
    channel_id = message.channel.id
    timerActive = True
    clock = message.content.split()[1].split(':')
    if len(clock) > 1:
      hour = int(clock[0])
      minute = int(clock[1])
    else:
      hour = int(clock[0])
    time = ":".join(clock)
    await message.channel.send(f"Timer has been turned on at {time}.")
  elif message.content == '.timerOFF':
    timerActive = False
    await message.channel.send("Timer has been turned off.")

  if message.content.startswith(".help"):
    embed = discord.Embed(title="Commands", color=0x00bfff)
    value = "pick random problem with specific difficulty according to your choice               difficulty may be [easy-medium-hard]"
    embed.add_field(name="`.prob <difficulty>`", value=value, inline=False)
    embed.add_field(name="`.timerON <time you want in 24H format>`",
                    value="specify time to send a message on it automatically",
                    inline=False)
    embed.add_field(name="`.timerOFF`", value="set timer off", inline=False)
    await message.channel.send(embed=embed)


async def send_problem_at_time(channel_id):
  global timerActive,duration
  tz = pytz.timezone("EET")
  now = datetime.datetime.now(tz)
  duration = 10
  if now.hour == hour and now.minute == minute:
    channel = client.get_channel(channel_id)
    message = f'https://leetcode.com/problems/{functions.get_problem(1)}'
    await channel.send(message)
    duration = 60

@client.event
async def on_guild_join(guild):
  default_channel = discord.utils.get(guild.text_channels, name='general')
  if default_channel:
    await default_channel.send(
      "Hello, I am leetcode bot you can know what i can do by typing `.help` have a        nice day :)"
    )


keep_alive()
client.run(os.getenv("TOKEN"))
