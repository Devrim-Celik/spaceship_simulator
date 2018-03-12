# Spaceship Simulator

## Todo List

* Urgent --> #2, #3, #4, #5

* Keep Updated
  - logging
  - sound

* Add more classes
  - obstacles (asteroid, killing you and moving as well in the atmosphere)
  - "enemy" (laser turret, shoot patter has something to do with fractals????)

* Add behaviour:
  - planets and missiles shouldnt be able to pass planets #4
  - planets shouldnt have any subset areas when spawning #5
  - planets can be shrinked by right click

* Look for new references for vectors
  - replace already built in stuff
    - (distance by constraint?)

* Add services:
  - argparsing
  - state returning function 5
    - what variables?
      - position x
      - position y
      - velocity
      - is someone in front of me 4
        - how far away is he?
      - where is my nearest target (position x and y) 4
      - where is the nearest thing that can kill me 4
      - self.alive
  - show frame rate 2
  - add __str__ and __repr__ once #1 is solved 3
  - add description
  - add why useful for RL

* Code Style
  - Look out, that the character limit of lines is not overshot

* Simulation Modes
  - Random Planet appearance and disappearance

* Setup file
  - Install Dependencies (p5, (numpy?), simpleaudio)

* Bugs:
  - __str__ and __repr__ #1 4
  - what exactly happens when two circle things collide, whats the new force #2
  - checking if two circles touch doesnt work (the circles first create a subset) #3

---
### Sounds
- ![Laser Sound](https://freesound.org/people/TheDweebMan/sounds/277218/)
- ![Explosion](https://freesound.org/people/sharesynth/sounds/341238/)
