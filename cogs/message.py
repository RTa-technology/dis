import discord
import asyncio
from discord.ext import commands


class ch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ch_create(self, ctx, ch_name, category_id):
        guild = ctx.guild
        category = guild.get_channel(int(category_id))
        ch = await guild.create_text_channel(ch_name, category=category)
        await message.channel.send(f"{ch.mention} を作成しました。")


async def setup(bot):
    await bot.add_cog(ch(bot))
