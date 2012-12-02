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
for i in range(0,50):
	points.append(unit(x=random.randint(1,1000),y=random.randint(1,700),vector=[random.randint(0,359)*(math.pi/180),100]))

	

def elastic(one,two):
	xdist = max(one.x,two.x)-min(one.x,two.x)
	ydist = max(one.y,two.y)-min(one.y,two.y)
	#print xdist,ydist, "x,y distance"
	if xdist==0:
		collision_angle = 0
	else:
		collision_angle = math.atan(ydist/xdist)
	#print collision_angle,"radians"
	onex_speed=one.vector[1]*math.cos(one.vector[0])
	oney_speed=one.vector[1]*math.sin(one.vector[0])
	twox_speed=two.vector[1]*math.cos(two.vector[0])
	twoy_speed=two.vector[1]*math.sin(two.vector[0])
	#rounding errors for the super tiny flaots that fuck everything
	onex_speed,oney_speed,twox_speed,twoy_speed = round(onex_speed),round(oney_speed),round(twox_speed),round(twoy_speed)
	#print onex_speed,oney_speed,twox_speed,twoy_speed,"1:x,y 2:x,y speeds"
	#object 1 final dx,dy
	one_finalx = math.cos(collision_angle)*twox_speed+math.cos(collision_angle+math.pi/2)*twoy_speed
	one_finaly = math.sin(collision_angle)*twox_speed+math.sin(collision_angle+math.pi/2)*twoy_speed
	#object 2 final dx,dy
	two_finalx = math.cos(collision_angle)*onex_speed+math.cos(collision_angle+math.pi/2)*oney_speed
	two_finaly = math.sin(collision_angle)*onex_speed+math.sin(collision_angle+math.pi/2)*oney_speed
	one_finalx,one_finaly,two_finalx,two_finaly = round(one_finalx),round(one_finaly),round(two_finalx),round(two_finaly)
	#print one_finalx,one_finaly,two_finalx,two_finaly,"1:x,y 2:x,y Final speeds"
	#print one.vector,two.vector, "initial vectors"
	#90 degree special cases
	if one_finaly == 0.0:
		if one_finalx < 0:
			new_vector_one = [math.pi,abs(one_finalx)]
		else:
			new_vector_one = [0,one_finalx]
	if two_finaly == 0:
		if two_finalx < 0:
			new_vector_two = [math.pi,abs(two_finalx)]
		else:
			new_vector_two = [0,two_finalx]
	#for up and down
	if one_finalx == 0:
		if one_finaly < 0:
			new_vector_one = [3*math.pi/2,abs(one_finaly)]
		else:
			new_vector_one = [math.pi/2,one_finaly]
	if two_finalx == 0:
		if two_finaly < 0:
			new_vector_two = [3*math.pi/2,abs(two_finaly)]
		else:
			new_vector_two = [math.pi/2,two_finaly]
			
	if 0 not in [one_finaly,one_finalx,two_finalx,two_finaly]:
		new_vector_one = [math.atan(one_finaly/one_finalx),math.sqrt(one_finalx**2+one_finaly**2)]
		new_vector_two =  [math.atan(two_finaly/two_finalx),math.sqrt(two_finalx**2+two_finaly**2)]
	#print new_vector_one,new_vector_two,"new vectors"
	return [new_vector_one,new_vector_two]


#where all the changes happen
def update(dt):

	collisions = rabbyt.collisions.brute_force(points)
	for group in collisions:
		try:
			new_vectors = elastic(group[0],group[1])
			group[0].rgb = lerp((0,1,0),(1,1,1), dt=.4)
			group[1].rgb = lerp((0,1,0),(1,1,1), dt=.4)
			group[0].vector = new_vectors[0]
			group[1].vector = new_vectors[1]
		except UnboundLocalError:
			if group[0].y > group[1].y:
				group[0].y += 2
				group[1].y -= 2
			else:
				group[1].y += 2
				group[0].y -= 2
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
