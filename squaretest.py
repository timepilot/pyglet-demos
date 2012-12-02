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
	

class Entity(rect):
	def __init__(self,x1,y1,size_x,size_y,color):
		rect.__init__(self)
		self.x = x1
		self.y = y1
		self.size_x = size_x
		self.size_y = size_y
		self.color = color
		self.add_quad(x1,y1,size_x,size_y,color)
	def change(self,x=None,y=None,size_x=None,size_y=None,color=None):
		if x == None:
			x = self.x
		else:
			self.x = x
		if y == None:
			y = self.y
		else:
			self.y = y
		if size_x == None:
			size_x = self.size_x
		else:
			self.size_x = size_x
		if size_y == None:
			size_y = self.size_y
		else:
			self.size_y = size_y
		if color == None:
			color = self.color
		else:
			self.color = color
		self.add_quad(x,y,size_x,size_y,color)
		self.update()
	

		
		

colors = []
for r in range(0,255,3):
	colors.append((r,r,r))
batch = pyglet.graphics.Batch()

squares = []
for x in range(0,1000,11):
	for y in range(0,800,11):
		squares.append(Entity(x,y,10,10,(255,255,0)))
#where all the changes happen
def update(dt):
	for i in squares:
		i.change()
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
