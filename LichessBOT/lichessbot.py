# REQUIRED IMPORTS
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import berserk
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from discord.ui import View, Button, Modal, TextInput
from discord import app_commands

# ENVIRONMENT VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# BOT CONFIGURATION
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

LichessBOT = commands.Bot(command_prefix="/", intents=intents)

@LichessBOT.event
async def on_ready():
    await LichessBOT.tree.sync()
    print(f"Bot {LichessBOT.user} is online and commands are synced!")

@LichessBOT.tree.command(name="init",description="LichessBOT's first command")
async def init(interaction:discord.Interaction):
    await interaction.response.send_message("Hello, I'm LichessBOT, a chess test bot for Discord")

class H2HModal(discord.ui.Modal, title="Compare against another player"):
    def __init__(self, username1):
        super().__init__()
        self.username1 = username1

        self.username2 = discord.ui.TextInput(
            label="Opponent's name (username2)",
            placeholder="E.g.: magnuscarlsen",
            required=True,
            max_length=30,
        )
        self.add_item(self.username2)

    async def on_submit(self, interaction: discord.Interaction):
        username1 = self.username1.strip()
        username2 = self.username2.value.strip()

        await interaction.response.defer()

        client = berserk.Client()
        try:
            for username in [username1, username2]:
                resp = requests.get(f"https://lichess.org/api/user/{username}")
                if resp.status_code != 200:
                    await interaction.followup.send(f"User '{username}' not found.", ephemeral=True)
                    return

            max_games = 1000
            games_iter = client.games.export_by_player(username1, vs=username2, as_pgn=False)

            username1_lower = username1.lower()
            username2_lower = username2.lower()

            wins1 = 0
            wins2 = 0
            draws = 0
            total = 0

            for i, game in enumerate(games_iter):
                if i >= max_games:
                    break

                white = game["players"].get("white", {}).get("user", {}).get("name", "").lower()
                black = game["players"].get("black", {}).get("user", {}).get("name", "").lower()

                if username2_lower not in [white, black]:
                    continue

                total += 1
                winner = game.get("winner")

                if not winner:
                    draws += 1
                else:
                    winner_name = game["players"][winner]["user"]["name"].lower()
                    if winner_name == username1_lower:
                        wins1 += 1
                    elif winner_name == username2_lower:
                        wins2 += 1

            if total == 0:
                await interaction.followup.send(
                    f"No games found between users: **{username1}** and **{username2}**.",
                    ephemeral=True
                )
                return

            # ==== IMAGE GENERATION ====
            avatar_url = "https://i.pinimg.com/736x/e5/c6/e6/e5c6e6f6f07cfca562b6965cfbfbc0e3.jpg"
            response = requests.get(avatar_url)
            avatar_img = Image.open(BytesIO(response.content)).resize((200, 200)).convert("RGBA")

            card_size = (600, 250)
            radius = 30
            card = Image.new("RGBA", card_size, (0, 0, 0, 255))

            mask = Image.new("L", card_size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle((0, 0, card_size[0], card_size[1]), radius=radius, fill=255)
            card.putalpha(mask)

            draw = ImageDraw.Draw(card)

            if os.name == "nt":
                font_large = ImageFont.truetype("arial.ttf", 28)
                font = ImageFont.truetype("arial.ttf", 22)
            else:
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

            draw.text((20, 20), "HEAD TO HEAD", fill="white", font=font_large)
            draw.text((20, 60), f"{username1} vs {username2}", fill="white", font=font)
            draw.text((20, 100), f"{username1}: {wins1}", fill="white", font=font)
            draw.text((20, 130), f"{username2}: {wins2}", fill="white", font=font)
            draw.text((20, 160), f"Draws: {draws}", fill="white", font=font)
            draw.text((20, 190), f"Total: {total}", fill="white", font=font)

            card.paste(avatar_img, (380, 25))

            buffer = BytesIO()
            card.save(buffer, format="PNG")
            buffer.seek(0)
            file = discord.File(buffer, filename="h2h_card.png")

            await interaction.followup.send(file=file, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Unexpected error: {str(e)}")

# COMMAND TO FETCH LICHESS USER INFO
@LichessBOT.tree.command(name="lichess_user", description="Fetches information about a Lichess user")
async def lichess_user(interaction: discord.Interaction, username: str):
    await interaction.response.defer()

    client = berserk.Client()

    try:
        resp = requests.get(f"https://lichess.org/api/user/{username}")
        if resp.status_code != 200:
            await interaction.followup.send(f"User '{username}' does not exist.")
            return
    except Exception:
        await interaction.followup.send(f"Error verifying user '{username}'.")
        return

    try:
        user_info = client.users.get_public_data(username)

        def get_rating(perf):
            return user_info['perfs'].get(perf, {}).get('rating', 'N/A')

        def format_play_time(seconds):
            hours = seconds // 3600
            return f"{hours}h" if hours > 0 else "<1h"

        # USER INFO
        username_display = user_info['username']
        online_status = user_info.get('online', False)
        title = user_info.get('title', 'None')
        total_play_time = user_info.get('playTime', {}).get('total', 0)  # in seconds
        formatted_play_time = format_play_time(total_play_time)

        # LEO STYLE CARD
        avatar_url = "https://i.pinimg.com/736x/d0/03/38/d00338a7a5c3c9d0285b2694491dc027.jpg"
        response = requests.get(avatar_url)
        avatar_img = Image.open(BytesIO(response.content)).resize((200, 200)).convert("RGBA")

        card_size = (600, 280)
        radius = 30

        card = Image.new("RGBA", card_size, (0, 0, 0, 255))

        mask = Image.new('L', card_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, card_size[0], card_size[1]), radius=radius, fill=255)

        card.putalpha(mask)

        draw = ImageDraw.Draw(card)

        card.paste(avatar_img, (25, 25))

        if os.name == "nt":
            font = ImageFont.truetype("arial.ttf", 24)
            small_font = ImageFont.truetype("arial.ttf", 18)
        else:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

        draw.text((250, 30), f"@{username_display}", fill="white", font=font)

        draw.text((250, 65), f"Online: {'Yes' if online_status else 'No'}", fill="white", font=small_font)
        draw.text((250, 90), f"Title: {title}", fill="white", font=small_font)
        draw.text((250, 115), f"Play time: {formatted_play_time}", fill="white", font=small_font)

        draw.text((250, 145), "Ratings:", fill="white", font=small_font)
        draw.text((270, 170), f"• Blitz: {get_rating('blitz')}", fill="white", font=small_font)
        draw.text((450, 170), f"• Bullet: {get_rating('bullet')}", fill="white", font=small_font)
        draw.text((270, 200), f"• Classical: {get_rating('classical')}", fill="white", font=small_font)
        draw.text((450, 200), f"• Rapid: {get_rating('rapid')}", fill="white", font=small_font)

        buffer = BytesIO()
        card.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="perfil_card.png")

        class ButtonProfile(discord.ui.View):
            def __init__(self, username):
                super().__init__()
                self.username = username

                url = f"https://lichess.org/@/{username}"
                self.add_item(discord.ui.Button(label="Lichess Profile", url=url))

            @discord.ui.button(label="Head to Head", style=discord.ButtonStyle.primary)
            async def h2h_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(H2HModal(username1=self.username))

        await interaction.followup.send(file=file, view=ButtonProfile(username_display))

    except berserk.exceptions.ResponseError:
        await interaction.followup.send("User not found or API error.")
    except Exception as e:
        await interaction.followup.send(f"Unexpected error: {str(e)}")


# COMMAND FOR HEAD-TO-HEAD BETWEEN TWO PLAYERS
@LichessBOT.tree.command(name="h2h", description="Compares match history between two Lichess users")
async def h2h(interaction: discord.Interaction, username1: str, username2: str):
    await interaction.response.defer()

    client = berserk.Client()

    for user in [username1, username2]:
        try:
            resp = requests.get(f"https://lichess.org/api/user/{user}")
            if resp.status_code != 200:
                await interaction.followup.send(f"User '{user}' does not exist.")
                return
        except Exception:
            await interaction.followup.send(f"Error verifying user '{user}'.")
            return

    try:
        max_games = 1000
        games_iter = client.games.export_by_player(username1.strip(), vs=username2.strip(), as_pgn=False)

        username1_lower = username1.strip().lower()
        username2_lower = username2.strip().lower()

        wins1 = 0
        wins2 = 0
        draws = 0
        total = 0

        for i, game in enumerate(games_iter):
            if i >= max_games:
                break

            white = game["players"].get("white", {}).get("user", {}).get("name", "").lower()
            black = game["players"].get("black", {}).get("user", {}).get("name", "").lower()

            if username2_lower not in [white, black]:
                continue

            total += 1
            winner = game.get("winner")

            if not winner:
                draws += 1
            else:
                winner_name = game["players"][winner]["user"]["name"].lower()
                if winner_name == username1_lower:
                    wins1 += 1
                elif winner_name == username2_lower:
                    wins2 += 1

        if total == 0:
            await interaction.followup.send(
                f"No games found between users: **{username1}** and **{username2}**."
            )
            return

        avatar_url = "https://i.pinimg.com/736x/e5/c6/e6/e5c6e6f6f07cfca562b6965cfbfbc0e3.jpg"
        response = requests.get(avatar_url)
        avatar_img = Image.open(BytesIO(response.content)).resize((200, 200)).convert("RGBA")

        card_size = (600, 250)
        radius = 30

        card = Image.new("RGBA", card_size, (0, 0, 0, 255))

        mask = Image.new("L", card_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, card_size[0], card_size[1]), radius=radius, fill=255)
        card.putalpha(mask)
        
        draw = ImageDraw.Draw(card)

        if os.name == "nt":
            font_large = ImageFont.truetype("arial.ttf", 28)
            font = ImageFont.truetype("arial.ttf", 22)
        else:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

        draw.text((20, 20), "HEAD TO HEAD", fill="white", font=font_large)
        draw.text((20, 60), f"{username1} vs {username2}", fill="white", font=font)
        draw.text((20, 100), f"{username1}: {wins1}", fill="white", font=font)
        draw.text((20, 130), f"{username2}: {wins2}", fill="white", font=font)
        draw.text((20, 160), f"Draws: {draws}", fill="white", font=font)
        draw.text((20, 190), f"Total: {total}", fill="white", font=font)

        card.paste(avatar_img, (380, 25))

        buffer = BytesIO()
        card.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="h2h_card.png")

        embed = discord.Embed(color=discord.Colour.dark_theme())
        embed.set_image(url="attachment://h2h_card.png")

        await interaction.followup.send(file=file)

    except berserk.exceptions.ResponseError as e:
        print(f"API error: {e}")
        await interaction.followup.send("Lichess API error.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        await interaction.followup.send("Unexpected bot error.")

# BOT EXECUTION
LichessBOT.run(TOKEN)