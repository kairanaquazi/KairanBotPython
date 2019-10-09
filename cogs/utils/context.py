import discord
from discord.ext import commands


class Context(commands.Context):

    async def send(self, *args, **kwargs):
        try:
            register = kwargs.pop("register_response")
        except KeyError:
            register = True

        sent = await super().send(
            *args, **kwargs
        )

        if register:
            await self.bot.register_response(sent, self.message)

        return sent

    async def paginate_with_embeds(self, content, *, without_annotation=False, prefix="```\n", suffix="```"):
        if not isinstance(prefix, str) or not isinstance(suffix, str) or not isinstance(content, str):
            raise TypeError

        if len(content) > (2048 - len(prefix) - len(suffix)):
            by_line = content.split("\n")
            current_length = 0
            current_index = 0
            while current_length <= 2048:
                current_length += len(by_line[current_index]) + len("\n")
                current_index += 1

            part1 = prefix + "\n".join(by_line[:current_index - 1]) + suffix
            part2 = prefix + "\n".join(by_line[current_index:]) + suffix

            emb1 = discord.Embed(description=part1, color=self.bot.embed_color)
            emb2 = discord.Embed(description=part2, color=self.bot.embed_color)

            if not without_annotation:
                emb1.set_author(name=self.me.name, icon_url=self.me.avatar_url)
                emb2.set_footer(
                    text=f"{self.bot.embed_footer} Requested by {self.author}", icon_url=self.author.avatar_url)

            await self.send(embed=emb1)
            await self.send(embed=emb2)
        else:
            if not without_annotation:
                emb = self.default_embed
            else:
                emb = discord.Embed(color=self.bot.embed_color)

            emb.description = prefix + content + suffix,

            await self.send(embed=emb)

    @property
    def default_embed(self):
        emb = discord.Embed(color=self.bot.embed_color)
        emb.set_thumbnail(url=self.me.avatar_url)
        emb.set_author(name=self.me.name, icon_url=self.me.avatar_url)
        emb.set_footer(text=f"{self.bot.embed_footer} Requested by {self.author}", icon_url=self.author.avatar_url)

        return emb