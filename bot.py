from typing import List

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
    intents.members = True
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
        await send_message(message, user_message, is_private=False)


    async def createFile(members):
        background = Editor(Canvas((800, 1000), color="#E7583D"))
        card_right_shape = [(500, 0), (800, 0), (800, 300), (800, 300)]
        second_picture_url = "https://tr.rbxcdn.com/957949d9b78d5d6cc276b82dd33bac96/150/150/Image/Png"
        second_picture = await load_image_async(str(second_picture_url))
        second_picture = Editor(second_picture).resize((150, 150))

        poppinns = Font.poppins(size=35)
        for i, member in enumerate(members):
            yPos = 75 + i * 94
            if i < 3:
                profile_picture_url = member['headshotUrl']
                profile_picture = await load_image_async(str(profile_picture_url))
                profile = Editor(profile_picture).resize((60, 60)).circle_image()
                background.paste(profile, (6, yPos-15))
            else:
                background.text((45, yPos), f"{str(member['rank'])}", font=poppinns, color="#FFFFFF", align='right')
            background.text((60, yPos), f" - {member['username']}: {member['infamy']}", font=poppinns, color="#FFFFFF", align='left')

        background.polygon(card_right_shape, color="#FFFFFF")
        background.paste(second_picture, (625, 20))


        file = discord.File(fp=background.image_bytes, filename=f"leaderboard{str(members[0]['rank'])}.png")
        embed = discord.Embed()
        embed.set_image(url=f"attachment://leaderboard.png")
        return file

    @bot.tree.command(name="leaderboard", description="Show the top members with the most infamy")
    async def leaderboard(interaction: discord.Interaction):
        await interaction.response.send_message(content="..The 44th is Thinking..", ephemeral=False)
        members = get_top_infamy()
        embeds = []
        file = await createFile(members[:10])
        await interaction.edit_original_response(attachments=[file], content=None)

    @bot.tree.command(name="infamy", description="Show the infamy of a member by their username")
    @app_commands.describe(robloxname="username")
    async def infamy(interaction: discord.Interaction, robloxname: str):
        await interaction.response.send_message(content="..The 44th is Thinking..", ephemeral=False)
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
            username = f"#{member['leaderboardrank']} {member['groupRank']} {member['username']}"
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
            await interaction.edit_original_response(attachments=[file], content=None)
        except Exception as e:
            await interaction.edit_original_response(content='User not in group, or has no infamy')

    @bot.tree.command(name="addinfamy", description="add infamy based on roblox username")
    @app_commands.describe(usernames = "List of usernames")
    @app_commands.describe(infamyammount="ammount of infamy to give")
    async def addinfamy(interaction: discord.Interaction, usernames: str, infamyammount: int):
        await interaction.response.send_message(content="..The 44th is Thinking..", ephemeral=True)
        usernames_list = usernames.split()
        has_senior_officer_role = any(role.name.lower() == "senior officer" for role in interaction.user.roles)
        if not has_senior_officer_role:
            await interaction.edit_original_response(content='You are not a Senior Officer.')
        else:
            data = {
                "usernames": usernames_list,
                "infamyToAdd": infamyammount
            }
            try:
                result = add_infamy_bulk(data)
                if len(result['error']) > 0:
                    error_str = '\n'.join(result['error'])
                    await interaction.edit_original_response(content=f"{error_str}")
                else:
                    await interaction.edit_original_response(content=f"Infamy successfully added")
            except Exception as e:

                await interaction.edit_original_response(  # Update message with the error
                    content=f"An error occurred while adding infamy: {e}")

    @bot.tree.command(name="removeinfamy", description="remove infamy based on roblox username")
    @app_commands.describe(usernames="List of usernames")
    @app_commands.describe(infamyammount="ammount of infamy to remove")
    async def removeinfamy(interaction: discord.Interaction, usernames: str, infamyammount: int):
        await interaction.response.send_message(content="..The 44th is Thinking..", ephemeral=True)
        usernames_list = usernames.split()
        has_senior_officer_role = any(role.name.lower() == "senior officer" for role in interaction.user.roles)
        if not has_senior_officer_role:
            await interaction.edit_original_response(content='You are not a Senior Officer.')
        else:
            data = {
                "usernames": usernames_list,
                "infamyToRemove": infamyammount
            }
            try:
                result = remove_infamy_bulk(data)
                if len(result['error']) > 0:
                    error_str = '\n'.join(result['error'])
                    await interaction.edit_original_response(content=f"{error_str}")
                else:
                    await interaction.edit_original_response(content=f"Infamy successfully removed")
            except Exception as e:
                await interaction.edit_original_response(  # Update message with the result
                    content=f"An error occurred while removing infamy: {e}")

    @bot.tree.command(name="getvc", description="Get usernames in vc")
    async def getvc(interaction: discord.Interaction):
        # Get the member who invoked the command
        member = interaction.user

        # Check if the member is connected to a voice channel
        if member.voice and member.voice.channel:
            voice_channel = member.voice.channel
            # Get a list of members in the voice channel
            members = voice_channel.members

            # Create an empty list to store the server profile names
            server_profile_names = []

            # Iterate over each member and get their server profile name
            for member in members:
                # Assuming the server profile name is stored as a custom attribute or field
                # Replace "server_profile_name" with the actual attribute or field name
                server_profile_name = member.display_name

                # Add the server profile name to the list
                server_profile_names.append(server_profile_name)

            names_string = "\n".join(server_profile_names)
            # Send a message with the server profile names
            await interaction.response.send_message(
                content=f"Server Profile Names in the Voice Channel:\n{names_string}",
                ephemeral=True
            )
        else:
            # If the member is not connected to a voice channel, send an error message
            await interaction.response.send_message(
                "You are not connected to a voice channel.",
                ephemeral=True
            )

    bot.run(TOKEN)
