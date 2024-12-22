![icon](https://raw.githubusercontent.com/GaelHF/pymakergame/refs/heads/main/pymakergame/icon.png)
# PyMakerGame
Python Library That Makes Pygame Easy

## About
- Released: 12/20/2024
- Author: [@GaelHF](https://github.com/GaelHF)

## Create a Game with PyMakerGame
Create the game window
```python
import pymakergame as pmg
jeux = pmg.Game("TEST GAME", (500, 500), 'YOUR ICON, EXEMPLE: assets/icon.png', (255, 255, 255))
```
It's Game(name, size, icon, background_color)