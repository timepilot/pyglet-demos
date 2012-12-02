import math


# private function doCollision(ball1:Ball, ball2:Ball):void
# {
    # var xDist:Number = ball1.x - ball2.x
    # var yDist:Number = ball1.y - ball2.y
    # var collisionAngle:Number = Math.atan2(yDist, xDist)
 
    # var magBall1:Number = Math.sqrt(ball1.xSpeed*ball1.xSpeed+ball1.ySpeed*ball1.ySpeed)
    # var magBall2:Number = Math.sqrt(ball2.xSpeed*ball2.xSpeed+ball2.ySpeed*ball2.ySpeed)
 
    # var angleBall1:Number = Math.atan2(ball1.ySpeed, ball1.xSpeed)
    # var angleBall2:Number = Math.atan2(ball2.ySpeed, ball2.xSpeed)
 
    # var xSpeedBall1:Number = magBall1 * Math.cos(angleBall1-collisionAngle)
    # var ySpeedBall1:Number = magBall1 * Math.sin(angleBall1-collisionAngle)
    # var xSpeedBall2:Number = magBall2 * Math.cos(angleBall2-collisionAngle)
    # var ySpeedBall2:Number = magBall2 * Math.sin(angleBall2-collisionAngle)
 
    # var finalxSpeedBall1:Number = ((ball1.mass-ball2.mass)*xSpeedBall1+(ball2.mass+ball2.mass)*xSpeedBall2)/(ball1.mass+ball2.mass)
    # var finalxSpeedBall2:Number = ((ball1.mass+ball1.mass)*xSpeedBall1+(ball2.mass-ball1.mass)*xSpeedBall2)/(ball1.mass+ball2.mass)
    # var finalySpeedBall1:Number = ySpeedBall1
    # var finalySpeedBall2:Number = ySpeedBall2
 
    # ball1.xSpeed = Math.cos(collisionAngle)*finalxSpeedBall1+Math.cos(collisionAngle+Math.PI/2)*finalySpeedBall1
    # ball1.ySpeed = Math.sin(collisionAngle)*finalxSpeedBall1+Math.sin(collisionAngle+Math.PI/2)*finalySpeedBall1
    # ball2.xSpeed = Math.cos(collisionAngle)*finalxSpeedBall2+Math.cos(collisionAngle+Math.PI/2)*finalySpeedBall2
    # ball2.ySpeed = Math.sin(collisionAngle)*finalxSpeedBall2+Math.sin(collisionAngle+Math.PI/2)*finalySpeedBall2
# }

	# self.x = self.x + speed*math.cos(angle)*dt
		# self.y = self.y + speed*math.sin(angle)*dt

class unit():
	def __init__(self,x,y,vector):
		self.x = x
		self.y = y
		self.vector = vector

		
herp = unit(250,750,[90*(math.pi/180),100])
derp = unit(250,450,vector=[270*(math.pi/180),100])

def elastic(one,two):
	xdist = max(one.x,two.x)-min(one.x,two.x)
	ydist = max(one.y,two.y)-min(one.y,two.y)
	print xdist,ydist, "x,y distance"
	if xdist==0:
		collision_angle = 0
	else:
		collision_angle = math.atan(ydist/xdist)
	print collision_angle,"radians"
	onex_speed=one.vector[1]*math.cos(one.vector[0])
	oney_speed=one.vector[1]*math.sin(one.vector[0])
	twox_speed=two.vector[1]*math.cos(two.vector[0])
	twoy_speed=two.vector[1]*math.sin(two.vector[0])
	#rounding errors for the super tiny flaots that fuck everything
	onex_speed,oney_speed,twox_speed,twoy_speed = round(onex_speed),round(oney_speed),round(twox_speed),round(twoy_speed)
	print onex_speed,oney_speed,twox_speed,twoy_speed,"1:x,y 2:x,y speeds"
	#object 1 final dx,dy
	one_finalx = math.cos(collision_angle)*twox_speed+math.cos(collision_angle+math.pi/2)*twoy_speed
	one_finaly = math.sin(collision_angle)*twox_speed+math.sin(collision_angle+math.pi/2)*twoy_speed
	#object 2 final dx,dy
	two_finalx = math.cos(collision_angle)*onex_speed+math.cos(collision_angle+math.pi/2)*oney_speed
	two_finaly = math.sin(collision_angle)*onex_speed+math.sin(collision_angle+math.pi/2)*oney_speed
	one_finalx,one_finaly,two_finalx,two_finaly = round(one_finalx),round(one_finaly),round(two_finalx),round(two_finaly)
	print one_finalx,one_finaly,two_finalx,two_finaly,"1:x,y 2:x,y Final speeds"
	print one.vector,two.vector, "initial vectors"
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
	print new_vector_one,new_vector_two,"new vectors"
	return [new_vector_one,new_vector_two]
	
	
	
elastic(herp,derp)
	
	
	
	
	
	
	
	
	
	