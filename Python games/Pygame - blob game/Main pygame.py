import os, pygame, sys
from time import sleep
from pygame.locals import *
from pygame.compat import geterror
import random

class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Queue():              # FIFO - First In First Out
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __iter__(self):
	    current = self.head
	    while current != None:
		    yield current
		    current = current.next

    def __len__(self):
	    print(self.size)

    def show(self):
        current = self.head
        lst = []
        while current != None:
            lst.append(current.data)
            current = current.next
        print("front(head) <- {} <- rear(tail)".format(lst))

    def add(self, item):
        """Adds to the rear"""
        temp = Node(item)
        self.size += 1

        if self.head == None: # if queue was empty
            self.head = temp
            self.tail = temp
        else:
            self.tail.next = temp
            temp.prev = self.tail
            self.tail = temp

    def pop_head(self):
        """Removes the item in the front"""
        current = self.head
        self.head = current.next
        self.size -= 1

        return current

    def remove(self, node):
        """removes an arbitrary node from the queue"""
        current = node

        if self.size == 1:
        	self.head = None
        	self.tail = None

        elif self.head == node:
        	self.pop_head()

        elif self.tail == node:
        	self.tail = current.prev
        	current.prev.next = None
        else:
	        current.prev.next = current.next

def testing_queue():
	q = Queue()
	for i in range(1, 5):
		q.add(i)
	q.show()
	q.pop_head()
	q.show()
	q.remove(q.head.next)
	q.show()
	q.add(9)
	q.show()
	q.add(16)
	q.show()
	q.remove(q.tail.prev)
	q.show()

	print(q.head.next.data)

def load_image(name, data_dir='C:/USERS/sebastian/desktop/Images/', subfolder='', transparent=False):
	fullname = os.path.join(data_dir + subfolder, name)
	image = pygame.image.load(fullname)

	try:
		image = pygame.image.load(fullname)
	except pygame.error:
		print('Could not load image:', fullname)

	if transparent:
		return image.convert_alpha()
	else:
		return image

def load_sound(name):
	class NoneSound:
		def play(self): pass

	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join(data_dir, name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error:
		print('Cannot load sound: %s' % fullname)
		return  # raise SystemExit(str(geterror()))
	return sound


# Load Images And Tiles
fire_img = load_image('fire.png')
blood_img = load_image('blood.png')
textures = ['GRASS', 'WATER', 'DIRT']
weights  = [0.7, 0.25, 0.8]
tiles = {
	'GRASS' : load_image('grass.png'),
	'WATER' : load_image('water.png'),
	'DIRT'  : load_image('dirt.png')
	}
tile_values = {
	'WATER' : 0,
	'GRASS': 1,
	'DIRT' : 2
	}

dragon_ani = {f'{direction}{i}': load_image(f'{direction}{i}.png', subfolder='WarGame/dragon')
              for i in range(10) for direction in ('left', 'right')}

heroes = {
	"sheep" : {'right' : load_image('sheep_right.png'), 'left' : load_image('sheep_left.png')},
	"human" : ...
	}


class Board:
	def __init__(self, screen, size=20):
		self.size = size
		self.screen = screen

		# Screen is the variable name of the surface to initialize board on
		self.board, self.grid = self.init_board()

	def init_board(self):
		"""Returns a randomly generated list of images of tiles, as well as the grid"""
		#Generates random tiles based on weights
		texture_lst = [random.choices(textures, weights, k=self.size) for r in range(self.size)]
		#Grid used for handling backend stuff - invisible for the player
		grid = [[tile_values[tile] for tile in texture_lst[r]] for r in range(self.size)]
		#Used to store surfaces instead of the texture name, to increase performance when displaying board
		board = [[tiles[texture] for texture in texture_lst[r]] for r in range(self.size)]

		return board, grid

	def show_board(self):
		"""Blits each tile from 'self.board' to the screen"""
		for r in range(self.size):
			for c in range(self.size):
				self.screen.blit(self.board[r][c], (c*20, r*20))

	def get_grid(self):
		return self.grid

	def grid_swap(self, x1,y1, x2,y2):
		#print('swap:', x1,y1, x2,y2)
		temp = self.grid[y2][x2]
		self.grid[y2][x2] = self.grid[y1][x1]
		self.grid[y1][x1] = temp

	def grid_place(self, x,y, val):
		self.grid[y][x] = val

	def get_adjecent_tiles(self, x,y):  #TEST fjender kan flytte udenfor brættet, sæt rule for at y og x ikke kan være over max size eller under 0
		"""Returns a gen that randomly returns the 4 adjecent tile values"""
		coords = [(0,-1), (-1,0), (0,1), (1,0)]
		random.shuffle(coords)
		for a,b in coords:
			try:
				yield self.grid[a + y][b + x], b+x, a+y
			except IndexError:
				continue

	def place_val_on_grid(self, x,y, val):
		self.grid[y][x] = val

class Blob:
	def __init__(self, x=None, y=None, auto_spawn=True):
		self.image = {'right' : load_image('blob_right.png'), 'left' : load_image('blob_left.png')}
		self.direction = 'left'
		self.speed = 1
		self.x = x
		self.y = y
		if auto_spawn:
			self.auto_spawn()

	def auto_spawn(self, area=5):
		"""Finds the first free tile in the area**2 in the down right corner"""
		grid = board.get_grid()
		for r in range(-1, -1*(area+1), -1):
			for i in range(-1, -1*(area+1), -1):
				if type(grid[r][i]) == int and grid[r][i] > 0:
					# Add board.size since we don't want negative coords
					self.spawn(i + board.size, r + board.size)
					return

	def spawn(self, x, y):
		"""Spawns """
		self.x = x
		self.y = y
		board.place_val_on_grid(x,y, val=-8)
		self.blit()

	def blit(self):
		screen.blit(self.image[self.direction], (self.x * board.size, self.y * board.size))

	def move(self):
		"""Randomly moves to a free tile"""
		gen = board.get_adjecent_tiles(self.x, self.y)

		for _ in range(4):
			try:
				val, x,y = next(gen)
			except StopIteration:
				return  # No avaialable tiles

			if type(val) == int and val > 0:
				# swap around the two values
				board.grid_swap(self.x,self.y, x,y)
				# update coordinates
				self.x = x
				self.y = y

class Dragon:
	def __init__(self, x=None, y=None, direction='left'):
		#self.image = {'left' : load_image('dragon.png'), 'right' : load_image('dragon 2.png')}
		self.speed = 1
		self.direction = direction
		self.ani_gen = self.animation()
		self.x = x
		self.y = y
		self.spawn()

	def spawn(self):
		"""Spawns """
		board.place_val_on_grid(self.x,self.y, val=-7)
		self.blit()

	def blit(self):
		screen.blit(next(self.ani_gen), (self.x * board.size, self.y * board.size))


	def animation(self):
		"""Gets the next picture in the dragon animation"""
		while True:
			for i in range(10):
				yield dragon_ani[self.direction + str(i)]

	def move(self):
		"""Randomly moves to a free tile"""
		gen = board.get_adjecent_tiles(self.x, self.y)

		for _ in range(4):
			try:
				val, x,y = next(gen)
			except StopIteration:
				return  # No available tiles

			if type(val) == int and val > -5:

				# Swap Around The Two Values
				board.grid_swap(self.x,self.y, x,y)

				# Update Direction
				if (self.direction == 'left') and (self.x - x == -1):
					self.direction = 'right'
				elif (self.direction == 'right') and (self.x - x == 1):
					self.direction = 'left'

				# Update Coordinates
				self.x = x
				self.y = y

class Shoot_Fire:
	def __init__(self, x, y, direction):
		self.image = fire_img
		self.direction = direction
		self.x = x
		self.y = y
		self.move()

	def blit(self):
		screen.blit(fire_img, (self.x * board.size, self.y * board.size))

	def move(self):
		if self.direction == 'right':
			self.x += 1
		elif self.direction == 'left':
			self.x -= 1

		if self.check_expired():
			if self.direction == 'right':
				fire_right.pop_head()
			else:
				fire_left.pop_head()
		else:
			self.blit()

	def check_expired(self):
		if 0 <= self.x < board.size:
			return False
		else:
			return True

def available_terrain(x,y):
	if (0 > y) or (y >= board.size) or (0 > x) or (x >= board.size):
		return False

	if board.get_grid()[y][x] == 0:
		return False
	else:
		return True

def main():
#Initialize Game
	fpsClock = pygame.time.Clock()
	pygame.init()
	pygame.font.init()
	global screen
	screen = pygame.display.set_mode((400, 400))
	global board
	board = Board(screen)

#Initialize Fonts
	comic30 = pygame.font.SysFont('Comic Sans MS', 45)
	GameOver = comic30.render('Game Over', True, (255,0,0))

#Initialize hero
	chosen_hero = heroes['sheep']
	direction = 'right'
	# Screen Coords
	hero_x = 40
	hero_y = 40
	# Grid Coords
	grid_x = 2
	grid_y = 2

#Initialize FireBalls
	fireballs = []
	global fire_right
	global fire_left
	fire_right = Queue()
	fire_left = Queue()


#Initialize Foes
	foes = [Blob() for i in range(3)]
	foeSpeed = 20
	time = 1

	dragon = Dragon(8, 8)

#Show Board and hero
	board.show_board()
	screen.blit(chosen_hero[direction], (40,40))
	pygame.display.update()

	run = True
	while run:
		if time == 19:###############################
			for i in board.get_grid():
				print(*i)
			else:
				exit()
		#######################
		fpsClock.tick(10)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					if available_terrain(grid_x, grid_y-1):
						hero_y -= 20
						grid_y -= 1
				elif event.key == pygame.K_s:
					if available_terrain(grid_x, grid_y+1):
						hero_y += 20
						grid_y += 1
				elif event.key == pygame.K_a:
					direction = 'left'
					if available_terrain(grid_x-1, grid_y):
						hero_x -= 20
						grid_x -= 1
				elif event.key == pygame.K_d:
					direction = 'right'
					if available_terrain(grid_x+1, grid_y):
						hero_x += 20
						grid_x += 1
				if event.key == pygame.K_SPACE:
					if direction == 'right':
						fire_right.add(Shoot_Fire(grid_x, grid_y, 'right'))
					else:
						fire_left.add(Shoot_Fire(grid_x, grid_y, 'left'))


		# Update Board    ##
		board.show_board()

		# Update Hero     ##
		screen.blit(chosen_hero[direction], (hero_x, hero_y))

		# Update Dragon   ##
		if time % 2 == 0 and time < 10:
			dragon.move()
			dragon.blit()
		else:dragon.blit()

		# Update Fireball ##
		for fire in fire_right:
			fire.data.move()
			# Hvis den rammer en blob
			for i in range(len(foes)-1, -1, -1):
				if foes[i].y == fire.data.y and foes[i].x == fire.data.x:
					screen.blit(blood_img, (fire.data.x * board.size, fire.data.y * board.size))
					del foes[i]
					fire_right.remove(fire)
			if dragon.x == fire.data.x and dragon.y == fire.data.y:
				screen.blit(blood_img, (fire.data.x * board.size, fire.data.y * board.size))
				del dragon
				fire_right.remove(fire)


		for fire in fire_left:
			fire.data.move()
			for i in range(len(foes)-1, -1, -1):
				if foes[i].y == fire.data.y and foes[i].x == fire.data.x:
					screen.blit(blood_img, (fire.data.x * board.size, fire.data.y * board.size))
					del foes[i]
					fire_left.remove(fire)
			if dragon.x == fire.data.x and dragon.y == fire.data.y:
				screen.blit(blood_img, (fire.data.x * board.size, fire.data.y * board.size))
				del dragon
				fire_right.remove(fire)




		# Check If Hero Moves Into A Foe   ##
		# Blobs
		for foe in foes:
			if foe.x == grid_x and foe.y == grid_y:
				[foe.blit() for foe in foes]
				screen.blit(chosen_hero[direction], (hero_x, hero_y))
				screen.blit(GameOver, (100, 150))
				pygame.display.update()
				sleep(10)
		# Dragons
		if dragon.x == grid_x and dragon.y == grid_y:
			screen.blit(chosen_hero[direction], (hero_x, hero_y))
			screen.blit(GameOver, (100, 150))
			pygame.display.update()
			sleep(10)

		# Update Foes     ##
		if time == 1 or time == 3:
			[foe.move() for foe in foes]
			time = foeSpeed
		time -= 1

		[foe.blit() for foe in foes]

		# Display Updates ##
		pygame.display.update()





if __name__ == '__main__':
	main()




