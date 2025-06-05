
#I will use discord.py for the Discord bot functionality and lichess

#return all ranks for a list of players from Lichess

# first retrive all the informations



import asyncio
import httpx

from rank import ChessUser


multiple_players = ["ffranczly", "mary", "another_player", "Ana"]  # Replace with actual usernames
async def get_all_ranks_lichess(players) -> list:
    
    url = "https://lichess.org/api/users"
    headers = {
        "content-type": "text/plain",
    }
    
    players_list = []
    
    async with httpx.AsyncClient() as client:
        
        response = await client.post(url, data=",".join(players), headers=headers
    )
    
    if response.status_code == 200:
        
        batch_response = response.json()
        
        
        
        for player in batch_response:
          username = player.get("username", "Unknown")
          rapid = player.get("perfs", {}).get("rapid", {}).get("rating", "N/A")
          blitz = player.get("perfs", {}).get("blitz", {}).get("rating", "N/A")
          bullet = player.get("perfs", {}).get("bullet", {}).get("rating", "N/A")
         
          player_info = ChessUser(username, rapid, blitz, bullet)
          
          players_list.append(player_info)
          
          print(f"Username: {username}")
          
        return players_list
            
            
    
    else:
        print("Failed to retrieve player data:", response.status_code)
        
        return []
            

# Example usage
if __name__ == "__main__":
    asyncio.run(get_all_ranks_lichess(multiple_players))