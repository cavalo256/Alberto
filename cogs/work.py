import discord
from discord.ext import commands
from database import Database
import random
import logging

db = Database()

class Trabalho(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 3600, commands.BucketType.user)

    @commands.command()
    @commands.guild_only()
    async def trabalhar(self, ctx):
        try:
            bucket = self.cooldown.get_bucket(ctx.message)
            retry_after = bucket.update_rate_limit()
            
            if retry_after:
                await ctx.send(f"Aguarde {round(retry_after)} segundos para trabalhar novamente!")
                return
            
            salario = random.randint(50, 150)
            novo_saldo = db.update_saldo(ctx.author.id, salario)
            await ctx.send(f"💼 Você trabalhou e ganhou 🪙{salario}! Novo saldo: 🪙{novo_saldo}")
        except Exception as e:
            logging.error(f"Erro no comando trabalhar: {e}")

async def setup(bot):
    await bot.add_cog(Trabalho(bot))