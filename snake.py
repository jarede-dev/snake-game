import pygame
import pygame as pg
from random import randrange
from pygame import mixer

#initialize pygame
pygame.init()

#initialize mixer
mixer.init()

#set window size
WINDOW = 580
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] 

snake = pg.rect.Rect([0, 0, TILE_SIZE -2, TILE_SIZE -2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0) 
time, time_step = 0, 110
food = pygame.image.load('images/food.png')
food_rect = food.get_rect(center=get_random_position())
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs_key = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
dirs_arrow ={pg.K_RIGHT: 1, pg.K_LEFT: 1, pg.K_DOWN: 1, pg.K_UP: 1}

#game title
pygame.display.set_caption('Snake Game')

#add score
current_score = 0
high_score = 0

#background and sounds
background = pygame.image.load('images/background.png')
bite_sound = mixer.Sound("music/bite.wav")
mixer.music.load("music/bite.wav")
mixer.music.play(1)
gameOver_sound = mixer.Sound("music/gameOver.wav")
mixer.music.load("music/gameOver.wav")
mixer.music.play(1)
mixer.music.load("music/bgm.wav")
mixer.music.play(-1)

#game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            # move snake using arrow keys
            if event.key == pg.K_UP and dirs_arrow[pg.K_UP]:
                dirs_arrow = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                snake_dir = (0, -TILE_SIZE)
            if event.key == pg.K_DOWN and dirs_arrow[pg.K_DOWN]:
                dirs_arrow = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                snake_dir = (0, TILE_SIZE)
            if event.key == pg.K_LEFT and dirs_arrow[pg.K_LEFT]:
                dirs_arrow = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
                snake_dir = (-TILE_SIZE, 0)
            if event.key == pg.K_RIGHT and dirs_arrow[pg.K_RIGHT]:
                dirs_arrow = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
                snake_dir = (TILE_SIZE, 0)
            # move snake using w,a,s,d keys
            if event.key == pg.K_w and dirs_key[pg.K_w]:
                dirs_key = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                snake_dir = (0, -TILE_SIZE)
            if event.key == pg.K_s and dirs_key[pg.K_s]:
                dirs_key = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                snake_dir = (0, TILE_SIZE)
            if event.key == pg.K_a and dirs_key[pg.K_a]:
                dirs_key = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                snake_dir = (-TILE_SIZE, 0)
            if event.key == pg.K_d and dirs_key[pg.K_d]:
                dirs_key = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
                snake_dir = (TILE_SIZE, 0)
    screen.fill("black")
    
    # check borders   selfeating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food_rect.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
        current_score = 0
        gameOver_sound.play()

        
    #check food
    if snake.center == food_rect.center:
        food_rect.center = get_random_position()
        length+=1 
        current_score = length - 1
        bite_sound.play()
        if current_score > high_score:
            high_score = current_score


    #draw background image
    screen.blit(background, (0, 0))

    #draw food
    screen.blit(food, food_rect)

    # draw snake
    [pg.draw.rect(screen, "green", segment) for segment in segments]

    #draw score
    font = pg.font.Font(None, 36)
    score_text = font.render(f"Current Score: {current_score}   High Score: {high_score}", True, "white")
    score_text_rect = score_text.get_rect(center=(screen.get_width()/2, 10))
    score_text_rect.y += 10 
    screen.blit(score_text, score_text_rect)

    # move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)