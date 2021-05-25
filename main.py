import discord, json, os
from discord.ext import commands
from dotenv import load_dotenv
from lor_deckcodes import LoRDeck, CardCodeAndCount

icon_link = ""

class Card():
    def __init__(self, info):
        self.data = None
        self.info = info
        self.state = self.find_card()

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

        embed = discord.Embed(description = f'_{self.data["flavorText"]}_', color = int(f'0x{color[self.data["region"]]}', 16))
        embed.set_author(name = f'({self.data["cost"]}) {self.data["name"]}', url = f'https://lor.mobalytics.gg/cards/{self.data["cardCode"]}', icon_url = icon_link)
        embed.set_thumbnail(url=self.data["assets"][0]["gameAbsolutePath"])
        if (self.data["type"] == 'Spell'):
            embed.add_field(name = "Speed", value = self.data["spellSpeed"], inline = False)
        elif (len(self.data["keywords"])):
            keyword = list(self.data["keywords"])
            embed.add_field(name = "Keywords", value = (', '.join(keyword[:])), inline = False)
        if (self.data["descriptionRaw"] != ""): embed.add_field(name = "Description", value = self.data["descriptionRaw"], inline = False)
        if (self.data["type"] == "Unit"):
            if (self.data["levelupDescriptionRaw"] != ""): embed.add_field(name = "Level Up", value = self.data["levelupDescriptionRaw"], inline = False)
            embed.add_field(name = ":crossed_swords:", value = self.data["attack"], inline = True)
            embed.add_field(name = ":heart:", value = self.data["health"], inline = True)
        return embed

class Deck():
    def __init__(self, deckcode, user, name):
        self.name = name if (name != "") else "Imported Deck"
        self.user = user
        self.deckcode = deckcode
        self.deck = list(LoRDeck.from_deckcode(deckcode))
        self.region = []
        # print(self.name)

    def add_region(self):
        for card in self.deck:
            card = Card(card[2:])
            if (card.data["region"] not in self.region):
                self.region.append(card.data["region"])

    def get_embed(self):
        embed = discord.Embed(title = self.name, description = f'_by {str(self.user)}_', url = f'https://lor.mobalytics.gg/decks/code/{self.deckcode}')
        followers = []
        champions = []
        spells = []
        landmarks = []

        for card in self.deck:
            amount = card[0]
            info = card[2:]
            de_card = Card(info)
            # print(card.data["type"])
            if (de_card.data["type"] == "Unit"):
                champions.append([amount, de_card]) if (de_card.data["supertype"] == "Champion") else followers.append([amount, de_card])
            else: spells.append([amount, de_card]) if (de_card.data["type"] == "Spell") else landmarks.append([amount, de_card])

        if (len(champions)):
            text = ""
            for champ in champions:
                text += f':{champ[1].data["rarity"].lower()[0:2]}: {champ[0]}x {champ[1].data["name"]} - {champ[1].data["region"]}\n'
            
            embed.add_field(name = "Champions", value = text, inline = False)

        if (len(followers)):
            text = ""
            for fol in followers:
                text += f':{fol[1].data["rarity"].lower()[0:2]}: {fol[0]}x {fol[1].data["name"]} - {fol[1].data["region"]}\n'
            
            embed.add_field(name = "Followers", value = text, inline = False)

        if (len(spells)):
            text = ""
            for spl in spells:
                text += f':{spl[1].data["rarity"].lower()[0:2]}: {spl[0]}x {spl[1].data["name"]} - {spl[1].data["region"]}\n'
            
            embed.add_field(name = "Spells", value = text, inline = False)

        if (len(landmarks)):
            text = ""
            for lnd in landmarks:
                text += f':{lnd[1].data["rarity"].lower()[0:2]}: {lnd[0]}x {lnd[1].data["name"]} - {lnd[1].data["region"]}\n'
            
            embed.add_field(name = "Landmarks", value = text, inline = False)

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
    if (card.data is not None): 
        await ctx.send(embed = card.get_embed())
        for refcard in card.data["associatedCardRefs"]:
            rcard = Card(refcard)
            rcard.find_card()
            await ctx.send(embed = rcard.get_embed())
    else: await ctx.send(":x: Card not found!")

@bot.group(name = 'deck', aliases = ['d'])
async def deck(ctx):
    pass

@deck.command(name = 'en_us', aliases = ['en'])
async def en_us(ctx, *args):
    deckcode = args[0]
    name = ' '.join(args[1:]) if (len(args) > 1) else "Imported Deck"
    # print(name)
    deck = Deck(deckcode, ctx.author, name)
    await ctx.send(embed = deck.get_embed())

# @bot.event
# async def on_command_error(ctx, exc):
#     print(str(exc))
# if (exc == discord.HTTPException):
#     ctx.send(":x: Error!")
# raise exc

bot.run(TOKEN)