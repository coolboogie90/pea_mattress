# game data

from argparse import Action
from random import randint
from sre_constants import JUMP
from tkinter import ANCHOR
import pygame
import pgzrun

import math

WIDTH = 800
HEIGHT = 600

GROUND = 458
GRAVITY = 200

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 100
JUMP_SPEED = 200
isJump = False

# game status
hasnotstarted = True
on_pause = False

# splash and game over screens
game_over = Actor("gameover_bg")
start_screen = Actor("startscreen.png")
life = Actor("life32", anchor=('center', 'center'))
life.pos = (765, 40)

walking_cycle_images = ["walking_princess_0", "walking_princess_1"]
walking_active = True
current_index = 0

jumping_cycle_images = ["jumping_princess_0", "jumping_princess_1"]

def set_index_0():
    global current_index
    current_index = 0

def set_index_1():
    global current_index
    current_index = 1


def draw_splashscreen():
    global hasnotstarted
    hasnotstarted = True
    start_screen.draw()


def draw_gameover():
    global endgame
    #print("gameover!")
    endgame = True
    game_over.draw()
    screen.draw.text(str("You lost!"), bottom = HEIGHT -500 , left = WIDTH / 2, fontname = "blueberry")
    screen.draw.text(str("Press R to restart"), bottom = HEIGHT -450 , right = WIDTH / 2, fontname = "blueberry")

# hero initialisation

hero = Actor("walking_princess.gif", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND)
hero_speed = 0

def reset():
    # game status & initialization
    global endgame, hasnotstarted
    global hero, hero_speed, hero_lives, life, next_enemy_time, score
    global next_box_time, boxes, enemies
    global backgrounds_bottom, backgrounds_top, NUMBER_OF_BACKGROUND
    global BOX_APPARTION, ENEMY_APPARTION

    # game status
    endgame = False
    hero_lives = 3
    score = 0

    hero = Actor("walking_princess.gif", anchor=('middle', 'bottom'))
    hero.pos = (64, GROUND)
    hero_speed = 0

    # enemies initialisations
    ENEMY_APPARTION = (1, 3)
    next_enemy_time = randint(ENEMY_APPARTION[0], ENEMY_APPARTION[1])
    enemies = []

    # background inititalisation

    BOX_APPARTION = (2, 5)
    next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])
    boxes = []

    # background inititalisation

    backgrounds_bottom = []
    backgrounds_top = []

    for n in range(NUMBER_OF_BACKGROUND):
        bg_b = Actor("background2_peamattress", anchor=('left', 'top'))
        bg_b.pos = n * WIDTH, 0
        backgrounds_bottom.append(bg_b)

        bg_t = Actor("background1_peamattress", anchor=('left', 'top'))
        bg_t.pos = n * WIDTH, 0
        backgrounds_top.append(bg_t)


def draw():
    global endgame

    if endgame == True:
        draw_gameover()
    elif hasnotstarted == True:
        draw_splashscreen()
    else:
        draw_game()

def draw_game():
    screen.clear()

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()

    for box in boxes:
        box.draw()
    
    for enemy in enemies:
        enemy.draw()

    hero.draw()
    life.draw()
    screen.draw.text(f"LIVES {hero_lives}", [600,20], color="pink", owidth=1, ocolor="black", fontsize=50, fontname = "quitemagical")
    screen.draw.text(f"SCORE  {score}", [10,20], color="pink", owidth=1, ocolor="black", fontsize=50, fontname = "quitemagical")


    if on_pause:
        screen.draw.text(f"PAUSE",[250,200], color="pink", owidth=1, ocolor="black", fontsize=120, fontname = "blueberry")

def update(dt):
    if not on_pause:
        if endgame:
            draw_gameover()
        elif hasnotstarted:
            draw_splashscreen()
        else:
            update_game(dt)

def update_game(dt):
    global endgame, isJump
    screen.clear()
    # enemies update
    # box
    global next_box_time, game_over, hero_lives, score

    # hero update

    global hero_speed, current_index

    hero_speed -= GRAVITY * dt
    x, y = hero.pos
    y -= hero_speed * dt

    if y > GROUND:
        y = GROUND
        hero_speed = 0
        isJump = False

    hero.pos = x, y

    if current_index == 1:
        clock.schedule(set_index_0, .2)
    else:
        clock.schedule(set_index_1, .2)

    if isJump:
        hero.image = jumping_cycle_images[current_index]
    else:
        hero.image = walking_cycle_images[current_index]


    # bg update

    for bg in backgrounds_bottom:
        x, y = bg.pos
        x -= GAME_SPEED * dt
        bg.pos = x, y

    if backgrounds_bottom[0].pos[0] <= - WIDTH:
        bg = backgrounds_bottom.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_bottom.append(bg)

    for bg in backgrounds_top:
        x, y = bg.pos
        x -= GAME_SPEED/3 * dt
        bg.pos = x, y

    if backgrounds_top[0].pos[0] <= - WIDTH:
        bg = backgrounds_top.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_top.append(bg)

    next_box_time -= dt
    if next_box_time <= 0:
        box = Actor("pillow", anchor=('left', 'bottom'))
        box.pos = WIDTH, GROUND
        boxes.append(box)
        next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])
    
    
    for box in boxes:
        x, y = box.pos
        x -= GAME_SPEED * dt
        box.pos = x, y
        if box.colliderect(hero):
            boxes.pop(0)
            score = score
            hero_lives -= 1

    if boxes:
        if boxes[0].pos[0] <= - 32:
            score += 10
            boxes.pop(0)

    global next_enemy_time
    global amplitude

    amplitude = 200

    next_enemy_time -= dt

    if next_enemy_time <= 0:
        enemy = Actor("pea_enemy", anchor=('left', 'bottom'))
        enemy.pos = WIDTH, GROUND
        enemies.append(enemy)
        next_enemy_time = randint(ENEMY_APPARTION[0], ENEMY_APPARTION[1])
        
    for enemy in enemies:
        x, y = enemy.pos
        x -= GAME_SPEED * dt
        y = math.sin(x/92 + 17.5) * amplitude + 300        # scale sine wave
        y = int(y)                            # needs to be int
        enemy.pos = x, y
        if enemy.colliderect(hero):
            enemies.pop(0)
            score = score
            hero_lives -= 1
    
    if enemies:
        if enemies[0].pos[0] <= - 32:
            score += 10
            enemies.pop(0)

    if hero_lives == 0:
        endgame = True 
        screen.clear()
        draw_gameover()

## controls
def on_key_down(key):
    global hero_speed, on_pause, hasnotstarted, isJump

    # jump
    if key == keys.SPACE and hero_speed == 0:
        isJump = True
        if hero_speed <= 0:
            hero_speed = JUMP_SPEED

        # else:
        #     hero_speed = hero_speed
        #     isJump = False
    
    elif key == keys.R and endgame == True:
        reset()

    elif key == keys.P:
        on_pause = not on_pause
    
    elif key == keys.S and hasnotstarted == True:
        reset()
        hasnotstarted = False
        
reset()

pgzrun.go()

        
