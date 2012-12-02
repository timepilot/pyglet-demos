#This work is licensed under a 
#Creative Commons Attribution-NonCommercial 2.5 License
#(the same as XKCD) so do whatever you want with it 
#as long as it stays free
#written by Marty S. (marty at geodex dot org) 
#

import pyglet
from pyglet.window import key
import random
from pyglet.gl import *
import population_model
#create a window
config = pyglet.gl.Config(resizable=True)
window = pyglet.window.Window(1200,800)

fps_display = pyglet.clock.ClockDisplay()
class rect():
	def __init__(self):	
		self.vertices = []
		self.colors = []
		self.list_exists = False
	def update(self):
		if self.list_exists == True:
			self.vertex_list.delete()
		self.vertex_list = batch.add(len(self.vertices)/2,pyglet.gl.GL_QUADS,None,
		('v2i', self.vertices),
		('c3B', self.colors)
		)
		self.list_exists = True
		self.colors = []
		self.vertices = []
	def add_quad(self,x1,y1,size_x,size_y,color):
		self.vertices += x1,y1,x1,y1 + size_y, x1 + size_x, y1 + size_y, x1 + size_x, y1
		self.colors += color*4
	def draw_list(self):
		self.vertex_list.draw(pyglet.gl.GL_QUADS)

class pop_model():
	def __init__(self):
		self.person_number = 1001
		self.day = 0
		self.time_scale = 10
		self.food_level = 100
		self.people = []
		for i in range(0,1000):
			self.people.append(population_model.Person('x' + str(i),random.randint(1,60),self.time_scale,self.food_level))
	def tick(self):
		for person in self.people:
			result = person.update()
			if result ==  True:
				self.people.append(population_model.Person('x' + str(self.person_number),1,self.time_scale,self.food_level))
				self.person_number+=1
			if person.dead == True:
				#print person.name, person.age,day
				del self.people[self.people.index(person)]

		if self.day % 365 == 0:
			print self.day/365,len(self.people),self.person_number - 1001

		self.day+=1*self.time_scale	
		
	

def color_gen():
	colors = []
	#for age tiles
	r = 4
	g = 255
	b = 240
	while g > 0:
		colors.append([r,g,b])
		if r < 255:
			r+=2
		else:
			r = 255
		g-=2
		if b > 0:
			b-=16
	return colors 	
	
	
	
batch = pyglet.graphics.Batch()
age_squares = rect()
colors = color_gen()

model = pop_model()






#where all the changes happen
def update(dt):

	return False





#draws everything
@window.event
def on_draw():
	window.clear()
	batch.draw()
	fps_display.draw()

pyglet.clock.schedule_interval(update,1/60.0)



	
@window.event
def on_key_press(symbol,modifiers):
	if symbol == key.ESCAPE:
		exit()
	if symbol == key.W:
		glShadeModel(GL_FLAT)
	if symbol == key.S:
		glShadeModel(GL_SMOOTH)
	else:
		print "a key was pressed"
	
pyglet.app.run()
