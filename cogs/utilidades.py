import discord
from discord.ext import commands
import requests
import python_weather
from database import Database

db = Database()

class Utilidades(commands.Cog):
    @commands.command()
    async def diario(self, ctx):
        db.update_saldo(ctx.author.id, 100)
        await ctx.send("🎁 Recompensa diária: 🪙100")

    @commands.command()
    async def meme(self, ctx):
        response = requests.get("https://meme-api.com/gimme")
        await ctx.send(response.json()['url'])

    @commands.command()
    async def clima(self, ctx, *, cidade: str):
        async with python_weather.Client() as client:
            weather = await client.get(cidade)
            await ctx.send(f"🌤 {cidade}: {weather.current.temperature}°C")

# Função setup() adicionada
async def setup(bot):
    await bot.add_cog(Utilidades(bot))