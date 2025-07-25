# Escratsou
*(Updated for escratsou version 24.7.25, Minecraft version 1.21.8)*
## About
**Escratsou** is a *Python* tool for making **Minecraft Datapacks** and **Minecraft Resourcepacks**
## Datapacks
To start, we can import the *datapack* tool from **escratsou**.
```python
from escratsou import datapack
```
We can define a *datapack* using `datapack.Base`. The first parameter is the *presentation name*, the second is the *namespace*, the third is the *datapack version*, and the fourth is the *description*.
```python
my_datapack = datapack.Base('My Datapack', 'my_datapack', 81, 'This is a example datapack.')
```
## Notice
Mojang is not affiliated with this project
