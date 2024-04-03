from backend import current_map, Agent, Hider
from screens import menu_screen
import pygame


for i in range(len(current_map.hider_position)):
    hider = Hider(current_map.hider_position[i], 3, (current_map.num_rows, current_map.num_cols), current_map.map_array)
    hider.announce(5)

ANNOUNCE_RANGE = 3
SEEKER_VISION_RADIUS = 3
HIDER_VISION_RADIUS = 2
map_ratio = current_map.num_rows / current_map.num_cols

INFO_BAR = 70
HEIGHT = 500
WIDTH = HEIGHT / map_ratio
HEIGHT += INFO_BAR
block_edge = (HEIGHT - INFO_BAR) / current_map.num_rows

pygame.init()
screen = pygame.display.init()
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 27)
counter = 0
seeker_images = []
for i in range(1, 5):
	seeker_images.append(pygame.transform.scale(pygame.image.load(f'Assets/seeker_images/water{i}.png'), (block_edge, block_edge)))
hider_images = []
for i in range(1, 5):
	hider_images.append(pygame.transform.scale(pygame.image.load(f'Assets/hider_images/freefire{i}.png'), (block_edge, block_edge)))
wall_image = pygame.transform.scale(pygame.image.load('Assets/wall_images/ice.png'), (block_edge, block_edge))
obstacle_image = pygame.transform.scale(pygame.image.load('Assets/obstacle_images/bush.png'), (block_edge, block_edge))
announce_image = pygame.transform.scale(pygame.image.load('Assets/announce_images/sparkle.png'), (block_edge, block_edge))

def draw_board(current_map):
	for i in range(current_map.num_rows):
		for j in range(current_map.num_cols):
			top = j * block_edge
			left = INFO_BAR + i * block_edge

			pygame.draw.rect(screen, 'pink', (top, left, block_edge, block_edge), 1)

			if current_map.map_array[i][j] == 1:
				screen.blit(wall_image, (top, left))
			if current_map.map_array[i][j] == 2:
				draw_agent(i, j, False)
			if current_map.map_array[i][j] == 3:
				draw_agent(i, j, True)
			if current_map.map_array[i][j] == 4:
				screen.blit(obstacle_image, (top, left))
			if current_map.map_array[i][j] == 5:
				screen.blit(announce_image, (top, left))
		
def draw_agent(i, j, isSeeker):
	VISION_RADIUS = 0
	VISION_COLOR = 0
	top =  j * block_edge
	left = INFO_BAR + i * block_edge
	if isSeeker == True:
		screen.blit(seeker_images[counter // 10], (top, left))
		VISION_RADIUS = SEEKER_VISION_RADIUS
		VISION_COLOR = (0, 128, 255, 64)
	else:
		screen.blit(hider_images[counter // 10], (top, left))
		VISION_RADIUS = HIDER_VISION_RADIUS
		VISION_COLOR = (255, 128, 0, 64)
	#Draw vision
	agent = Agent((i, j), VISION_RADIUS, (current_map.num_rows, current_map.num_cols), current_map.map_array)
	agent.agent_valid_vision()
	for valid in agent.valid_vision:
		top_ = valid[1] * block_edge
		left_ = INFO_BAR + valid[0] * block_edge
		#Blending transparently
		s = pygame.Surface((block_edge, block_edge), pygame.SRCALPHA)
		s.fill(VISION_COLOR)
		screen.blit(s, (top_, left_))

level_map = []
running = True
while running:
	if len(level_map) == 0:
		menu_screen(font, level_map)
		if len(level_map) != 2:
			break

		pygame.display.quit()
		screen = pygame.display.set_mode([WIDTH, HEIGHT])
		pygame.display.set_caption("HideAndSeek")

	timer.tick(fps)
	if counter < 39:
		counter += 1
	else:
		counter = 0

	screen.fill((64, 64, 64))
	draw_board(current_map)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()

