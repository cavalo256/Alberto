import discord
from discord.ext import commands
from database import Database
import random
import time

db = Database()

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.investimentos_ativos = {}

    @commands.command()
    async def saldo(self, ctx):
        """Ver seu saldo de moedas"""
        saldo = db.get_saldo(ctx.author.id)
        await ctx.send(f'{ctx.author.mention}, seu saldo é: 🪙{saldo}')

    @commands.command()
    async def transferir(self, ctx, membro: discord.Member, quantidade: int):
        """Transferir moedas para outro usuário"""
        if quantidade <= 0:
            return await ctx.send('Valor inválido!')
        
        if ctx.author.id == membro.id:
            return await ctx.send('Não pode transferir para si mesmo!')

        if db.get_saldo(ctx.author.id) < quantidade:
            return await ctx.send('Saldo insuficiente!')

        db.update_saldo(ctx.author.id, -quantidade)
        db.update_saldo(membro.id, quantidade)
        await ctx.send(f'✅ Transferidos 🪙{quantidade} para {membro.mention}')

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def apostar(self, ctx, quantidade: int):
        """Apostar moedas (45% de chance de ganhar)"""
        if quantidade <= 0:
            return await ctx.send('Valor inválido!')

        saldo_atual = db.get_saldo(ctx.author.id)
        if saldo_atual < quantidade:
            return await ctx.send('Saldo insuficiente!')

        if random.random() < 0.45:
            ganho = round(quantidade * 1.5)
            db.update_saldo(ctx.author.id, ganho)
            await ctx.send(f'🎉 Ganhou 🪙{ganho}! Novo saldo: 🪙{db.get_saldo(ctx.author.id)}')
        else:
            db.update_saldo(ctx.author.id, -quantidade)
            await ctx.send(f'😢 Perdeu 🪙{quantidade}. Novo saldo: 🪙{db.get_saldo(ctx.author.id)}')

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def roubar(self, ctx, alvo: discord.Member, quantidade: int):
        """Tentar roubar moedas de outro usuário (40% de chance)"""
        if db.get_saldo(alvo.id) < quantidade:
            return await ctx.send('Alvo não tem moedas suficientes!')
        
        if random.random() < 0.4:
            db.update_saldo(ctx.author.id, quantidade)
            db.update_saldo(alvo.id, -quantidade)
            await ctx.send(f'💰 Roubo bem sucedido! Você roubou 🪙{quantidade}')
        else:
            multa = quantidade // 2
            db.update_saldo(ctx.author.id, -multa)
            await ctx.send(f'🚔 Roubo falhou! Multa de 🪙{multa}')

    @commands.command()
    async def investir(self, ctx, quantidade: int):
        """Investir moedas por 24 horas (20% de retorno)"""
        if quantidade < 10:
            return await ctx.send('Mínimo 🪙10 para investir!')
            
        if db.get_saldo(ctx.author.id) < quantidade:
            return await ctx.send('Saldo insuficiente!')

        db.update_saldo(ctx.author.id, -quantidade)
        termino = int(time.time()) + 86400
        db.execute_query(
            'INSERT INTO investments (user_id, amount, end_time) VALUES (?, ?, ?)',
            (ctx.author.id, quantidade, termino)
        )
        await ctx.send(f'📈 Investimento de 🪙{quantidade} feito! Retorno em 24h (+20%).')

    @commands.command()
    async def rank_moedas(self, ctx):
        """Top 10 usuários mais ricos"""
        users = db.execute_query(
            'SELECT user_id, saldo FROM economia ORDER BY saldo DESC LIMIT 10'
        ).fetchall()
        
        embed = discord.Embed(title="🏦 Ranking de Moedas", color=0xffd700)
        
        for index, user in enumerate(users, start=1):
            member = ctx.guild.get_member(user[0])
            if member:
                embed.add_field(
                    name=f"{index}. {member.display_name}",
                    value=f"🪙{user[1]}",
                    inline=False
                )
        
        await ctx.send(embed=embed)

    @apostar.error
    async def apostar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Aguarde {error.retry_after:.1f}s para apostar novamente!")

async def setup(bot):
    await bot.add_cog(Economia(bot))