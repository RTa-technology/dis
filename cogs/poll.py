import discord
import asyncio
from discord.ext import commands


class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#     @commands.command()
#     async def cmd(self, ctx):
#         await ctx.send("コマンドを受信しました。")
    @commands.command()
    async def poll(self, ctx, *args):
        text = "**{}**".format(args[0])
        n = len(args)-1
        if(n == 0):
            return
        if(n > 10):
            await ctx.reply("選択肢は10個以下にしてください")
            return
        emojis =  ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
        embed = discord.Embed()
        for i in range(n):
            embed.add_field(name=emojis[i]+" "+args[i+1], value="投票待ち", inline=False)
        message = await ctx.reply(text,embed=embed)
        for i in range(n):
            await message.add_reaction(emojis[i])
        await message.add_reaction("🔄")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        """リアクションが追加されたときに、集計対象メッセージであれば+1する関数
        Args:
            reaction (discord.Reaction): reactionオブジェクト
        """
        if reaction.member.bot:
            return
        elif reaction.emoji.name=="🔄" :
            channel = self.bot.get_channel(reaction.channel_id)
            poll_msg = await channel.fetch_message(reaction.message_id)
            re_msg = await channel.fetch_message(poll_msg.reference.message_id)
            re_content = re_msg.content.replace("/poll ", "").split(' ')
            text = "**{}**".format(re_content[0])
            n = len(re_content)-1
            if(n == 0):
                return
            if (n > 10):
                await ctx.reply("選択肢は10個以下にしてください")
                return
            emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
            embed = discord.Embed()
            for i in range(n):
                embed.add_field(name=emojis[i] + " " + re_content[i + 1], value="投票待ち", inline=False)
            if re_msg.author.id == reaction.member.id:
                message = await poll_msg.edit(text, embed=embed)
                for i in range(n):
                    await poll_msg.add_reaction(emojis[i])
                await poll_msg.add_reaction("🔄")
        else:
            channel = self.bot.get_channel(reaction.channel_id)
            message = await channel.fetch_message(reaction.message_id)
            try:
                embed, emojis  = message.embeds[0], ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
                index = emojis.index(reaction.emoji.name)
            except Exception as e:
                return
            if embed.fields[index].value  == "投票待ち":
                embed.set_field_at(index, name=embed.fields[index].name, value=reaction.member.mention, inline=False)
            elif reaction.member.mention in embed.fields[index].value:
                return
            else:
                embed.set_field_at(index, name=embed.fields[index].name, value=embed.fields[index].value+" "+reaction.member.mention, inline=False)
            await message.edit(embed=embed)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        """リアクションが追加されたときに、集計対象メッセージであれば+1する関数

        Args:
            reaction (discord.Reaction): reactionオブジェクト
        """
        channel = self.bot.get_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
        try:
            embed, emojis  = message.embeds[0], ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
            index = emojis.index(reaction.emoji.name)
        except Exception as e:
            return
        guild = self.bot.get_guild(reaction.guild_id)
        remove_usr = guild.get_member(reaction.user_id)
        if " " in embed.fields[index].value:
            mention = embed.fields[index].value.split()
            mention.remove(remove_usr.mention)
            mention = " ".join(mention)
            embed.set_field_at(index, name=embed.fields[index].name, value=mention, inline=False)
        elif embed.fields[index].value == remove_usr.mention:
            embed.set_field_at(index, name=embed.fields[index].name, value="投票待ち", inline=False)
        else:
            return
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(poll(bot))
