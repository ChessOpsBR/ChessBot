from PIL import Image, ImageDraw, ImageFont
import os

class GetAllRanksTemplate:
    """ This class creates a single chess rank card image for multiple players using Pillow."""
    
    def __init__(self, players_data):
    
        self.players_data = players_data
    
    def _get_font(self, size):
        """Helper method to load fonts with fallback"""
        font_paths = [
            "arial.ttf",
            "/System/Library/Fonts/Arial.ttf",  
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  
            "C:/Windows/Fonts/arial.ttf"  
        ]
        
        for path in font_paths:
            try:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size=size)
            except:
                continue
        
        return ImageFont.load_default()
    
    async def generate_card(self, filename="all_players_ranks.png"):
     
        num_players = len(self.players_data)
        if num_players == 0:
            return None
        
        # Base dimensions
        width = 1000
        header_height = 120
        player_height = 120  # Height per player
        footer_height = 60
        padding = 20
        
        total_height = header_height + (player_height * num_players) + footer_height + (padding * 2)
        
        # Create image
        image = Image.new('RGB', (width, total_height), color="#000000")
        draw = ImageDraw.Draw(image)
        
        # Load fonts
        font_title = self._get_font(36)
        font_subtitle = self._get_font(24)
        font_text = self._get_font(20)
        font_small = self._get_font(16)
        
        # Draw border
        draw.rectangle([(10, 10), (width-10, total_height-10)], 
                      outline='#ECF0F1', width=3)
        
        # Draw header
        header_text = "♟️ Lichess Player Rankings"
        draw.text((50, 40), header_text, fill="#FFFFFF", font=font_title)
        draw.text((50, 80), f"Total Players: {num_players}", fill="#FFFFFF", font=font_subtitle)
        
        # Draw separator line
        draw.line([(30, header_height), (width-30, header_height)], 
                 fill="#ECF0F1", width=2)
        
        # Colors for different game types
        colors = {
            'bullet': "#E74C3C",   # Red
            'blitz': "#F39C12",    # Orange  
            'rapid': "#27AE60"     # Green
        }
        
        # Draw each player
        current_y = header_height + padding
        
        for i, player in enumerate(self.players_data):
            # Get player data (handle both object methods and dictionary access)
            try:
                if hasattr(player, 'get_username'):
                    username = player.get_username()
                    bullet = player.get_bullet()
                    blitz = player.get_blitz()  
                    rapid = player.get_rapid()
                else:
                    username = player['username']
                    bullet = player['bullet']
                    blitz = player['blitz']
                    rapid = player['rapid']
            except (AttributeError, KeyError) as e:
                username = f"Player {i+1}"
                bullet = blitz = rapid = "N/A"
            
            # Draw player background (alternating colors)
            bg_color = "#000000" if i % 2 == 0 else "#070F16"
            draw.rectangle([(30, current_y), (width-30, current_y + player_height - 10)], 
                          fill=bg_color, outline="#5D6D7E", width=1)
            
            # Draw player name
            draw.text((50, current_y + 10), f"{username}", 
                     fill="#ECF0F1", font=font_subtitle)
            
            # Draw rankings in columns
            rank_y = current_y + 45
            
            # Bullet
            draw.ellipse([(50, rank_y), (65, rank_y + 15)], fill=colors['bullet'])
            draw.text((75, rank_y - 2), f"Bullet: {bullet}", 
                     fill="#ECF0F1", font=font_text)
            
            # Blitz  
            draw.ellipse([(250, rank_y), (265, rank_y + 15)], fill=colors['blitz'])
            draw.text((275, rank_y - 2), f"Blitz: {blitz}", 
                     fill="#ECF0F1", font=font_text)
            
            # Rapid
            draw.ellipse([(450, rank_y), (465, rank_y + 15)], fill=colors['rapid'])
            draw.text((475, rank_y - 2), f"Rapid: {rapid}", 
                     fill="#ECF0F1", font=font_text)
            
            # Draw rank number
            rank_text = f"#{i+1}"
            draw.text((width - 100, current_y + 25), rank_text, 
                     fill="#95A5A6", font=font_subtitle)
            
            current_y += player_height
        
        # Draw footer
        footer_y = total_height - footer_height + 20
        draw.line([(30, footer_y - 10), (width-30, footer_y - 10)], 
                 fill="#ECF0F1", width=2)
        draw.text((50, footer_y), "Generated Chess Rankings Card", 
                 fill="#95A5A6", font=font_small)
        
        # Save the image
        try:
            image.save(filename)
            print(f"Multi-player card saved as {filename}")
            return filename
        except Exception as e:
            print(f"Error saving image: {e}")
            return None