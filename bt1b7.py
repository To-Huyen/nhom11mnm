import pygame, sys, random, time
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Window size
WINDOWWIDTH = 800
WINDOWHEIGHT = 500

# Set up the display
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Chém Hoa Quả')

# Load background and fruits images
BG = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\canh.jpg')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))

# Fruits
tao = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\tao.jpg')
tao = pygame.transform.scale(tao, (40, 50))
cam = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\cam.jpg')
cam = pygame.transform.scale(cam, (40, 50))
xoai = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\xoai.jpg')
xoai = pygame.transform.scale(xoai, (40, 50))

# Load knife image
knife_image = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\knife.jpg')
knife_image = pygame.transform.scale(knife_image, (30, 30))  # Adjust size if needed

# Font for displaying text
font = pygame.font.SysFont('Verdana', 30)

# Game settings
FPS = 60
diem = 0
time0 = time.time()
toc_do = 1  # Base speed, will be changed based on difficulty level
fpsClock = pygame.time.Clock()
current_level = 1  # Start at level 1
max_level = 3  # Total 3 levels
level_score_threshold = 50  # 50 points to pass each level

# Function to display text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Main menu function
def main_menu():
    while True:
        w.blit(BG, (0, 0))
        draw_text('Chọn Cấp Độ:', font, (255, 255, 255), w, 300, 150)
        draw_text('1. Dễ', font, (255, 255, 255), w, 350, 200)
        draw_text('2. Trung bình', font, (255, 255, 255), w, 350, 250)
        draw_text('3. Khó', font, (255, 255, 255), w, 350, 300)

        pygame.display.update()

        # Check for player input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position
                if 330 <= mouse_pos[0] <= 470:
                    if 190 <= mouse_pos[1] <= 220:  # Easy
                        return 'easy'
                    if 240 <= mouse_pos[1] <= 270:  # Medium
                        return 'medium'
                    if 290 <= mouse_pos[1] <= 320:  # Hard
                        return 'hard'

# Start the game with the chosen difficulty
def start_game(level):
    global toc_do, current_level, diem, time0

    # Adjust speed based on difficulty
    if level == 'easy':
        toc_do = 1
    elif level == 'medium':
        toc_do = 5
    elif level == 'hard':
        toc_do = 10

    fruits = [
        {"img": tao, "pos": [450, 0], "speed": [random.choice([-5, 5]), toc_do], "sliced": False},
        {"img": cam, "pos": [250, 0], "speed": [random.choice([-5, 5]), toc_do], "sliced": False},
        {"img": xoai, "pos": [350, 0], "speed": [random.choice([-5, 5]), toc_do], "sliced": False}
    ]

    # Hide default mouse cursor and set knife image
    pygame.mouse.set_visible(False)

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Check if player wins (3 levels completed)
        if current_level > max_level:
            win_screen()
            return

        # Mouse slicing logic
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0]:  # Left mouse button pressed
            for fruit in fruits:
                if not fruit['sliced'] and check_slice(fruit, mouse_pos):
                    fruit['sliced'] = True
                    global diem
                    diem += 5  # Increase score

        # Clear the screen
        w.blit(BG, (0, 0))

        # Update and draw fruits
        for fruit in fruits:
            if not fruit['sliced']:
                move_fruit(fruit)
                draw_fruit(fruit)
            else:
                fruit['sliced'] = False  # Respawn after being sliced
                fruit['pos'][1] = 0  # Reset fruit position
                fruit['pos'][0] = random.randint(0, WINDOWWIDTH - 40)
                fruit['speed'][1] = random.randint(2, 5)  # Random speed

        # Draw the knife at the mouse position
        w.blit(knife_image, (mouse_pos[0] - 15, mouse_pos[1] - 15))  # Adjust position as needed

        # Update score and time
        time1 = time.time()
        text_score = font.render('Tổng điểm: {} '.format(diem), True, (255, 0, 0))
        text_time = font.render('Thời gian: {} '.format(int(time1 - time0)), True, (255, 0, 0))

        # Render score and time
        w.blit(text_score, (50, 50))
        w.blit(text_time, (50, 80))

        # Check for level up (after 30 seconds or at least 50 points)
        if (time1 - time0) > 30:
            if diem >= level_score_threshold:
                current_level += 1
                time0 = time.time()  # Reset time for the next level
                diem = 0  # Reset score for next level
                level_up_screen()
            else:
                game_over_screen()
                return

        # Refresh the display
        pygame.display.update()
        fpsClock.tick(FPS)

# Function to move fruit
def move_fruit(fruit):
    fruit['pos'][0] += fruit['speed'][0]
    fruit['pos'][1] += fruit['speed'][1]
    if fruit['pos'][1] > WINDOWHEIGHT:
        fruit['pos'][1] = 0  # Respawn at the top
        fruit['pos'][0] = random.randint(0, WINDOWWIDTH - 40)
        fruit['speed'][1] = random.randint(2, 5)  # Random falling speed

# Function to check if a fruit is sliced
def check_slice(fruit, mouse_pos):
    fruit_rect = pygame.Rect(fruit['pos'][0], fruit['pos'][1], 40, 50)
    return fruit_rect.collidepoint(mouse_pos)

# Function to draw the fruit on the screen
def draw_fruit(fruit):
    if not fruit['sliced']:
        w.blit(fruit['img'], fruit['pos'])

# Screen displayed when player wins
def win_screen():
    while True:
        w.blit(BG, (0, 0))
        draw_text('Bạn đã chiến thắng!', font, (255, 255, 255), w, 300, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

# Screen displayed when game over
def game_over_screen():
    while True:
        w.blit(BG, (0, 0))
        draw_text('Game Over! Chơi lại?', font, (255, 0, 0), w, 300, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                main_menu()

# Screen displayed between levels
def level_up_screen():
    while True:
        w.blit(BG, (0, 0))
        draw_text(f'Chuyển qua cấp độ {current_level}!', font, (255, 255, 255), w, 300, 200)
        pygame.display.update()
        time.sleep(2)  # Pause for 2 seconds before next level
        return

# Main loop
level = main_menu()
start_game(level)
