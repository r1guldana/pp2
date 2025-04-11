import pygame
import random
import time
import psycopg2
from datetime import datetime

# ========== DATABASE SETUP ========== #
def connect():
    return psycopg2.connect(
        dbname="snake_g",
        user="postgres",
        password="thismysql2025forpp2", 
        host="localhost",
        port="5432"
    )

def get_or_create_user(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
        print(f"Welcome, {username}! START GAME!!!")
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO user_score (user_id) VALUES (%s)", (user_id,))
        print(f"Created new user: {username}")

    conn.commit()
    cur.close()
    conn.close()
    return user_id

def load_progress(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result if result else (0, 1)
#saveeeee
def save_progress(user_id, score, level):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_score SET score = %s, level = %s, last_updated = NOW()
        WHERE user_id = %s
    """, (score, level, user_id))
    conn.commit()
    cur.close()
    conn.close()
    print("save.")

# ==========  GAME SNAKEEE  ========== #
blue = (50, 153, 213)
black = (0, 0, 0)
red = (213, 50, 80)
white = (255, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

width, height = 600, 400
snake_block = 10

pygame.init()
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Генерация еды
def generate_food(snake_list, current_walls):
    while True:
        food_x = random.randint(0, (width // snake_block) - 1) * snake_block
        food_y = random.randint(0, (height // snake_block) - 1) * snake_block
        food_pos = (food_x, food_y)
        if food_pos not in snake_list and food_pos not in current_walls:
            food_type = random.choices(['normal', 'big', 'disappearing'], weights=[0.7, 0.2, 0.1])[0]
            food_data = {'position': food_pos, 'type': food_type}
            if food_type == 'disappearing':
                food_data['spawn_time'] = time.time()
            return food_data

def print_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(display, black, [segment[0], segment[1], snake_block, snake_block])

def main():
    # ========== USERs LOGIN ========== #
    username = input("input user name : ")
    user_id = get_or_create_user(username)
    score, level = load_progress(user_id)
    speed = 10 + (level - 1) * 2

    # Walls
    walls = [(x, 0) for x in range(0, width, snake_block)] + [(x, height - snake_block) for x in range(0, width, snake_block)]
    walls += [(0, y) for y in range(0, height, snake_block)] + [(width - snake_block, y) for y in range(0, height, snake_block)]

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length = 1
    food = generate_food(snake_list, walls)

    game_over = False
    while not game_over:
        display.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    # Сохраняем игру
                    save_progress(user_id, score, level)
                    print("save.")

        x1 += x1_change
        y1 += y1_change

        if (x1, y1) in walls or x1 < 0 or x1 >= width or y1 < 0 or y1 >= height:
            game_over = True

        for wall in walls:
            pygame.draw.rect(display, black, [wall[0], wall[1], snake_block, snake_block])

        if food['type'] == 'normal':
            pygame.draw.rect(display, red, [food['position'][0], food['position'][1], snake_block, snake_block])
        elif food['type'] == 'big':
            pygame.draw.rect(display, green, [food['position'][0], food['position'][1], snake_block, snake_block])
        elif food['type'] == 'disappearing':
            if time.time() - food['spawn_time'] > 5:
                food = generate_food(snake_list, walls)
            else:
                pygame.draw.rect(display, yellow, [food['position'][0], food['position'][1], snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        if snake_head in snake_list[:-1]:
            game_over = True

        print_snake(snake_block, snake_list)

        if (x1, y1) == food['position']:
            if food['type'] == 'normal':
                length += 1
                score += 1
            elif food['type'] == 'big':
                length += 3
                score += 3
            elif food['type'] == 'disappearing':
                length += 5
                score += 5

            food = generate_food(snake_list, walls)

            if score % 3 == 0:
                level += 1
                speed += 2

        font = pygame.font.SysFont(None, 30)
        display.blit(font.render(f"Score: {score}", True, white), (10, 10))
        display.blit(font.render(f"Level: {level}", True, white), (10, 40))

        pygame.display.update()
        clock.tick(speed)

    save_progress(user_id, score, level)
    pygame.quit()

if __name__ == '__main__':
    main()
