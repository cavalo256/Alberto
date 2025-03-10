import discord
from discord.ext import commands
import time
from database import Database

db = Database()

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, motivo=None):
        """Expulsa um membro do servidor"""
        await member.kick(reason=motivo)
        embed = discord.Embed(
            title="🚨 Usuário Expulso",
            description=f"{member.mention} foi kickado por {ctx.author.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Motivo", value=motivo or "Não especificado")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, motivo=None):
        """Bane um membro do servidor"""
        await member.ban(reason=motivo)
        embed = discord.Embed(
            title="🔨 Usuário Banido",
            description=f"{member.mention} foi banido por {ctx.author.mention}",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Motivo", value=motivo or "Não especificado")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, tempo: int, *, motivo=None):
        """Muta um usuário temporariamente"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        
        await member.add_roles(muted_role)
        
        db.execute_query(
            'INSERT INTO warns (user_id, moderator_id, reason, timestamp) VALUES (?, ?, ?, ?)',
            (member.id, ctx.author.id, f"Mute: {motivo}", int(time.time()))
        )
        
        await ctx.send(f"🔇 {member.mention} mutado por {tempo} minutos. Motivo: {motivo}")

    @commands.command()
    async def warns(self, ctx, member: discord.Member):
        """Mostra advertências de um usuário"""
        warns = db.execute_query(
            'SELECT reason, timestamp FROM warns WHERE user_id = ?',
            (member.id,)
        ).fetchall()
        
        embed = discord.Embed(title=f"⚠ Advertências de {member}", color=0xff9900)
        for warn in warns:
            embed.add_field(
                name=f"<t:{warn[1]}:F>",
                value=warn[0],
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx, quantidade: int = 10):
        """Apaga mensagens (máx 100)"""
        quantidade = min(100, max(1, quantidade))
        await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(f"🧹 {quantidade} mensagens apagadas!", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))