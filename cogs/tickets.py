import discord
from discord.ext import commands
from discord.ui import Button, View
from database import Database
import logging

db = Database()

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def ticket(self, ctx):
        try:
            button = Button(label="Abrir Ticket", style=discord.ButtonStyle.green, emoji="🎫")
            
            async def button_callback(interaction):
                existing = db.execute_query(
                    'SELECT * FROM tickets WHERE user_id = ? AND status = "aberto"',
                    (interaction.user.id,)
                ).fetchone()
                
                if existing:
                    await interaction.response.send_message("🚫 Você já tem um ticket aberto!", ephemeral=True)
                    return
                
                channel = await interaction.guild.create_text_channel(
                    name=f'ticket-{interaction.user.name}',
                    overwrites={
                        interaction.user: discord.PermissionOverwrite(read_messages=True),
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
                    }
                )
                
                db.execute_query(
                    'INSERT INTO tickets (user_id, channel_id) VALUES (?, ?)',
                    (interaction.user.id, channel.id)
                )
                
                await channel.send(f"{interaction.user.mention} Suporte chegando em breve!")
                await interaction.response.send_message(f"🎟️ Ticket criado: {channel.mention}", ephemeral=True)

            button.callback = button_callback
            view = View()
            view.add_item(button)
            await ctx.send("Clique para criar um ticket:", view=view)
        except Exception as e:
            logging.error(f"Erro no sistema de tickets: {e}")

async def setup(bot):
    await bot.add_cog(Tickets(bot))