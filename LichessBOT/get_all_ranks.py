
#I will use discord.py for the Discord bot functionality and lichess

#return all ranks for a list of players from Lichess

# first retrive all the informations



import asyncio
import httpx

from rank import ChessUser


async def get_all_ranks_lichess() -> list:
    
    url = "https://lichess.org/api/users"
    headers = {
        "content-type": "text/plain",
    }
    
    players_list = []
    
    async with httpx.AsyncClient() as client:
        try: 
            with open('playersLichess.txt', 'r',  encoding='utf-8') as file:
                file_content = file.read().replace('\n', ',').strip()

                response = await client.post(url, data=file_content, headers=headers)


            if response.status_code == 200:

                batch_response = response.json()

                if isinstance(batch_response, list):
                
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
            

# Example usage
if __name__ == "__main__":
    asyncio.run(get_all_ranks_lichess())