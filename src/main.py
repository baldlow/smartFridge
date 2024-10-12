import pygame
import os
import random

# init pygame
pygame.init()
#screen = pygame.display.set_mode((320,180))
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_surface = pygame.Surface((320,180))
# conts
IDLE = 0
RUNNING = 1
MOVE_SPEED = 200 # 100 px

# get path of assest folder using os module
# load sprite sheet for idle then for running as well
assetsDir = os.path.join(os.path.dirname(__file__),'assets')
idle_sprite_sheet_path = os.path.join(assetsDir, "Punk_idle.png");
running_sprite_sheet_path = os.path.join(assetsDir, "Punk_run.png");
refriegator_idle_sprite_sheet_path = os.path.join(assetsDir, "enemy_idle.png");
idle_sprite_sheet= pygame.image.load(idle_sprite_sheet_path).convert_alpha()
running_sprite_sheet = pygame.image.load(running_sprite_sheet_path).convert_alpha()
refriegator_idle_sprite_sheet = pygame.image.load(refriegator_idle_sprite_sheet_path).convert_alpha()


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

# create sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_images = frames
        self.running_images = running_frames
        self.frames = self.idle_images
        self.current_frame = 0
        self.rect = self.frames[0].get_rect()
        self.animation_speed = 0.1
        self.frame_time = 0
        self.state = IDLE
        self.pos = [320/2, 180/2]
        
    def update(self, delta_time, is_running):
        # update th fame based on animation speed
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
        self.frames = self.idle_images
        self.current_frame = 0
        self.rect = self.frames[0].get_rect()
        self.animation_speed = 0.1
        self.frame_time = 0
        self.state = IDLE
        self.pos = [x,y]
    def update(self, delta_time):
        # update th fame based on animation speed
        self.frame_time += delta_time
        self.rect.center = (self.pos[0] + 10, self.pos[1] + 25)
        self.rect = self.frames[0].get_rect(center = self.rect.center)
        
        #new_state = RUNNING if is_running else IDLE
        #if new_state != self.state:
        #    self.state = new_state
        #    self.current_frame = 0
        #    self.frames =self.running_images if is_running else self.idle_images
        
        if len(self.frames) > 0:
            if self.frame_time >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.frame_time = 0
    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], self.pos)
enemies_group = pygame.sprite.Group()

for _ in range(5):
    x = random.randint(0,1280 - 20)
    y = random.randint(0,720 - 20)
    collectible = Collectible(x,y)
    collectibles_group.add(collectible)
for _ in range(5):
    x = random.randint(0, 1280 - 20)
    y = random.randint(0,720 - 20)
    enemy = Enemy(x,y)
    enemies_group.add(enemy)

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(collectibles_group)
all_sprites.add(enemies_group)
running = True


while running:
    delta_time = clock.get_time() / 1000.0

    #start polling for events
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
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
        print(f"Collected {len(collected_items)} collectibles(s)!")

    game_surface.fill((0,0,0))

    # scales rendered game surface to 1280,720
    scaled_surface = pygame.transform.scale(game_surface,(1280,720))

    #render game here
    #all_sprites.draw(scaled_surface)
    #sprite.draw(sruface)
    # we then blit to that surface
    collectibles_group.draw(scaled_surface)
    for enemy in enemies_group:
        enemy.update(delta_time)
        enemy.draw(scaled_surface)

    player.draw(scaled_surface)
    #pygame.draw.rect(scaled_surface, "RED",player.rect, 2)
    # figure out how to add enimeies
    pygame.draw.circle(scaled_surface, (255, 0, 0), (player.get_center()),5)
    # blit the scaled surface to the screen
    screen.blit(scaled_surface, (0,0))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()

