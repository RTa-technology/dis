import logging
import pathlib
import time
from datetime import datetime
from zoneinfo import ZoneInfo


import aiohttp
import discord
from discord.ext import commands, tasks

from .utils.common import CommonUtil


ret = {}


class Admin(commands.Cog, name="管理用コマンド群"):
    """
    管理用のコマンドです
    """

    def __init__(self, bot):
        self.bot = bot
        self.c = CommonUtil()

        self.master_path = pathlib.Path(__file__).parents[1]

        self.local_timezone = ZoneInfo("Asia/Tokyo")

    async def cog_check(self, ctx):
        return ctx.guild and await self.bot.is_owner(ctx.author)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """on_guild_join時に発火する関数"""
        embed = discord.Embed(
            title="サーバーに参加しました", description=f"スレッド保守bot {self.bot.user.display_name}", color=0x2FE48D
        )
        embed.set_author(name=f"{self.bot.user.name}", icon_url=f"{self.bot.user.avatar.replace(format='png').url}")
        try:
            await guild.system_channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.command(aliases=["re"], hidden=True)
    async def reload(self, ctx):
        reloaded_list = []
        for cog in self.master_path.glob("cogs/*.py"):
            try:
                await self.bot.unload_extension(f"cogs.{cog.stem}")
                await self.bot.load_extension(f"cogs.{cog.stem}")
                reloaded_list.append(cog.stem)
            except Exception as e:
                print(e)
                await ctx.reply(e, mention_author=False)

        await ctx.reply(f"{' '.join(reloaded_list)}をreloadしました", mention_author=False)

    @commands.command(aliases=["st"], hidden=True)
    async def status(self, ctx, word: str = "全権管理"):
        try:
            await self.bot.change_presence(activity=discord.Game(name=word))
            await ctx.reply(f"ステータスを{word}に変更しました", mention_author=False)

        except discord.Forbidden or discord.HTTPException:
            logging.warning("ステータス変更に失敗しました")

    @commands.command(aliases=["p"], hidden=False, description="疎通確認")
    async def ping(self, ctx):
        """Pingによる疎通確認を行うコマンド"""
        start_time = time.time()
        mes = await ctx.reply("Pinging....")
        await mes.edit(content="pong!\n" + str(round(time.time() - start_time, 3) * 1000) + "ms")

    @commands.command(aliases=["wh"], hidden=True)
    async def where(self, ctx):
        server_list = [i.name.replace("\u3000", " ") for i in ctx.bot.guilds]
        await ctx.reply(f"現在入っているサーバーは以下の通りです\n{' '.join(server_list)}", mention_author=False)


    @commands.command(hidden=True, name="exec")
    @commands.is_owner()
    async def _exec(self, ctx, *, script):
        script = script.removeprefix("```py").removesuffix("```")
        async with aiohttp.ClientSession() as session:
            ret[ctx.message.id] = ""

            async def get_msg(url):
                return await commands.MessageConverter().convert(ctx, url)

            def _print(*txt):
                ret[ctx.message.id] += " ".join(map(str, txt)) + "\n"
            exec(
                'async def __ex(self,_bot,_ctx,ctx,session,print,get_msg): '
                + '\n'.join(f'    {l}' for l in script.split('\n'))
            )
            r = await locals()['__ex'](self, self.bot, ctx, ctx, session, _print, get_msg)
        try:
            if ret[ctx.message.id]:
                await ctx.send(f"stdout:```py\n{str(ret[ctx.message.id])[:1980]}\n```".replace(self.bot.http.token, "[Token]"))
            if r:
                await ctx.send(f"return:```py\n{str(r)[:1980]}\n```".replace(self.bot.http.token, "[Token]"))
        except BaseException:
            pass
        await ctx.message.add_reaction("\U0001f44d")
        del ret[ctx.message.id]

    @commands.command(hidden=True, name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, script):
        await ctx.send(
            eval(script.replace("```py", "").replace("```", ""))
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))