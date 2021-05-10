import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN1 = (0,255,0)
GREEN2 = (150,255,0)

BLOCK_SIZE = 20
SPEED = 1

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        self.direction2 = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.head2 = Point(self.w/2+2*BLOCK_SIZE,self.h/2+2*BLOCK_SIZE)    
                  
        self.snake2 = [self.head2, 
              Point(self.head2.x-BLOCK_SIZE, self.head2.y),
              Point(self.head2.x-(2*BLOCK_SIZE), self.head2.y)]              
        
        self.score = 0
        self.score2 = 0
        self.food = None
        self._place_food()
        self.snake1gone = 0
        self.snake2gone = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        elif self.food in self.snake2:
     	    self._place_food()	
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
		#Player 1 Movements
                if self.snake1gone == 0:
                    if event.key == pygame.K_LEFT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self.direction = Direction.DOWN

		#Player 2 Movements
                if self.snake2gone == 0:
                    if event.key == pygame.K_a:
                        self.direction2 = Direction.LEFT
                    elif event.key == pygame.K_d:
                        self.direction2 = Direction.RIGHT
                    elif event.key == pygame.K_w:
                        self.direction2 = Direction.UP
                    elif event.key == pygame.K_s:
                        self.direction2 = Direction.DOWN

        # 2. move
        if self.snake1gone == 0:
            self._move(self.direction) # update the head
            self.snake.insert(0, self.head)
        if self.snake2gone == 0:
            self._move2(self.direction2)
            self.snake2.insert(0,self.head2)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            self.snake1gone = 1
            self.snake = []
        if self._is_collision2():
            self.snake2gone = 1
            self.snake2 = []

        #Both snakes gone game over
        if self.snake1gone and self.snake2gone:
           game_over = True
           return game_over, self.score, self.score2

        # 4. place new food or just move
        #Did first snake eat a food ?
        if self.snake1gone == 0:
            if self.head == self.food:
                self.score += 1
                self._place_food()
            else:
                self.snake.pop()

        #Did second snake eat a food ?
        if self.snake2gone == 0:
            if self.head2 == self.food:
                self.score2 += 1
                self._place_food()
            else:
                self.snake2.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score, self.score2
    
    def _is_collision(self):
        # Snake 1 hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # Snake 1 hits itself
        if self.head in self.snake[1:]:
            return True
        # Snake 1 hits Snake 2
        if self.head in self.snake2:
            return True
        return False

    def _is_collision2(self):
        # Snake 2 hits boundry
        if self.head2.x > self.w - BLOCK_SIZE or self.head2.x < 0 or self.head2.y > self.h - BLOCK_SIZE or self.head2.y < 0:
            return True
        # Snake 2 hits itself
        if self.head2 in self.snake2[1:]:
            return True
        # Snake 2 hits Snake 1:
        if self.head2 in self.snake:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        #SNAKE 1 DISPLAY
        if self.snake1gone == 0:
            for pt in self.snake:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        #SNAKE 2 DISPLAY
        if self.snake2gone == 0:  
            for pt in self.snake2:
                pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))


    	#FOOD
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Player 1 Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        text2 = font.render("Player 2 Score: " + str(self.score2), True, WHITE)
        self.display.blit(text2, [0, 30])

        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            
    def _move2(self, direction):
        x = self.head2.x
        y = self.head2.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head2 = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score, score2 = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score player 1 = ', score)
    print('Final Score player 2 = ', score2)
        
        
    pygame.quit()
