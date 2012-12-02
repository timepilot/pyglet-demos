import pyglet
from pyglet.window import key
import random
from pyglet.gl import *
import population_model
#create a window
config = pyglet.gl.Config(resizable=True,depth_size=24)
window = pyglet.window.Window(1200,800,config=config)
glPointSize(5.0)

fps_display = pyglet.clock.ClockDisplay()
class points():
	def __init__(self):	
		self.vertices = []
		self.colors = []
		self.list_exists = False
	
	def update(self):
		if self.list_exists == False:
			self.vertex_list = pyglet.graphics.vertex_list(len(self.vertices)/2,
			('v2i', self.vertices),
			('c3B', self.colors)
			)
			self.list_exists = True
		else:
			self.off_screen()
			self.vertex_list.resize(len(self.vertices)/2)
			self.vertex_list.vertices = self.vertices
			self.vertex_list.colors = self.colors
		
	def off_screen(self):
		i = 0
		while i < len(self.vertices):
			if self.vertices[i] > 1200 or self.vertices[i+1] > 800:
				self.vertices.pop(i)
				self.vertices.pop(i)
				self.colors.pop(i+i/2)
				self.colors.pop(i+i/2)
				self.colors.pop(i+i/2)
			i+=2
		
		
	def add_point(self,x1,y1,color):
		self.vertices += x1,y1
		self.colors += color
	def draw(self):
		self.vertex_list.draw(pyglet.gl.GL_POINTS)
		
		
	
		

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
point = points()
colors = color_gen()


x=400
y=400
z=0
for i in range(0,100):
	point.add_point(x,y,random.choice(colors))
	if y == 600:
		y = 0
		x+=2
	else:
		y +=2
	z+=1
point.update()



#where all the changes happen
def update(dt):
	for i in range(0,len(point.vertices)):
		point.vertices[i] += random.randint(0,2)
	point.add_point(0,0,random.choice(colors))
	point.update()
	return False





#draws everything
@window.event
def on_draw():
	window.clear()
	#batch.draw()
	fps_display.draw()
	point.draw()
pyglet.clock.schedule_interval(update,1/60.0)



	
@window.event
def on_key_press(symbol,modifiers):
	if symbol == key.ESCAPE:
		exit()

	
pyglet.app.run()
