import pygame
import math
import random
class SceneBase:
    def __init__(self):
        self.next = self
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")
    def Update(self):
        print("uh-oh, you didn't override this in the child class")
    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    def Terminate(self):
        self.SwitchToScene(None)
def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()       
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True


            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
               \
                self.SwitchToScene(GameScene())
    def Update(self):
        pass



    def Render(self, screen):
        screen.fill((102, 255, 255))
        font = pygame.font.SysFont("comicsansms", 35)
        text = font.render("Enter->", True, (255, 51, 51))
        screen.blit(text, (255 - text.get_width() // 5, 100 - text.get_height() // 2))

class GameOverScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(TitleScene())



    def Update(self):
        pass



    def Render(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("comicsansms", 55)
        text = font.render("Game over!", True, (255, 0, 0))
        screen.blit(text, (190 - text.get_width() // 2, 150 - text.get_height() // 2))
        
   
class GamePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Food:
    def __init__(self,location):
        self.location = location
        self.color = (255, 255, 0)
    def draw(self, screen):
        pygame.draw.rect(
            screen, 
            self.color, 
            pygame.Rect(
                self.location.x,
                self.location.y,
                10,
                10
            )
        )


class Snake:
    def __init__(self, head):
        self.body = []
        self.body.append(head)
        self.color = (51, 255, 51)
        self.dx = 10
        self.dy = 0

    def saveNewDirection(self, dx, dy):
        self.dx = dx
        self.dy = dy


    def updateSnakePosition(self):
        newHeadPosition = GamePoint(self.body[0].x + self.dx, self.body[0].y + self.dy)

        for i in range(len(self.body) -1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x = newHeadPosition.x
        self.body[0].y = newHeadPosition.y



    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def canEatFood(self, food):
        if self.distance(self.body[0], food.location) < 2:
            return True

    def canChangeLevel(self):
        return len(self.body) == 5


    def hasCollisionWithWall(self, wall):
        res = False
        for brick in wall:
            for part in self.body:
                if part.x == brick.x and part.y == brick.y:
                    res = True
                    break
        return res

    def increase(self, point):
        tail = self.body[len(self.body) - 1]
        newTail = GamePoint(tail.x - 10, tail.y)
        self.body.append(newTail)

    def draw(self, screen):
        for i in range(0, len(self.body), 1):
            pygame.draw.rect(
                screen, 
                self.color, 
                pygame.Rect(

                    self.body[i].x,
                    self.body[i].y,
                    10,
                    10
                )
            )


    def printStatus(self, screen):
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render("length: {}".format(len(self.body)), True, (0, 255, 255))
        screen.blit(text, (320- text.get_width() // 2, 240 - text.get_height() // 2))


class Wall:
    def __init__(self, level):
        self.body = []
        self.color = (0, 0, 255)
        f = open("levels/level{0}.txt".format(level), "r")
        rowNumber = -1
        for row in f:
            rowNumber += 1
            for columNumber in range(0, len(row)):
                if row[columNumber] == '#':
                    brick = GamePoint(columNumber * 10, rowNumber * 10)
                    self.body.append(brick)


    def draw(self, screen):
        for i in range(0, len(self.body), 1):
            pygame.draw.rect(
                screen, 
                self.color, 
                pygame.Rect(
                    self.body[i].x,
                    self.body[i].y,
                    10,
                    10
                )
            )



class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.snake = Snake(GamePoint(50, 50))
        self.food = Food(GamePoint(30, 140))
        self.currentLevel = 1
        self.maxLevels = 3
        self.wall = Wall(1)

    def ProcessInput(self, events, pressed_keys):
        if pressed_keys[pygame.K_UP]: 
            self.snake.saveNewDirection(0, -10)
        elif pressed_keys[pygame.K_DOWN]:
            self.snake.saveNewDirection(0, 10)
        elif pressed_keys[pygame.K_LEFT]: 
            self.snake.saveNewDirection(-10, 0)
        elif pressed_keys[pygame.K_RIGHT]:
            self.snake.saveNewDirection(10, 0)


    def Update(self):
        self.snake.updateSnakePosition()
        if self.snake.hasCollisionWithWall(self.wall.body):
            self.SwitchToScene(GameOverScene())
        else:
            if self.snake.canEatFood(self.food):
                self.snake.increase(self.food.location)
                self.food = Food(GamePoint(random.randrange(30) * 10, random.randrange(30) * 10))
                if self.snake.canChangeLevel():
                    self.currentLevel += 1

                    if self.currentLevel > self.maxLevels:

                        self.currentLevel = 1

                    self.wall = Wall(self.currentLevel)
                    
                    self.snake = Snake(GamePoint(100, 100))


    def Render(self, screen):


        screen.fill((255, 0, 127))

        

        self.wall.draw(screen)
        self.snake.draw(screen)
        self.food.draw(screen)
        

run_game(555, 300, 10, TitleScene())