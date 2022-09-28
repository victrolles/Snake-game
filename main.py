from turtle import width
import pygame
import time
import random

from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
SIZE_SCREEN = (1000,800) #multiple de 40 obligatoire 1000 800

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode(SIZE_SCREEN)
        self.surface.fill((255,255,255))

        pygame.mixer.init()
        self.play_background_music()

        self.snake = Snake(self.surface,2)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()



    def run(self): 
        running = True
        self.pause = False
        self.over = False
        
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if self.pause:
                        if event.key == K_ESCAPE:
                            pygame.mixer.music.unpause()
                            self.pause = False
                    elif self.over:
                        if event.key == K_ESCAPE:
                            running = False
                        
                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            self.over = False
                    else:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_ESCAPE:
                            self.pause = True

                elif event.type == QUIT:
                    running = False

            if self.pause:
                self.game_paused()

            if not self.pause and not self.over:
                self.play()

            

            time.sleep(0.2)



    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.apple.move()
            self.snake.increase_length()

        #snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                self.game_over()
                break

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= SIZE_SCREEN[0] and 0 <= self.snake.y[0] <= SIZE_SCREEN[1]):
            self.play_sound('crash')
            self.game_over()

    def game_over(self):
        self.render_background()

        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render(f"To play again press Enter. To exit press ESC", True, (255,255,255))
        self.surface.blit(line2, (200,350))

        pygame.display.flip()
        pygame.mixer.music.pause()

        self.over = True
        self.reset()

    def game_paused(self):
        self.render_background()

        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game paused ", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render(f"To resume press ESC.", True, (255,255,255))
        self.surface.blit(line2, (200,350))

        pygame.display.flip()
        pygame.mixer.music.pause()


    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score,(800,10))

    def is_collision(self,x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    
    def play_sound(self,name):
        sound = pygame.mixer.Sound(f"resources/1_snake_game_resources_{name}.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface,2)
        self.apple = Apple(self.surface)

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def move_up(self):
        if self.y[0] <= self.y[1]:
            self.direction = 'up'

    def move_down(self):
        if self.y[0] >= self.y[1]:
            self.direction = 'down'

    def move_right(self):
        if self.x[0] >= self.x[1]:
            self.direction = 'right'

    def move_left(self):
        if self.x[0] <= self.x[1]:
            self.direction = 'left'

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*2
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        #available_place = False
        #while not available_place:
        #    available_place = True
        #    self.x = random.randint(0,SIZE_SCREEN[0]/SIZE-1)*SIZE
        #    self.y = random.randint(0,SIZE_SCREEN[1]/SIZE-1)*SIZE
        #    for i in range(0,self.sna):
        #        if self.x == Snake.x[i] or self.y == Snake.y[i]:
        #            available_place = False
        
        self.x = random.randint(0,SIZE_SCREEN[0]/SIZE-1)*SIZE
        self.y = random.randint(0,SIZE_SCREEN[1]/SIZE-1)*SIZE

class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.flip()
        return action
    
    def tamere(self):
        pass

if __name__ == "__main__":
    game = Game()
    game.run()
    