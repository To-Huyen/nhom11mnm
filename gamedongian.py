import pygame
import random

pygame.init()

#Thiết lập màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Thiết lập kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#Đặt tên cho game window
pygame.display.set_caption("Simple Dodge Game")

#Thiết lập đồng hồ
clock = pygame.time.Clock()

#Thiết lập vị trí ban đầu của nhân vật
player_x = screen_width // 2
player_y = screen_height - 50
player_speed = 5

#Tạo danh sách vật cản
obstacles = []
obstacle_speed = 7
obstacle_width = 50
obstacle_height = 50

#Hàm vẽ nhân vật và vật cản
def draw_player(x, y):
    pygame.draw.rect(screen, RED, [x, y, 50, 50])

def draw_obstacle(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, [obstacle[0], obstacle[1], obstacle_width, obstacle_height])

#Main game loop
running = True
while running:
    screen.fill(WHITE)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

# Điều khiển nhân vật
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT] and player_x > 0:
    player_x -= player_speed
if keys[pygame.K_RIGHT] and player_x < screen_width - 50:
    player_x += player_speed

# Tạo vật cản ngẫu nhiên
if random.randint(1, 20) == 1:
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacles.append([obstacle_x, -obstacle_height])
#Di chuyển vật cản
for obstacle in obstacles:
    obstacle[1] += obstacle_speed

# Xóa vật cản khi ra khỏi màn hình
obstacles = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]

# Vẽ nhân vật và vật cản
draw_player(player_x, player_y)
draw_obstacle(obstacles)
#Kiểm tra va chạm
for obstacle in obstacles:
    if player_x < obstacle[0] + obstacle_width and player_x + 50 > obstacle[0] and player_y < obstacle[1] + obstacle_height and player_y + 50 > obstacle[1]:
        running = False

# Cập nhật màn hình
pygame.display.flip()

# Giới hạn FPS
clock.tick(60)
#Thoát game
pygame.quit()