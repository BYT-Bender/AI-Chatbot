# bot.py
import os
import sys
import json
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import numpy as np


parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_directory)

from chatbot import Chatbot

def load_config(config_file):
    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Config file '{config_file}' not found.")
    except Exception as error:
        raise Exception(f"Error loading configuration: {error}")
    
config_file = "config.json"
config = load_config(config_file)
config["log_file"] = config["log_files"]["discord"]
chatbot_instance = Chatbot(config)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = 1164578591556767936

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True 
intents.message_content = True
intents.members = True

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='/', description="STELLA - AI Chatbot (Beta 6.3)", help_command=help_command, intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user.name} is connected to {guild.name}!')

    # async for member in guild.fetch_members(limit=150):
    #     print(member.name)
    

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == CHANNEL:
        if message.content == 'raise-exception':
            raise discord.DiscordException
        
        else:
            chatbot_response = chatbot_instance.generate_response(message.content)

            if chatbot_response:
                await message.channel.send(chatbot_response)

    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('log/error.log', 'a', encoding='utf-8') as f:
        if event == 'on_message':
            # clean_message = ''.join(char if char.isprintable() else '?' for char in args[0])
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)