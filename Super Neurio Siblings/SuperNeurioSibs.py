import pygame
import os
import sys
import random
import time
import os
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("Super Neurio Siblings")


screen_height = 780
screen_width = 1152

screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load(os.path.join(sys.path[0], "NeurioBackground.png"))

neurio = pygame.image.load(os.path.join(sys.path[0], 'NeurioDormant.png'))

neurio_agonists = [
    pygame.image.load(os.path.join(sys.path[0], "BlackTarHeroin.png")),
    pygame.image.load(os.path.join(sys.path[0], "CokeStash.png")),
    pygame.image.load(os.path.join(sys.path[0], "LineOfCoke.png")),
    pygame.image.load(os.path.join(sys.path[0], "Pill.png"))
]

agonist_names = [
    "BlackTarHeroin.png",
    "CokeStash.png",
    "LineOfCoke.png",
    "Pill.png"
]

font = pygame.font.SysFont('Comic Sans MS', 50)

neurio_antagonist = pygame.image.load(os.path.join(sys.path[0], "Antagonist.png"))

princess_neuron = pygame.image.load(os.path.join(sys.path[0], 'PrincessNeuron.png'))
rewards = {
    
    "CokeStash.png" : 200,
    "LineOfCoke.png" : 100,
    "BlackTarHeroin.png" : 50,
    "Pill.png" : 25
    
}


sound = pygame.mixer.Sound("NeurioTheme.ogg")
punch_sound = pygame.mixer.Sound("NeurioPunch.mp3")
sniff_sound = pygame.mixer.Sound("NeurioSniff.ogg")
end_theme = pygame.mixer.Sound("NeurioEndTheme.mp3")

class Neurio:
    
    DY = 8
    IMG = neurio
    
    def __init__(self, x, y, jumping):
        
        self.x = x
        self.y = y
        self.jumping = jumping
        
        self.jump_state = 0
        self.jump_limit = 80
        
        self.dy = self.DY
        
        self.img = self.IMG
        
        self.angle = 0
        
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.gravity = 1
        
        self.score = 0
        self.threshold = 1500
    
    def draw(self):
        
        self.img = pygame.transform.rotate(self.IMG, self.angle)
        
        screen.blit(self.img, (self.x, self.y))
        
    def update(self):
        global agonists, antagonists, generate_obstacles
        
        if self.jumping:
            
            self.dy = self.DY

            if self.jump_state < self.jump_limit:
                
                self.y -= self.dy
                self.jump_state += self.dy
                
            else:
                
                self.jumping = False
                self.jump_state = 0
            
            self.draw()
        
        else:
            
            if self.y < screen_height-neurio.get_height()-20:
                self.y += self.dy
                self.dy += self.gravity
            
            self.draw()
        
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        
        
        for index, agonist in enumerate(agonists):
            
            if pygame.Rect.colliderect(self.rect, agonist.rect):
                
                sniff_sound.play()
                self.score += rewards[agonist_names[agonist.index]]
                
                print(self.score)
                
                agonists.pop(index)
                
        for index, antagonist in enumerate(antagonists):
            
            if pygame.Rect.colliderect(self.rect, antagonist.rect):
                
                punch_sound.play()
                self.score = (self.score // 2)
                
                antagonists.pop(index)
        
        if self.score > self.threshold:
            
            generate_obstacles = False
        
        if self.score < self.threshold and not generate_obstacles:
            generate_obstacles = True
            
class Substance:
    
    def __init__(self, x, y, dx):
        
        self.x = x
        self.y = y
        self.dx = dx
        
    def draw(self):
        
        screen.blit(self.img, (self.x, self.y))

class Wall:
    
    def __init__(self, x, width, dy):
        
        self.x = x
        self.width = width
        self.dy = dy
        
        self.height = 0
        self.rising = False
        
    def draw(self):
        
        pygame.draw.rect(screen, (255, 192, 203), pygame.Rect(self.x, 0, self.width, self.height))
        
    def update(self):
        
        if not self.rising:
            
            if self.height < screen_height:
                self.height += self.dy
                
        else:
            
            if self.height > 0:
                self.height -= self.dy
                
        self.draw()
        
class Princess:
    
    IMG = princess_neuron
    
    def __init__(self, x, y, dx):
        
        self.x = x
        self.y = y
        self.img = princess_neuron
        
        self.dx = dx
        
    def draw(self):
        
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        
        if self.x > (screen_width-self.img.get_width()-10):
            
            self.x -= self.dx
        
        self.draw()
class Agonist(Substance):

    def __init__(self, x, y, dx):
        Substance.__init__(self, x, y, dx)
        
        self.index = random.randint(0, 3)
        self.img = neurio_agonists[self.index]
        
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        
    def update(self):
        
        global agonists
        self.x -= self.dx

        
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
   
        self.draw()
        
class Antagonist(Substance):
    
    def __init__(self, x, y, dx):
        Substance.__init__(self, x, y, dx)
        
        self.img = neurio_antagonist
        
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        
    def update(self):
        
        global antagonists
        
        self.x -= self.dx
        
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        self.draw()
        
user = Neurio((screen_width // 2) - 20, screen_height-neurio.get_height()-20, False)

princess = Princess(screen_width, screen_height-290, 2)

wall = Wall(screen_width - 200, 20, 5)

user_password = ''
true_password = 'gspcamdsngm'

def main():
    
    global agonists, antagonists, generate_obstacles, user_password, true_password
    
    agonists = []
    antagonists = []
    dy = 2
    
    generate_obstacles = True
    
    if random.random() > 0.5:
        
        agonists.append(Agonist(
            screen_width + 10,
            random.random() * (screen_height - 150),
            2
        ))
        
    else:
        
        antagonists.append(Antagonist(
            screen_width + 10,
            random.random() * (screen_height - 150),
            2
        ))
        
    counter = 0
    rate = 150
    
    sound.play()
    
    while True:
        
        screen.blit(background, (0, 0))
        
        text_surface = font.render(f'{user.score}', False, (255, 255, 255))
        
        screen.blit(text_surface, ((screen_width / 2)-30, 20))
        user.update();
        
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    user.jumping = True
                    
                if event.key == pygame.K_LEFT:
                    user.x -= 5
                    
                elif event.key == pygame.K_RIGHT:
                    user.x += 5
                    
                elif event.key == pygame.K_DOWN:
                    pass
                
                else:
                    user_password += pygame.key.name(event.key)

            elif event.type == pygame.QUIT:
                
                sys.exit()
                
        for index, agonist in enumerate(agonists):
            
            if agonist.update() == -1:
                agonists.pop(index)
        
        for index, antagonist in enumerate(antagonists):
            
            if antagonist.update() == -1:
                antagonists.pop(index)
        
        if (counter % rate == 0) and generate_obstacles:
            
            substances = [
                Agonist(
                    screen_width + 10,
                    random.random() * (screen_height - 150),
                    dy
                ),
                Agonist(
                    -60,
                    random.random() * (screen_height - 150),
                    -dy
                ),
                Antagonist(
                    screen_width + 10,
                    random.random() * (screen_height - 150),
                    dy
                ),
                Antagonist(
                    -60,
                    random.random() * (screen_height - 150),
                    -dy
                ),
            ]
            
            random_substance = random.choice(substances)
            
            if type(random_substance).__name__ == 'Agonist':
                agonists.append(random_substance)
            else:
                antagonists.append(random_substance)
        
        counter += 1
        
        if (counter % 2000) == 0 and generate_obstacles:
            
            dy *= 1.4
            rate -= 10
        
        agonists_truth = all([agonist.x > screen_width or agonist.x < -agonist.img.get_width() for agonist in agonists])
        antagonists_truth = all([antagonist.x > screen_width or antagonist.x < -antagonist.img.get_width() for antagonist in antagonists])
        
        first_flag = False
        
        if agonists_truth and antagonists_truth and not generate_obstacles:
            
            if user.x > 100 and not wall.rising:
                user.x -= 5
            
            wall.update()
            princess.update()
            
            if len(user_password) >= len(true_password):
                
                if user_password[-len(true_password):] == true_password:
                    wall.rising = True
    
            if wall.rising == True and wall.height < 20:
                
                if abs(user.x-princess.x) > 100:
                    user.x += 5
                    princess.x -= 5

        pygame.display.update()
        
main()
