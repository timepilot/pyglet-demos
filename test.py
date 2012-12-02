
#This work is licensed under a 
#Creative Commons Attribution-NonCommercial 2.5 License
#(the same as XKCD) so do whatever you want with it 
#as long as it stays free
#written by Marty S. (marty at geodex dot org) 
#
#test file is just a working file with whatever I happen to be working with at the time, may not run well
#or do anything
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


class Vector2D():
	def __init__(self,dx,dy,speed):
		self.dx = dx
		self.dy = dy
		self.speed = speed
		self.mag = self.magnitude(self.dx,self.dy)
		self.normalize()
	def normalize(self):
		self.norm_x,self.norm_y = [self.dx/self.mag,self.dy/self.mag]
	def magnitude(self,dx,dy):
		return math.sqrt((dx**2+dy**2))
	def towards(self,target_x,target_y,current_x,current_y):
		dx = target_x - current_x
		dy = target_y - current_y 
		direction_vector_mag = self.magnitude(dx,dy)
		#normalize the vector for a direction
		new_direction = [dx/direction_vector_mag,dy/direction_vector_mag]
		return new_direction
	
	def update(self):
		self.mag = self.magnitude(self.dx,self.dy)
		self.normalize()
	
class unit(rabbyt.Sprite):
	def __init__(self,x,y,vector):
		rabbyt.Sprite.__init__(self,None,shape=(-2,2,2,-2))
		self.x = x
		self.y = y
		#normalize vector for direction
		self.vector = Vector2D(vector[0],vector[1],vector[2])
		self.acceleration = 25
	def update(self,dt):
		#checks screen bounds and reflects
		if self.x > 1200 or self.x < 0:
			self.vector.norm_x = -self.vector.norm_x
			self.rgb = lerp((1,0,0),(1,1,1), dt=.4)
		if self.y > 800 or self.y < 0:
			self.vector.norm_y = -self.vector.norm_y
			self.rgb = lerp((1,0,0),(1,1,1), dt=.4)
			

		self.x = self.x + self.vector.speed*self.vector.norm_x*dt
		self.y = self.y + self.vector.speed*self.vector.norm_y*dt
		if self.vector.speed < 150:
			self.vector.speed += self.acceleration
	def go_to(self,x,y):
		new_vec = self.vector.towards(x,y,self.x,self.y)
		self.vector.norm_x = new_vec[0]
		self.vector.norm_y = new_vec[1]
		self.vector.speed = 50
		
points = []
for i in range(0,100):
	points.append(unit(x=random.randint(1,1000),y=random.randint(1,700),vector=[random.random(),1,200]))



#where all the changes happen
def update(dt):
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
