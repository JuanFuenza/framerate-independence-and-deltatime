import pygame, time

# Init pygame
pygame.init()

# set display
WID = 800
HEI = 600
ds = pygame.display.set_mode((WID,HEI))

# set fps
clock = pygame.time.Clock()
fps = [60, 120, 200, 360, 600]
fps_index = 0

# test image with animation
class Test(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # animation
        self.frames = [pygame.image.load(f"assets/{i}.png").convert_alpha() for i in range(2)]
        self.frame_index = 0

        # images & rect
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midleft = (0,360))

        # movement
        self.rotation = 0
        self.direction = 1
        self.move_speed = 200
        self.animation_speed = 5
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def move(self, dt):
        self.pos.x += self.direction * self.move_speed * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right > 800 or self.rect.left < 0:
            self.direction *= -1

    def rotate(self, dt):
        self.rotation += 50 * dt
        self.image = pygame.transform.rotozoom(self.image, self.rotation,1)

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
        self.rotate(dt)

test_group = pygame.sprite.Group()
test_group.add(Test())

# font
font = pygame.font.SysFont("Arial", 18, bold = True)

# event to change fps
change_fps_event = pygame.USEREVENT + 1
pygame.time.set_timer(change_fps_event, 5000)

# texts
text = font.render("Framerate independence", True, (255, 255, 255))
text_rect = text.get_rect(center = (WID//2, 50))
descriptive_text = font.render("fps changes after 5 seconds", True, (255, 255, 255))
descriptive_text_rect = descriptive_text.get_rect(center = (WID//2, 100))

# functions
def fps_counter():
    """
    Display a fps counter on top left on the screen
    returns: None
    """
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, True, (255, 255, 255))
    ds.blit(fps_t, (0,0))

def game_time():
    current_time = pygame.time.get_ticks()//1000
    display_time = font.render(f"Time: {current_time}", True, (255, 255, 255))
    display_rect = display_time.get_rect(center = (WID//2, 150))
    ds.blit(display_time, display_rect)


# main game loop
prev_time = time.time()
running = True
while running:
    # fps cap
    clock.tick(fps[fps_index])
    # deltatime
    dt = time.time() - prev_time
    prev_time = time.time()

    # input event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # change fps to a given event
        if event.type == change_fps_event:
            if fps_index >= len(fps) - 1:
                fps_index = 0
            else:
                fps_index += 1

    # refresh screen
    ds.fill('black')
    
    # displays test, fps, texts and time
    test_group.update(dt)
    test_group.draw(ds)
    fps_counter()
    ds.blit(text, text_rect)
    ds.blit(descriptive_text, descriptive_text_rect)
    game_time()

    # update screen
    pygame.display.update()

pygame.quit()