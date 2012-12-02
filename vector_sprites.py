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
	def __init__(self,x,y,vector):
		rabbyt.Sprite.__init__(self,None,shape=(-2,2,2,-2))
		self.x = x
		self.y = y
		self.vector = vector
		self.acceleration = 5
	def update(self,dt):
		(angle,speed) = self.vector
		if self.x > 1200 or self.x < 0:
			self.vector = [180*(math.pi/180)-angle,speed]
			self.rgb = lerp((1,0,0),(1,1,1), dt=.4)
		if self.y > 800 or self.y < 0:
			self.vector = [-angle,speed]
			self.rgb = lerp((1,0,0),(1,1,1), dt=.4)
		(angle,speed) = self.vector
		self.x = self.x + speed*math.cos(angle)*dt
		self.y = self.y + speed*math.sin(angle)*dt
		
		
		
points = []
for i in range(0,100):
	points.append(unit(x=random.randint(1,1000),y=random.randint(1,700),vector=[random.randint(0,359)*(math.pi/180),100]))
	
#where all the changes happen
def update(dt):
	collisions = rabbyt.collisions.aabb_collide(points)
	for group in collisions:
		for i in group:
			print i
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
