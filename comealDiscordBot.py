import os
import discord
import dotenv
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from config import comealBotToken, comealGuild
from iracingData import this_week_imsa_races, race_results

MY_GUILD = discord.Object(id=comealGuild)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.tree.command(name='raceresults', description='Show the latest IMSA race GTP results')
async def raceresults(interaction: discord.Interaction):
    try:
        df = raceResults()
        if df.empty:
            await interaction.response.send_message("No race results available.")
            return
        # Create an embed
        embed = discord.Embed(
            title="Race Results",
            description="Here are the latest race results:",
            color=discord.Color.blue()
        )
        # Add fields for each driver
        for index, row in df.iterrows():
            driver_info = (
                f"**Driver**: {row['Driver']}\n"
                f"**Class**: {row['Class']}\n"
                f"**Car**: {row['Car']}\n"
            )
            embed.add_field(name=row['Result'], value=driver_info, inline=False)

        # Send the embed
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")


@client.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


client.run(comealBotToken)