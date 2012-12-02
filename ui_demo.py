#This work is licensed under a 
#Creative Commons Attribution-NonCommercial 2.5 License
#(the same as XKCD) so do whatever you want with it 
#as long as it stays free
#written by Marty S. (marty at geodex dot org) 
#
#SimpleUI not included in repo,not that great anyway

import pyglet
from pyglet.window import key
import random
from pyglet.gl import *
from simplui import *

#create a window
window = pyglet.window.Window(
	1200, 800, caption='TEST' ,
	resizable=True, vsync=False)
glPointSize(2.0)
fps_display = pyglet.clock.ClockDisplay()

# load some gui themes
themes = [Theme('themes/macos'), Theme('themes/pywidget')]
theme = 0
# create a frame to contain our gui,
frame = Frame(themes[theme], w=1200, h=800)
# let the frame recieve events from the window
window.push_handlers(frame)

#callbacks

def text_action(input):
	print 'text entered:', input.text

def slider_action(slider):
	print slider.value
	point.number = int(slider.value)
dialogue2 = Dialogue('Controls', x=500, y=550, content=
	# lets try a flow layout...
	FlowLayout(w=250, children=[
		TextInput(w=200,text='edit me', action=text_action),
		Slider(w=100, min=1, max=100000, action=slider_action)
		])
	)
frame.add( dialogue2 )

# add the dialogue to the frame

	
class points():
	def __init__(self):	
		self.vertices = []
		self.colors = []
		self.list_exists = False
		self.number = 1
	def update(self):
		if self.list_exists == True:
			self.vertex_list.delete()
		self.vertex_list = batch.add(len(self.vertices)/2,pyglet.gl.GL_POINTS,None,
		('v2i', self.vertices),
		('c3B', self.colors)
		)
		self.list_exists = True
		self.colors = []
		self.vertices = []
	def add_quad(self,x1,y1,color):
		self.vertices += x1,y1
		self.colors += color
	def draw_list(self):
		self.vertex_list.draw(pyglet.gl.POINTS)


		
		
	
		

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

#where all the changes happen
def update(dt):
	x = 100
	y = 10
	for i in range(0,point.number):
		point.add_quad(x,y,random.choice(colors))
		if y < 770:
			y+=6
		else:
			y=10
			x+=6
	point.update()
	return False





#draws everything
@window.event
def on_draw():
	window.clear()
	batch.draw()
	fps_display.draw()
	frame.draw()
pyglet.clock.schedule_interval(update,1/60.0)



	
@window.event
def on_key_press(symbol,modifiers):
	if symbol == key.ESCAPE:
		exit()
window.push_handlers(on_key_press)	
pyglet.app.run()
