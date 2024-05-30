import pygame
import button
from random import randrange

RES = 800
SIZE = 50

global surface
global clock

pygame.init()

surface = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()

eat_sound = pygame.mixer.Sound("eat.mp3")
lost_sound = pygame.mixer.Sound('lost.mp3')
lost_sound.set_volume(0.35)
button_sound = pygame.mixer.Sound('button.mp3')
button_sound.set_volume(1.2)

font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)
font_title = pygame.font.SysFont('Arial', 50, bold=True)
font_restart = pygame.font.SysFont('Arial', 45, bold=True)
pygame.display.set_caption('Snake Game by @TryH4ckM3')

start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
apple_image = pygame.image.load('Apple.png').convert_alpha()
restart_image = pygame.image.load('restart.png').convert_alpha()

exit_image = pygame.image.load('exit.png').convert_alpha()
pygame.transform.scale(exit_image, (100, 100))

menu_img = pygame.image.load('snake.jpg').convert()

def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def play_main():

    pygame.mixer.music.load('back.wav')

    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.pause()
    pygame.mixer.music.play(-1)

    showtext = True
    x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    fps = 60
    dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
    score = 0
    speed_count, snake_speed = 1, 10

    color1 = '#564242'
    color2 = '#504545'
    snake_color = '#95E77B'
    snake_head_color = '#4DFB6F'

    move = True
    lost = False

    while True:

        pygame.draw.rect(surface, pygame.Color('black'), (0, 0, 800, 800))

        [pygame.draw.rect(surface, pygame.Color(color1), (i, j, SIZE-1, SIZE-1)) for i in range(0, 801, 100) for j in range(0, 801, 100)]
        [pygame.draw.rect(surface, pygame.Color(color1), (i+50, j, SIZE-1, SIZE-1)) for i in range(0, 801, 100) for j in range(50, 801, 100)]

        [pygame.draw.rect(surface, pygame.Color(color2), (i+50, j, SIZE-1, SIZE-1)) for i in range(0, 801, 100) for j in range(0, 801, 100)]
        [pygame.draw.rect(surface, pygame.Color(color2), (i, j, SIZE-1, SIZE-1)) for i in range(0, 801, 100) for j in range(50, 801, 100)]




        # drawing snake, apple
        [pygame.draw.rect(surface, pygame.Color(snake_color), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
        pygame.draw.rect(surface, pygame.Color(snake_head_color), (snake[len(snake)-1][0], snake[len(snake)-1][1], 49, 49))
        surface.blit(apple_image, (*apple, SIZE, SIZE))

        if showtext:
            render_title = font_title.render(f'Use WASD to play', 1, pygame.Color('orange'))
            surface.blit(render_title, (RES // 2 - 220, RES // 3 - 150))

        # show score
        render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        surface.blit(render_score, (5, 5))

        # snake movement
        if move == True:
            speed_count += 1
            if not speed_count % snake_speed:
	            x += dx * SIZE
	            y += dy * SIZE
	            snake.append((x, y))
	            snake = snake[-length:]
            # eating food
            if snake[-1] == apple:
                apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
                length += 1
                score += 1
                #snake_speed -= 10
                snake_speed = max(snake_speed, 4)
                pygame.mixer.Sound.play(eat_sound)

        # game over
        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            surface.blit(render_end, (RES // 2 - 200, RES // 3))
            restart_button = button.Button(430, 415, restart_image, 0.6)
            exit_button = button.Button(250, 400, exit_image, 0.6)
            pygame.mixer.music.pause()
            if lost == False:
                pygame.mixer.Sound.play(lost_sound)
                lost = True
            move = False
            if restart_button.draw(surface):
                pygame.mixer.Sound.play(button_sound)
                play_main()
            elif exit_button.draw(surface):
                 pygame.mixer.Sound.play(button_sound)
                 close_game()
                 pygame.quit()
                 exit(0)

        pygame.display.flip()
        clock.tick(fps)
        close_game()
        # controls
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            if dirs['W']:
                dx, dy = 0, -1
                dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
                showtext = False
        elif key[pygame.K_s]:
            if dirs['S']:
                dx, dy = 0, 1
                dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
                showtext = False
        elif key[pygame.K_a]:
            if dirs['A']:
                dx, dy = -1, 0
                dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
                showtext = False
        elif key[pygame.K_d]:
            if dirs['D']:
                dx, dy = 1, 0
                dirs = {'W': True, 'S': True, 'A': False, 'D': True, }
                showtext = False


start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(450, 200, exit_img, 0.8)

run = True
menu_music = pygame.mixer.music.load('menu.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.pause()
pygame.mixer.music.play(-1)
while run:
    
    surface.blit(menu_img, (0, 0))
    render_title = font_title.render(f'Snake Game', 1, pygame.Color('#4E3535'))
    surface.blit(render_title, (RES // 2 - 150, RES // 3 - 150))

    if start_button.draw(surface):
        pygame.mixer.Sound.play(button_sound)
        play_main()
    if exit_button.draw(surface):
        pygame.mixer.Sound.play(button_sound)
        pygame.quit()
        exit(0)

	#event handler
    for event in pygame.event.get():
		#quit game
	    if event.type == pygame.QUIT:
		    run = False

    pygame.display.update()
