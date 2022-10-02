import pygame
import time
import random
import pandas as pd

from datetime import datetime, date
from pygame.locals import *

SIZE = 40
DELAY = 0.15
BACKGROUND_COLOR = (110, 110, 5)
SIZE_SCREEN = (1040,800) #multiple de 40 obligatoire 1040 800

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
        self.menu = True
        self.pause = False
        self.over = False
        self.win = False
        self.mode = ""
        self.init_bot = True
        
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if self.pause:
                        if event.key == K_ESCAPE:
                            pygame.mixer.music.unpause()
                            self.pause = False

                    elif self.over:
                        if event.key == K_ESCAPE:
                            self.menu = True
                            self.over = False
                            self.mode = False      
                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            self.over = False

                    elif self.win:
                        if event.key == K_ESCAPE:
                            self.menu = True
                            self.win = False
                            self.mode = False
                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            self.win = False

                    elif self.menu: 
                        if event.key == K_ESCAPE:
                            running = False
                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            self.menu = False
                            self.mode = "human"
                        if event.key == K_a:
                            pygame.mixer.music.unpause()
                            self.menu = False
                            self.mode = "bot1"

                    else:
                        if self.mode == "human":
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

            if self.mode == "bot1":
                self.IA_BOT1()

            if self.pause:
                self.game_paused()

            if self.menu:
                self.main_menu()

            if not self.pause and not self.over and not self.win and not self.menu:
                self.play()

            

            time.sleep(DELAY)

    def main_menu(self):
        self.render_background()
        self.stat = Stat()

        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"MAIN MENU", True, (255,255,255))
        self.surface.blit(line1, (300,200))
        line2 = font.render(f"Best score : {self.stat.best_score_stat('Scores')}", True, (255,255,255))
        self.surface.blit(line2, (200,300))
        line3 = font.render(f"Best score time : {self.stat.best_score_stat('Time')}", True, (255,255,255))
        self.surface.blit(line3, (200,350))
        line4 = font.render(f"Best score Dim : ({self.stat.best_score_stat('Dim X')}px, {self.stat.best_score_stat('Dim Y')}px)", True, (255,255,255))
        self.surface.blit(line4, (500,300))
        line5 = font.render(f"Best score player : {self.stat.best_score_stat('Users')}", True, (255,255,255))
        self.surface.blit(line5, (500,350))
        line55 = font.render(f"Best score speed : {self.stat.best_score_stat('Speed')}", True, (255,255,255))
        self.surface.blit(line55, (200,400))
        line6 = font.render(f"Press Enter to start Normal Game. Press A to start Bot Game", True, (255,255,255))
        self.surface.blit(line6, (200,500))
        line7 = font.render(f"Press ESC to exit game", True, (255,255,255))
        self.surface.blit(line7, (200,550))

        pygame.display.flip()
        pygame.mixer.music.pause()
        self.time = datetime.now()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.apple.move(self.snake)
            self.snake.increase_length()

        #snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                print("dead on him")
                self.play_sound("crash")
                self.game_over()
                break

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] < SIZE_SCREEN[0] and 0 <= self.snake.y[0] < SIZE_SCREEN[1]):
            print("dead by collision")
            self.play_sound('crash')
            self.game_over()

        # victory
        if self.snake.length == int((SIZE_SCREEN[0]*SIZE_SCREEN[1])/(SIZE*SIZE)):
            self.play_sound('win')
            print("win")
            self.game_win()

    def game_over(self):
        self.save_score_in_DB(False)
        self.stat = Stat()
        self.render_background()

        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is over!", True, (255,255,255))
        self.surface.blit(line1, (300,200))
        line2 = font.render(f"Your score : {self.stat.last_game_stat('Scores')}", True, (255,255,255))
        self.surface.blit(line2, (200,300))
        line3 = font.render(f"Your time : {self.stat.last_game_stat('Time')}", True, (255,255,255))
        self.surface.blit(line3, (200,350))
        line4 = font.render(f"Dim : ({self.stat.last_game_stat('Dim X')}px, {self.stat.last_game_stat('Dim Y')}px)", True, (255,255,255))
        self.surface.blit(line4, (200,400))
        line5 = font.render(f"Player : {self.stat.last_game_stat('Users')}", True, (255,255,255))
        self.surface.blit(line5, (200,450))
        line55 = font.render(f"Speed : {self.stat.last_game_stat('Speed')}", True, (255,255,255))
        self.surface.blit(line55, (200,500))
        line6 = font.render(f"Best score : {self.stat.best_score_stat('Scores')}", True, (255,255,255))
        self.surface.blit(line6, (500,300))
        line7 = font.render(f"Best score time : {self.stat.best_score_stat('Time')}", True, (255,255,255))
        self.surface.blit(line7, (500,350))
        line8 = font.render(f"Best score Dim : ({self.stat.best_score_stat('Dim X')}px, {self.stat.best_score_stat('Dim Y')}px)", True, (255,255,255))
        self.surface.blit(line8, (500,400))
        line9 = font.render(f"Best score player : {self.stat.best_score_stat('Users')}", True, (255,255,255))
        self.surface.blit(line9, (500,450))
        line99 = font.render(f"Best score player : {self.stat.best_score_stat('Speed')}", True, (255,255,255))
        self.surface.blit(line99, (500,500))
        line10 = font.render(f"Press Enter to restart Game. Press ESC to go to main menu", True, (255,255,255))
        self.surface.blit(line10, (200,600))

        pygame.display.flip()
        pygame.mixer.music.pause()
        self.over = True
        self.reset()

    def game_win(self):
        self.save_score_in_DB(True)
        self.stat = Stat()
        
        self.render_background()
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"You win!!!!!!!!", True, (255,255,255))
        self.surface.blit(line1, (300,200))
        line2 = font.render(f"Your score : {self.stat.last_game_stat('Scores')}", True, (255,255,255))
        self.surface.blit(line2, (200,300))
        line3 = font.render(f"Your time : {self.stat.last_game_stat('Time')}", True, (255,255,255))
        self.surface.blit(line3, (200,350))
        line4 = font.render(f"Dim : ({self.stat.last_game_stat('Dim X')}px, {self.stat.last_game_stat('Dim Y')}px)", True, (255,255,255))
        self.surface.blit(line4, (500,300))
        line5 = font.render(f"Player : {self.stat.last_game_stat('Users')}", True, (255,255,255))
        self.surface.blit(line5, (500,350))
        line55 = font.render(f"Speed : {self.stat.last_game_stat('Speed')}", True, (255,255,255))
        self.surface.blit(line55, (200,400))
        line6 = font.render(f"Press Enter to restart Game. Press ESC to go to main menu", True, (255,255,255))
        self.surface.blit(line6, (200,500))

        pygame.display.flip()
        pygame.mixer.music.pause()
        self.win = True
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
        score2 = font.render(f"Timer: {datetime.now().second}", True, (255,255,255))
        self.surface.blit(score2,(800,50))
        pygame.display.flip()

    def save_score_in_DB(self,Win):
        addstat = {
            'Scores':[self.snake.length],
            'Dates':[date.today().strftime("%d/%m/%y")],
            'Time':[(datetime.now() - self.time).seconds],
            'Speed':[int(1/DELAY)],
            'Dim X':[SIZE_SCREEN[0]],
            'Dim Y':[SIZE_SCREEN[1]],
            'Users':[self.mode],
            'Win':[Win],
        }
        df1 = pd.DataFrame(addstat)
        df1.to_csv("resources/database.csv", header=False, index=False, mode='a')

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
        self.init_bot = True

    def IA_BOT1(self):
        #print("x = " + str(self.snake.x[0]) + " y = " +str(self.snake.y[0]) + " dir = " + self.snake.direction)
        if self.snake.x[0] == 0 and self.snake.y[0] == 40 and self.snake.direction == 'down':
            self.init_bot = False

        if self.init_bot == True:
            if self.snake.direction == 'down':
                self.snake.move_right()
            elif self.snake.direction == 'right':
                self.snake.move_up()
            elif self.snake.y[0] == 0 and self.snake.x[0] != 0:
                self.snake.move_left()
            elif self.snake.x[0] == 0:
                self.snake.move_down()
        else:
                if self.snake.y[0] == int(SIZE_SCREEN[1]-SIZE) and self.snake.x[0] == self.snake.x[1]:
                    self.snake.move_right()
                elif self.snake.direction == 'right' and self.snake.y[0] == int(SIZE_SCREEN[1]-SIZE):
                    self.snake.move_up()
                elif self.snake.y[0] == SIZE and self.snake.x[0] == self.snake.x[1] and self.snake.x[0] != 0 and self.snake.x[0] != int(SIZE_SCREEN[0]-SIZE):
                    self.snake.move_right()
                elif self.snake.direction == 'right' and self.snake.y[0] == SIZE:
                    self.snake.move_down()
                elif self.snake.y[0] == 0 and self.snake.x[0] == int(SIZE_SCREEN[0]-SIZE):
                    self.snake.move_left()
                elif self.snake.y[0] == 0 and self.snake.x[0] == 0:
                    self.snake.move_down()

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

    def move(self,snake):
        available_place = False
        while not available_place:
            available_place = True
            self.x = random.randint(0,SIZE_SCREEN[0]/SIZE-1)*SIZE
            self.y = random.randint(0,SIZE_SCREEN[1]/SIZE-1)*SIZE
            for i in range(snake.length):
                if self.x == snake.x[i] and self.y == snake.y[i]:
                    available_place = False
        self.draw()

class Stat:
    def __init__(self):
        self.df = pd.read_csv('resources/database.csv')

    def best_score_stat(self,name):
        return self.df[f"{name}"][self.df[self.df["Scores"]==self.df["Scores"].max()].index[0]]

    def last_game_stat(self,name):
        return self.df[f"{name}"][self.df.tail(1).index[0]]

if __name__ == "__main__":
    game = Game()
    game.run()
    