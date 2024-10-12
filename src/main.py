import pygame
import os

# init pygame
pygame.init()
screen = pygame.display.set_mode((320,180))
clock = pygame.time.Clock()
# conts
IDLE = 0
RUNNING = 1
MOVE_SPEED = 100 # 100 px

# get path of assest folder using os module
# load sprite sheet for idle then for running as well
assetsDir = os.path.join(os.path.dirname(__file__),'assets')
idle_sprite_sheet_path = os.path.join(assetsDir, "Punk_idle.png");
running_sprite_sheet_path = os.path.join(assetsDir, "Punk_run.png");
idle_sprite_sheet= pygame.image.load(idle_sprite_sheet_path).convert_alpha()
running_sprite_sheet = pygame.image.load(running_sprite_sheet_path).convert_alpha()


# define frame properties
idle_frame_width = idle_sprite_sheet.get_width() // 4
idle_frame_height = idle_sprite_sheet.get_height()

running_frame_width = running_sprite_sheet.get_width() // 6
running_frame_height = running_sprite_sheet.get_height()
running_total_frames = 6
# extract frames
frames = []
total_frames = 4
# extract running frames
running_frames = []
for i in range(total_frames):
    frame = idle_sprite_sheet.subsurface((i * idle_frame_width, 0, idle_frame_width, idle_frame_height))
    frames.append(frame)

for i in range(running_total_frames):
    run_frame = running_sprite_sheet.subsurface((i * running_frame_width, 0, running_frame_width, running_frame_height))
    running_frames.append(run_frame)

# create sprite class
class AnimatedSprite:
    def __init__(self, frames, running_frames):
        super().__init__()
        self.idle_images = frames
        self.running_images = running_frames
        self.frames = self.idle_images
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_time = 0
        self.state = IDLE
        self.pos = [320/2, 180/2]
    def update(self, delta_time, is_running):
        # update th fame based on animation speed
        self.frame_time += delta_time
        
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

sprite = AnimatedSprite(frames,running_frames)
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
        sprite.pos[1] -= MOVE_SPEED / 60
        is_running = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        sprite.pos[1] += MOVE_SPEED / 60
        is_running = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sprite.pos[0] -= MOVE_SPEED / 60
        is_running = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sprite.pos[0] += MOVE_SPEED / 60
        is_running = True

    # update the sprite
    sprite.update(delta_time, is_running)

    screen.fill("black")

    #render game here
    sprite.draw(screen)

    pygame.display.flip()

    clock.tick(60)


pygame.quit()

