import pygame
import cmath
import math

WIDTH = 500
HEIGHT = 500
START_R = -2
END_R = 2
START_I = -2
END_I = 2
win = pygame.display.set_mode((WIDTH,HEIGHT))
run = True
clock = pygame.time.Clock()

points = []
total_dist = []


def pixel_to_complex(x,y):
	re = (x/WIDTH) * (END_R-START_R) - (END_R-START_R)/2
	im = (y/HEIGHT) * -1*(END_I-START_I) + (END_I-START_I)/2
	return (re, im)

def complex_to_pixel(re,im):
	x = (re+2)/4 * WIDTH
	y = (im-2)/(-4) * HEIGHT
	return (x,y)

def dist(a,b):
	x,y = a
	x1,y1 = b
	return math.sqrt((x1-x)**2 + (y1-y)**2)

t = 0
run = True
endpts = []
finished = False
drawing_path = True
path = []
path_length = 0

def calculate():
	global path_length
	path_length = 0
	for i in range(len(path)-1):
		x,y = path[i]
		x1,y1 = path[i+1]
		path_length += dist((x,y),(x1,y1))
	if len(path) > 0:
		x,y = path[len(path)-1]
		x1,y1 = path[0]
		path_length += dist((x,y),(x1,y1))
	
def f(t):
	t = round(t,2)
	target_dist = t * path_length
	seen_dist = 0
	for i in range(len(path)-1):
		x,y = path[i]
		x1,y1 = path[i+1]
		if seen_dist + dist((x,y),(x1,y1)) > target_dist:
			# seen_dist + X*dist = target_dist
			percent = (target_dist-seen_dist)/dist((x,y),(x1,y1))
			newX = x + percent*(x1-x)
			newY = y + percent*(y1-y)
			return pixel_to_complex(newX,newY)
		seen_dist += dist((x,y),(x1,y1))
	if len(path) > 0:
		x,y = path[len(path)-1]
		x1,y1 = path[0]
		if seen_dist + dist((x,y),(x1,y1)) > target_dist:
			percent = (target_dist-seen_dist)/dist((x,y),(x1,y1))
			newX = x + percent*(x1-x)
			newY = y + percent*(y1-y)
			return pixel_to_complex(newX,newY)


		
		
coefficients = []
def get_coefficients():
	global coefficients
	for n in range(-50,51,1):
		s = 0
		t = 0
		delta = 0.01
		while t < 1:
			a,b = f(t)
			s += cmath.exp(complex(0,-2*math.pi*n*t)) * complex(a,b) * delta
			t += delta
		coefficients.append([n,s])




def draw_path():
	global path
	if pygame.mouse.get_pressed()[0]:
		x,y = pygame.mouse.get_pos()
		path.append((x,y))
		calculate()

def draw():
	s = complex(0,0)
	for val in coefficients:
		n,z = val
		other = cmath.exp(complex(0,n*2*math.pi*t))
		s += z*other
	x,y = complex_to_pixel(s.real,s.imag)
	h = 0
	running_sum = coefficients[50+h][1]
	x,y = complex_to_pixel(running_sum.real,running_sum.imag)
	pygame.draw.line(win,(255,255,255),(250,250),(x,y),1)
	r = dist((x,y),(250,250))
	pygame.draw.circle(win,(255,255,255),(250,250),r,1)
	h += 1
	while h < 50:
		n,z = coefficients[50+h]
		running_sum += z*cmath.exp(complex(0,2*math.pi*t*n))
		x1,y1 = complex_to_pixel(running_sum.real,running_sum.imag)
		pygame.draw.line(win,(255,255,255),(x,y),(x1,y1),1)
		r = dist((x,y),(x1,y1))
		pygame.draw.circle(win,(255,255,255),(x,y),r,1)
		x,y = x1,y1
		n,z = coefficients[50-h]
		running_sum += z*cmath.exp(complex(0,2*math.pi*t*n))
		x1,y1 = complex_to_pixel(running_sum.real,running_sum.imag)
		pygame.draw.line(win,(255,255,255),(x,y),(x1,y1),1)
		r = dist((x,y),(x1,y1))
		pygame.draw.circle(win,(255,255,255),(x,y),r,1)
		x,y = x1,y1
		h += 1
		if h == 50 and not finished:
			endpts.append((x1,y1))
	for pt in range(len(endpts)-1):
		x,y = endpts[pt]
		x1,y1 = endpts[pt+1]
		pygame.draw.line(win,(255,0,255),(x,y),(x1,y1),1)



while run:
	clock.tick(60)
	win.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE and drawing_path:
				calculate()
				get_coefficients()
				drawing_path = False
	if t >= 1:
		t = 0
		finished = True

	if drawing_path:
		draw_path()
		for i in range(len(path)-1):
			x,y = path[i]
			x1,y1 = path[i+1]
			pygame.draw.line(win,(255,255,255),(x,y),(x1,y1),1)
		if len(path) > 0:
			x,y = path[len(path)-1]
			x1,y1 = path[0]
			pygame.draw.line(win,(255,255,255),(x,y),(x1,y1),1)
	else:
		draw()
		t += 0.001


	pygame.display.update()