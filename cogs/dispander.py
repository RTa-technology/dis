"""
dispander

Copyright (c) 2020 1ntegrale9

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php

Satsuki's dispander

Copyright (c) 2021 being24

"""


from discord import Embed
from discord.ext import commands
import re
from cogs.utils.common import CommonUtil

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class ExpandDiscordMessageUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c = CommonUtil()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.dispand(message)

    async def dispand(self, message):
        messages = await self.extract_messsages(message)
        for m in messages:
            try:
                if message.content:
                    await message.channel.send(embed=self.compose_embed(m))
                for embed in m.embeds:
                    await message.channel.send(embed=embed)
            except BaseException as e:
                raise


    async def extract_messsages(self, message):
        messages = []
        for ids in re.finditer(regex_discord_message_url, message.content):
            url_guild_id = int(ids['guild'])
            msg_guild = self.bot.get_guild(url_guild_id)
            if msg_guild is None:
                msg = await message.channel.send("サーバに入室していません")
                await self.c.autodel_msg(msg=msg)
                return []
            fetched_message = await self.fetch_message_from_id(
                self=self.bot,
                guild=msg_guild,
                channel_id=int(ids['channel']),
                message_id=int(ids['message']),
            )
            if fetched_message is None:
                await message.channel.send("閲覧許可がありません")
                return []
            messages.append(fetched_message)
        return messages


    @staticmethod
    async def fetch_message_from_id(self, guild, channel_id, message_id):
        channel = guild.get_channel_or_thread(channel_id)
        if channel is None:
            channel = self.get_channel(channel_id)
            print(dir(self))
        try:
            message = await channel.fetch_message(message_id)
            return message
        except Exception:
            return None

    @staticmethod
    def compose_embed(message):
        embed = Embed(
            description=message.content,
            timestamp=message.created_at,
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.avatar.url,
        )
        if message.guild.icon is None:
            embed.set_footer(
                text=message.guild.name+" in "+message.channel.name,
            )
        else:
            embed.set_footer(
                text=message.guild.name+" in "+message.channel.name,
                icon_url=message.guild.icon.url,
            )
        if message.attachments and message.attachments[0].proxy_url:
            embed.set_image(
                url=message.attachments[0].proxy_url
            )
        return embed


async def setup(bot):
    await bot.add_cog(ExpandDiscordMessageUrl(bot))
