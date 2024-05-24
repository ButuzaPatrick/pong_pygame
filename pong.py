import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720
FPS = 90
ball_speed_x = 5 * random.choice((-1,1))
ball_speed_y = 5 * random.choice((-1,1))
difficulty_change = 5 * FPS
difficulty_counter = 0

player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0

#setting up text
font = pygame.font.Font(None, 100)

play_pressed = False

def move_ball():
    global ball_speed_x, ball_speed_y, play_pressed, player_score, opponent_score

    if play_pressed:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

    #ball boundaries
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    
    #ball scores
    if ball.left <= 0 or ball.right >= screen_width:

        if ball.left <= 0:
            print(ball.left)
            player_score += 1
        if ball.right >= screen_width:
            print(ball.right)
            opponent_score += 1

        reset_ball()

    #ball hits players
    if pygame.Rect.colliderect(ball, player) or pygame.Rect.colliderect(ball, opponent):
        ball_speed_x *= -1
        ball_speed_y *= random.choice((-1,1))

def move_player():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

    player.y += player_speed

def opponent_movement():
    if ball.y < opponent.y + 70:
        opponent.y -= opponent_speed
    if ball.y > opponent.y -70:
        opponent.y += opponent_speed

    if opponent.top <= 0:
       opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def reset_ball():
    global ball_speed_y, ball_speed_x, play_pressed

    play_pressed = False
    ball_speed_x = 5
    ball_speed_y = 5

    ball.center = (screen_width/2,screen_height/2)

    if play_pressed:
        ball_speed_x *= random.choice((-1,1))
        ball_speed_y *= random.choice((-1,1))

def increment_difficulty():
    global difficulty_counter, difficulty_change, ball_speed_y, ball_speed_x

    if difficulty_counter > difficulty_change:

        if ball_speed_y < 0:
            ball_speed_y -= 1
        else:
            ball_speed_y += 1
        
        if ball_speed_x < 0:
            ball_speed_x -= 1
        else:
            ball_speed_y += 1

        difficulty_counter = 0
    else:
        difficulty_counter += 1

#setting up the screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

#setting up ball and players
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 20, 140)
opponent = pygame.Rect(0, screen_height/2 - 70, 20, 140)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 10
            elif event.key == pygame.K_UP:
                player_speed -= 10
            elif event.key == pygame.K_SPACE:
                print(ball_speed_x,ball_speed_y)
                play_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 10
            elif event.key == pygame.K_UP:
                player_speed += 10

    move_ball()
    move_player()
    opponent_movement()
    increment_difficulty()

    opponent_text_surface = font.render(str(player_score), True, (255,255,255), None)
    player_text_surface = font.render(str(opponent_score), True, (255,255,255), None)

    #visuals
    screen.fill('black')
    pygame.draw.aaline(screen, (130,130,130), (screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.rect(screen, (200,200,200), player)
    pygame.draw.rect(screen, (200,200,200), opponent)
    pygame.draw.ellipse(screen, (200,200,200), ball)

    #text
    screen.blit(opponent_text_surface, (screen_width/4 - 40, screen_height/4 - 100))
    screen.blit(player_text_surface, ((3*screen_width/4) - 40, screen_height/4 - 100))

    pygame.display.update()
    pygame.display.flip()
    clock.tick(FPS)