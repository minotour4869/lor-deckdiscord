import discord, json, os
from discord.ext import commands
from dotenv import load_dotenv
from lor_deckcodes import LoRDeck, CardCodeAndCount
from datetime import datetime
import asyncio

icon_link = ""

class Card():
    def __init__(self, info):
        self.data = None
        self.info = info
        self.reference = []
        self.state = self.find_card()
        self.curid = 1

    # def find_reference(self)

    def find_card(self):
        for v in range(4):
            with open(f"data\en_us\set{v + 1}.json", "r", encoding = "utf8") as f:
                data = json.load(f)

            for card in data:
                if (card["cardCode"].lower() == self.info.lower() or card["name"].lower() == self.info.lower()):
                    # print(f'Found a card: {card["cardCode"]}')
                    self.data = card
                    global icon_link
                    with open("data\en_us\globals.json", "r", encoding = "utf8") as f:
                        global_info = json.load(f)

                    for region in global_info["regions"]:
                        if (region["name"] == card["region"]):
                            icon_link = region["iconAbsolutePath"]
                            break
                    
                    self.reference.append(card["cardCode"])
                    for c in card["associatedCardRefs"]: self.reference.append(c)
                    return True

        # print(self.data["name"])
        return False

    def find_data(self, info):
        for v in range(4):
            with open(f"data\en_us\set{v + 1}.json", "r", encoding = "utf8") as f:
                data = json.load(f)

            for card in data:
                if (card["cardCode"].lower() == info.lower() or card["name"].lower() == info.lower()):
                    # print(f'Found a card: {card["cardCode"]}')
                    return card

    def get_embed(self):
        global icon_link
        # if (self.data is None): return None

        card_data = self.find_data(self.reference[self.curid - 1])
        # print(card_data["name"])

        with open("data\en_us\color.json", "r", encoding = "utf8") as f:
            color = json.load(f)
        
        embed = discord.Embed(description = f'_{card_data["flavorText"]}_', color = int(f'0x{color[card_data["region"]]}', 16))
        embed.set_author(name = f'({card_data["cost"]}) {card_data["name"]}', url = f'https://lor.mobalytics.gg/cards/{card_data["cardCode"]}', icon_url = icon_link)
        embed.set_thumbnail(url=card_data["assets"][0]["gameAbsolutePath"])
        embed.set_footer(text = f'{self.curid}/{len(self.reference)}')
        if (card_data["type"] == 'Spell'):
            embed.add_field(name = "Speed", value = card_data["spellSpeed"], inline = False)
        elif (len(card_data["keywords"])):
            keyword = list(card_data["keywords"])
            embed.add_field(name = "Keywords", value = (', '.join(keyword[:])), inline = False)
        if (card_data["descriptionRaw"] != ""): embed.add_field(name = "Description", value = card_data["descriptionRaw"], inline = False)
        if (card_data["type"] == "Unit"):
            if (card_data["levelupDescriptionRaw"] != ""): embed.add_field(name = "Level Up", value = card_data["levelupDescriptionRaw"], inline = False)
            embed.add_field(name = ":crossed_swords:", value = card_data["attack"], inline = True)
            embed.add_field(name = ":heart:", value = card_data["health"], inline = True)
        return embed

class Deck():
    def __init__(self, deckcode, user, name):
        self.name = name if (name != "") else "Imported Deck"
        self.user = user
        self.deckcode = deckcode
        self.deck = list(LoRDeck.from_deckcode(deckcode))
        self.region = []
        self.add_region()
        # print(self.name)

    def add_region(self):
        for card in self.deck:
            card = Card(card[2:])
            if (card.data["region"] not in self.region):
                self.region.append(card.data["region"])

    def get_embed(self):
        with open("data\\rarity.json", "r", encoding = "utf8") as f:
            ra = json.load(f)

        region_text = " - ".join(self.region[:])

        embed = discord.Embed(title = self.name, description = f'**Regions:** {region_text}', url = f'https://lor.mobalytics.gg/decks/code/{self.deckcode}', timestamp = datetime.now())
        embed.set_footer(icon_url = self.user.avatar_url, text = f'by {str(self.user)}')
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
                ratext = champ[1].data["rarity"].lower()[0:2]
                text += f'<:{ratext}:{ra[ratext]}> {champ[0]}x {champ[1].data["name"]} - {champ[1].data["region"]}\n'
            
            embed.add_field(name = "Champions", value = text, inline = False)

        if (len(followers)):
            text = ""
            for fol in followers:
                ratext = fol[1].data["rarity"].lower()[0:2]
                text += f'<:{ratext}:{ra[ratext]}> {fol[0]}x {fol[1].data["name"]} - {fol[1].data["region"]}\n'
            
            embed.add_field(name = "Followers", value = text, inline = False)

        if (len(spells)):
            text = ""
            for spl in spells:
                ratext = spl[1].data["rarity"].lower()[0:2]
                text += f'<:{ratext}:{ra[ratext]}> {spl[0]}x {spl[1].data["name"]} - {spl[1].data["region"]}\n'
            
            embed.add_field(name = "Spells", value = text, inline = False)

        if (len(landmarks)):
            text = ""
            for lnd in landmarks:
                ratext = lnd[1].data["rarity"].lower()[0:2]
                text += f'<:{ratext}:{ra[ratext]}> {lnd[0]}x {lnd[1].data["name"]} - {lnd[1].data["region"]}\n'
            
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
    emoji_list = ['⬅️', '➡️'] 

    card = Card(info)
    if (card.state):
        cur_card = await ctx.send(embed = card.get_embed())
        for emoji in emoji_list: 
            await cur_card.add_reaction(emoji)
        
        def check(react, user):
            return (user == ctx.message.author and str(react.emoji) in emoji_list)
        
        # for refcard in card.data["associatedCardRefs"]:
        #     rcard = Card(refcard)
        #     rcard.find_card()
        #     await ctx.send(embed = rcard.get_embed())
        while True:
            try:
                react, user = await bot.wait_for('reaction_add', check = check)
            except asyncio.TimeoutError:
                return await cur_card.clear_reactions()

            if (user != ctx.message.author): pass
            elif ('⬅️' in str(react.emoji)):
                await cur_card.remove_reaction('⬅️', user)
                card.curid -= 1
                if (not card.curid): card.curid = len(card.reference)
                await cur_card.edit(embed = card.get_embed())
            elif ('➡️' in str(react.emoji)):
                await cur_card.remove_reaction('➡️', user)
                card.curid += 1
                if (card.curid > len(card.reference)): card.curid = 1
                await cur_card.edit(embed = card.get_embed())
    else: await ctx.send(":x: Card not found!")

@bot.group(name = 'deck', aliases = ['d'])
async def deck(ctx):
    pass

@deck.command(name = 'en_us', aliases = ['en'])
async def en_us(ctx, *args):
    deckcode = args[0]
    name = ' '.join(args[1:]) if (len(args) > 1) else "Imported Deck"
    # print(name)
    deck = Deck(deckcode, ctx.message.author, name)
    await ctx.send(embed = deck.get_embed())

# @bot.event
# async def on_command_error(ctx, exc):
#     print(str(exc))
# if (exc == discord.HTTPException):
#     ctx.send(":x: Error!")
# raise exc

bot.run(TOKEN)