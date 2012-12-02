
import random
import math
from collections import Counter
import time

#import death rates


#person object, tracks various stats and status updates like death/child birth etc
class Person:
	def __init__(self,name,age,time_multiplier,food_level):
		self.name = name
		self.age = age
		self.start_age = self.age
		self.gender = random.sample(['m','f'],1)
		self.dead = False
		#start day for simulation
		self.day = 1
		#foodz
		self.food_level = food_level
		# pro-creation values
		self.pregnant = False
		self.pregnant_time =  False
		self.children_count = 0
		self.max_children = 2
		#number of days per loop set during object creation
		self.time_multiplier = time_multiplier
		#food value (1kg /day is highest growth , less than that will result in lower birth rates, really low is death)
		#essentially a number between 0-1
		#.5 ideally slows growth to zero, pregnancies still happen but elderly
		# and infant mortality rise to compensate
		self.death_rates = self.death_rate_calculator()
		#death function
	
	#pregnancy chance calculator based on yearly rates, pregnancy ability is linear
	def preg_chance(self):
		chance = (float(-89.0/27)*self.age+float(448.0/3))/100.0
		#controls birth rate as function of food_level 
		chance = chance*(self.food_level/100.0)
		return chance
	def birth_calculator(self):
		#different birth calculation, should work better and be more stable now, need
		# to tweak chance to work with time scale
		if self.pregnant == False:
			if self.gender[0] == 'f':
				if self.age in range(18,40):
					chance = self.preg_chance()/(365.0/self.time_multiplier)
					if self.children_count < self.max_children:
						if random.random() < chance:
							self.pregnant = True
							self.pregnant_time = self.day

		if self.pregnant == True:
			if self.day - self.pregnant_time == 270:
				self.children_count+=1
				self.pregnant = False
				self.pregnant_time = False
				return True
	#calculations starvation chance in percent according to equation
	#somewhat age skewed for young < 5 and old > 60, only runs at food level < 50, above that birth rates are lowered
	def starvation_calculator(self):
		starvation_chance = (-27.14 * math.log(self.food_level)+125)/100.0
		starvation_chance = starvation_chance/(365.0/self.time_multiplier)
		starvation_chance = round(starvation_chance,3)
		if self.age < 5 or self.age > 60:
			starvation_chance *= 10
		death_roll = random.random()
		if death_roll < starvation_chance:
			#print "DERP"
			return True
		else:
			return False
		
	def death_rate_calculator(self):
		f = open('deathrates.txt','r')
		rates = f.read()
		rates = rates.split('\n')
		rates = [ float(x) for x in rates ]
		return rates
	#determines if a person has died of something on a given day/cycle
	def death_calculator(self):
		death_roll = random.randint(1,int(1/((self.death_rates[self.age])))*(365/self.time_multiplier))
		if death_roll == 1:
			self.dead = True
		if self.food_level < 50:
			if self.starvation_calculator() == True:
				self.dead = True
	#calculate age
	def age_calculator(self):
		self.age = self.start_age + self.day/365
		#print self.age
	def update(self):
		# generates birth data, update returns true is a new person is generated
		birth = self.birth_calculator()
		# kill
		self.death_calculator()
		self.age_calculator()
		self.day +=1*self.time_multiplier
		if birth == True:
			return True
		
class pop_model():
	def __init__(self):
		self.person_number = 1001
		self.day = 0
		self.time_scale = 1
		self.food_level = 100
		
	def pop_model_tick(self):
		for person in people:
			result = person.update()
			if result ==  True:
				people.append(Person('x' + str(self.person_number),1,self.time_scale,self.food_level))
				self.person_number+=1
			if person.dead == True:
				#print person.name, person.age,day
				del people[people.index(person)]

		if self.day % 365 == 0:
			print self.day/365,len(people),self.person_number - 1001

		self.day+=1*self.time_scale