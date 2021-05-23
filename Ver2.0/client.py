import discord, json, os
from discord.ext import commands
from dotenv import load_dotenv
from lor_deckcodes import LoRDeck, CardCodeAndCount

icon_link = ""

class Card():
    def __init__(self, info):
        self.data = self.ver = None
        self.info = info
        # self.state = self.find_card(info)

    def find_card(self):
        for v in range(4):
            with open(f"data\en_us\set{v + 1}.json", "r", encoding = "utf8") as f:
                data = json.load(f)

            for card in data:
                if (card["cardCode"].lower() == self.info.lower() or card["name"].lower() == self.info.lower()):
                    # print(f'Found a card: {card["cardCode"]}')
                    self.data = card
                    return True

        # print(self.data["name"])
        return False

    def get_embed(self):
        global icon_link
        # if (self.data is None): return None

        with open("data\en_us\color.json", "r", encoding = "utf8") as f:
            color = json.load(f)

        with open("data\en_us\globals.json", "r", encoding = "utf8") as f:
            global_info = json.load(f)
        
        for region in global_info["regions"]:
            if (region["name"] == self.data["region"]):
                icon_link = region["iconAbsolutePath"]
                break

        embed = discord.Embed(description = self.data["flavorText"], color = int(f'0x{color[self.data["region"]]}', 16))
        embed.set_author(name = f'({self.data["cost"]}) {self.data["name"]}', url = f'https://lor.mobalytics.gg/cards/{self.data["cardCode"]}', icon_url = icon_link)
        embed.set_thumbnail(url=self.data["assets"][0]["gameAbsolutePath"])
        if (self.data["type"] == "Unit"):
            keyword = list(self.data["keywords"])
            embed.add_field(name = "Keywords", value = (', '.join(keyword[:])), inline = False)
        elif (self.data["type"] == 'Spell'):
            embed.add_field(name = "Speed", value = self.data["spellSpeed"], inline = False)
        if (self.data["descriptionRaw"] != ""): embed.add_field(name = "Description", value = self.data["descriptionRaw"], inline = False)
        if (self.data["type"] == "Unit"):
            if (self.data["levelupDescriptionRaw"] != ""): embed.add_field(name = "Level Up", value = self.data["levelupDescriptionRaw"], inline = True)
            embed.add_field(name = ":crossed_swords:", value = self.data["attack"], inline = False)
            embed.add_field(name = ":heart:", value = self.data["health"], inline = True)
        return embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
data = {}
bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'Yawn, {bot.user.name} is running...')

@bot.group(name = 'card', aliases = ['c'])
async def card(ctx):
    pass

@card.command(name = 'en_us', aliases = ['en'])
async def en_us(ctx, *args):
    info = ' '.join(args[:])

    card = Card(info)
    card.find_card()
    if (card.data is not None): 
        await ctx.send(embed = card.get_embed())
        for refcard in card.data["associatedCardRefs"]:
            rcard = Card(refcard)
            rcard.find_card()
            await ctx.send(embed = rcard.get_embed())
    else: await ctx.send(":x: Card not found!")

@bot.event
async def on_command_error(ctx, exc):
    print(str(exc))
    # if (exc == discord.HTTPException):
    #     ctx.send(":x: Error!")
    # raise exc

bot.run(TOKEN)