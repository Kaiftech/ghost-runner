import pygame
from sys import exit
from random import randint
screen = pygame.display.set_mode((900,650))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load('player/p1.png').convert_alpha()
        player_walk1 = pygame.transform.scale2x(walk1)
        walk2 = pygame.image.load('player/p2.png').convert_alpha()
        player_walk2 = pygame.transform.scale2x(walk2)
        walk3 = pygame.image.load('player/p3.png').convert_alpha()
        player_walk3 = pygame.transform.scale2x(walk3)
        walk4 = pygame.image.load('player/p4.png').convert_alpha()
        player_walk4 = pygame.transform.scale2x(walk4)
        self.player_walk = [player_walk1,player_walk2,player_walk3,player_walk4]
        jump = pygame.image.load('player/pjump.png').convert_alpha()
        self.player_jump = pygame.transform.scale2x(jump)
        self.player_index = 0
        self.jump_sound = pygame.mixer.Sound('music/jump.mp3')
        self.jump_sound.set_volume(0.2)
        self.image= self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (90,618))
        self.gravity = 0
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 618:
            self.gravity = -16
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 618:
            self.rect.bottom = 618

    def animation_state(self):
        if self.rect.bottom < 618:
        	self.image = self.player_jump
        else:
            self.player_index += 0.15
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 0:            
            bat_frame1 = pygame.image.load('bat/bat1.png').convert_alpha()
            bat_frame2 = pygame.image.load('bat/bat2.png').convert_alpha()
            bat_frame3 = pygame.image.load('bat/bat3.png').convert_alpha()
            bat_frame4 = pygame.image.load('bat/bat4.png').convert_alpha()
            bat_frame5 = pygame.image.load('bat/bat5.png').convert_alpha()
            self.frames =[bat_frame1,bat_frame2,bat_frame3,bat_frame4,bat_frame5]
            y_position = 540
        else:            
            dude_walk1 = pygame.image.load('pink/pink1.png').convert_alpha()
            dude_walk2 = pygame.image.load('pink/pink2.png').convert_alpha()
            dude_walk3 = pygame.image.load('pink/pink3.png').convert_alpha()
            dude_walk4 = pygame.image.load('pink/pink4.png').convert_alpha()
            dude_walk5 = pygame.image.load('pink/pink5.png').convert_alpha()
            dude_walk6 = pygame.image.load('pink/pink6.png').convert_alpha()
            self.frames = [dude_walk1,dude_walk2,dude_walk3,dude_walk4,dude_walk5,dude_walk6]
            y_position = 607
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (randint(1200,1201),y_position))
    def animation_state(self):
        self.animation_index += 0.5
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destory()
    def destory(self):
        if self.rect.x <= -100:
            self.kill()
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}',False,(111,106,199))
    score_rect = score_surf.get_rect(center = (450,50))
    screen.blit(score_surf,score_rect)
    return current_time
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,enemy_group,False):
        enemy_group.empty()
        return False
    else : return True


pygame.init()
width = 900
height = 650
game_active = True
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('music/bg.mp3')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)
player = pygame.sprite.GroupSingle()
player.add = (Player())

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ghost Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font('font.ttf', 50)


background_image = pygame.image.load('night.png').convert()

enemy_group = pygame.sprite.Group()

player_stand = pygame.image.load('player/p1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,5)
player_stand_rect = player_stand.get_rect(center = (450,350))

game_name = text_font.render('Ghost Runner',False,(111,106,199))
game_name_rect = game_name.get_rect(center = (450,230))

game_msg = text_font.render('Press space to run ',False,(111,106,199))
game_msg_rect = game_msg.get_rect(center = (450,440))


Timer = pygame.USEREVENT + 1
pygame.time.set_timer(Timer,900)
stand_timer = pygame.USEREVENT + 1
pygame.time.set_timer(stand_timer,1000)
player = pygame.sprite.GroupSingle()
player.add(Player())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == Timer :
                enemy_group.add(enemy(randint(0,2)))
        else:               
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(background_image,(0,0))
        score = display_score()
        player.draw(screen)
        player.update()

        enemy_group.draw(screen)
        enemy_group.update()
        game_active = collision_sprite()       
    else:
        screen.fill((0,0,0))
        screen.blit(player_stand,player_stand_rect)
        score_msg = text_font.render(f'Your score: {score} ' + '\n' + ' Press space to play again',False,(111,106,199))
        score_msg_rect = score_msg.get_rect(center =(450,440))
        screen.blit(game_name,game_name_rect)
        
        if score == 0: screen.blit(game_msg,game_msg_rect)
        else: screen.blit(score_msg,score_msg_rect)

        
    pygame.display.update()
    clock.tick(60)
