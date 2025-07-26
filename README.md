# Escratsou
> [!NOTE]
> This is upadeted for escratsou version 26.7.25 and Minecraft version 1.21.8

## About
**Escratsou** is a *Python* tool for making **Minecraft Datapacks** and **Minecraft Resourcepacks**

## Datapacks
> [!TIP]
> Using '&namespace&' will use the defined namespace.

To start, we can import the *datapack* tool from **escratsou**.
```python
from escratsou.datapack import create
```
We can define a *datapack* using `datapack.Base`. The first parameter is the *presentation name*, the second is the *namespace*, the third is the *datapack version*, and the fourth is the *description*.
```python
my_datapack = create.Base('My Datapack', 'my_datapack', 81, 'This is a example datapack.')
```

Using `Load()` will run a specified function when loaded in game. Using `Tick()` will run a specified function every tick in game.
```python
# When loaded
my_datapack.Load('&namespace&:tell_a_story')

# Every tick
my_datapack.Tick('&namespace&:check_position')
```

A function can be defined with `Function()`. Requires a name and the contents.
```python
# Create a function
my_datapack.Function('tell_a_story', 'say I will tell you a story!')
```

Create a advancement with `Advancement()`, using a **name** and **string**.
```python
# Open a file for the advancement
with open('my_advancement.json', 'r') as file:
	my_datapack.Advancement('my_advancement', file.read())
```

## Notice
Mojang is not affiliated with this project
