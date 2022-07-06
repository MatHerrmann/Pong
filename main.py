import pygame
import color_constants
from pathlib import Path

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900,600
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
pygame.mixer
VY = 5
VX = 5
PLAYER_L_LOST_EVENT = pygame.USEREVENT + 1
PLAYER_R_LOST_EVENT = pygame.USEREVENT + 2

class Ball(pygame.Rect):
  LENGTH=20
  START_X, START_Y = (SCREEN_WIDTH- LENGTH) //2, (SCREEN_HEIGHT - LENGTH) // 2
  def __init__(self, color, left=START_X, top=START_Y, width=LENGTH, height=LENGTH):
    super().__init__(left, top, width, height)
    self._start_left = left
    self._start_top = top
    self.color = color

  def restore_position(self):
    self.move_ip(self._start_left - self.x, self._start_top - self.y)


class Player:
  def __init__(self, paddle, textbox_x, path_to_sound) -> None:
    self.paddle=paddle
    self.score=0
    self.textbox = Textbox(SCORE_FONT, paddle.color, "", textbox_x, 20)
    self.sound = pygame.mixer.Sound(path_to_sound)

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
  WIDTH, HEIGHT = 20,120
  def __init__(self, color, left, top, width=WIDTH, height=HEIGHT):
    super().__init__(left, top, width, height)
    self.color = color
    self._start_left = left
    self._start_top = top

  def restore_position(self):
    self.move_ip(self._start_left - self.x, self._start_top - self.y)

# Left paddle
def handle_mov_player_left(keys_pressed, paddle_L):
  if keys_pressed[pygame.K_w] and paddle_L.y - VY > 0:
    paddle_L.move_ip(0,-VY)
  if keys_pressed[pygame.K_s] and paddle_L.y + paddle_L.height + VY < SCREEN_HEIGHT:
    paddle_L.move_ip(0,VY)

# Right paddle
def handle_mov_player_right(keys_pressed, paddle_R):
  if keys_pressed[pygame.K_UP] and paddle_R.y - VY > 0:
    paddle_R.move_ip(0,-VY)
  if keys_pressed[pygame.K_DOWN] and paddle_R.y + paddle_R.height + VY < SCREEN_HEIGHT:
    paddle_R.move_ip(0,VY)

ball_VY, ball_VX = 2,2
def handle_mov_ball(ball, player_L, player_R):
  global ball_VX, ball_VY
  if ball.x + ball.width + ball_VX > SCREEN_WIDTH:
    # Game lost
    pygame.event.post(pygame.event.Event(PLAYER_R_LOST_EVENT))
  elif  ball.x + ball_VX < 0:
    pygame.event.post(pygame.event.Event(PLAYER_L_LOST_EVENT))


  # Rebouncing with player right
  if ball.colliderect(player_R.paddle):
    player_R.sound.play()
    intersect_rectangle = ball.clip(player_R.paddle)
    if intersect_rectangle.width > intersect_rectangle.height:
      ball_VY *= -1
    else:
      ball_VX *= -1

  # Rebouncing with player left
  elif ball.colliderect(player_L.paddle):
    player_L.sound.play()
    intersect_rectangle = ball.clip(player_L.paddle)
    if intersect_rectangle.width > intersect_rectangle.height:
      ball_VY *= -1
    else:
      ball_VX *= -1

  # Rebouncing at screen
  if ball.y + ball.height + ball_VY > SCREEN_HEIGHT or ball.y + ball_VY < 0:
    ball_VY *= -1
  ball.move_ip(ball_VX, ball_VY)

def draw(ball, player_L, player_R):
  WIN.fill(color_constants.BLACK)
  pygame.draw.rect(WIN, ball.color, ball)
  player_L.draw_paddle(WIN)
  player_L.draw_score(WIN)
  player_R.draw_paddle(WIN)
  player_R.draw_score(WIN)

def main():
  pygame.display.set_caption('Pong')
  clock = pygame.time.Clock()
  game_started=False
  running = True
  FPS=60
  PLAYER_START_X, PLAYER_START_Y =  20, (SCREEN_HEIGHT-Paddle.HEIGHT)//2
  ball = Ball(color_constants.WHITE)
  paddle_L = Paddle( color_constants.WHITE, PLAYER_START_X, PLAYER_START_Y)
  paddle_R = Paddle( color_constants.WHITE, SCREEN_WIDTH - PLAYER_START_X - Paddle.WIDTH, PLAYER_START_Y)
  player_L = Player(paddle_L, SCREEN_WIDTH // 4, str(Path("assets") / '4390__noisecollector__pongblipf-4.wav'))
  player_R = Player(paddle_R, SCREEN_WIDTH *3 // 4, str(Path("assets") / '4391__noisecollector__pongblipf-5.wav'))
  while running:
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running=False
      if event.type == PLAYER_L_LOST_EVENT:
        player_R.score += 1
        ball.restore_position()
        player_L.paddle.restore_position()
        player_R.paddle.restore_position()
      elif event.type == PLAYER_R_LOST_EVENT:
        ball.restore_position()
        player_L.score += 1
        ball.restore_position()
        player_L.paddle.restore_position()
        player_R.paddle.restore_position()


    keys_pressed=pygame.key.get_pressed()
    handle_mov_player_left(keys_pressed, paddle_L)
    handle_mov_player_right(keys_pressed, paddle_R)
    handle_mov_ball(ball, player_L, player_R)



    draw(ball, player_L, player_R)
    pygame.display.update()

  pygame.quit()

if __name__ == '__main__':
  main()