import requests
import json
import discord
import asyncio
from discord.ext import commands
from cogs.utils.common import CommonUtil
# from cogs.utils.pager import PagerWithEmojis

apiurl = "https://bcdice.onlinesession.app/v1/"

class BCdice(commands.Cog, name='BCDice'):
    """
    管理用のコマンドです
    """
    def __init__(self, bot):
        self.bot = bot
        self.c = CommonUtil()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("/d "):
            if message.content.count(' ') >= 2:
                m_content = message.content.replace("/d ", "")
                # await message.channel.send(m_content)
                system = m_content.split(' ', 1)[0]
                diceroll = m_content.split(' ', 1)[1]
                # await message.channel.send(system)
                # await message.channel.send(diceroll)
                url = apiurl + "diceroll?system=" + system + "&command=" + diceroll
                response = requests.get(url)
                jsonData = response.json()
                if jsonData["ok"]:
                    if jsonData["secret"]:
                        async with message.channel.typing():
                            msg = await message.author.send("https://discord.com/channels/"+str(message.guild.id)+"/"+str(message.channel.id)+"/"+str(message.id))
                            await self.c.autodel_msg(msg=msg)
                            await message.author.send("----------\n"+diceroll+" "+jsonData["result"])
                            await message.reply("シークレットダイス :game_die:")
                    else:
                        await message.reply("**"+diceroll+"**"+" "+jsonData["result"])
                else:
                    await message.reply("引数が不適切です。")
            elif message.content.count(' ') == 1:
                diceroll = message.content.replace("/d ", "")
                url = apiurl + "diceroll?system=Cthulhu7th&command=" + diceroll
                response = requests.get(url)
                jsonData = response.json()
                if jsonData["ok"]:
                    if jsonData["secret"]:
                        async with message.channel.typing():
                            msg = await message.author.send("https://discord.com/channels/"+str(message.guild.id)+"/"+str(message.channel.id)+"/"+str(message.id))
                            await self.c.autodel_msg(msg=msg)
                            await message.author.send("----------\n"+diceroll+" "+jsonData["result"])
                            await message.reply("シークレットダイス :game_die:")
                    else:
                        await message.reply("**"+diceroll+"**"+" "+jsonData["result"])
                else:
                    await message.reply("引数が不適切です。")
            else:
                await message.reply("引数が不足しています。")



    @commands.command()
    async def d(self, ctx, message):
        """BCDiceAPIにてダイスロールを行うコマンド"""
        # if ctx == null:
        #     await ctx.send("引数が正しくない/指定してください。")
        #     await ctx.send(ctx.content)


    # @commands.command()
    # async def page_test(self, ctx: commands.Context):
    #     """BCDiceAPiにて使用可能なシステムを表示するコマンド"""
    #     await ctx.send("引数が正しくない/指定してください。")


        # url = apiurl + "names"
        # response = requests.get(url)
        # jsonData = response.json()
        #
        # for key in jsonData['names']:
        #     print(key['name'])

        # embed_1.append(discord.Embed(title="1ページ目です。", description="最初のページなので、右矢印とバツマークのリアクションが追加されます。", color=discord.Color.random()))
        # embed_1.append(discord.Embed(title="2ページ目です。", description="2最初のページなので、右矢印とバツマークのリアクションが追加されます。", color=discord.Color.random()))
        # embed_1.append(discord.Embed(title="3ページ目です。", description="3最初のページなので、右矢印とバツマークのリアクションが追加されます。", color=discord.Color.random())
        #
        # for num in range(20):
        #     embed_1.add_field(name=num, value="DiceBot", inline=True)
        #
        #
        #
        # pages: list[discord.Embed] = [
        #     embed_1,embed_2,embed_3
        # ]
        # pager = PagerWithEmojis(pages)
        # await pager.discord_pager(ctx)


async def setup(bot):
    await bot.add_cog(BCdice(bot))
