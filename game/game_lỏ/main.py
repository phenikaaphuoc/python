import tkinter as tk
import pygame
import random

def read_high_score():
    try:
        with open("maxpoint.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def start_game():
    root.destroy()

    # Khởi tạo Pygame
    pygame.init()

    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Created By Tuấn Đẹp Try")

    icon = pygame.image.load("icon.jpg")
    pygame.display.set_icon(icon)

    white = (255, 255, 255)
    red = (255, 0, 0)
    cyan = (0, 255, 255)
    orange = (255, 165, 0)

    player_size = 50
    player_x = (screen_width - player_size) // 2
    player_y = screen_height - player_size

    khoi_vuongs_cyan = []
    khoi_vuongs_orange = []

    num_khoi_vuongs = 20
    khoi_vuong_size = 50

    for i in range(num_khoi_vuongs):
        khoi_vuong_x = random.randint(0, screen_width - khoi_vuong_size)
        khoi_vuong_y = i * (screen_height // num_khoi_vuongs)
        if len(khoi_vuongs_orange) < num_khoi_vuongs // 2:
            khoi_vuongs_orange.append((khoi_vuong_x, khoi_vuong_y))
        else:
            khoi_vuongs_cyan.append((khoi_vuong_x, khoi_vuong_y))

    khoi_vuong_speed = 7

    # Hàm để vẽ người chơi dưới dạng hình vuông
    def draw_player(x, y):
        pygame.draw.rect(screen, red, (x, y, player_size, player_size))

    # Thiết lập điểm số
    score = 0
    font = pygame.font.Font(None, 36)

    # Biến kiểm tra game over
    game_over = False

    # Tên tệp lưu điểm số cao nhất
    high_score_file = "maxpoint.txt"

    # Khởi tạo điểm số cao nhất từ tệp
    high_score = read_high_score()

    def update_high_score(score):
        nonlocal high_score
        if score > high_score:
            high_score = score
            with open(high_score_file, "w") as file:
                file.write(str(high_score))

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 10
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += 10

        if not game_over:
            # Cập nhật vị trí khối vuông xanh
            for i in range(len(khoi_vuongs_cyan)):
                khoi_vuong_x, khoi_vuong_y = khoi_vuongs_cyan[i]
                khoi_vuong_y += khoi_vuong_speed
                khoi_vuongs_cyan[i] = (khoi_vuong_x, khoi_vuong_y)

                # Nếu Khối ra khỏi màn hình, tạo lại ở vị trí ngẫu nhiên
                if khoi_vuong_y > screen_height:
                    khoi_vuong_x = random.randint(0, screen_width - khoi_vuong_size)
                    khoi_vuong_y = 0
                    khoi_vuongs_cyan[i] = (khoi_vuong_x, khoi_vuong_y)

                # Kiểm tra va chạm với khối vuông xanh
                if player_x < khoi_vuong_x + khoi_vuong_size and player_x + player_size > khoi_vuong_x and player_y < khoi_vuong_y + khoi_vuong_size and player_y + player_size > khoi_vuong_y:
                    score += 1
                    khoi_vuong_x = random.randint(0, screen_width - khoi_vuong_size)
                    khoi_vuong_y = 0
                    khoi_vuongs_cyan[i] = (khoi_vuong_x, khoi_vuong_y)

            # Cập nhật vị trí khối vuông cam
            for i in range(len(khoi_vuongs_orange)):
                khoi_vuong_x, khoi_vuong_y = khoi_vuongs_orange[i]
                khoi_vuong_y += khoi_vuong_speed
                khoi_vuongs_orange[i] = (khoi_vuong_x, khoi_vuong_y)

                # Nếu Khối ra khỏi màn hình, tạo lại ở vị trí ngẫu nhiên
                if khoi_vuong_y > screen_height:
                    khoi_vuong_x = random.randint(0, screen_width - khoi_vuong_size)
                    khoi_vuong_y = 0
                    khoi_vuongs_orange[i] = (khoi_vuong_x, khoi_vuong_y)

                # Kiểm tra va chạm với khối vuông cam
                if player_x < khoi_vuong_x + khoi_vuong_size and player_x + player_size > khoi_vuong_x and player_y < khoi_vuong_y + khoi_vuong_size and player_y + player_size > khoi_vuong_y:
                    game_over = True

        screen.fill(white)
        draw_player(player_x, player_y)

        # Vẽ khối vuông xanh
        for khoi_vuong_x, khoi_vuong_y in khoi_vuongs_cyan:
            pygame.draw.rect(screen, cyan, (khoi_vuong_x, khoi_vuong_y, khoi_vuong_size, khoi_vuong_size))

        # Vẽ khối vuông cam
        for khoi_vuong_x, khoi_vuong_y in khoi_vuongs_orange:
            pygame.draw.rect(screen, orange, (khoi_vuong_x, khoi_vuong_y, khoi_vuong_size, khoi_vuong_size))

        # Hiển thị điểm số
        score_display = font.render("Score: " + str(score), True, red)
        screen.blit(score_display, (10, 10))

        # Hiển thị điểm số cao nhất
        high_score_text = font.render("High Score: " + str(high_score), True, red)
        screen.blit(high_score_text, (10, 50))

        # Hiển thị điểm số
        if game_over:
            game_over_text = font.render("Game Over", True, red)
            out_game_text = font.render("Press 'o' to exit game OR Press 'r' to play again", True, red)
            score_text = font.render("Score: " + str(score), True, red)
            screen.blit(game_over_text, (screen_width // 2 - 60, screen_height // 2 - 60))
            screen.blit(out_game_text, (screen_width // 2 - 280, screen_height // 2 - 20))
            screen.blit(score_text, (screen_width // 2 - 60, screen_height // 2 + 40))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                running = False
            elif keys[pygame.K_r]:
                update_high_score(score)
                game_over = False
                score = 0
                khoi_vuongs_cyan = []
                khoi_vuongs_orange = []

                for i in range(num_khoi_vuongs):
                    khoi_vuong_x = random.randint(0, screen_width - khoi_vuong_size)
                    khoi_vuong_y = i * (screen_height // num_khoi_vuongs)
                    if len(khoi_vuongs_orange) < num_khoi_vuongs // 2:
                        khoi_vuongs_orange.append((khoi_vuong_x, khoi_vuong_y))
                    else:
                        khoi_vuongs_cyan.append((khoi_vuong_x, khoi_vuong_y))

        pygame.display.update()
        clock.tick(60)

    # Khi kết thúc trò chơi, đảm bảo đã lưu điểm số cao nhất vào tệp.
    update_high_score(score)
    pygame.quit()

def reset_high_score():
    high_score_file = "maxpoint.txt"
    with open(high_score_file, "w") as file:
        file.write("0")
    
    # Cập nhật lại nhãn hiển thị điểm số cao nhất
    high_score_value = read_high_score()
    high_score_label.config(text="Điểm Số Cao Nhất Của Bạn: " + str(high_score_value))

root = tk.Tk()
root.title("Game Created By Tuấn Đẹp Trai")
root.iconbitmap('icon_tkinter.ico')

high_score_value = read_high_score()

high_score_label = tk.Button(root, font=50, fg='red', text="Điểm Số Cao Nhất Của Bạn: " + str(high_score_value))
root.geometry('800x400')
high_score_label.pack()

start_button = tk.Button(root, font=50, fg='red', text="[                         Start                         ]", command=start_game)
start_button.place(x=270, y=350)

reset_button = tk.Button(root, font=50, fg='red', text="[              Reset High Score              ]", command=reset_high_score)
reset_button.place(x=270, y=310)

root.mainloop()
