__author__ = "Devrim Celik"

import datetime
from p5 import *
from classes import Spaceship, Planet
from __global_var__ import *
import logging


def setup():
    """
    Setup for sketch
    """
    logging.info("[*] Simulation started")

    global _width, _height
    # size of window
    size(_width, _height)
    title("SPACE SIMULATOR")



def draw_borders():
    """
    Draw the screen borders
    args
        WALL_THICKNESS      (int)   Width of borders in pixel
    """
    global _wall_thickness

    # color of the border
    stroke(0)
    # color of the field
    fill(255)
    for i in range(_wall_thickness):
        rect((i,i), (width-i, height-i), mode="CORNERS")
        # TODO why are there white points that I have to fill like this
        point(i,i)
        point(width-i, height-i)



def remove_objects(spaceships=[], missiles=[]):
    """
    Given lists of all objects, will remove some (depending on the context):
        * spaceship will be removed, if they get hits by a missile
        * missile will be removed, if it hits a spacheship
        * missile will be removed, if it leaves the screen
    args
        spaceships      (list)      list of all spaceship objects
        missiles        (list)      list of all missile objects
    """

    # NOTE: after deleting the object from the list (only reference in the
    # script) python garbage collector will take care of the rest

    # list to save the coordinates of every missile
    # note: it will reset every time
    missile_positions = []

    for indx_m, m in enumerate(missiles):
        # append position to list
        missile_positions.append((m.position.x, m.position.y))
        # check if missile is stick on the screen
        if not m.on_screen():
            del missiles[indx_m]

    for indx_s, s in enumerate(spaceships):
        # check if spaceship got hit by any of the missiles
        indx_m = s.is_hit(missile_positions)
        # if it did, s.is_hit() will return a int
        if indx_m is not None:
            del spaceships[indx_s]
            del missiles[indx_m]

def draw():
    """
    Calculation steps and draw on sketch
    """
    global _spaceships, _missiles, _planets, _wall_thickness, _grav_const

    # draw borders
    draw_borders()
    # remove objects
    remove_objects(_spaceships, _missiles)

    for p in _planets:
        p.display()

    for m in _missiles:
        m.update(_planets, _grav_const)
        m.display()

    for indx_s, s in enumerate(_spaceships):
        s.update(_planets, _grav_const)

        # go through all other spaceships to check if you bounce,
        # exclude yourself
        for indx_s2, s2 in enumerate(_spaceships):
            if indx_s != indx_s2:
                s.touch_circle(s2)
        # check if you touch a planet
        for p in _planets:
            # TODO should it bounce or die?
            s.touch_circle(p)

        s.display()



def key_pressed(event):
    global _human_enabled, _spaceships, _missiles
    if _human_enabled:
        logging.info("[*] User Input: {}".format(event.key))
        if event.key == "UP":
            _spaceships[0].boost()
        elif event.key == "LEFT":
            _spaceships[0].turn(-0.4)
        elif event.key == "RIGHT":
            _spaceships[0].turn(+0.4)
        elif event.key == "DOWN":
            _spaceships[0].breaks()
        elif event.key == "SPACE":
            _missiles.append(_spaceships[0].shoot())



def mouse_pressed(event):
    """
    When mouse is pressed, create a planet # TODO
    """
    global _planets
    for p in _planets:
        if p.is_inside(event.x, event.y):
            p.make_bigger()
            return
    _planets.append(Planet(event.x, event.y))



def spaceship_simulation(width=1080, height=720, frame_rate=30,
    wall_thickness=10, human_enabled=True, show_frame_rate = True,
    grav_const=1):
    # TODO show_frame rate how? (log/terminal/sketch)
    logging.info("""
                ==================================================
                [*] Simulation started at {:%Y-%m-%d %H:%M:%S}
                ==================================================
                """.format(datetime.datetime.now()))
    global _width, _height, _spaceships, _missiles, _planets, _frame_rate,    \
        _show_frame_rate, _wall_thickness, _human_enabled, _grav_const
    _width = width
    _height = height
    _frame_rate = frame_rate
    _wall_thickness = wall_thickness
    _show_frame_rate = show_frame_rate
    _human_enabled = True
    _grav_const = grav_const

    # NOTE first element has the option to be human player if human_enabled
    _spaceships = [Spaceship(_width/2+100,_height/2+100, _wall_thickness),
                    Spaceship(_width/2,_height/2, _wall_thickness)]
    _missiles = []
    _planets = []


    run(frame_rate=_frame_rate)

if __name__=="__main__":
    spaceship_simulation()
