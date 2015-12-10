import pygame, random, math
from sys import argv

background_colour = (255,255,255)
(width, height) = (800, 640)

left_edge = 0
right_edge = width
top_edge = 0
bottom_edge = height

def addVectors((angle1, length1), (angle2, length2)):
			x = math.sin(angle1)*length1+math.sin(angle2)*length2
			y = math.cos(angle1)*length1+math.cos(angle2)*length2
			
			length = math.hypot(x, y)
			angle = 0.5*math.pi-math.atan2(y, x)
			
			return (angle, length)

def findParticle(particles, x, y):
	for p in particles:
		if math.hypot(p.x-x, p.y-y) <= p.size:
			return p
	return None
			
def collide(p1, p2):
	distance = math.hypot((p1.x - p2.x), (p1.y - p2.y))
	
	if distance < p1.size + p2.size:
	
		tangent = math.atan2((p1.x - p2.x), (p1.y - p2.y))
		
		#angle between two particles - 90 degrees to the tangent
		angle = 0.5 * math.pi + tangent
		
		#get they're new angle of direction
		#note that the particle will reflect off the tangent where 
		#the particles meet, at an the same angle it hits the tangent at
		#that angle will be the angle of the tangent - the angle of direction
		#Once we know that we use trig to find its new angle of direction
		# that will be pi - (third angle in triangle created between circle 
		#vector and horizontal plane)
		angle1 = 2*tangent - p1.angle
		angle2 = 2*tangent - p2.angle
		
		#Then we need to exchange the speeds of the two particles as they 
		#transfer their energy to on another.
		#reduce particle energy after collision w/elasticity
		speed1 = p2.speed*elasticity
		speed2 = p1.speed*elasticity

		(p1.angle, p1.speed) = (angle1, speed1)
		(p2.angle, p2.speed) = (angle2, speed2)
		
		#now we seprate them by a distance of 1 pixel to make
		#sure theyre not overlapping - this will lead to them 
		#getting caught in an infinte loop where they constantly think 
		#theyre colliding off eachother
		overlap = 0.5*(p1.size + p2.size - dist+1)
		p1.x += overlap*math.sin(angle)
		p1.y -= overlap*math.cos(angle)
		p2.x -= overlap*math.sin(angle)
		p2.y += overlap*math.cos(angle)

		
		
class Particle:
	def __init__(self, (x, y), size, mass=1):
		self.x = x
		self.y = y
		self.size = size
		self.mass = mass

		self.colour = (0, 0, 255)
		self.thickness = 2
		self.speed = 0.01
		self.angle = 0
		
	def display(self):
		pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
	
	# This function will change the x, y coordinates of the particle
	# based on its speed and the angle of its movement.
	# angles are all in radians - 1 radians = 180/pi
	def move(self):
		self.x += (math.sin(self.angle) * self.speed)
		self.y -= (math.cos(self.angle) * self.speed)
		(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
		self.speed *= drag

	def edge_bounce(self):
		if self.x <= (left_edge + self.size):
			#turn and bounce back the to the right
			self.x = 2*self.size-self.x
			self.angle = -self.angle
			self.speed *= elasticity
			
		if self.x >= (right_edge - self.size):
			#turn and bounce back the to the left
			self.x = 2*(width-self.size)-self.x
			self.angle = -self.angle
			self.speed *= elasticity
			
		if self.y <= (top_edge + self.size):
			self.y = 2*self.size-self.y
			self.angle = math.pi-self.angle
			self.speed *= elasticity
			
		if self.y >= (bottom_edge - self.size):
			self.y = 2*(height - self.size)-self.y 
			self.angle = math.pi-self.angle
			self.speed *= elasticity
			
		def virtual_torus(self):
			pass
			#if self.x <= (left_edge + self.size):
			#come from the right edge
			#self.x = right_edge + (self.x-(width-self.size))
			
		
		
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')

script, no_o_cirk = argv
no_o_cirks = int(no_o_cirk)
my_particles = []


#creates blue(0,0,255) circle object centred at (150, 50) w/radius 15 & thickness of 1 pixel
#must be called after screen.fill(background_colour)
for n in range(no_o_cirks):
	size = random.randint(50, 75)
	x = random.randint(size, width - size)
	y = random.randint(size, height - size)
	
	my_random_particle = Particle((x, y), size)
	my_random_particle.speed = random.uniform(0, 0.001)
	my_random_particle.angle = random.uniform(0, math.pi*2)

	my_particles.append(my_random_particle)
	
gravity = (math.pi, 0.002)	
drag = 0.9999
elasticity = 0.80

selected_particle = None
last_particle = None

initX = 0
initY = 0
initMx = 0
initMy = 0

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_particle = findParticle(my_particles, mouseX, mouseY)
			
			if selected_particle:
				selected_particle.colour = (255,0,0)
				initX = selected_particle.x
				initY = selected_particle.y
				initMx = mouseX
				initMy = mouseY
		elif event.type == pygame.MOUSEBUTTONUP:
			if selected_particle:
				selected_particle.colour = (0,0,255)
			selected_particle = None
			
			
	if selected_particle:
		dist = math.sqrt( (initMx - initX)**2 + (initMy - initY)**2 )
		ang = math.atan2((initY - initMy), (initX - initMx))
		(mouseX, mouseY) = pygame.mouse.get_pos()
		#Make particle follow arrow with the centre = centre +dist @ angle
		selected_particle.x = mouseX + dist*math.cos(ang)
		selected_particle.y = mouseY + dist*math.sin(ang)
		selected_particle.angle = ang
		selected_particle.speed = dist*0.1
				
	screen.fill(background_colour)
	
	for i, my_random_particle in enumerate(my_particles):
	#enumerate(my_random_particle) = current particle index - n
		my_random_particle.move()
		my_random_particle.edge_bounce()
		#compare particle with all of the particles with index n+1
		#(prior particles will have already been compared)
		# by slicing list 
		for particle2 in my_particles[i+1:]:
			collide(my_random_particle, particle2)
		my_random_particle.display()
	pygame.display.flip()
