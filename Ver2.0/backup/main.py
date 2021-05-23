import os, discord, json
from dotenv import load_dotenv
from discord.ext import commands
from client import UserDeck
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

data = {}

def init_user_data(user):
    global data

    with open("userdata\data.json", "r", encoding = "utf8") as f:
        data = json.load(f)

    if (user.id not in data):
        data[str(user.id)] = {}
        data[str(user.id)]["deck"] = []
        data[str(user.id)]["elo"] = 1000

    with open("userdata\data.json", "w", encoding = "utf8") as f:
        json.dump(data, f, indent = 4)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Yawn, {bot.user.name} is running...')

@bot.group(name = 'deck', aliases = ['d'], invoke_without_command = True)
async def deck(ctx):
    await ctx.send("Hi, Dad!")

@deck.command(name = 'add', aliases = ['a'], pass_context = True)
async def add(ctx, name = "Imported Deck", deckcode = None):
    print(ctx.author.name)

    try:
        userdeck = UserDeck(name, deckcode)
        if (deckcode is not None): print(deckcode)
        init_user_data(ctx.author)
        data[str(ctx.author.id)]["deck"].append(userdeck.deck)
        with open("userdata\data.json", "w", encoding = "utf8") as f:
            json.dump(data, f, indent = 4)
        await ctx.send(":white_check_mark: Imported deck.")
    except Exception as err:
        await ctx.send(":x: Import deck failed!")
        raise Exception

@bot.group(name = 'card', invoke_without_command = True)
async def card(ctx):
    pass

@card.command(name = 'info', aliases = ['i'], rest_is_raw = True)
async def _info(ctx, *card):
    found = False
    cardinfo = ' '.join(card[:])
    with open(f"data\en_us\color.json", "r", encoding = "utf8") as f:
        color = json.load(f)

    for v in range(4):
        with open(f"data\en_us\set{v + 1}.json", "r", encoding = "utf8") as f:
            data = json.load(f)

        for dcard in data:
            if (dcard["cardCode"].lower() == cardinfo.lower() or dcard["name"].lower() == cardinfo.lower()):
                embed=discord.Embed(title = dcard["name"], description=dcard["flavorText"], color=int(f'0x{color[dcard["region"]]}', 16))
                embed.set_thumbnail(url=dcard["assets"][0]["gameAbsolutePath"])
                if (dcard["type"] == "Unit"):
                    embed.add_field(name=":crossed_swords: Attack", value=dcard["attack"], inline=False)
                    embed.add_field(name=":heart: Health", value=dcard["health"], inline=True)
                elif (dcard["type"] == "Spell"): embed.add_field(name="Speed", value=dcard["spellSpeed"], inline=False)
                embed.add_field(name="Description", value=dcard["descriptionRaw"], inline=False)
                if (dcard["supertype"] == "Champion"): embed.add_field(name="Level Up", value=dcard["levelupDescriptionRaw"], inline=False)
                await ctx.send(embed=embed)
                # time.sleep(1)
                found = True
    
    if (not found): await ctx.send(":x: Card not found!")

bot.run(TOKEN)