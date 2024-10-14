import pygame
import os
import random

# init pygame
pygame.init()
#screen = pygame.display.set_mode((320,180))
pygame.font.get_init()
TEXT_FONT = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_surface = pygame.Surface((320,180))
# conts
IDLE = 0
RUNNING = 1
MOVE_SPEED = 200 # 100 px
ATTACK_STATE = 2
GAME_OVER = False
BOUNDS_X = (66,1214)
BOUNDS_Y = (50,620)

# get path of assest folder using os module
# load sprite sheet for idle then for running as well
assetsDir = os.path.join(os.path.dirname(__file__),'assets')
idle_sprite_sheet_path = os.path.join(assetsDir, "Punk_idle.png");
running_sprite_sheet_path = os.path.join(assetsDir, "Punk_run.png");
refriegator_idle_sprite_sheet_path = os.path.join(assetsDir, "enemy_idle.png");
refriegator_hungry_sprite_sheet_path = os.path.join(assetsDir, "enemy_hungry.png");
idle_sprite_sheet= pygame.image.load(idle_sprite_sheet_path).convert_alpha()
running_sprite_sheet = pygame.image.load(running_sprite_sheet_path).convert_alpha()
refriegator_idle_sprite_sheet = pygame.image.load(refriegator_idle_sprite_sheet_path).convert_alpha()
refriegator_hungry_sprite_sheet = pygame.image.load(refriegator_hungry_sprite_sheet_path).convert_alpha()

background_path = os.path.join(assetsDir, "background.png");
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (320,180))


# define frame properties
idle_frame_width = idle_sprite_sheet.get_width() // 4
idle_frame_height = idle_sprite_sheet.get_height()
frames = []
total_frames = 4

running_frame_width = running_sprite_sheet.get_width() // 6
running_frame_height = running_sprite_sheet.get_height()
running_frames = []
running_total_frames = 6

refriegator_idle_frame_width = refriegator_idle_sprite_sheet.get_width() // 6
refriegator_idle_frame_height = refriegator_idle_sprite_sheet.get_height()
refriegator_idle_frames = []
refriegator_idle_total_frames = 6

refriegator_hungry_frame_width = refriegator_idle_sprite_sheet.get_width() // 6
refriegator_hungry_frame_height = refriegator_idle_sprite_sheet.get_height()
refriegator_hungry_frames = []
refriegator_hungry_total_frames = 6
# extract frames
# extract running frames
for i in range(total_frames):
    frame = idle_sprite_sheet.subsurface((i * idle_frame_width, 0, idle_frame_width, idle_frame_height))
    frames.append(frame)

for i in range(running_total_frames):
    run_frame = running_sprite_sheet.subsurface((i * running_frame_width, 0, running_frame_width, running_frame_height))
    running_frames.append(run_frame)

for i in range(refriegator_idle_total_frames):
    refriegator_idle_frame = refriegator_idle_sprite_sheet.subsurface((i * refriegator_idle_frame_width, 0, refriegator_idle_frame_width, refriegator_idle_frame_height))
    refriegator_idle_frames.append(refriegator_idle_frame)
    refriegator_hungry_frame = refriegator_hungry_sprite_sheet.subsurface((i * refriegator_hungry_frame_width, 0, refriegator_hungry_frame_width, refriegator_hungry_frame_height))
    refriegator_hungry_frames.append(refriegator_hungry_frame)


# create sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 10
        self.max_Health = 10
        self.idle_images = frames
        self.running_images = running_frames
        self.frames = self.idle_images
        self.current_frame = 0
        self.rect = self.frames[0].get_rect()
        self.animation_speed = 0.1
        self.frame_time = 0
        self.state = IDLE
        self.pos = [320/2, 180/2]
        # stores food in inventory
        self.food = 0
        # stores amount of food
        
    def update(self, delta_time, is_running):
        # update th fame based on animation speed
        self.pos[0] = max(BOUNDS_X[0], min(self.pos[0], BOUNDS_X[1] - 32))
        self.pos[1] = max(BOUNDS_Y[0], min(self.pos[1], BOUNDS_Y[1] - 32))
        self.frame_time += delta_time
        self.rect.center = (self.pos[0] + 10, self.pos[1] + 25)
        self.rect = self.frames[0].get_rect(center = self.rect.center)
        
        new_state = RUNNING if is_running else IDLE
        if new_state != self.state:
            self.state = new_state
            self.current_frame = 0
            self.frames =self.running_images if is_running else self.idle_images
        
        if len(self.frames) > 0:
            if self.frame_time >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.frame_time = 0

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], self.pos)
    def get_center(self):
        return  self.pos[0] + self.rect.width /2, self.pos[1] + self.rect.height /2
class Collectible(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def update(self):

        pass
collectibles_group = pygame.sprite.Group()
print(len(refriegator_idle_frames))
class Enemy(pygame.sprite.Sprite):
    # refrigertors have predifened spawn points
    def __init__(self, x,y ):
        super().__init__()
        self.idle_images = refriegator_idle_frames
        self.hungry_images = refriegator_hungry_frames
        self.frames = self.idle_images
        self.current_frame = 0
        self.rect = self.frames[0].get_rect()
        self.animation_speed = 0.1
        self.frame_time = 0
        self.state = IDLE
        self.pos = [x,y]
        # 10 seconds before it gets hungry
        self.hungry = 10000
        self.init_time = pygame.time.get_ticks()
    def update(self, delta_time):
        # update th fame based on animation speed
        current_time = pygame.time.get_ticks()
        if(current_time - self.init_time >= self.hungry):
            self.state = ATTACK_STATE
            self.frames = self.hungry_images
        self.frame_time += delta_time
        self.rect.center = (self.pos[0] + 17 , self.pos[1] + 15)
        self.rect = self.frames[0].get_rect(center = self.rect.center)
        
        if len(self.frames) > 0:
            if self.frame_time >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.frame_time = 0
        if self.state == ATTACK_STATE:
            player_center = player.get_center()
            enemey_center = self.get_center()
            self.velocity = [player_center[0] - enemey_center[0], player_center[1] - enemey_center[1]]
        # normalize velocity
            magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
            self.velocity = [self.velocity[0] / magnitude * 2 ,self.velocity[1] / magnitude * 2 ]
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]
    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], self.pos)
    def get_center(self):
        return  self.pos[0] + self.rect.width /2, self.pos[1] + self.rect.height /2
    def deposited_coin(self):
        self.init_time = pygame.time.get_ticks()
enemies_group = pygame.sprite.Group()


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True

def coin_spawner():
    while True:
        for i in range(120):
            yield

        x = random.randint(0, 1280 - 200)
        y = random.randint(0,720 - 200)
        collectible = Collectible(x,y)
        collectibles_group.add(collectible)
        all_sprites.add(collectibles_group)
        
def enemy_spawner():
    while True:
        for i in range(150):
            yield
        x = random.randint(0, 1280 - 500)
        y = random.randint(0,720 - 500)
        enemy = Enemy(x,y)
        player_center = player.get_center()
        while abs(player_center[0] - enemy.pos[0]) < 250 and abs(player_center[1] - enemy.pos[1]) < 250:
            enemy.pos[0] = random.randint(0, 1280 - 500) 
            enemy.pos[1] = random.randint(0, 720 - 500) 
        enemies_group.add(enemy)
        all_sprites.add(enemies_group)

spawner = enemy_spawner()
spawner_coin = coin_spawner()
score = 0
def display_ui(screen):
    for i in range(player.max_Health):
        healthImg = pygame.image.load("assets/emptyHeart.png" if i >= player.health else "assets/fullHeart.png")
        screen.blit(healthImg, (i * 32 + 320 - player.max_Health * 16, 16))

    

    display_tut = TEXT_FONT.render('Press e to deposit food to robots', True, "BLACK")

    score_text = TEXT_FONT.render(f'Score: {score}', True, "BLACK")
    screen.blit(score_text, (score_text.get_width() / 2, 16))
    screen.blit(display_tut, (1280 - 700 / 2, 16))
    
def update_screen():
    pygame.display.flip()
    clock.tick(60)

while running:
    delta_time = clock.get_time() / 1000.0

    do_damage = pygame.sprite.spritecollide(player, enemies_group, False)
    #start polling for events
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and do_damage:
            if player.food > 0:
                for enemy in do_damage:
                    if(enemy.state == IDLE):
                        enemy.deposited_coin()
                        score += 1
                        player.food -= 1

    keys = pygame.key.get_pressed()
    is_running = False
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.pos[1] -= MOVE_SPEED / 60
        is_running = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.pos[1] += MOVE_SPEED / 60
        is_running = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.pos[0] -= MOVE_SPEED / 60
        is_running = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.pos[0] += MOVE_SPEED / 60
        is_running = True


    # update the sprite
    player.update(delta_time, is_running)
    collectibles_group.update()
    collected_items = pygame.sprite.spritecollide(player, collectibles_group, True)
    if collected_items:
        player.food += len(collected_items)
    for enemy in do_damage:
        if enemy.state == ATTACK_STATE:
            player.health -= 1
    game_surface.blit(background, (0,0))

    # scales rendered game surface to 1280,720
    scaled_surface = pygame.transform.scale(game_surface,(1280,720))

    #render game here
    # we then blit to that surface
    if GAME_OVER:
        score_text = TEXT_FONT.render('GAME OVER', True, "BLACK")
        screen.blit(score_text, ( 1280/ 2, 720/2))
        update_screen()
        continue
    if player.health <= 0:
        if not GAME_OVER:
            GAME_OVER = True
    collectibles_group.draw(scaled_surface)
    #if do_damage:
    #    print("colliding with enemy")
    next(spawner)
    next(spawner_coin)
    # checks enemies that have collided with us
    for enemy in do_damage:
        if(enemy.state != IDLE):
            # deletes enemy if HUNGRY
            enemy.kill()
    for enemy in enemies_group:
        enemy.update(delta_time)
        enemy.draw(scaled_surface)


    player.draw(scaled_surface)
    display_ui(scaled_surface)
    # blit the scaled surface to the screen
    screen.blit(scaled_surface, (0,0))

    update_screen()

pygame.quit()

