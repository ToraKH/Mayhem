# Cosmic Cavern

## Mayhem
The manager file consists of a game of Mayhem, a space-themed game where two players navigate a space cave while trying to shoot each other down. The ships need to refuel, and avoid hazards such as aliens and cave walls. Players earn points by shooting opponents and loose some if they perish. The scores and wins of each round are tallied up. May the best space pilot win!

All the images, sounds and other environmental variables are contained in the config file.
This is our solution to the third obligatory assignment in INF-1400: Objektorientert Programmering.

### Authors
Tora K. Homme

Dulmini S. Gamage

## Installing pygame
Ensure that python is installed

```bash
  python --version
```

Ensure that PIP is installed

```bash
  pip --version
```

Install pygame 

```bash
  pip install pygame
```

## Run the game
Go to src directory

```bash
  cd inf1400-tohom2986-3/src 
```

Run simulation

```bash
  python3 manager.py
```

## Key Commands
- Start Screen
    - ```to start game, press "SPACE"```


- Player 1
  - ```to thrust, press "W"```
  - ```to move left, press "A"```
  - ```to move right, press "D"```
  - ```to shoot, press "LEFT SHIFT"```

- Player 2
  - ```to thrust, press "ARROW UP"```
  - ```to move left, press "ARROW LEFT"```
  - ```to move right, press "ARROW RIGHT"```
  - ```to shoot, press "RIGHT CTRL"```

- End Screen
    - ```to restart game, press "SPACE"```

## Features
- Music 🎵
- Crash sound and effect 💥
- Gravity 🕳
- Ships loose fuel in motion, but can refuel 🚀
- Scary, evil alien 👽
- Scoreboards 📊
- Start/game/end screen ⏱
