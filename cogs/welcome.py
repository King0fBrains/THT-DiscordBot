import discord
import os
import json

from PIL import Image, ImageDraw, ImageOps, ImageFont
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_size = 48
        self.color = (255, 215, 0)
        self.path = os.path.join(os.path.dirname(__file__), "assets\\background.png")
        self.card_path = os.path.dirname(__file__)
        with open("config.json") as c:
            config = json.load(c)
            self.channel_id = int(config['bot']['welcome'])

    def make_card(self, user_image, user_name, user_id):
        """As written, this function cannot handle avatars with no transparency data
        This is a problem with default avatars as they are 8 bit PNGs.
        The current workaround is to return a new 'default' avatar when a user has no display avatar
        I foresee this being an issue with other strangely formatted avatars"""

        with Image.open(user_image) as pfp:
            # Create a circular mask for pfp
            mask = Image.new('L', pfp.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, pfp.width, pfp.height), fill=255)
            circle = ImageOps.fit(pfp, mask.size, method=0, bleed=0.0, centering=(0.5, 0.5))
            circle.putalpha(mask)

            # Create border and paste it onto the pfp
            border = Image.new('RGBA', (pfp.width, pfp.height), color=0)
            draw = ImageDraw.Draw(border)
            draw.ellipse((0, 0, pfp.width, pfp.height), outline=(255, 215, 0), width=10)
            circle.paste(border, (0, 0), border)

            # Resize PFP
            small = circle.resize((246, 246))

            bg = Image.open(self.path)
            bg.paste(small, (424, 75), small)

            font = ImageFont.truetype("arial.ttf", size=self.text_size)
            draw = ImageDraw.Draw(bg)
            draw.text((550, 400), text=user_name, anchor="ms", font=font, fill=self.color)

            path = os.path.join(self.card_path, f"assets\\{user_id}.png")
            bg.save(path)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        avatar_path = os.path.join(self.card_path, f"assets\\{member.name}.png")

        if member.avatar is None:
            self.make_card("cogs/assets/blank.png", member.name, member.id)
        else:
            await member.display_avatar.save(avatar_path)
            self.make_card(os.path.join(avatar_path), member.name, member.id)

        path = os.path.join(self.card_path, f"assets\\{member.id}.png")
        file = discord.File(f'{path}', filename=f"{member.id}.png")
        welcome = self.bot.get_channel(self.channel_id)
        await welcome.send(content=f"Hey {member.mention}, welcome to The High Table!\n\n"
                                   "Make sure you click the ✅ in the <#807830259990659085> channel to gain access "
                                   "to"
                                   "the rest of the server!\n"
                                   "Don't forget to read the Rules carefully\nEnjoy the server and remember, "
                                   "satisfy"
                                   "your greed!",
                           file=file
                           )
        try:
            os.remove(path)
            os.remove(avatar_path)
        except FileNotFoundError as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
