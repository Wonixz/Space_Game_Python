#Space Invaders
import pygame
import random
import os
pygame.font.init()
#Icon
programIcon = pygame.image.load('assets/icon.png')

pygame.display.set_icon(programIcon)
#Screen
width , height = 900,600
Win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space war")

#Load Images
Red_space_ship = pygame.image.load(os.path.join('assets','red.png'))
Blue_space_ship = pygame.image.load(os.path.join('assets','blue.png'))
Green_space_ship = pygame.image.load(os.path.join('assets','green.png'))
Yellow_space_ship = pygame.image.load(os.path.join('assets','yellow.png'))

#Player Ship
Player_space_ship = pygame.image.load(os.path.join('assets','player1.png'))

#Bomb
Red_bomb =pygame.image.load(os.path.join('assets','red_bomb.png'))
Blue_bomb =pygame.image.load(os.path.join('assets','blue_bomb.png'))
Green_bomb =pygame.image.load(os.path.join('assets','green_bomb.png'))
Yellow_bomb =pygame.image.load(os.path.join('assets','yellow-bomb.png'))

#Player Bomb
Player_bomb = pygame.image.load(os.path.join('assets','player_bomb.png'))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets','background.jpg')),(width,height))

class Bomb:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not(self.y <= height and self.y >=0)
    def collision(self,obj):
        return collide(self,obj)


class Ship():
    Cooldown = 30
    def __init__(self,x,y,health =100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bomb_img = None
        self.bombs = []
        self.cool_down_counter = 0
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for bomb in self.bombs :
            bomb.draw(window)

    def move_bomb(self,vel,obj):
        self.cooldown()
        for bomb in self.bombs:
            bomb.move(vel)
            if bomb.off_screen(height):
                self.bombs.remove(bomb)
            elif bomb.collision(obj):
                obj.health -=10
                self.bombs.remove(bomb)

    def cooldown(self):
        if self.cool_down_counter>=self.Cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1

    def shoot(self):
        if self.cool_down_counter == 0:
            bomb = Bomb(self.x,self.y,self.bomb_img)
            self.bombs.append(bomb)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = Player_space_ship
        self.bomb_img = Player_bomb
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_bomb(self, vel, objs):
            self.cooldown()
            for bomb in self.bombs:
                bomb.move(vel)
                if bomb.off_screen(height):
                    self.bombs.remove(bomb)
                else:
                    for obj in objs:
                        if bomb.collision(obj):
                            objs.remove(obj)
                            if bomb in self.bombs :
                                self.bombs.remove(bomb)
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)
    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y + self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y + self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))
class Enemy(Ship):
    Color_map = {
        "red" : (Red_space_ship,Red_bomb),
        "green" : (Green_space_ship,Green_bomb),
        "blue"  :   (Blue_space_ship,Blue_bomb),
        "yellow":   (Yellow_space_ship,Yellow_bomb)
    }


    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img ,self.bomb_img = self.Color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def  move(self,vel):
        self.y +=vel
    def shoot(self):
        if self.cool_down_counter == 0:
            bomd = Bomb(self.x-10,self.y,self.bomb_img)
            self.bombs.append(bomd)
            self.cool_down_counter =1



def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y=  obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None
def main():
    run =True
    FPS = 60
    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans",30)
    lost_font = pygame.font.SysFont("comicsans",70)

    enemies = []
    wave_lenght = 5
    enemy_vel = 1
    player_vel = 5
    bomb_vel = 4

    player = Player(450,500)

    Clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        Win.blit(BG,(0,0))

        lives_label = main_font.render(f"Lives : {lives}",1,(255,255,255))
        level_label = main_font.render(f"Level : {level}",1,(255,255,255))

        Win.blit(lives_label,(10,10))
        Win.blit(level_label,(width - level_label.get_width() - 10 ,10))


        for enemy in enemies:
            enemy.draw(Win)
        player.draw(Win)

        if lost:
            lost_label = lost_font.render("GAME OVER",1,(255,255,255))
            Win.blit(lost_label,(width/2-lost_label.get_width()/2,300))
        pygame.display.update()


    while run:
        Clock.tick(FPS)
        redraw_window()

        if lives <=0 or player.health<=0:
            lost = True
            lost_count+=1
        if lost:
            if lost_count>FPS*3:
                run = False
            else:
                continue

        if len(enemies) == 0 :
            level+=1
            wave_lenght+=5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(["red","blue","green","yellow"]))
                enemies.append(enemy)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel >0 :
            player.x -=player_vel
        if keys[pygame.K_d] and player.x +player_vel + player.get_width()<width:
            player.x +=player_vel
        if keys[pygame.K_w] and player.y - player_vel >0:
            player.y -=player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 22 < height:
            player.y +=player_vel
        if keys[pygame.K_SPACE] :
            player.shoot()
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bomb(bomb_vel,player)

            if random.randrange(0,2*60) == 1:
                enemy.shoot()

            if collide(enemy,player):
                player.health-=10

            elif enemy.y + enemy.get_height() > height:
                lives -=1
                enemies.remove(enemy)

        player.move_bomb(-bomb_vel,enemies)
main()

'''
def main_menu():
    title_font = pygame.font.SysFont("comicsans",65)
    BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background.jpg')), (width, height))
    run = True
    while run :
        Win.blit(BG,(width,height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Win.blit(BG, (0, 0))
                title_label = title_font.render("Press the mouse to begin", 1, (24, 255, 255))
                Win.blit(title_label, (width / 2 - title_label.get_width() / 2, 300))
                main()
    pygame.quit()
main_menu()
'''