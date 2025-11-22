# Alien Invasion 🚀

A classic arcade-style space shooter game developed in **Python** using the **Pygame** library. The player controls a ship to destroy fleets of descending aliens while dodging attacks and tracking high scores.

## 🎮 Game Features

* **Player Control:** Smooth movement and shooting mechanics.
* **Dynamic Gameplay:** The game gets harder as you progress—aliens move faster and are worth more points.
* **Score Tracking:** Real-time scoring, level tracking, and high-score retention during the session.
* **Lives System:** The player has 3 ships (lives) before the game ends.
* **Fullscreen Mode:** The game automatically adapts to your monitor's fullscreen resolution.

## 🛠️ Prerequisites

To run this game, you must have Python installed on your machine. You also need the `pygame` library.

### Install Dependencies
Run the following command in your terminal to install Pygame:

```bash
pip install pygame
```

## 🚀 How to Run

* Ensure all project files (.py files) and the images/ folder are in the same directory.
* Open your terminal or command prompt in the project folder.
* Run the main game file:

```bash
python alien_invasion.py
```

## 🕹️ Controls
| Key | Action |
|:------------|---------------:|
| Right Arrow | Move Ship Right |
| Left Arrow | Move Ship Left |
| Spacebar | Fire Bullet |
| P | Play/Restart Game |
| Q | Quit Game |
| Mouse Click | Click play to start |


## 📂 Project Structure
* ```alien_invasion.py```: The main file. Initializes the game, handles the main loop, and processes events (keyboard/mouse).

* ```settings.py```: Configurations for screen settings, ship speed, bullet settings, and alien speed scaling.

* ```ship.py```: Manages the player's ship, its position, and movement logic.

* ```bullet.py```: Manages the bullets fired by the ship.

* ```alien.py```: Manages the alien assets and their position in the fleet.

* ```game_stats.py```: Tracks statistics like current score, high score, level, and ships left.

* ```scoreboard.py```: Handles the visual rendering of the score, level, and remaining ships on the screen.

* ```button.py```: Creates the interactive "Play" button.

## ⚙️ Game Logic Highlights
* Fleet Movement: The alien fleet moves horizontally until it hits an edge, then drops down and changes direction.

* Leveling Up: When a fleet is destroyed, a new fleet is created, the game speed increases by 1.1x, and alien point values increase by 1.5x.

* Collisions: The game checks for collisions between bullets and aliens (scoring), and between aliens and the player ship (losing a life).