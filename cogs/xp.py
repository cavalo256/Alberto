import discord
import logging  # Adicionado
from discord.ext import commands
from database import Database
import random

db = Database()

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        bucket = self.xp_cooldown.get_bucket(message)
        if bucket.update_rate_limit():
            return

        xp = random.randint(10, 20)
        self.add_xp(message.author.id, xp)
        
    def add_xp(self, user_id, xp):
        try:
            current = db.execute_query(
                'SELECT xp, level FROM xp WHERE user_id = ?',
                (user_id,)
            ).fetchone()
            
            if current:
                new_xp = current[0] + xp
                new_level = new_xp // 100
                if new_level > current[1]:
                    db.execute_query(
                        'UPDATE xp SET xp = ?, level = ? WHERE user_id = ?',
                        (new_xp, new_level, user_id)
                    )
                    return
                db.execute_query(
                    'UPDATE xp SET xp = ? WHERE user_id = ?',
                    (new_xp, user_id)
                )
            else:
                db.execute_query(
                    'INSERT INTO xp (user_id, xp) VALUES (?, ?)',
                    (user_id, xp)
                )
        except Exception as e:
            logging.error(f"Erro ao adicionar XP: {e}")

    @commands.command()
    async def rank(self, ctx):
        try:
            users = db.execute_query(
                'SELECT user_id, xp, level FROM xp ORDER BY xp DESC LIMIT 10'
            ).fetchall()
            
            embed = discord.Embed(title="🏆 Leaderboard", color=0x00ff00)
            
            for index, user in enumerate(users, start=1):
                member = ctx.guild.get_member(user[0])
                if member:
                    embed.add_field(
                        name=f"{index}. {member.display_name}",
                        value=f"Level: {user[2]} | XP: {user[1]}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{index}. Usuário não encontrado",
                        value="---",
                        inline=False
                    )
            
            await ctx.send(embed=embed)
        except Exception as e:
            logging.error(f"Erro no comando rank: {e}")

async def setup(bot):
    await bot.add_cog(XPSystem(bot))