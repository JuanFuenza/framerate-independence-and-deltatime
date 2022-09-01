import pygame, time

pygame.init()

ds = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

test_rect = pygame.Rect(0,310,100,100)
test_rect_pos = test_rect.x
test_speed = 200

previous_time = time.time()

running = True
while running:
    # dt = clock.tick(60) / 1000
    dt = time.time() - previous_time
    previous_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ds.fill('white')

    test_rect_pos += test_speed * dt
    test_rect.x = round(test_rect_pos)

    pygame.draw.rect(ds, 'red', test_rect)

    pygame.display.update()

pygame.quit()