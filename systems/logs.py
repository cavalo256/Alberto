import logging
import discord
from discord.ext import commands
from datetime import datetime

class LogSystem:
    def _init_(self, bot):
        self.bot = bot
        self.log_channel_id = None
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='bot.log'
        )

    async def send_log(self, action: str, details: str):
        if self.log_channel_id:
            channel = self.bot.get_channel(self.log_channel_id)
            embed = discord.Embed(
                title=f"📝 Log: {action}",
                description=details,
                color=0x7289da,
                timestamp=datetime.now()
            )
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        log_msg = f"{ctx.author} usou {ctx.command} em #{ctx.channel}"
        logging.info(log_msg)
        await self.send_log("Comando Executado", log_msg)