import json
import os

# Create directory if it does not exist
def combineDirectories(directory: str, path: str):
	'''Create directory if nonexistant'''
	if not os.path.exists(os.path.join(directory, path)): os.makedirs(os.path.join(directory, path))

# Create file if it does not exist
def combineFiles(directory: str, path: str, contents: str):
	'''Create file with content if nonexistant'''
	if not os.path.isfile(os.path.join(directory, path)):
		with open(os.path.join(directory, path), 'x') as file:
			file.write(contents)

def appendFile(directory: str, path: str, contents: str):
	'''Appends content to file or creates file with content if nonexistant'''
	if not os.path.isfile(os.path.join(directory, path)):
		with open(os.path.join(directory, path), 'x') as file:
			file.write(contents)
	else:
		with open(os.path.join(directory, path), 'a') as file:
			file.write(contents)

# Update JSON file
def updateJSON(path: str, update: str, content: str):
	'''Appends content to part of JSON file'''
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
