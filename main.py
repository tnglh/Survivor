import random

import pygame
from sys import exit
from random import randint,choice


pygame.init()
pygame.mixer.init()
#create the screen
def display_detail():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surface = test_font.render(f"{current_time}",False,"Black")
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)

    #bullet_photo = pygame.image.load("/Users/Toan/Desktop/graphics/bullet_left.png").convert_alpha()
    bullet_left_surface = test_font.render(f"Bullet: {player.sprite.bullet}", False, "Black")
    bullet_left_rect = bullet_left_surface.get_rect(center=(90, 20))
    screen.blit(bullet_left_surface,bullet_left_rect)

    lives_left_surface = test_font.render(f"Live: {player.sprite.live}", False, "Black")
    lives_left_rect = lives_left_surface.get_rect(center=(80, 50))
    screen.blit(lives_left_surface, lives_left_rect)




# def obstacle_movement(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#             if obstacle_rect.y >= 250:
#                 screen.blit(snail_surface,obstacle_rect)
#             else:
#                 screen.blit(fly_surface,obstacle_rect)
#             obstacle_list = [ obstacle for obstacle in obstacle_list if obstacle.x >-100 ]
#         return obstacle_list
#     else:
#         return []


def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# def player_animation():
#     global player_surface,player_index
#     if player_rect.bottom <300:
#         player_surface = player_jump
#     else:
#         player_index += 0.1
#         if player_index >= 2: player_index =0
#         player_surface = player_walk[int(player_index)]
def collisions_player_obstacle():

    if pygame.sprite.spritecollide(player.sprite, obstacle_group,True):
        player.sprite.live -= 1
        if player.sprite.live <= 0:
            player.sprite.reset()
            return False
    return True

def collisions_bullet_obstacle():
    pygame.sprite.groupcollide(bullet_group, obstacle_group,False,True)

def collisions_player_loot():
    if pygame.sprite.spritecollide(player.sprite, loot_group, True):
        player.sprite.bullet +=5

#class Heart(pygame.sprite.Sprite):
#    def __init__(self):
#        super().__init__()
#        big_image = pygame.image.load('/Users/Toan/Desktop/graphics/fire.png').convert_alpha()
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        big_image = pygame.image.load('graphics/bullet/fire.png').convert_alpha()
        self.image = pygame.transform.scale(big_image,(50,50))
        self.rect = self.image.get_rect(midleft=(player.sprite.rect.centerx, player.sprite.rect.centery))
        self.bullet =5
    def trigger(self):
        if self.bullet >0:
            self.bullet -=1
    def destroy(self):
        if self.rect.x > 900:
            self.kill()
    def update(self):
        self.rect.x += 10
        self.destroy()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
        self.jumpleft = 2
        self.bullet = 5
        self.jumpsound = pygame.mixer.Sound('sound/jump-sound.mp3')
        self.jumpsound.set_volume(0.3)

        self.live = 2
        self.attack_cooldown = 0

    def player_input(self):


        # if event.type == pygame.KEYDOWN:
        #     if event.type == pygame.K_RIGHT:
        #         self.rect.right += 50
        #     if event.type == pygame.K_SPACE  and self.jumpleft > 0:
        #         self.gravity = -15
        #         self.jumpleft -= 1
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE] and self.jumpleft > 0:
        #     self.gravity = -15
        #     self.jumpleft -=1
        if self.rect.x <= 750:
            if keys[pygame.K_d] :
                self.rect.right += 10
        if  0 < self.rect.x :
            if keys[pygame.K_a]:
                self.rect.left -= 10
        if keys[pygame.K_DOWN]:
            self.gravity += 3
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom =300
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image =self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= 2:
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def jump(self):
        if self.jumpleft > 0 :
            self.gravity = -15
        self.jumpleft -=1
        self.jumpsound.play()


    def reset(self):
        self.rect.x = 200
        self.gravity = 0
    def update(self):
        self.player_input()
        self.apply_gravity()
        if self.rect.bottom == 300:
             self.jumpleft = 2
        self.animation_state()
        if self.attack_cooldown > 0:
            self.attack_cooldown -=1

class Loot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        photo = pygame.image.load('graphics/loot/chest.png').convert_alpha()
        self.image = pygame.transform.scale(photo,(75,75))
        self.rect = self.image.get_rect(midbottom =(randint(900,1100),300))
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    def update(self):
        self.rect.x -= 1
        self.destroy()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames= [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index =0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom= (randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= 2: self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    def update(self):
        self.animation_state()
        self.rect.x -= 3
        self.destroy()
start_time = 0

screen = pygame.display.set_mode((800, 400))
game_active = False

bgsound = pygame.mixer.Sound('sound/music.wav')
bgsound.set_volume(0.3)
bgsound.play(loops=-1)
# name the app
pygame.display.set_caption("Survivor")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)

# display an image
ground_surface = pygame.image.load('graphics/background/ground.png')

# add text
text_surface = test_font.render("hello", False, "Black")
text_x_pos =400
text_rect = text_surface.get_rect(center = (text_x_pos,50))
play_surface = test_font.render("play",False,"Black")
play_rect = play_surface.get_rect(center=(500,50))


#add sky
sky_surface = pygame.image.load('graphics/background/sky.png').convert()

# #add obstacle
# snail_1 = pygame.image.load('/Users/Toan/Desktop/graphics/snail1.png').convert_alpha()
# snail_2 = pygame.image.load('/Users/Toan/Desktop/graphics/snail2.png').convert_alpha()
# snail = [snail_1, snail_2]
# snail_index =0
# snail_surface = snail[snail_index]
#
#
# fly_1= pygame.image.load('/Users/Toan/Desktop/graphics/Fly1.png').convert_alpha()
# fly_2 = pygame.image.load('/Users/Toan/Desktop/graphics/Fly2.png').convert_alpha()
# fly = [fly_1,fly_2]
# fly_index = 0
# fly_surface = fly[fly_index]


# # add player and player_rect
# player_walk_1 = pygame.image.load('/Users/Toan/Desktop/graphics/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('/Users/Toan/Desktop/graphics/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_1,player_walk_2]
# player_index = 0
# player_jump = pygame.image.load('/Users/Toan/Desktop/graphics/jump.png').convert_alpha()
# player_surface = player_walk[player_index]
# player_rect = player_surface.get_rect(midbottom = (80,300))
 # mit spriteGroup
player = pygame.sprite.GroupSingle() #player in this case is a group not a sprite
player.add( Player())

obstacle_group = pygame.sprite.Group()

bullet_group = pygame.sprite.Group()

loot_group = pygame.sprite.Group()



# game intro scence
player_stand = pygame.image.load('graphics/player/player_stand.png').convert()
player_stand =  pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))
#player_gravity = 0
#obstacle
#obstacle_rect_list = []

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

loot_timer = pygame.USEREVENT +2
pygame.time.set_timer(loot_timer, randint(5000,7000))
# snail_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_timer, 500)
#
# fly_timer = pygame.USEREVENT+3
# pygame.time.set_timer(fly_timer,200)
#
# jumpleft =2

# event-loop
while True:
    # event_handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active == True :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    player.sprite.jump()
            #     elif event.key == pygame.K_DOWN:
            #         player_gravity += 3
            #     elif event.key == pygame.K_LEFT:
            #         player_rect.left -= 50
            #     elif event.key == pygame.K_RIGHT:
            #         player_rect.right += 50
                if event.key == pygame.K_k:
                    if player.sprite.bullet > 0 and player.sprite.attack_cooldown == 0:
                        bullet_group.add(Bullet())
                        player.sprite.bullet -=1
                        player.sprite.attack_cooldown = 50
            if event.type == obstacle_timer:
                # if randint(1,2) ==1 :
                #     obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900,1200),300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1200), 200)))
                obstacle_group.add(Obstacle(random.choice(["fly","snail","snail","snail"])))
            # if event.type == snail_timer:
            #     if snail_index == 0: snail_index =1
            #     else: snail_index == 0
            #     snail_surface = snail[snail_index]
            # if event.type == fly_timer:
            #     if fly_index == 0: fly_index =1
            #     else: fly_index == 0
            #     fly_surface = fly[fly_index]
            if event.type == loot_timer:
                loot_group.add(Loot())

        else:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        text_x_pos = 400

        screen.blit(ground_surface, (0, 300))

        screen.blit(sky_surface,(0,0))
        display_detail()

        #obstacle move
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #mouse_pos = pygame.mouse.get_pos()
        # player_animation()
        # player_gravity += 1
        # player_rect.y += player_gravity
        #
        # if player_rect.bottom >= 300:
        #     player_rect.bottom =300
        #     jumpleft = 2
        #
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        bullet_group.draw(screen)
        bullet_group.update()

        loot_group.draw(screen)
        loot_group.update()
        collisions_bullet_obstacle()
        collisions_player_loot()
        # game_active = collisions(player_rect,obstacle_rect_list)
        game_active = collisions_player_obstacle()




    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(text_surface,text_rect)
        player.sprite.reset()
        obstacle_group.empty()
        bullet_group.empty()
        loot_group.empty()
        player.sprite.bullet = 5
        player.sprite.live = 2

        # player_rect.x = 80
        # player_gravity = 0
        # obstacle_rect_list.clear()

    pygame.display.update()
    clock.tick(60)
