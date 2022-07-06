import pygame
import color_constants
import random
import sys

pygame.init()
WIDTH, HEIGHT = 900,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
VY = 5
VX = 5
PLAYER_L_LOST_EVENT = pygame.USEREVENT + 1
PLAYER_R_LOST_EVENT = pygame.USEREVENT + 2

class Ball(pygame.Rect):
  def __init__(self, left, top, width, height, color):
    super().__init__(left, top, width, height)
    self._start_left = left
    self._start_top = top
    self.color = color

  def restore_position(self):
    self.move_ip(self._start_left - self.x, self._start_top - self.y)


class Player:
  def __init__(self, paddle, textbox) -> None:
    self.paddle=paddle
    self.score=0
    self.textbox = textbox

  def draw_paddle(self, screen):
    pygame.draw.rect(screen, self.paddle.color, self.paddle)

  def draw_score(self, screen):
    self.textbox.text=f'{self.score}'
    self.textbox.draw(screen)

class Textbox:
  def __init__(self, font, color, text, left, top) -> None:
    self.font = font
    self.color = color
    self.text = text
    self.left = left
    self.top = top

  def draw(self, screen):
    rendered_text = self.font.render(f'{self.text}', 1, self.color)
    screen.blit(rendered_text,( self.left, self.top))




class Paddle(pygame.Rect):
  def __init__(self, left, top, width, height, color):
    super().__init__(left, top, width, height)
    self.color = color
    self._start_left = left
    self._start_top = top

  def restore_position(self):
    self.move_ip(self._start_left - self.x, self._start_top - self.y)

# Left paddle
def handle_mov_player_left(keys_pressed, paddle_L):
  if keys_pressed[pygame.K_w] and paddle_L.y - VY > 0:
    paddle_L.y -= VY
  if keys_pressed[pygame.K_s] and paddle_L.y + paddle_L.height + VY < HEIGHT:
    paddle_L.y += VY

# Right paddle
def handle_mov_player_right(keys_pressed, paddle_R):
  if keys_pressed[pygame.K_UP] and paddle_R.y - VY > 0:
    paddle_R.y -= VY
  if keys_pressed[pygame.K_DOWN] and paddle_R.y + paddle_R.height + VY < HEIGHT:
    paddle_R.y += VY

ball_VY, ball_VX = 2,2
def handle_mov_ball(ball, paddle_L, paddle_R):
  global ball_VX, ball_VY
  if ball.x + ball.width + ball_VX > WIDTH:
    # Game lost
    pygame.event.post(pygame.event.Event(PLAYER_R_LOST_EVENT))
  elif  ball.x + ball_VX < 0:
    pygame.event.post(pygame.event.Event(PLAYER_L_LOST_EVENT))


  # Rebouncing with player right
  if ball.colliderect(paddle_R):
    intersect_rectangle = ball.clip(paddle_R)
    if intersect_rectangle.width > intersect_rectangle.height:
      ball_VY *= -1
    else:
      ball_VX *= -1

  # Rebouncing with player left
  elif ball.colliderect(paddle_L):
    intersect_rectangle = ball.clip(paddle_L)
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
  player_L.draw_paddle(WIN)
  player_L.draw_score(WIN)
  player_R.draw_paddle(WIN)
  player_R.draw_score(WIN)

def initialize():
  BALL_LENGTH=20
  BALL_START_X, BALL_START_Y = (WIN.get_width()- BALL_LENGTH) //2, (WIN.get_height() - BALL_LENGTH) // 2
  PLAYER_WIDTH, PLAYER_HEIGHT = 20,120
  PLAYER_START_X, PLAYER_START_Y =  20, (WIN.get_height()-PLAYER_HEIGHT)//2
  ball = Ball(BALL_START_X, BALL_START_Y, BALL_LENGTH, BALL_LENGTH, color_constants.WHITE)
  textbox_L = Textbox(SCORE_FONT, color_constants.WHITE, "Dummy", WIDTH // 4, 20)
  textbox_R = Textbox(SCORE_FONT, color_constants.WHITE, "Dummy", 3* WIDTH // 4, 20)
  paddle_L = Paddle(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, color_constants.WHITE)
  paddle_R = Paddle(WIN.get_width() - PLAYER_START_X - PLAYER_WIDTH, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, color_constants.WHITE)
  return ball, paddle_L, paddle_R, textbox_L, textbox_R


def main():
  pygame.display.set_caption('Pong')
  clock = pygame.time.Clock()
  game_started=False
  running = True
  FPS=60
  ball,paddle_L,paddle_R, textbox_L, textbox_R=initialize()
  player_L = Player(paddle_L, textbox_L)
  player_R = Player(paddle_R, textbox_R)
  while running:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running=False
      if event.type == PLAYER_L_LOST_EVENT:
        player_R.score += 1
        ball.restore_position()
        player_L.restore_position()
        player_R.restore_position()
        # ball,paddle_L,paddle_R=initialize()
      elif event.type == PLAYER_R_LOST_EVENT:
        ball.restore_position()
        player_L.score += 1
        ball.restore_position()
        player_L.paddle.restore_position()
        player_R.paddle.restore_position()


    keys_pressed=pygame.key.get_pressed()
    handle_mov_player_left(keys_pressed, paddle_L)
    handle_mov_player_right(keys_pressed, paddle_R)
    handle_mov_ball(ball, paddle_L, paddle_R)



    draw(ball, player_L, player_R)
    pygame.display.update()

  pygame.quit()

if __name__ == '__main__':
  main()