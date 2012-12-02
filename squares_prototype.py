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
squares = rect()
colors = color_gen()
	

ages = range(0,100)

for x in range(10,560,11):
	for y in range(10,790,11):
		squares.add_quad(x,y,10,10,random.choice(colors))


squares.update()
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
