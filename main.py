import os, discord, dotenv, json
from pathlib import Path
from discord.errors import DiscordException
from discord.ext import commands
from deck import UserDeck

dotenv.load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
base = Path("Data")

def write_json(user, deck, deckname):
    json_path = base/f"{user}.json"
    base.mkdir(exist_ok=True)
    data = {
        "deck": deck,
        "deckname": deckname
    }
    json_path.write_text(json.dumps(data))

@bot.event
async def on_ready():
    print(f"Yawn, {bot.user} is awaken!")

@bot.command(aliases=['deck', 'd'])
async def _deck(ctx, *arg):
    if (len(arg)):
        if (arg[0] == "add"):
            deckcode = arg[1]
            name = arg[2]
            try:
                deck = UserDeck(deckcode, name)
                write_json(ctx.author.name, deck.deck, deck.name)
                await ctx.send(f":white_check_mark: Imported new deck: {deck.name}.")
            except Exception as err:
                await ctx.send(f":x: Import deck failed!\nError: {str(err)}")
                return
        else:
            await ctx.send(":x: Invalid command, please try again...")
            raise DiscordException
    else: 
        pass

bot.run(token)