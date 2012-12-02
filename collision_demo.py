import pyglet
from pyglet.window import key
import random
from pyglet.gl import *
import rabbyt
import math
from rabbyt import lerp, wrap


#create a window
config = pyglet.gl.Config(resizable=True,depth_size=24)
window = pyglet.window.Window(1200,800,config=config)
glPointSize(6.0)

fps_display = pyglet.clock.ClockDisplay()
##changes tick/dt to rabbyt?
pyglet.clock.schedule(rabbyt.add_time)


class unit(rabbyt.Sprite):
	def __init__(self,x,y,direction,speed):
		rabbyt.Sprite.__init__(self,None,shape=(-2,2,2,-2))
		self.x = x
		self.y = y
		self.speed = speed
		self.acceleration = 5
		self.direction = direction
		self.x_dir = math.cos(self.direction)
		self.y_dir = math.sin(self.direction)
	def update(self,dt):
		if self.x > 1200 or self.x < 0:
			self.x_dir = -self.x_dir
			self.rgb = lerp((1,0,0),(1,1,1), dt=.4)
		if self.y > 800 or self.y < 0:
			self.y_dir = -self.y_dir
		#self.x_dir = math.cos(self.direction)
		#self.y_dir = math.sin(self.direction)		
		self.speed += self.acceleration*dt
		self.x = self.x + self.speed*self.x_dir*dt
		self.y = self.y + self.speed*self.y_dir*dt
points = []
for i in range(0,100):
	points.append(unit(x=random.randint(1,1000),y=random.randint(1,100),direction=2*math.pi/3,speed=10))
	
#where all the changes happen
def update(dt):
	collisions = rabbyt.collisions.aabb_collide(points)
	for group in collisions:
		for s in group:
			s.x_dir = -s.x_dir
			s.y_dir = -s.y_dir
			s.rgb = lerp((0,1,0),(1,1,1), dt=.4)
	for i in points:
		i.update(dt)
	return False



pyglet.clock.schedule(update)

#draws everything
@window.event
def on_draw():
	window.clear()
	fps_display.draw()
	rabbyt.render_unsorted(points)
	





	
@window.event
def on_key_press(symbol,modifiers):
	if symbol == key.ESCAPE:
		exit()

	
pyglet.app.run()
