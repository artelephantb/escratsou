import json
import os
import shutil

# Import tools
from .. import file_tools

# Base datapack
class Base:
	# Setup
	def __init__(self, name: str, namespace: str, version: int, description: str):
		self.name = name
		self.namespace = namespace
		self.version = version
		self.description = description

		self.loads = []
		self.ticks = []

		self.functions = []
		self.advancements = []

	# Add load (on load)
	def Load(self, contents: str):
		if '\n' in contents:
			raise ValueError('One line only')
		self.loads += [contents.replace('&namespace&', self.namespace)]

	# Add tick (every tick)
	def Tick(self, contents: str):
		if '\n' in contents:
			raise ValueError('One line only')
		self.ticks += [contents.replace('&namespace&', self.namespace)]

	# Add function (when called)
	def Function(self, name: str, contents: str, sub_dir=''):
		self.functions += [[name, contents.replace('&namespace&', self.namespace), sub_dir]]
	
	# Add advancement (with conditions)
	def Advancement(self, name: str, contents: str, sub_dir=''):
		self.advancements += [[name, contents.replace('&namespace&', self.namespace), sub_dir]]

	def export(self, directory, replace=False, combine=False):
		# Check if datapack exsists
		if os.path.exists(os.path.join(directory, self.name)):
			if replace == False:
				if combine == False:
					raise FileExistsError(f'Datapack {self.name} exsists in {directory}')
			else:
				shutil.rmtree(os.path.join(directory, self.name))

		# Create folders
		file_tools.combineDirectories(directory, self.name + '/data/' + self.namespace)
		if len(self.loads) > 0 or len(self.ticks) > 0:
			file_tools.combineDirectories(directory, self.name + '/data/minecraft/tags/function')
		if len(self.functions) > 0:
			file_tools.combineDirectories(directory, self.name + '/data/' + self.namespace + '/function')
		if len(self.advancements) > 0:
			file_tools.combineDirectories(directory, self.name + '/data/' + self.namespace + '/advancement')

		# Output pack settings
		file_tools.combineFiles(directory, self.name + '/pack.mcmeta', str(json.dumps({'pack':{'description': self.description, 'pack_format': self.version}}, indent='	')).replace('\'', '"'))

		# Output loads
		if len(self.loads) > 0:
			full = {'values':[]}
			for load in self.loads:
				full['values'] += [load]
			file_tools.combineFiles(directory, self.name + '/data/minecraft/tags/function/load.json', str(json.dumps(full, indent='	')).replace('\'', '"'))

		# Output ticks
		if len(self.ticks) > 0:
			full = {"values":[]}
			for tick in self.ticks:
				full['values'] += [tick]
			file_tools.combineFiles(directory, self.name + '/data/minecraft/tags/function/tick.json', str(json.dumps(full, indent='	')).replace('\'', '"'))

		# Output functions
		for function in self.functions:
			directory_full = self.name + '/data/' + self.namespace + '/function/' + function[2]
			file_tools.combineDirectories(directory, directory_full)
			file_tools.combineFiles(directory, os.path.join(directory_full, function[0]) + '.mcfunction', function[1])

		# Output advancements
		for advancement in self.advancements:
			directory_full = self.name + '/data/' + self.namespace + '/advancement/' + advancement[2]
			file_tools.combineFiles(directory, os.path.join(directory_full, advancement[0]) + '.json', advancement[1])

# Simple datapack
class Projectile(Base):
	def __init__(self, name: str, namespace: str, version: int, description: str):
		super().__init__(name, namespace, version, description)
		self.projectiles = []
	
	# Add projectile (when called)
	def Projectile(self, name: str, item: dict, speed: float, particle: dict):
		self.projectiles += [[name, item, speed, particle]]

		# Add projectile functions
		self.Function(name + '.spawn', 'summon item_display ~ ~ ~ {\'item\':' + str(item) + ', Tags:[\'projectile\', \'' + self.namespace + '\', \'' + name + '\']}', 'projectiles')
		self.Function(name + '.tick', 'execute as @e[tag=projectile, tag=' + self.namespace + ', tag=' + name + '] at @s run teleport @s ^ ^ ^1\nexecute as @e[tag=projectile, tag=' + self.namespace + ', tag=' + name + '] at @s unless entity @a[distance=..100] run kill @s', 'projectiles')

		# Add projectile tick
		self.Tick(self.namespace + ':projectiles/' + name + '.tick')

	def export(self, directory, replace=False, combine=False):
		super().export(directory, replace, combine)

		if len(self.projectiles) > 0:
			full = ''
			self.Tick(self.namespace + ':projectiles/tick')

			for projectile in self.projectiles:
				full += 'execute as @e[tag=projectile, tag=' + self.namespace + ', tag=' + projectile[0] + '] at @s run return run function ' + self.namespace + ':projectiles/' + projectile[0] + '.tick\n'
		
			file_tools.combineFiles(directory, self.name + '/data/' + self.namespace + '/function/projectiles/tick.mcfunction', full)
