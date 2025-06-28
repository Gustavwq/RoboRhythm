import pygame
import sys
import time
import random
import os
import traceback

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robo Rhythm")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
freeze_input = False
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SKYBLUE = (85, 180 ,255)

MAX_HEALTH = 3
castleentry_x = 7695
castleentry_y = 250
lives = MAX_HEALTH

# Menu assets
menu_button_path = "assets/images/mainmenu"
hi_main_menu = pygame.image.load(os.path.join(menu_button_path, "RobotHI.png")).convert_alpha()
play_button = pygame.image.load(os.path.join(menu_button_path, "PlayButton.png")).convert_alpha()
quit_button = pygame.image.load(os.path.join(menu_button_path, "QuitButton.png")).convert_alpha()
menu_bg = pygame.image.load(os.path.join(menu_button_path, "Background.jpeg")).convert()
shield_key_img = pygame.image.load("assets/images/Keybinds3.png").convert_alpha()
shield_key_img = pygame.transform.scale(shield_key_img, (300, 150))  
title_image = pygame.image.load(os.path.join(menu_button_path, "TitleScreen.png")).convert_alpha()
cloud_image = pygame.image.load("assets/images/Clouds.png").convert_alpha()
cloud_image = pygame.transform.scale(cloud_image, (140, 80)) 
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
play_button = pygame.transform.scale(play_button, (350, 145))
quit_button = pygame.transform.scale(quit_button, (350, 145))
title_image = pygame.transform.scale(title_image, (430, 50)) 
hi_main_menu = pygame.transform.scale(hi_main_menu, (100, 75)) 

spritesheet = pygame.image.load("assets/images/sheet.png").convert_alpha()
CastleEntry = pygame.image.load("assets/images/CastleEntry.png").convert_alpha()
castle_image = pygame.image.load("assets/images/CastleTower.png").convert_alpha()
tree_image = pygame.image.load("assets/images/Trees.png").convert_alpha()
tree_image = pygame.image.load("assets/images/Keybinds.png").convert_alpha()
tree_image = pygame.image.load("assets/images/Trees.png").convert_alpha()
tree_image = pygame.transform.scale(tree_image, (150, 150))
giant_tree_image = pygame.image.load("assets/images/GiantTree.png").convert_alpha()
waterbg_image = pygame.image.load("assets/images/WaterBG.png").convert_alpha()
interact_prompt = pygame.image.load("assets/images/Keybinds2.png").convert_alpha()
waterbg_image = pygame.transform.scale(waterbg_image, (600, 200))
giant_tree_image = pygame.transform.scale(giant_tree_image, (500, 700))
interact_prompt = pygame.transform.scale(interact_prompt, (125, 78))
castle_image = pygame.transform.scale(castle_image, (300, 600))
CastleEntry = pygame.transform.scale(CastleEntry, (300, 300))
TILE_SIZE = 16
grass_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
grass_tile.blit(spritesheet, (0, 0), (112, 0, TILE_SIZE, TILE_SIZE))

explosion_sound = pygame.mixer.Sound("assets/sfx/Explosion.mp3")
hit_sound = pygame.mixer.Sound("assets/sfx/hit.mp3")
main_menu_music = pygame.mixer.Sound("assets/music/MainMenu.mp3")
game_music = pygame.mixer.Sound("assets/music/InGame.mp3")
game_music.set_volume(0.3)
show_level_intro = True
level_intro_start = None
enemies = []
trees = [] 

in_quiz = False
quiz_questions = []
current_question_index = 0
tip_font = pygame.font.Font("assets/fonts/joystixmono.otf", 18)

# Positions
tip_y = HEIGHT - 40  # near bottom of screen
prefix_x = 20
selected_answer = None
quiz_cleared = False

CHARSPRITE_PATH = "assets/images/charsprites"
SPRITE_SIZE = 60

def draw_quiz():
    global selected_answer

    # ✅ prevent crash after quiz ends
    if not quiz_questions or current_question_index >= len(quiz_questions):
        return
    if not quiz_questions:
        print("Quiz list is empty")
        return

    screen.fill((30, 30, 30))

    q = quiz_questions[current_question_index]
    question_text = big_font.render(q["question"], True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 100))

    mouse_clicked = pygame.mouse.get_pressed()[0]
    mx, my = pygame.mouse.get_pos()

    for i, ans in enumerate(q["answers"]):
        rect = pygame.Rect(150 + i * 140, 250, 120, 60)
        pygame.draw.rect(screen, (70, 70, 220), rect)
        ans_text = font.render(str(ans), True, WHITE)
        text_rect = ans_text.get_rect(center=rect.center)
        screen.blit(ans_text, text_rect)

        if mouse_clicked and rect.collidepoint(mx, my) and selected_answer is None:
            print("Answer selected:", ans)
            selected_answer = ans
            pygame.time.set_timer(pygame.USEREVENT + 1, 300)
def handle_quiz_screen():
    global selected_answer, current_question_index, in_quiz, quiz_cleared, game_won

    screen.fill((30, 30, 30))

    q = quiz_questions[current_question_index]
    question_text = big_font.render(q["question"], True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - 100, 100))

    answer_rects = []

    for i, ans in enumerate(q["answers"]):
        rect = pygame.Rect(200 + i * 130, 250, 120, 60)
        answer_rects.append((rect, ans))
        pygame.draw.rect(screen, (50, 50, 200), rect)
        ans_text = font.render(str(ans), True, WHITE)
        screen.blit(ans_text, (rect.x + 30, rect.y + 15))

    # Process mouse click
    if selected_answer is None and pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        for rect, ans in answer_rects:
            if rect.collidepoint(mx, my):
                selected_answer = ans
                pygame.time.set_timer(pygame.USEREVENT + 1, 300)  # slight delay
                break

    pygame.display.flip()
    clock.tick(60)

def generate_quiz():
    ops = ['+', '-', '*', '/']
    questions = []
    for _ in range(3):
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
        op = random.choice(ops)

        # Avoid division by zero
        if op == '/':
            b = random.randint(1, 100) or 1
            a = b * random.randint(1, 100)
            correct = a // b
            question_str = f"{a} / {b}"
        elif op == '+':
            correct = a + b
            question_str = f"{a} + {b}"
        elif op == '-':
            correct = a - b
            question_str = f"{a} - {b}"
        elif op == '*':
            correct = a * b
            question_str = f"{a} * {b}"

        wrong = set()
        attempts = 0
        while len(wrong) < 3 and attempts < 100:
            fake = correct + random.randint(-10, 10)
            if fake != correct and fake >= 0:
                wrong.add(fake)
            attempts += 1
        while len(wrong) < 3:
            wrong.add(correct + random.randint(1, 100))

        all_answers = list(wrong) + [correct]
        random.shuffle(all_answers)

        questions.append({
            "question": question_str,
            "correct": correct,
            "answers": all_answers
        })
    return questions

def load_image(name):
    path = os.path.join(CHARSPRITE_PATH, f"{name}.png")
    return pygame.image.load(path).convert_alpha()

idle_frame = load_image("RobotIdle")
jump_frames = load_image("RobotJump")
hi_frame = load_image("RobotHI")
falling_frame = load_image("RobotFalling")
sit_frame = load_image("RobotSit") 
walk_frames = [load_image(f"RobotWalk{i}") for i in range(1, 7)]
shield_image = pygame.image.load("assets/images/Shield.png").convert_alpha()
explosion_frames = [load_image(f"RobotExplode{i}") for i in range(1, 4)]
ENEMY_PATH = "assets/images/enemysprites"

def load_enemy_image(name):
    return pygame.image.load(os.path.join(ENEMY_PATH, f"{name}.png")).convert_alpha()

enemy_idle = load_enemy_image("EnemyIdle")
enemy_walk = [load_enemy_image(f"EnemyWalk{i}") for i in range(1, 7)]

player_speed = 5
jump_power = 15
gravity = 0.6

GAME_DURATION = 180

font = pygame.font.Font("assets/fonts/joystixmono.otf", 22)
smallerfont = pygame.font.Font("assets/fonts/joystixmono.otf", 15)
big_font = pygame.font.Font("assets/fonts/joystixmono.otf", 36) 

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SPRITE_SIZE
        self.height = SPRITE_SIZE
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.frame_index = 0
        self.anim_timer = 0
        self.facing_right = True  # Controls flip
        self.active = True
        self.respawn_timer = 0
        self.last_direction_change_time = time.time()
        self.direction_change_cooldown = 1.0  # 1 second delay

    def deactivate(self):
        self.active = False
        self.respawn_timer = time.time()

    def try_respawn(self, player_x):
        if not self.active and time.time() - self.respawn_timer > 3:
            while True:
                new_x = random.randint(0, WIDTH * 5)
                if abs(new_x - player_x) >= 2 * SPRITE_SIZE:
                    self.x = new_x
                    break
            self.y = HEIGHT - SPRITE_SIZE - 50
            self.vx = 0
            self.vy = 0
            self.active = True


    def update(self, player_x, player_y, platforms):
        if not self.active:
            self.try_respawn(player_x)
            return

        self.vy += gravity
        self.y += self.vy
        self.on_ground = False

        for plat in platforms:
            if (self.x + self.width > plat["x"] and
                self.x < plat["x"] + plat["width"] and
                self.y + self.height > plat["y"] and
                self.y + self.height < plat["y"] + plat["height"] + self.vy and
                self.vy >= 0):
                self.y = plat["y"] - self.height
                self.vy = 0
                self.on_ground = True
                break

        dx = player_x - self.x
        distance = abs(dx)
        follow_range = SPRITE_SIZE * 4
        now = time.time()

        if distance < follow_range:
            if now - self.last_direction_change_time > self.direction_change_cooldown:
                new_vx = 1 if dx > 0 else -1
                if new_vx != self.vx:
                    self.vx = new_vx
                    self.last_direction_change_time = now
        else:
            if self.on_ground and random.random() < 0.01:
                if now - self.last_direction_change_time > self.direction_change_cooldown:
                    self.vx *= -1
                    self.last_direction_change_time = now

        self.x += self.vx

        # Update facing direction
        if self.vx > 0:
            self.facing_right = True
        elif self.vx < 0:
            self.facing_right = False

        self.anim_timer += 1
        if self.anim_timer % 8 == 0:
            self.frame_index = (self.frame_index + 1) % len(enemy_walk)

    def draw(self, surface, camera_x, camera_y):
        if not self.active:
            return
        image = enemy_walk[self.frame_index] if abs(self.vx) > 0.2 else enemy_idle

        # Flip if sprite faces left by default and enemy is facing right
        if self.facing_right:
            image = pygame.transform.flip(image, True, False)

        scaled = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
        surface.blit(scaled, (self.x - camera_x, self.y - camera_y))


def check_overlap(a, b):
    return (a["x"] < b["x"] + b["width"] and
            a["x"] + a["width"] > b["x"] and
            a["y"] < b["y"] + b["height"] and
            a["y"] + a["height"] > b["y"])

def draw_text_with_stroke(surface, text, font, x, y, text_color, stroke_color=BLACK, stroke_width=2, center=False):
    text_surface = font.render(text, True, text_color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
    else:
        rect = text_surface.get_rect(topleft=(x, y))

    # Draw stroke by rendering the text around the original position
    for dx in [-stroke_width, 0, stroke_width]:
        for dy in [-stroke_width, 0, stroke_width]:
            if dx == 0 and dy == 0:
                continue
            offset_pos = (rect.x + dx, rect.y + dy)
            stroke_surf = font.render(text, True, stroke_color)
            surface.blit(stroke_surf, offset_pos)

    # Draw the main text
    surface.blit(text_surface, rect)

def generate_platforms():
    global trees
    platforms = []
    total_ground_width = WIDTH * 10 + 250
    ground_y = HEIGHT - 50
    segment_width = 300
    hole_width = 200
    safe_spawn_x = 400
    CASTLE_SAFE_ZONE_START = castleentry_x - 100
    CASTLE_SAFE_ZONE_END = castleentry_x + 250

    x = 0
    while x < total_ground_width:
        if x < safe_spawn_x or (CASTLE_SAFE_ZONE_START <= x <= CASTLE_SAFE_ZONE_END):
            segment = {"x": x, "y": ground_y, "width": segment_width, "height": 50}
            platforms.append(segment)
            x += segment_width
            continue

        if random.random() < 0.15:  # 15% chance for a hole
            x += hole_width
        else:
            width = random.randint(150, 300)
            segment = {"x": x, "y": ground_y, "width": width, "height": 50}
            platforms.append(segment)
            x += width

    # ✅ LEFT and RIGHT walls
    platforms.append(left_wall)
    platforms.append(right_wall)
    

    # HOLE DETECTION for helper platforms
    holes = []
    for x in range(0, total_ground_width, 64):  # scan in 64px chunks
        overlapping = any(p["x"] <= x <= p["x"] + p["width"] for p in platforms if p["y"] == ground_y)
        if not overlapping:
            holes.append(x)

    # Spawn helper platforms above those holes
    for hole_x in holes:
        plat_width = random.randint(100, 160)
        plat_x = hole_x - random.randint(0, plat_width // 2)
        plat_x = max(50, plat_x)
        plat_y = ground_y - random.randint(100, 150)

        platform = {
            "x": plat_x,
            "y": plat_y,
            "width": plat_width,
            "height": 20
        }

        # Avoid overlap
        if not any(check_overlap(platform, p) for p in platforms):
            platforms.append(platform)

    for platform in platforms:
        if platform["y"] == HEIGHT - 50 and random.random() < 0.25:  # 30% chance to place tree
            tree_x = platform["x"] + random.randint(0, platform["width"] - 100)
            tree_y = platform["y"] - 150  # adjust to stand on top
            trees.append({"x": tree_x, "y": tree_y})

    return platforms, trees

def reset_game():
    global lives, shields, start_time, game_time, has_shield
    global player_x, player_y, y_velocity, is_jumping, facing_right, anim_timer, walk_index
    global camera_x, camera_y
    global game_over, game_won, exploding, explosion_timer, explosion_frame_index, explosion_finished_time
    global explosion_played
    global platforms
    global last_input_time
    global shield_flash_timer
    global shield_flashing
    global enemies
    global invincible, invincible_timer
    global clouds
    global health, MAX_HEALTH
    global show_level_intro, level_intro_start
    global right_wall
    global left_wall
    global freeze_input
    global in_quiz, quiz_cleared
    global using_shield
    using_shield = False
    in_quiz = False
    quiz_cleared = False
    selected_answer = None
    freeze_input = False

    health = MAX_HEALTH
    show_level_intro = True
    level_intro_start = time.time()

    shield_flash_timer = 0
    shield_flashing = False
    last_input_time = time.time()
    lives = 3
    shields = 3
    has_shield = False
    start_time = time.time()
    game_time = GAME_DURATION
    invincible = False
    invincible_timer = 0
    right_wall = {"x": 8250, "y": 0, "width": 1, "height": HEIGHT}
    left_wall = {"x": -10, "y": 0, "width": 1, "height": HEIGHT}

    player_x, player_y = 100, HEIGHT - SPRITE_SIZE - 50
    # Clouds
    clouds = []
    used_x_positions = []
    cloud_count = 15
    min_cloud_spacing = 200
    world_width = WIDTH * 10 + 250

    ground_y = HEIGHT - 50
    cloud_min_y = 40
    cloud_max_y = ground_y - 80  # Never touch the ground

    def generate_cloud_y():
        while True:
            y = random.randint(cloud_min_y, cloud_max_y)
            if abs(y - player_y) > 60:  # Avoid player's Y level
                return y

    # Near player clouds
    near_player_clouds = random.randint(1, 2)
    for _ in range(near_player_clouds):
        for attempt in range(20):
            cloud_x = random.randint(player_x - 300, player_x + 300)
            cloud_x = max(0, min(cloud_x, world_width))
            if all(abs(cloud_x - ux) >= min_cloud_spacing for ux in used_x_positions):
                used_x_positions.append(cloud_x)
                cloud_y = generate_cloud_y()
                drift_speed = random.uniform(0.03, 0.1)
                clouds.append({"x": cloud_x, "y": cloud_y, "vx": drift_speed})
                break

    # Remaining clouds
    while len(clouds) < cloud_count:
        cloud_x = random.randint(0, world_width)
        if any(abs(cloud_x - ux) < min_cloud_spacing for ux in used_x_positions):
            continue
        used_x_positions.append(cloud_x)
        cloud_y = generate_cloud_y()
        drift_speed = random.uniform(0.03, 0.1)
        clouds.append({"x": cloud_x, "y": cloud_y, "vx": drift_speed})
    y_velocity = 0
    is_jumping = False
    facing_right = True
    anim_timer = 0
    walk_index = 0

    camera_x, camera_y = 0, 0

    game_over = False
    game_won = False
    exploding = False
    explosion_timer = 0
    explosion_frame_index = 0
    explosion_finished_time = None
    explosion_played = False

    platforms, trees = generate_platforms()
    ground_platforms = [p for p in platforms if p["y"] == HEIGHT - 50 and p["width"] >= SPRITE_SIZE * 2]

    # Fallback if none found
    if not ground_platforms:
        ground_platforms = [{"x": 0, "y": HEIGHT - 50, "width": 300, "height": 50}]

    enemies = []
    enemy_count = 5
    spawn_attempts = 0
    max_attempts = 100

    while len(enemies) < enemy_count and spawn_attempts < max_attempts:
        ground = random.choice(ground_platforms)
        ex = random.randint(ground["x"], ground["x"] + ground["width"] - SPRITE_SIZE)
        ey = ground["y"] - SPRITE_SIZE
        enemy_rect = {"x": ex, "y": ey, "width": SPRITE_SIZE, "height": SPRITE_SIZE}
        player_rect = {"x": player_x, "y": player_y, "width": SPRITE_SIZE, "height": SPRITE_SIZE}

        too_close_to_player = check_overlap(enemy_rect, player_rect)
        too_close_to_others = any(check_overlap(enemy_rect, {"x": e.x, "y": e.y, "width": e.width, "height": e.height}) for e in enemies)

        if not too_close_to_player and not too_close_to_others:
            enemies.append(Enemy(ex, ey))

        spawn_attempts += 1


def lose_life():
    global lives, game_time, shields, has_shield, game_over
    global exploding, explosion_timer, explosion_played
    global player_x, player_y, y_velocity, is_jumping
    global shield_flashing, shield_flash_timer
    global health, explosion_finished_time

    if game_won or exploding:
        return

    if using_shield and shields > 0:
        shields -= 1
        shield_flashing = True
        shield_flash_timer = time.time()
        hit_sound.play()
        if shields == 0:
            has_shield = False
    else:
        health -= 1
        game_time -= random.randint(15, 30)
        if game_time < 0:
            game_time = 0
        if health <= 0:
            # Don't reset player position here!
            exploding = True
            explosion_timer = 0
            explosion_played = False
            explosion_finished_time = None  # RESET this too
        else:
            player_x = 100
            player_y = HEIGHT - SPRITE_SIZE - 50
            y_velocity = 0
            is_jumping = False

def draw_player():
    global walk_index, anim_timer, shield_flashing

    if invincible and int(time.time() * 10) % 2 == 0:
        return  # Flash off

    # Force pose: down = sit, up = hi
    if keys[pygame.K_LCTRL]:
        image = sit_frame
    elif keys[pygame.K_SPACE]:
        image = hi_frame
    elif is_jumping:
        if y_velocity > 0:
            image = falling_frame
        else:
            image = jump_frames
    elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        anim_timer += 1
        if anim_timer % 6 == 0:
            walk_index = (walk_index + 1) % len(walk_frames)
        image = walk_frames[walk_index]
    else:
        image = idle_frame

    if not facing_right:
        image = pygame.transform.flip(image, True, False)

    image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
    screen.blit(image, (player_x - camera_x, player_y - camera_y))

    # Draw shield
    if has_shield and shields > 0:
        now = time.time()
        flashing_duration = 0.5
        show_shield = True
        if shield_flashing:
            if now - shield_flash_timer > flashing_duration:
                shield_flashing = False
            else:
                show_shield = int((now - shield_flash_timer) * 10) % 2 == 0
        if show_shield:
            shield_scaled = pygame.transform.scale(shield_image, (SPRITE_SIZE + 20, SPRITE_SIZE + 20))
            shield_x = player_x - camera_x - 10
            shield_y = player_y - camera_y - 10
            screen.blit(shield_scaled, (shield_x, shield_y))

def draw_explosion():
    global explosion_frame_index, explosion_timer, exploding, explosion_finished_time, freeze_input
    if explosion_timer < 2:
        frame_duration = 2 / len(explosion_frames)
        explosion_frame_index = int(explosion_timer // frame_duration)
        frame = explosion_frames[min(explosion_frame_index, len(explosion_frames)-1)]
        scale = SPRITE_SIZE + int(explosion_timer * 60)
        frame = pygame.transform.scale(frame, (scale, scale))
        screen.blit(frame, (player_x - camera_x - scale//2 + SPRITE_SIZE//2, player_y - camera_y - scale//2 + SPRITE_SIZE//2))
    else:
        if not explosion_finished_time:
            explosion_finished_time = time.time()
            freeze_input = True  # Freeze inputs immediately
        exploding = False

def show_main_menu():
    screen.blit(menu_bg, (0, 0))  # Use the image instead of solid color
    screen.blit(title_image, (179, 150))
    screen.blit(hi_main_menu, (325, 200))
    play_rect = play_button.get_rect(center=(WIDTH // 2.1, HEIGHT // 1.45 - 80))
    quit_rect = quit_button.get_rect(center=(WIDTH // 1.8, HEIGHT // 1.7 + 80))
    screen.blit(play_button, play_rect)
    screen.blit(quit_button, quit_rect)
    pygame.display.flip()
    return play_rect, quit_rect

# Start in menu
in_main_menu = True
reset_game()
clock = pygame.time.Clock()
last_time = time.time()

while True:

    for cloud in clouds:
        cloud["x"] += cloud["vx"]

    # Reappear on the left when off the right edge
    if cloud["x"] > WIDTH * 5:
        cloud["x"] = -100

    # Optional wrap-around
    if cloud["x"] > WIDTH * 5:
        cloud["x"] = -100
    elif cloud["x"] < -100:
        cloud["x"] = WIDTH * 5

    if in_quiz:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                q = quiz_questions[current_question_index]
                if selected_answer == q["correct"]:
                    current_question_index += 1
                    if current_question_index >= len(quiz_questions):
                        quiz_cleared = True
                        game_won = True
                        in_quiz = False
                else:
                    lose_life()
                    in_quiz = False
                selected_answer = None
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        draw_quiz()
        pygame.display.flip()
        clock.tick(60)
        continue


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        if in_main_menu and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if play_rect.collidepoint(mx, my):
                game_music.play(-1)
                in_main_menu = False
                reset_game()
            elif quit_rect.collidepoint(mx, my):
                pygame.quit()
                sys.exit()
        if (game_over or game_won) and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
        if game_won:
            screen.blit(big_font.render("YOU WIN!", True, GREEN), (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            screen.blit(font.render("Press R to restart", True, WHITE), (WIDTH // 2 - 100, HEIGHT // 2 + 10))
        if event.type == pygame.USEREVENT + 1 and in_quiz:
            print("Timer triggered!")
            q = quiz_questions[current_question_index]
            if selected_answer == q["correct"]:
                current_question_index += 1
                if current_question_index >= len(quiz_questions):
                    quiz_cleared = True
                    game_won = True
                    in_quiz = False
            else:
                lose_life()
                in_quiz = False
            selected_answer = None
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)

    if in_main_menu:
        play_rect, quit_rect = show_main_menu()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()
    if any(keys) or any(pygame.mouse.get_pressed()) or pygame.mouse.get_rel() != (0, 0):
        last_input_time = time.time()
    if not game_over and not exploding and not game_won and not freeze_input:
        elapsed = time.time() - start_time
        remaining_time = max(0, game_time - elapsed)
        if invincible:
            if time.time() - invincible_timer > 0.5:
                invincible = False
        else:
            player_rect = {"x": player_x, "y": player_y, "width": SPRITE_SIZE, "height": SPRITE_SIZE}
            for enemy in enemies:
                enemy.update(player_x, player_y, platforms)
                if not enemy.active:
                    continue
                enemy_rect = {"x": enemy.x, "y": enemy.y, "width": enemy.width, "height": enemy.height}
                if check_overlap(player_rect, enemy_rect) and not game_won:
                    lose_life()
                    enemy.deactivate()
                    invincible = True
                    invincible_timer = time.time()
                    break
        if remaining_time <= 0 and not exploding and not game_won:
            exploding = True
            explosion_timer = 0
            explosion_played = False

        original_x = player_x
        player_rect = {"x": player_x, "y": player_y, "width": SPRITE_SIZE, "height": SPRITE_SIZE}
        
        if not keys[pygame.K_SPACE] and not keys[pygame.K_LCTRL]:
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
                facing_right = False
                if player_x < left_wall["x"] + left_wall["width"]:
                    player_x = left_wall["x"] + left_wall["width"]
            if keys[pygame.K_RIGHT]:
                player_x += player_speed
                if player_x + SPRITE_SIZE > right_wall["x"]:
                    player_x = right_wall["x"] - SPRITE_SIZE
                facing_right = True
            if keys[pygame.K_UP] and not is_jumping:
                y_velocity = -jump_power
                is_jumping = True
            if keys[pygame.K_e] and shields > 0:
                using_shield = True
                has_shield = True
            else:
                using_shield = False
                has_shield = False

        for platform in platforms:
            if platform["x"] < 0 and platform["width"] == 50:
                wall_rect = {"x": platform["x"], "y": platform["y"], "width": platform["width"], "height": platform["height"]}
                if check_overlap(player_rect, wall_rect):
                    player_x = original_x
                    break

        y_velocity += gravity
        player_y += y_velocity

        for platform in platforms:
            if (player_x + SPRITE_SIZE > platform["x"] and
                player_x < platform["x"] + platform["width"] and
                player_y + SPRITE_SIZE > platform["y"] and
                player_y + SPRITE_SIZE < platform["y"] + platform["height"] + y_velocity and
                y_velocity > 0):
                player_y = platform["y"] - SPRITE_SIZE
                y_velocity = 0
                is_jumping = False

        if player_y > HEIGHT and not game_won:
            lose_life()

    if exploding:
        explosion_timer += dt
        if not explosion_played:
            explosion_sound.play()
            explosion_played = True

    if not game_won and explosion_finished_time and time.time() - explosion_finished_time > 1:
        game_over = True

    target_camera_x = player_x - WIDTH // 2 + SPRITE_SIZE // 2
    target_camera_y = player_y - HEIGHT // 2 + SPRITE_SIZE // 2

    camera_x += (target_camera_x - camera_x) * 0.1
    max_camera_x = right_wall["x"] + right_wall["width"] - WIDTH
    camera_x = max(min(camera_x, max_camera_x), 0)
    camera_y += (target_camera_y - camera_y) * 0.1

    floor_y = HEIGHT - 50
    max_camera_y = floor_y - HEIGHT
    camera_y = max(min(camera_y, max_camera_y), 0)

    screen.fill(SKYBLUE)
    tree_parallax_x = camera_x * 0.1  # 30% of camera movement
    water_parallax_x = camera_x * 0.1

    screen.blit(giant_tree_image, (-tree_parallax_x, 0))
    for i in range(-1, 20):
        screen.blit(waterbg_image, (i * waterbg_image.get_width() - water_parallax_x, 525))
    cloud_parallax_x = camera_x * 0.2  # further back
    cloud_parallax_y = camera_y * 0.1  # slight vertical parallax

    for cloud in clouds:
        screen.blit(cloud_image, (
            cloud["x"] - cloud_parallax_x,
            cloud["y"] - cloud_parallax_y
        ))
    for tree in trees:
        screen.blit(tree_image, (tree["x"] - camera_x, tree["y"] - camera_y))
    castle_x = 7435
    castle2_x = 7965
    castleentry_rect = pygame.Rect(castleentry_x + 80, castleentry_y + 120, 150, 180)
    castle_y = -10
    screen.blit(CastleEntry, (castleentry_x - camera_x, castleentry_y - camera_y))
    screen.blit(castle_image, (castle_x - camera_x, castle_y - camera_y))
    screen.blit(castle_image, (castle2_x - camera_x, castle_y - camera_y))
    for platform in platforms:
        draw_x = platform["x"] - camera_x
        draw_y = platform["y"] - camera_y
        full_tiles = platform["width"] // 64
        leftover = platform["width"] % 64
        tile = pygame.transform.scale(grass_tile, (64, platform["height"]))
        for i in range(full_tiles):
            screen.blit(tile, (draw_x + i * 64, draw_y))
        if leftover:
            partial = pygame.transform.scale(grass_tile, (leftover, platform["height"]))
            screen.blit(partial, (draw_x + full_tiles * 64, draw_y))
    # LEVEL INTRO TEXT
    if show_level_intro:
        fade_duration = 1.5
        total_duration = 3
        elapsed_intro = time.time() - level_intro_start

        if elapsed_intro > total_duration:
            show_level_intro = False
        else:
            alpha = 255
            if elapsed_intro < fade_duration:
                alpha = int(255 * (elapsed_intro / fade_duration))  # fade in
            elif elapsed_intro > total_duration - fade_duration:
                alpha = int(255 * ((total_duration - elapsed_intro) / fade_duration))  # fade out

            level_text = big_font.render("LEVEL 1 - Os Campos", True, WHITE)
            level_text.set_alpha(alpha)
            prefix_text = tip_font.render("Aperte", True, WHITE)
            suffix_text = tip_font.render("para usar o escudo.", True, WHITE)
            key_x = prefix_x + prefix_text.get_width() + 10
            suffix_x = key_x + shield_key_img.get_width() + 10
            suffix_text.set_alpha(alpha)
            prefix_text.set_alpha(alpha)
            shield_key_img.set_alpha(alpha)
            rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(level_text, rect)
        screen.blit(prefix_text, (prefix_x, tip_y))
        screen.blit(shield_key_img, (-5,450))
        screen.blit(suffix_text, (suffix_x - 250, tip_y))

    if not game_over and not game_won:
        keys = pygame.key.get_pressed()
        player_rect = pygame.Rect(player_x, player_y, 40, 60)

        if player_rect.colliderect(castleentry_rect):
            prompt_x = player_x - camera_x + SPRITE_SIZE // 2 - interact_prompt.get_width() // 2
            prompt_y = player_y - camera_y - interact_prompt.get_height() - 10  # 10px above head
            screen.blit(interact_prompt, (prompt_x, prompt_y))
            text = font.render("SPACE", True, WHITE)
            text_rect = text.get_rect(center=(
                    prompt_x + interact_prompt.get_width() // 2,
                    prompt_y + interact_prompt.get_height() // 2
                ))
            screen.blit(text, text_rect)

        if player_rect.colliderect(castleentry_rect) and keys[pygame.K_SPACE] and not in_quiz and not quiz_cleared:
            in_quiz = True
            quiz_questions = generate_quiz()  # dynamic generation
            current_question_index = 0
            selected_answer = None
            explosion_played = True  # prevent explosion sound
            exploding = False        # stop any explosion event
        if exploding:
            draw_explosion()
        else:
            draw_player()
        for enemy in enemies:
            enemy.update(player_x, player_y, platforms)
            enemy.draw(screen, camera_x, camera_y)
        bar_x = 10
        bar_y = 30
        sbar_x = 10
        sbar_y = 80
        MAX_SHIELDS = 3
        bar_width = 200
        bar_height = 20
        health_ratio = health / MAX_HEALTH
        shield_ratio = shields / MAX_SHIELDS
        health_color = RED if health_ratio < 0.3 else YELLOW if health_ratio < 0.6 else GREEN
        shield_color = BLUE

        pygame.draw.rect(screen, WHITE, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
        pygame.draw.rect(screen, WHITE, (sbar_x - 2, sbar_y - 2 , bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, BLACK, (sbar_x, sbar_y, bar_width, bar_height))
        pygame.draw.rect(screen, shield_color, (sbar_x, sbar_y, int(bar_width * shield_ratio), bar_height))
        health_text = font.render(f"{int(health)}/{MAX_HEALTH}", True, WHITE)
        shield_text = font.render(f"{int(shields)}/{MAX_SHIELDS}", True, WHITE)
        label_text = font.render("VIDAS:", True, WHITE)
        label_rect = label_text.get_rect(center=(bar_x + bar_width // 2, bar_y - 16))
        slabel_text = font.render("ESCUDOS:", True, WHITE)
        slabel_rect = label_text.get_rect(center=(sbar_x + bar_width // 2 - 10, sbar_y - 16))
        draw_text_with_stroke(screen, "VIDAS:", font, bar_x + bar_width // 2, bar_y - 16, WHITE, center=True)
        draw_text_with_stroke(screen, "ESCUDOS:", font, sbar_x + bar_width // 2 + 8, sbar_y - 16, WHITE, center=True)
        screen.blit(label_text, label_rect)
        screen.blit(slabel_text, slabel_rect)
        text_rect = health_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        stext_rect = shield_text.get_rect(center=(sbar_x + bar_width // 2, sbar_y + bar_height // 2))
        screen.blit(health_text, text_rect)
        screen.blit(shield_text, stext_rect)
        health_str = f"{int(health)}/{MAX_HEALTH}"
        shield_str = f"{int(shields)}/{MAX_SHIELDS}"
        draw_text_with_stroke(screen, health_str, font, bar_x + bar_width // 2, bar_y + bar_height // 2, WHITE, center=True)
        draw_text_with_stroke(screen, shield_str, font, sbar_x + bar_width // 2, sbar_y + bar_height // 2, WHITE, center=True)
        bar_width = 200
        bar_height = 20
        bar_x = WIDTH - bar_width - 10
        bar_y = 30

        time_ratio = remaining_time / GAME_DURATION
        time_color = RED if time_ratio < 0.2 else YELLOW if time_ratio < 0.5 else YELLOW
        pygame.draw.rect(screen, WHITE, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))  # border
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))  # background
        pygame.draw.rect(screen, time_color, (bar_x, bar_y, int(bar_width * time_ratio), bar_height))  # fill

        label_text = font.render("TEMPO:", True, WHITE)
        label_rect = label_text.get_rect(center=(bar_x + bar_width // 2, bar_y - 16))
        draw_text_with_stroke(screen, "TEMPO:", font, bar_x + bar_width // 2, bar_y - 16, WHITE, center=True)

        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        time_string = f"{minutes:02}:{seconds:02}"
        time_text = font.render(time_string, True, WHITE)
        text_rect = time_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        draw_text_with_stroke(screen, time_string, font, bar_x + bar_width // 2, bar_y + bar_height // 2, WHITE, center=True)
    elif game_over and not game_won:
        screen.blit(big_font.render("Você Perdeu!", True, RED), (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(font.render('Aperte "R" Para tentar novamente.', True, RED), (WIDTH//2 - 250, HEIGHT//2 + 10))
    if game_won:
        screen.fill(BLACK)
        win_text = big_font.render("Você completou a fase 1!", True, GREEN)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(win_text, win_rect)

        restart_text = font.render('Aperte "R" Para voltar.', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, restart_rect)
        isrestart_text = smallerfont.render('Infelizmente, não conseguimos terminar o sistema de mudar de fases', True, BLUE)
        isrestart_rect = restart_text.get_rect(center=(WIDTH // 2 - 202, HEIGHT // 2 + 40))
        screen.blit(isrestart_text, isrestart_rect)

    pygame.display.flip()
    clock.tick(60)
