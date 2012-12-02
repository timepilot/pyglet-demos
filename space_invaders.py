import pyglet
from pyglet.window import key
import random
from pyglet.gl import *
import rabbyt
import math
from rabbyt import lerp, wrap

#Space Invaders like demo, still in the early stages but the basic mechanics are there
#need better shooting code


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
		rabbyt.Sprite.__init__(self,None,shape=(-5,5,5,-5))
		self.x = x
		self.y = y
		self.rgb = (1,0,0)
		#normalize vector for direction
		self.vector = Vector2D(vector[0],vector[1],vector[2])
		self.acceleration = 0
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

class Player(rabbyt.Sprite):
	def __init__(self,x,y,vector):
		rabbyt.Sprite.__init__(self,None,shape=(-20,10,20,-10))
		self.x = x
		self.y = y
		#normalize vector for direction
		self.vector = Vector2D(vector[0],vector[1],vector[2])
		self.acceleration = 0
		self.shooting = False
		self.mousex=0
		self.mousey=0
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
		

		

class Bullet(rabbyt.Sprite):
	def __init__(self,x,y,vector):
		rabbyt.Sprite.__init__(self,None,shape=(-2,2,2,-2))
		self.x = x
		self.y = y
		#normalize vector for direction
		self.vector = Vector2D(vector[0],vector[1],vector[2])
		self.acceleration = 50
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
		self.vector.speed += self.acceleration*dt	
	#def trajectory(self):
		
bullets = []
points = []
def make_enemies(dt):
	x=200
	y=790
	for i in range(0,50):
		points.append(unit(x=x,y=y,vector=[0,-1,10]))
		x+=11
		

make_enemies(5)	
player = Player(x=600,y=50,vector=[1,0,450])

def make_bullets(dt):
	if player.shooting==True:
		bullets.append(Bullet(x=player.x,y=player.y,vector=[player.mousex-player.x,player.mousey-player.y,100]))


#where all the changes happen
def update(dt):
	collisions = rabbyt.collisions.aabb_collide_groups(points,bullets)
	for group in collisions:
		for s in group:
			if s in bullets:
				bullets.remove(s)
			if s in points:
				points.remove(s)
	for i in points:
		i.update(dt)
	if len(bullets)>0:
		for i in bullets:
			i.update(dt)
	player.update(dt)





pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(make_enemies,5.0)
pyglet.clock.schedule_interval(make_bullets,1/20.0)

#draws everything
@window.event
def on_draw():
	window.clear()
	fps_display.draw()
	rabbyt.render_unsorted(points)
	if len(bullets)>0:
		rabbyt.render_unsorted(bullets)
	player.render()
	

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
			player.shooting = True
			player.mousex=x
			player.mousey=y
@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
			player.shooting = False

	
@window.event
def on_key_press(symbol,modifiers):
	if symbol == key.ESCAPE:
		exit()
	if symbol == key.A:
		player.vector.dx = -1
		player.vector.dy = 0
		player.vector.speed = 350
		player.vector.update()
	if symbol == key.D:
		player.vector.dx = 1
		player.vector.dy = 0
		player.vector.speed = 350
		player.vector.update()
		

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.A:
        player.vector.speed = 25
    elif symbol == key.D:
        player.vector.speed = 25
pyglet.app.run()
