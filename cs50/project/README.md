# Full Knight

#### Video Demo
A video demo of the game can be found at https://youtu.be/oRdRdx-P7Lc.

#### Description
Full Knight is a 2D platformer minigame created using the Love2D game engine. The game features a player character that must navigate various levels while avoiding obstacles and enemies to collect coins and defeat the boss at the end of the game.

#### Assets
The 'assets' folder contains all the assets used in the game, including graphics, sound effects, and fonts.

#### Maps
The 'map' folder contains the maps in both Lua and TMX formats, which are used throughout the game.

#### STI
The 'sti' folder contains an external library that was used in the development of the game. STI, or Simple Tiled Implementation, is a tool that can be used to turn TMX files created in programs like Tiled into functioning maps for your game.

#### Boss
The 'boss' file contains the code necessary to create instances of the boss character in the game. This file requires animations, a physical body, health, and a few other attributes to work properly.

#### Button
The 'button' file is used to create buttons for the game's menus. It returns a function with a few methods that are used to create and display buttons on the screen.

#### Cam
The 'cam' file takes care of the camera needs of the game so that the camera stays with the player and doesn't leave the map.

#### Camera
The 'camera' file is another external program used in the development of the game. This program was used to create a camera instance that could follow certain x and y coordinates in the game.

#### Coin
The 'coin' file is used to create and remove coins in the game. This file requires animations, a physical body, and a few other attributes to work properly.

#### Conf
The 'conf' file is a Love2D file that can be used to set certain parameters for the game window, such as width, height, and which display to use for the window.

#### Enemy
The 'enemy' file is similar to the 'boss' file in that it contains the code necessary to create instances of enemy characters in the game. This file requires certain mechanics, such as when the enemy should turn around, to work properly.

#### GUI
The 'gui' file is used to create the player's health and coin displays, which appear on the screen but are not part of the game world.

#### Main
The 'main' file is where everything in the game is called, and is the only file that is actually run.

#### Map
The 'map' file began as a way to handle which maps should be displayed in the game, but it eventually turned into a kind of state machine that handles other aspects of the game as well.

#### Player
The 'player' file is the largest and most complex file in the game. It contains the physics, animations, mechanics, and status of the player character, and was designed to make the player feel smooth and responsive.

#### Spikes
The 'spikes' file is used to implement spikes in the game. This file requires physics, animations, collisions, and other mechanics to work properly. One tricky aspect of this file was figuring out how to respawn the player character in a different location after they hit the spikes, even if the animations were still playing.

Overall, Full Knight was a challenging project to create, but it taught the developer the importance of keeping an open mind about the final outcome of a project, and provided valuable experience in game development using Love2D.