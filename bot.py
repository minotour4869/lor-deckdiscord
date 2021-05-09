import os, discord, json
from dotenv import load_dotenv
from discord.ext import commands
from deck import Deck

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='d!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} is running...')

@bot.command(name='new', help='Create a new deck from scratch or from a deck code')
async def new(ctx, *args):
    name = args[0]
    code = args[1]
    if (code != ''):
        user_deck = Deck([], code)._decode()
    else:
        user_deck = Deck()
    await ctx.send(f'Sucessfully created deck with name {name}')

@bot.command(name='list')
async def list(ctx, *args):
    pass

bot.run(TOKEN)
