import discord
from discord.ext import commands
from database import Database

db = Database()

class Social(commands.Cog):
    @commands.command()
    async def casar(self, ctx, parceiro: discord.Member):
        if parceiro == ctx.author:
            return await ctx.send("Não pode casar consigo mesmo!")
            
        db.execute_query(
            "INSERT INTO relationships VALUES (?, ?, 'casado')",
            (ctx.author.id, parceiro.id)
        )
        await ctx.send(f"💍 {ctx.author.mention} e {parceiro.mention} estão agora casados!")

    @commands.command()
    async def melhor_amigo(self, ctx, amigo: discord.Member):
        db.execute_query(
            "INSERT INTO relationships VALUES (?, ?, 'amigo')",
            (ctx.author.id, amigo.id)
        )
        await ctx.send(f"🤝 {amigo.mention} é seu novo melhor amigo!")

# Função setup() adicionada
async def setup(bot):
    await bot.add_cog(Social(bot))