import json
import os
import shutil

# Create directory if it does not exist
def combineDirectories(directory: str, path: str):
	if not os.path.exists(os.path.join(directory, path)): os.makedirs(os.path.join(directory, path))

# Create file if it does not exist
def combineFiles(directory: str, path: str, contents: str):
	if not os.path.isfile(os.path.join(directory, path)):
		with open(os.path.join(directory, path), 'x') as file:
			file.write(contents)

# Update JSON file
def updateJSON(path: str, update: str, content: str):
	if not os.path.isfile(path):
		raise FileNotFoundError('No file at ' + path)

	with open(path, 'r') as file:
		original = json.load(file)

	if not update in original:
		raise NameError('Invalid JSON file')
	original[update] += content
	moddified = json.dumps(original)

	with open(path, 'w') as file:
		file.write(moddified)

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
		combineDirectories(directory, self.name + '/data/' + self.namespace)
		if len(self.loads) > 0 or len(self.ticks) > 0:
			combineDirectories(directory, self.name + '/data/minecraft/tags/function')
		if len(self.functions) > 0:
			combineDirectories(directory, self.name + '/data/' + self.namespace + '/function')
		if len(self.advancements) > 0:
			combineDirectories(directory, self.name + '/data/' + self.namespace + '/advancement')

		# Output pack settings
		combineFiles(directory, self.name + '/pack.mcmeta', str(json.dumps({'pack':{'description': self.description, 'pack_format': self.version}}, indent='	')).replace('\'', '"'))

		# Output loads
		if len(self.loads) > 0:
			full = {'values':[]}
			for load in self.loads:
				full['values'] += [load]
			combineFiles(directory, self.name + '/data/minecraft/tags/function/load.json', str(json.dumps(full, indent='	')).replace('\'', '"'))

		# Output ticks
		if len(self.ticks) > 0:
			full = {"values":[]}
			for tick in self.ticks:
				full['values'] += [tick]
			combineFiles(directory, self.name + '/data/minecraft/tags/function/tick.json', str(json.dumps(full, indent='	')).replace('\'', '"'))

		# Output functions
		for function in self.functions:
			directory_full = self.name + '/data/' + self.namespace + '/function/' + function[2]
			combineDirectories(directory, directory_full)
			combineFiles(directory, os.path.join(directory_full, function[0]) + '.mcfunction', function[1])

		# Output advancements
		for advancement in self.advancements:
			directory_full = self.name + '/data/' + self.namespace + '/advancement/' + advancement[2]
			combineFiles(directory, os.path.join(directory_full, advancement[0]) + '.json', advancement[1])

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