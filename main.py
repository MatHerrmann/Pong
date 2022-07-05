import pygame
import color_constants
import random
import sys

pygame.init()
WIDTH, HEIGHT = 900,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
VY = 5
VX = 5
GAME_OVER_EVENT = pygame.USEREVENT + 1

class Ball(pygame.Rect):
  def __init__(self, left, top, width, height, color):
    super().__init__(left, top, width, height)
    self.color = color

class Paddle(pygame.Rect):
  def __init__(self, left, top, width, height, color):
    super().__init__(left, top, width, height)
    self.color = color

# Left paddle
def handle_mov_player_left(keys_pressed, player_L):
  if keys_pressed[pygame.K_w] and player_L.y - VY > 0:
    player_L.y -= VY
  if keys_pressed[pygame.K_s] and player_L.y + player_L.height + VY < HEIGHT:
    player_L.y += VY

# Right paddle
def handle_mov_player_right(keys_pressed, player_R):
  if keys_pressed[pygame.K_UP] and player_R.y - VY > 0:
    player_R.y -= VY
  if keys_pressed[pygame.K_DOWN] and player_R.y + player_R.height + VY < HEIGHT:
    player_R.y += VY

ball_VY, ball_VX = 2,2
def handle_mov_ball(ball, player_L, player_R):
  global ball_VX, ball_VY
  if ball.x + ball.width + ball_VX > WIDTH or ball.x + ball_VX < 0:
    # Game lost
    pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))


  # Rebouncing with player right
  if ball.colliderect(player_R):
    intersect_rectangle = ball.clip(player_R)
    if intersect_rectangle.width > intersect_rectangle.height:
      ball_VY *= -1
    else:
      ball_VX *= -1

  # Rebouncing with player left
  elif ball.colliderect(player_L):
    intersect_rectangle = ball.clip(player_L)
    if intersect_rectangle.width > intersect_rectangle.height:
      ball_VY *= -1
    else:
      ball_VX *= -1

  # Rebouncing at screen
  if ball.y + ball.height + ball_VY > HEIGHT or ball.y + ball_VY < 0:
    ball_VY *= -1
  ball.x += ball_VX
  ball.y += ball_VY

def draw(ball, player_L, player_R):
  WIN.fill(color_constants.BLACK)
  pygame.draw.rect(WIN, ball.color, ball)
  pygame.draw.rect(WIN, player_L.color, player_L)
  pygame.draw.rect(WIN, player_R.color, player_R)

def initialize():
  BALL_LENGTH=20
  BALL_START_X, BALL_START_Y = (WIN.get_width()- BALL_LENGTH) //2, (WIN.get_height() - BALL_LENGTH) // 2
  PLAYER_WIDTH, PLAYER_HEIGHT = 50,90
  PLAYER_START_X, PLAYER_START_Y =  20, (WIN.get_height()-PLAYER_HEIGHT)//2
  ball = Ball(BALL_START_X, BALL_START_Y, BALL_LENGTH, BALL_LENGTH, color_constants.WHITE)
  player_L = Paddle(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, color_constants.WHITE)
  player_R = Paddle(WIN.get_width() - PLAYER_START_X - PLAYER_WIDTH, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, color_constants.WHITE)
  return ball, player_L, player_R


def main():
  pygame.display.set_caption('Pong')
  clock = pygame.time.Clock()
  game_started=False
  running = True
  FPS=60
  ball,player_L,player_R=initialize()
  while running:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running=False
      if event.type == GAME_OVER_EVENT:
        ball,player_L,player_R=initialize()


    keys_pressed=pygame.key.get_pressed()
    handle_mov_player_left(keys_pressed, player_L)
    handle_mov_player_right(keys_pressed, player_R)
    handle_mov_ball(ball, player_L, player_R)



    draw(ball, player_L, player_R)
    pygame.display.update()

  pygame.quit()

if __name__ == '__main__':
  main()