import pygame, sys, random
from pygame.locals import *

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
chieu_dai = 800
chieu_rong = 500

# Tạo cửa sổ game
w = pygame.display.set_mode((chieu_dai, chieu_rong))
pygame.display.set_caption('Chương trình chim bay và bom nổ')

# Tạo nền của game là 1 ảnh
anh_nen = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\canh.jpg')  # Thay bằng ảnh nền của bạn
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))

# Tạo ảnh cho con chim
chim = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\chim.jpg')  # Thay bằng ảnh chim
chim = pygame.transform.scale(chim, (80, 70))  # Điều chỉnh kích thước ảnh

nui = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\nui.jpg')
nui = pygame.transform.scale(nui, (250, 250))

bom = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\bom.jpg')  # Thêm ảnh bom
bom = pygame.transform.scale(bom, (50, 50))

tao = pygame.image.load(r'D:\Ki 7\Ma nguon mo\b7\tao.jpg')  # Thêm ảnh quả táo
tao = pygame.transform.scale(tao, (30, 30))

# Vị trí chim
x1 = 0  
y1 = 200  

# Vị trí nền
x_nen1 = 0
x_nen2 = chieu_dai

# Tạo danh sách táo
so_tao = 5
taos = []
for _ in range(so_tao):
    x_tao = random.randint(0, chieu_dai - 30)
    y_tao = -50
    van_toc_tao = random.randint(3, 7)
    taos.append([x_tao, y_tao, van_toc_tao])

# Vị trí bom
x_bom = random.randint(0, chieu_dai - 50)
y_bom = -50
van_toc_bom = random.randint(3, 7)

# Vận tốc của chim
van_toc_chim = 3

# Điểm số và HP cho chim
chim_hp = 100
diem = 0

# Trọng lực
trong_luc = 2

# Khởi tạo font để hiển thị
font = pygame.font.SysFont('Verdana', 30)

# Khởi tạo khung thời gian (FPS)
FPS = 60
fpsClock = pygame.time.Clock()

# Cờ điều khiển di chuyển chim
di_len = False
di_xuong = False

# Vòng lặp game
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Khi nhấn phím, kích hoạt cờ điều khiển
        if event.type == KEYDOWN:
            if event.key == K_UP:
                di_len = True
            if event.key == K_DOWN:
                di_xuong = True

        # Khi nhả phím, hủy cờ điều khiển
        if event.type == KEYUP:
            if event.key == K_UP:
                di_len = False
            if event.key == K_DOWN:
                di_xuong = False

    # Di chuyển chim theo hướng lên hoặc xuống
    if di_len and y1 > 0:
        y1 -= 5
    elif di_xuong and y1 < chieu_rong - 70:
        y1 += 5
    else:
        y1 += trong_luc  # Áp dụng trọng lực khi không điều khiển

    # Chim di chuyển liên tục sang phải và quay lại từ đầu khi ra khỏi màn hình
    x1 += van_toc_chim
    if x1 > chieu_dai:
        x1 = -80  # Đưa chim quay lại từ trái

    # Cập nhật vị trí của bom
    y_bom += van_toc_bom
    if y_bom > chieu_rong:
        x_bom = random.randint(0, chieu_dai - 50)  # Vị trí bom mới ngẫu nhiên
        y_bom = -50
        van_toc_bom = random.randint(3, 7)  # Vận tốc mới ngẫu nhiên

    # Cập nhật vị trí của táo
    for tao_item in taos:
        tao_item[1] += tao_item[2]  # Di chuyển táo
        if tao_item[1] > chieu_rong:
            tao_item[0] = random.randint(0, chieu_dai - 30)  # Vị trí táo mới ngẫu nhiên
            tao_item[1] = -50
            tao_item[2] = random.randint(3, 7)  # Vận tốc mới ngẫu nhiên

    # Kiểm tra va chạm giữa chim và bom
    chim_rect = pygame.Rect(x1, y1, 80, 70)
    bom_rect = pygame.Rect(x_bom, y_bom, 50, 50)

    if chim_rect.colliderect(bom_rect):
        chim_hp = 0  # Chim bị nổ, HP về 0
        # Hiển thị thông báo "Chơi lại"
        w.blit(font.render("Bạn đã thua! Chơi lại", True, (255, 0, 0)), (chieu_dai // 2 - 100, chieu_rong // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        # Reset game
        x1, y1 = 0, 200
        chim_hp = 100
        diem = 0
        y_bom = -50
        for tao_item in taos:
            tao_item[1] = -50

    # Kiểm tra va chạm giữa chim và quả táo
    for tao_item in taos:
        tao_rect = pygame.Rect(tao_item[0], tao_item[1], 30, 30)
        if chim_rect.colliderect(tao_rect):
            diem += 5  # Tăng điểm khi ăn quả táo
            tao_item[0] = random.randint(0, chieu_dai - 30)  # Đặt vị trí táo mới ngẫu nhiên
            tao_item[1] = -50
            tao_item[2] = random.randint(3, 7)  # Vận tốc mới ngẫu nhiên

    # Kiểm tra điều kiện chiến thắng
    if diem >= 50:
        w.blit(font.render("Bạn đã chiến thắng!", True, (0, 255, 0)), (chieu_dai // 2 - 100, chieu_rong // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Vẽ nền chạy liên tục
    x_nen1 -= 2
    x_nen2 -= 2
    if x_nen1 <= -chieu_dai:
        x_nen1 = chieu_dai
    if x_nen2 <= -chieu_dai:
        x_nen2 = chieu_dai
    w.blit(anh_nen, (x_nen1, 0))
    w.blit(anh_nen, (x_nen2, 0))

    # Vẽ núi, chim, bom và táo

    w.blit(chim, (x1, y1))
    w.blit(bom, (x_bom, y_bom))
    for tao_item in taos:
        w.blit(tao, (tao_item[0], tao_item[1]))

    # Hiển thị HP và điểm số
    chim_hp_text = font.render(f"Chim HP: {chim_hp}%", True, (255, 0, 0))
    diem_text = font.render(f"Điểm: {diem}", True, (255, 255, 255))
    w.blit(chim_hp_text, (10, 10))
    w.blit(diem_text, (10, 40))

    # Cập nhật màn hình
    pygame.display.update()

    # Điều chỉnh tốc độ của game
    fpsClock.tick(FPS)
