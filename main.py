import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    case_insensitive=True
)

cogs = [
    'cogs.money',
    'cogs.work',
    'cogs.xp',
    'cogs.mod',
    'cogs.tickets',
    'cogs.social',
    'cogs.utilidades'
]

@bot.event
async def on_ready():
    print(f'Bot {bot.user} conectado!')
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f'Carregado: {cog}')
        except Exception as e:
            print(f'Falha ao carregar {cog}: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para isso!")
    else:
        logging.error(f"Erro no comando: {error}")

bot.run(os.getenv('TOKEN'))