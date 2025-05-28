import pygame
import random
import sys
import time
import os
from PIL import Image

class MemoryGame:
    # Constants
    TILE_SIZE = 150
    PADDING = 20
    FONT_SIZE = 48
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    TABLE_OPACITY = 163  # 64% opacity for table background
    BUTTON_COLOR = (50, 50, 50)
    HOVER_COLOR = (100, 100, 100)
    BUTTON_RADIUS = 15
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Screen setup
        info = pygame.display.Info()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Memory Game")
        
        # Load fonts
        self.load_fonts()
        
        # Load assets
        self.load_backgrounds()
        self.load_tile_images()
        self.load_sounds()
        
        # Game state
        self.current_background = None
        self.active_tiles = []
        self.start_x = 0
        self.start_y = 0
        self.score = 0
        self.level = 1
        self.energy = 3
        self.clock = pygame.time.Clock()
        
    def load_fonts(self):
        try:
            self.georgian_font = pygame.font.Font("assets/fonts/ARIALUNI.ttf", self.FONT_SIZE)
        except:
            print("Error loading Georgian font. Using system font instead.")
            self.georgian_font = pygame.font.SysFont("Arial", self.FONT_SIZE)
    
    def load_backgrounds(self):
        self.background_images = []
        for i in range(1, 5):
            path = f"assets/background_img/bg{i}.jpg"
            if os.path.exists(path):
                self.background_images.append(
                    pygame.transform.scale(
                        self.load_jpg(path), 
                        (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                    )
                )
        
        if not self.background_images:
            # Create a fallback background if images not found
            bg = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            bg.fill((30, 30, 80))
            self.background_images = [bg]
    
    def load_jpg(self, path, opacity=207):
        try:
            img = Image.open(path).convert("RGBA")
            alpha = img.getchannel("A").point(lambda p: opacity)
            img.putalpha(alpha)
            return pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Return a placeholder surface
            surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            surface.fill((200, 0, 200, opacity))
            return surface
    
    def load_tile_images(self):
        self.image_names = {
            "1.png": "Monkey", "2.png": "Chameoleona", "3.png": "Chameleonb", "4.png": "Frog",
            "5.png": "Lion", "6.png": "Bat", "7.png": "Bison", "8.png": "Panda",
            "9.png": "Parrot", "10.png": "Enot", "11.png": "Whale", "12.png": "Wolf",
            "13.png": "Chiamaia", "14.png": "Pumba", "15.png": "ieremi", "16.png": "Fish",
            "17.png": "Cikvi", "18.png": "Zarmaco", "19.png": "Owl", "20.png": "Whitebear", "21.png": "Snake"
        }
        
        self.back_image_name = "A.png"
        self.loaded_images = {}
        
        # Load all images with error handling
        for name in list(self.image_names.keys()) + [self.back_image_name]:
            path = f"assets/animals_wallpaper/{name}"
            try:
                self.loaded_images[name] = pygame.transform.scale(
                    pygame.image.load(path), 
                    (self.TILE_SIZE, self.TILE_SIZE)
                )
            except:
                print(f"Error loading image: {path}")
                # Create a placeholder image
                surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE), pygame.SRCALPHA)
                surface.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)
                self.loaded_images[name] = surface
    
    def load_sounds(self):
        # Helper function to safely load sounds
        def load_sound(path):
            try:
                return pygame.mixer.Sound(path)
            except:
                print(f"Error loading sound: {path}")
                # Return a silent sound
                return pygame.mixer.Sound(buffer=bytes([0]*44))
        
        # Background music
        self.background_music_tracks = [
            "assets/background_music/background_music1.mp3",
            "assets/background_music/background_music2.mp3",
            "assets/background_music/background_music3.mp3"
        ]
        
        # Try to play background music
        try:
            track = random.choice(self.background_music_tracks)
            if os.path.exists(track):
                pygame.mixer.music.load(track)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error playing background music: {e}")
        
        # Game sounds
        self.click_sound = load_sound("assets/choice_audio/click.mp3")
        self.good_sound = load_sound("assets/choice_audio/good_choice.mp3")
        self.button_click_sound = load_sound("assets/menu_click/click.mp3")
        self.lose_sound = load_sound("assets/winlose_audio/lose.mp3")
        
        # Win sounds
        self.win_sounds = [
            load_sound("assets/winlose_audio/win.mp3"),
            load_sound("assets/winlose_audio/win2.mp3"),
            load_sound("assets/winlose_audio/win3.mp3")
        ]
        
        # Animal sounds
        self.animal_sounds = {
            "1.png": load_sound("assets/animals_audio/monkey.mp3"),
            "4.png": load_sound("assets/animals_audio/frog.mp3"),
            "5.png": load_sound("assets/animals_audio/lion.mp3"),
            "9.png": load_sound("assets/animals_audio/parrot.mp3"),
            "12.png": load_sound("assets/animals_audio/wolf.mp3"),
            "17.png": load_sound("assets/animals_audio/redsqurrel.mp3"),
            "18.png": load_sound("assets/animals_audio/sloth.mp3"),
            "19.png": load_sound("assets/animals_audio/owl.mp3"),
            "20.png": load_sound("assets/animals_audio/bear.mp3"),
            "21.png": load_sound("assets/animals_audio/snake.mp3")
        }
    
    def save_game(self):
        try:
            with open("game_save.txt", "w") as f:
                f.write(f"{self.score}\n{self.level}\n{self.energy}")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load_game(self):
        try:
            with open("game_save.txt", "r") as f:
                self.score = int(f.readline())
                self.level = int(f.readline())
                self.energy = int(f.readline())
        except:
            self.score, self.level, self.energy = 0, 1, 3
    
    def reset_game(self):
        self.score, self.level, self.energy = 0, 1, 3
        self.save_game()
    
    def draw_table_background(self, cols, rows):
        table_width = cols * self.TILE_SIZE + (cols - 1) * self.PADDING
        table_height = rows * self.TILE_SIZE + (rows - 1) * self.PADDING
        table_surface = pygame.Surface((table_width, table_height), pygame.SRCALPHA)
        table_surface.fill((0, 0, 0, self.TABLE_OPACITY))
        self.screen.blit(table_surface, (self.start_x, self.start_y))
    
    def draw_tiles(self):
        self.screen.blit(self.current_background, (0, 0))
        self.draw_table_background(4, 4)
        for tile in self.active_tiles:
            tile.draw(self.screen, self.loaded_images)
    
    def display_text(self, text, x, y, color=WHITE, centered=True):
        surface = self.georgian_font.render(text, True, color)
        if centered:
            rect = surface.get_rect(center=(x, y))
        else:
            rect = surface.get_rect(topleft=(x, y))
        self.screen.blit(surface, rect)
    
    def create_level(self):
        self.current_background = random.choice(self.background_images)
        self.screen.blit(self.current_background, (0, 0))
        pygame.display.flip()
        
        # Select random tiles for this level
        tile_keys = list(self.image_names.keys())
        random.shuffle(tile_keys)
        selected_keys = tile_keys[:8]
        tile_images = selected_keys * 2
        random.shuffle(tile_images)
        
        # Create tile grid
        tiles = []
        cols, rows = 4, 4
        self.start_x = (self.SCREEN_WIDTH - (self.TILE_SIZE + self.PADDING) * cols + self.PADDING) // 2
        self.start_y = (self.SCREEN_HEIGHT - (self.TILE_SIZE + self.PADDING) * rows + self.PADDING) // 2
        
        for i in range(rows):
            for j in range(cols):
                x = self.start_x + j * (self.TILE_SIZE + self.PADDING)
                y = self.start_y + i * (self.TILE_SIZE + self.PADDING)
                idx = i * cols + j
                tiles.append(Tile(x, y, tile_images[idx], self.TILE_SIZE))
        
        # Show all tiles briefly
        for tile in tiles:
            tile.revealed = True
        
        self.active_tiles = tiles
        self.draw_tiles()
        pygame.display.flip()
        
        # Wait and hide tiles
        time.sleep(2)
        for tile in tiles:
            tile.revealed = False
        
        return tiles
    
    def shake_tiles(self, tiles):
        for _ in range(6):
            for tile in tiles:
                tile.shake_offset = random.choice([-5, 5])
            self.draw_tiles()
            pygame.display.flip()
            time.sleep(0.05)
            
            for tile in tiles:
                tile.shake_offset = 0
            self.draw_tiles()
            pygame.display.flip()
            time.sleep(0.05)
    
    def retry_prompt(self):
        retry_text = self.georgian_font.render("სცადეთ თავიდან", True, self.WHITE)
        retry_rect = retry_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(retry_text, retry_rect)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(e.pos):
                        waiting = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                        waiting = False
    
    def create_button(self, text, rect, mouse_pos=None):
        color = self.HOVER_COLOR if mouse_pos and rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=self.BUTTON_RADIUS)
        text_surf = self.georgian_font.render(text, True, self.WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        return rect
    
    def game_loop(self):
        self.load_game()
        tries_left = self.energy
        
        # Create back button
        back_button_width = 180
        back_button_height = 50
        back_button_rect = pygame.Rect(
            self.SCREEN_WIDTH - back_button_width - 20, 
            20, 
            back_button_width, 
            back_button_height
        )
        
        while tries_left > 0:
            tiles = self.create_level()
            selected = []
            matched = 0
            start_time = pygame.time.get_ticks()
            time_limit = random.choice([30, 60, 90, 120])
            consecutive_mistakes = 0
            exit_to_menu = False
            
            while True:
                elapsed = (pygame.time.get_ticks() - start_time) // 1000
                time_left = max(0, time_limit - elapsed)
                
                # Check for time out
                if time_left <= 0:
                    self.lose_sound.play()
                    time.sleep(1)
                    tries_left -= 1
                    if tries_left == 0:
                        self.display_text("თამაში დასრულდა! სცადეთ თავიდან!", 
                                         self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                        pygame.display.flip()
                        time.sleep(2)
                        self.reset_game()
                        return
                    else:
                        self.retry_prompt()
                        break
                
                # Draw game state
                self.draw_tiles()
                
                # Display HUD
                self.display_text(f"ქულა: {self.score}     დრო: {elapsed}წმ     ენერგია: {tries_left}", 
                                 self.SCREEN_WIDTH // 2, 20)
                                # Time limit warning
                time_color = self.WHITE
                if time_left <= 10:  # Warning when time is running out
                    time_color = (255, 50, 50) if time_left % 2 == 0 else self.WHITE
                
                self.display_text(f"დრო: {time_left}წმ", self.SCREEN_WIDTH // 2, 
                                 self.SCREEN_HEIGHT - 50, time_color)
                
                # Draw back button
                mouse_pos = pygame.mouse.get_pos()
                self.create_button("უკან", back_button_rect, mouse_pos)
                
                pygame.display.flip()
                self.clock.tick(60)  # Limit to 60 FPS for consistent performance
                
                # Handle events
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            exit_to_menu = True
                            break
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        
                        # Check back button
                        if back_button_rect.collidepoint(pos):
                            self.button_click_sound.play()
                            exit_to_menu = True
                            break
                        
                        # Check tile clicks
                        for tile in tiles:
                            if tile.check_click(pos) and tile not in selected:
                                self.click_sound.play()
                                selected.append(tile)
                                break
                        
                        # Process pair selection
                        if len(selected) == 2:
                            pygame.display.flip()
                            time.sleep(0.5)
                            
                            if selected[0].image_name == selected[1].image_name:
                                # Match found
                                selected[0].found = True
                                selected[1].found = True
                                self.score += 7
                                matched += 1
                                self.good_sound.play()
                                
                                # Play animal sound if available
                                if selected[0].image_name in self.animal_sounds:
                                    self.animal_sounds[selected[0].image_name].play()
                                
                                # Celebrate animation
                                selected[0].celebrate(self.screen, self.loaded_images, self.active_tiles, self.draw_tiles)
                                selected[1].celebrate(self.screen, self.loaded_images, self.active_tiles, self.draw_tiles)
                                
                                consecutive_mistakes = 0
                            else:
                                # No match
                                self.shake_tiles(selected)
                                for t in selected:
                                    t.revealed = False
                                
                                consecutive_mistakes += 1
                                if consecutive_mistakes == 3:
                                    self.display_text("მცდარი სვლებია", 
                                                    self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                                    pygame.display.flip()
                                    time.sleep(2)
                                    consecutive_mistakes = 0
                            
                            selected = []
                
                if exit_to_menu:
                    self.save_game()
                    return
                
                if matched == 8:
                    # Level completed
                    random.choice(self.win_sounds).play()
                    self.level += 1
                    self.save_game()
                    
                    # Show level complete message
                    self.display_text(f"დონე {self.level-1} დასრულებულია!", 
                                     self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                    pygame.display.flip()
                    time.sleep(2)
                    break
    
    def menu(self):
        self.load_game()
        self.current_background = random.choice(self.background_images)
        
        # Button properties
        button_width = 400
        button_height = 80
        button_spacing = 40
        
        # Texts
        button_texts = ["თამაში დაწყება", "განახლება", "გასვლა"]
        
        # Pre-rendered buttons
        buttons = []
        total_height = len(button_texts) * button_height + (len(button_texts) - 1) * button_spacing
        start_y = (self.SCREEN_HEIGHT - total_height) // 2
        
        for idx, text in enumerate(button_texts):
            rect = pygame.Rect(
                (self.SCREEN_WIDTH - button_width) // 2,
                start_y + idx * (button_height + button_spacing),
                button_width,
                button_height
            )
            buttons.append((text, rect))
        
        # Main menu loop
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw background
            self.screen.blit(self.current_background, (0, 0))
            
            # Draw title
            self.display_text("მეხსიერების თამაში", self.SCREEN_WIDTH // 2, start_y - 100)
            self.display_text(f"ქულა: {self.score} | დონე: {self.level}", 
                             self.SCREEN_WIDTH // 2, start_y - 40)
            
            # Draw buttons
            for text, rect in buttons:
                self.create_button(text, rect, mouse_pos)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            # Handle events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    for idx, (_, rect) in enumerate(buttons):
                        if rect.collidepoint(e.pos):
                            self.button_click_sound.play()
                            
                            if idx == 0:  # Start
                                self.game_loop()
                                self.load_game()  # Refresh displayed score/level
                            elif idx == 1:  # Reset
                                self.reset_game()
                            elif idx == 2:  # Exit
                                running = False
        
        pygame.quit()
        sys.exit()


class Tile:
    def __init__(self, x, y, image, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.image_name = image
        self.revealed = False
        self.found = False
        self.shake_offset = 0
        self.match_scale = 1.0
    
    def draw(self, screen, loaded_images):
        img = loaded_images[self.image_name] if self.revealed or self.found else loaded_images["A.png"]
        
        if self.found:
            img = pygame.transform.rotozoom(img, 0, self.match_scale)
        
        rect = img.get_rect(center=self.rect.center)
        if self.shake_offset:
            rect.x += self.shake_offset
        
        screen.blit(img, rect)
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos) and not self.revealed and not self.found:
            self.revealed = True
            return True
        return False
    
    def celebrate(self, screen, loaded_images, all_tiles, draw_function):
        original_scale = self.match_scale
        
        for scale in [1.05, 1.1, 1.15, 1.2, 1.15, 1.1, 1.05, 1.0]:
            self.match_scale = scale
            draw_function()
            pygame.display.flip()
            pygame.time.delay(30)
        
        self.match_scale = original_scale


def main():
    game = MemoryGame()
    game.menu()


if __name__ == "__main__":
    main()
