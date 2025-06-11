

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os



from get_all_ranks import get_all_ranks_lichess
from get_all_ranks_Template import GetAllRanksTemplate


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(handlers=[handler], level=logging.DEBUG)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    logging.info(f'{bot.user} has connected to Discord!')

@bot.command()
async def getAllRanks(ctx):
    try:
        embed = discord.Embed(title="♟️ Lichess Player Rankings", color=discord.Color.blue())
       
        initial_msg = await ctx.send(embed=embed)
        
        # Get player data
        players = await get_all_ranks_lichess()
        
        if not players:
            await initial_msg.edit(content="No player data found.", embed=None)
            return
        
      
        await initial_msg.edit(embed=embed)
        

        template = GetAllRanksTemplate(players)
        
        # Generate the single image file
        filename = "all_players_ranks.png"
        file_path = await template.generate_card(filename)
        
        if file_path and os.path.exists(file_path):
            # Send the single image
            file = discord.File(file_path, filename="chess_rankings.png")
            await ctx.send(file=file)
            
          
            try:
                os.remove(file_path)
            except OSError:
                pass
            
            # Update final embed
         
            await initial_msg.edit(embed=embed)
        else:
            await ctx.send("Failed to generate the rankings card.")
            
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        await ctx.send(error_msg)
        logging.error(f"Error in getAllRanks command: {str(e)}")


if __name__ == "__main__":
    if not token:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        logging.error("DISCORD_TOKEN not found in environment variables!")
    else:
        try:
            print("Starting bot...")
            bot.run(token, log_handler=handler, log_level=logging.DEBUG)
        except Exception as e:
            print(f"Failed to start bot: {e}")
            logging.error(f"Failed to start bot: {e}")  
