import discord
import responses
import os
import math
import datetime
import httpx
from paginator import PaginatorView
from dotenv import load_dotenv
from api_client import get_top_infamy, get_infamy, add_infamy_bulk, remove_infamy_bulk
from discord import app_commands
from discord.ext import commands
from easy_pil import Editor, Canvas, load_image_async, Font
from filePaginator import FilePaginatorView


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response is not None:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        await send_message(message, user_message, is_private=False)

    @bot.tree.command(name="leaderboard", description="Show the top members with the most infamy")
    async def leaderboard(interaction: discord.Interaction):
        members = get_top_infamy()
        embeds = []
        counter = 0
        for i, member in enumerate(members, start=1):
            if counter == 0:
                embed = discord.Embed(title='Infamy Leaderboard')
            embed.add_field(name=f"#{i} {member['username']}", value=f"{member['infamy']} infamy", inline=False)
            embed.color = 0xE7583D
            embed.set_thumbnail(url="https://tr.rbxcdn.com/957949d9b78d5d6cc276b82dd33bac96/150/150/Image/Png")
            embed.timestamp = datetime.datetime.utcnow()
            counter += 1
            if counter == 10:
                embeds.append(embed)
                counter = 0
        if counter > 0:
            embeds.append(embed)
        view = PaginatorView(embeds)
        await interaction.response.send_message(embed=view.initial, view=view, ephemeral=True)

    async def createEmbed(members):
        background = Editor(Canvas((800, 1000), color="#E7583D"))
        card_right_shape = [(500, 0), (800, 0), (800, 300), (800, 300)]
        background.polygon(card_right_shape, color="#FFFFFF")
        background.rectangle((0, 0), width=60, height=1000, fill="#FFFFFF")
        second_picture_url = "https://tr.rbxcdn.com/957949d9b78d5d6cc276b82dd33bac96/150/150/Image/Png"
        second_picture = await load_image_async(str(second_picture_url))
        second_picture = Editor(second_picture).resize((150, 150))

        poppinns = Font.poppins(size=40)
        for i, member in enumerate(members):
            yPos = 40 + i * 100
            text_width, text_height = poppinns.getsize(str(member['rank']))
            max_width = 40
            if text_width > max_width:
                ratio = max_width / text_width
                font_size = int(40 * ratio)
                poppinns = Font.poppins(size=font_size)
                text_width, text_height = poppinns.getsize(str(member['rank']))
            background.text((45, yPos), str(member['rank']), font=poppinns, color="#282828", align='right')


        background.paste(second_picture, (625, 20))


        file = discord.File(fp=background.image_bytes, filename=f"leaderboard{str(members[0]['rank'])}.png")
        embed = discord.Embed()
        embed.set_image(url=f"attachment://leaderboard.png")
        return embed, file

    @bot.tree.command(name="wipleaderboard", description="Show the top members with the most infamy")
    async def wipleaderboard(interaction: discord.Interaction):
        members = get_top_infamy()
        embeds = []
        files = []
        for i in range(0, len(members), 10):
            members_slice = members[i:i + 10]
            embed, file = await createEmbed(members_slice)
            embeds.append(embed)
            files.append(file)

        view = FilePaginatorView(files)
        await interaction.response.send_message(file=view._files[0], view=view, ephemeral=True)

    @bot.tree.command(name="infamy", description="Show the infamy of a member by their username")
    @app_commands.describe(robloxname="username")
    async def infamy(interaction: discord.Interaction, robloxname: str):
        try:
            member_infamy = get_infamy(robloxname)
            member = member_infamy['member']
            background = Editor(Canvas((900, 300), color="#E7583D"))
            profile_picture_url = member['headshotUrl'].replace('/48/48/', '/150/150/')
            profile_picture = await load_image_async(str(profile_picture_url))
            profile = Editor(profile_picture).resize((150, 150)).circle_image()

            # Load the second image and resize it to 48x48
            second_picture_url = "https://tr.rbxcdn.com/957949d9b78d5d6cc276b82dd33bac96/150/150/Image/Png"
            second_picture = await load_image_async(str(second_picture_url))
            second_picture = Editor(second_picture).resize((150, 150))

            poppinns = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

            background.polygon(card_right_shape, color="#FFFFFF")
            background.paste(profile, (30, 30))
            background.paste(second_picture, (730, 25))
            username = f"{member['groupRank']} {member['username']}"
            text_width, text_height = poppinns.getsize(username)
            max_width = 400
            if text_width > max_width:
                ratio = max_width / text_width
                font_size = int(40 * ratio)
                poppinns = Font.poppins(size=font_size)
                text_width, text_height = poppinns.getsize(username)

            background.text((200, 40), username, font=poppinns, color="#FFFFFF")

            background.rectangle((200, 100), width=350, height=2, fill="#FFFFFF")
            if not member['infamyToGain'] == "NaN" and int(member['infamy']) > 0:
                progressText = f"Progress To {member['nextGroupRank']}: {int(member['infamy'])} / {int(member['infamy']) + int(member['infamyToGain'])}"
                text_width, text_height = poppins_small.getsize(progressText)
                max_width = 400
                if text_width > max_width:
                    ratio = max_width / text_width
                    font_size = int(30 * ratio)
                    poppins_small = Font.poppins(size=font_size)
                    text_width, text_height = poppinns.getsize(progressText)

                memberPercentage = round((int(member['infamy']) / ((int(member['infamy']) + int(member['infamyToGain']))) * 100))
                background.rectangle((30, 220), width=600, height=50, color="#FFFFFF", radius=20)
                background.bar((30, 220), max_width=600, height=50, percentage=memberPercentage, color="#282828", radius=20)
                background.text(
                    (200, 130),
                    progressText,
                    font=poppins_small,
                    color="#FFFFFF",
                )
            else:
                background.text(
                    (200, 130),
                    f"Infamy: {int(member['infamy'])}",
                    font=poppins_small,
                    color="#FFFFFF",
                )

            file = discord.File(fp=background.image_bytes, filename="levelcard.png")
            await interaction.response.send_message(file=file)
        except Exception as e:
            await interaction.response.send_message('User not in group, or has no infamy', ephemeral=True)

    #  @bot.tree.command(name="addinfamy", description="add infamy based on roblox name")
    #  @app_commands.describe(robloxnames = "List of usernames")
    #  async def bulkaddInfamy(interaction: discord.Interaction, robloxname: List[str]):

    bot.run(TOKEN)
