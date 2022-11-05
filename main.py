from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot =  commands.Bot(command_prefix='!')

for filename in os.listdir("./cogs"):
    if filename.endswith('.py') and filename != "__init__.py": #and filename != "duplicate.py":
        bot.load_extension("cogs.{}".format(filename[:-3]))

bot.run(os.getenv("DISCORD_TOKEN"))
