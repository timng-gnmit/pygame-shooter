import pygame

#fonts
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont('comicsansms',40)
WINNER_FONT = pygame.font.SysFont('comicsansms',100)

#dimensions of window, initializing
WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
PADDING = 10
pygame.display.set_caption("First Game!")

#framerate
FPS = 60

#colors used in the game
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#collision events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#set up the center line
BORDER_WIDTH = 10
BORDER = pygame.Rect((WIDTH+BORDER_WIDTH)//2,0,BORDER_WIDTH,HEIGHT)

#ship size, speed
SHIPWIDTH,SHIPHEIGHT = 55,40
SHIPSPEED = 5
STARTING_HEALTH = 10

#bullet size, speed
BULLETWIDTH, BULLETHEIGHT = 10,5
MAXBULLETS = 3
BULLETSPEED = 7

red = pygame.Rect(100,200,SHIPWIDTH,SHIPHEIGHT)
yellow = pygame.Rect(800-SHIPWIDTH,200,SHIPWIDTH,SHIPHEIGHT)

#RED SHIP ON LEFT
#YELLOW SHIP ON RIGHT

#speed factor
SHIPSPEED = SHIPSPEED*60//FPS
BULLETSPEED = BULLETSPEED*60//FPS

###################################################################
#how to make rectangles
def draw_spaceship(surf,color,x,y):
    pygame.draw.rect(surf,color,pygame.Rect(x,y,SHIPWIDTH,SHIPHEIGHT))

#screen refresh
def draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN,WHITE,BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (PADDING, PADDING))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - PADDING, PADDING))

    draw_spaceship(WIN,YELLOW,yellow.x,yellow.y)
    draw_spaceship(WIN,RED,red.x,red.y)

    for bullet in red_bullets:
        pygame.draw.rect(WIN,GREEN,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,BLUE,bullet)

    pygame.display.update()

#red movements
def handle_red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_a] and red.x - SHIPSPEED > 0: # red move left
        red.x -= SHIPSPEED
    if keys_pressed[pygame.K_d] and red.x + SHIPSPEED < BORDER.x - SHIPWIDTH: # red move right
        red.x += SHIPSPEED
    if keys_pressed[pygame.K_w] and red.y - SHIPSPEED > 0: # red move up
        red.y -= SHIPSPEED
    if keys_pressed[pygame.K_s] and red.y + SHIPSPEED < HEIGHT - SHIPHEIGHT: # red move down
        red.y += SHIPSPEED

#yellow movements
def handle_yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - SHIPSPEED > BORDER.x + BORDER_WIDTH: # yellow move left
        yellow.x -= SHIPSPEED
    if keys_pressed[pygame.K_RIGHT] and yellow.x + SHIPSPEED < WIDTH-SHIPWIDTH: # yellow move right
        yellow.x += SHIPSPEED
    if keys_pressed[pygame.K_UP] and yellow.y - SHIPSPEED > 0: # yellow move up
        yellow.y -= SHIPSPEED
    if keys_pressed[pygame.K_DOWN] and yellow.y + SHIPSPEED < HEIGHT - SHIPHEIGHT: # yellow move down
        yellow.y += SHIPSPEED

#bullet movement and collisions
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x -= BULLETSPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x <= 0:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x += BULLETSPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x >= WIDTH - BULLETWIDTH:
            red_bullets.remove(bullet)

#when someone wins
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, ((WIDTH/2 - draw_text.get_width()/2), (HEIGHT/2 - draw_text.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(5000)
    red.x = 100
    red.y = 200
    yellow.x = 800-SHIPWIDTH
    yellow.y = 200

#main function
def main():
    red_bullets = []
    yellow_bullets = []

    red_health = STARTING_HEALTH
    yellow_health = STARTING_HEALTH

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAXBULLETS: # red player bullet
                    bullet = pygame.Rect(red.x + SHIPWIDTH, red.y + SHIPHEIGHT//2, BULLETWIDTH ,BULLETHEIGHT)
                    red_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAXBULLETS: # yellow player bullet
                    bullet = pygame.Rect(yellow.x, yellow.y + SHIPHEIGHT//2, BULLETWIDTH, BULLETHEIGHT)
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health)
            draw_winner(winner_text)
            main()

        keys_pressed = pygame.key.get_pressed()

        handle_red_movement(keys_pressed,red)
        handle_yellow_movement(keys_pressed,yellow)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health)

if __name__ == "__main__":
    main()