__author__ = "Devrim Celik"

from p5 import *
import simpleaudio as sa
import logging

class Missile():
    """
    Missile Class, represented by a small black dot.
    """
    def __init__(self, x, y, direction, speed=None, mass=None):
        """
        args
            x           (float)     x position of spawning location
            y           (flaot)     y position of spawning location
            direction   (float)     angle (in radians) of current direction
            speed       (float)     magnitude of velocity (speed)
            radius      (flaot)     radius of missiles circles
        """
        self.position = Vector(x,y)

        # calculate the force vector, given the current direction
        force = Vector(cos(direction),sin(direction))
        if speed == None:
            self.velocity = force * 10
        else:
            self.velocity = force * speed

        if mass == None:
            self.mass = 20
        else:
            self.mass = mass
        self.radius = self.mass/10

        self.acceleration = Vector(0,0)


    def addForce(self, boost):
        """
        Apply boost onto acceleration
        args
            boost                   (Vector)    vector describing where a force
                                                is pushing and how strong it is
                                                (depending on its magnitude)
        """
        self.acceleration += boost



    def grav_Force(self, _planets, _grav_const):
        """
        Given the list of planets, calculate the total gravitation Force
        upon the missile and add it to the acceleration
        args
            _planets        (list)          list of all current Planet objects
            _grav_const     (float)         gravitational constant of the
        """
        for p in _planets:
            # Vector towards planet
            pull_v = Vector((p.position.x - self.position.x),
                            (p.position.y - self.position.y))
            # length between spaceship and planet
            dist = pull_v.magnitude
            # normalize vector so we can choose its strength
            pull_v.normalize()
            # equation for gravitational force
            pull_v *= (_grav_const*self.mass*p.mass)/(dist**2)

            self.addForce(pull_v)



    def update(self, _planets, _grav_const):
        """
        Given the current position velocity and acceleration,
        calculate new position
        """
        self.grav_Force(_planets, _grav_const)
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0


    def display(self):
        """
        Draw missile on sketch
        """
        fill(0)
        circle(self.position, self.radius, mode="RADIUS")



    def on_screen(self):
        """
        Check if missile is still in the window

        returns
            (boolean)   true if still on screen, false otherwise
        """
        return (self.position.x <= width and self.position.x >= 0 and self.position.y <= height and self.position.y >= 0)





class Planet():
    """
    Missile Class, represented by a small black dot.
    """
    def __init__(self, x, y, mass=None):
        """
        args
            x           (float)     x position of spawning location
            y           (flaot)     y position of spawning location
            mass        (float)     mass of the planet (force calculations)
        """
        self.position = Vector(x,y)

        if mass == None:
            self.mass = 30
        else:
            self.mass = mass

        self.radius = self.mass/2

        logging.info("[*] Planet created")


    def is_inside(self, x, y):
        """
        Given x and y coordinates, checks if point is inside planet.
        args
            x           (float)             x coordinate
            y           (float)             y coordinate
        returns
            bool
        """
        return (x - self.position.x)**2 +   \
            (y - self.position.y)**2 < self.radius**2



    def make_bigger(self, size=10):
        """
        When called, increase mass by argument size and radius by size/2
        """
        self.mass += size
        self.radius += size/2



    def display(self):
        """
        Draw missile on sketch
        """
        fill(50, 175, 200)
        circle(self.position, self.radius, mode="RADIUS")





class Spaceship():
    """
    Spaceship Class, represented by a triangle (spaceship), two rectangles
    (boosters) and a circle (forcefield)
    """
    def __init__(self, x, y, wall_thickness, direction=None, mass=None,
        damping=None, max_speed=None, enable_audio=None):
        """
        args
            x               (float)     x value of starting coordinates
            y               (float)     y value of starting coordinates
            wall_thickness  (int)       thickness of walls on map
            direction       (float)     starting direction, in radiant, where
                                            pointing to the right of the 2D
                                            plane represents 0
            mass            (float)     radius of circle of animation and mass
            damping         (float)     value higher than 0 and maximal 1,
                                            applied to velocity so it
                                        reaches 0 if no acceleration is applied
            max_speed       (float)     maximum speed
            enable_audio    (bool)      should audio be enabled

        """
        self.alive = True
        # position
        self.position = Vector(x,y)
        # velocity
        self.velocity = Vector(0,0)
        # acceleration
        self.acceleration = Vector(0,0)

        self.wall_thickness = wall_thickness

        if direction is None:
            self.direction = 0
        else:
            self.direction = direction

        if mass is None:
            self.mass = 30
        else:
            self.mass = mass
        self.radius = self.mass # for collision

        if damping is None:
            self.damping = 0.99
        else:
            self.damping = damping

        if max_speed is None:
            self.max_speed = 10
        else:
            self.max_speed = max_speed

        if enable_audio is None:
            self.enable_audio = True
            # if sounds are enable, load all necessary sounds
            self.sound_laser = sa.WaveObject.from_wave_file("./sound/laser.wav")
            self.sound_laser.play()
            self.sound_explosion = sa.WaveObject.from_wave_file("./sound/explosion.wav")
            self.sound_explosion.play()
        else:
            self.enable_audio = False

        logging.info("[*] Spaceship created")



    def turn(self, change):
        """
        Change in direction
        args
            change      (float)         change in radiant, where a positive
                                            value represents a clockwise turn
                                            and a negative value represents a
                                            counterclockwise turn
        """
        self.direction += change



    def breaks(self, percentage=0.5):
        """
        Slows ship velocity down by percentage
        args
            percentage  (flaot)         between 0 and 1, decides how much
                                            to keep of the current velocity
                                            (in percent)
        """
        self.acceleration *= 0
        self.velocity *= percentage



    def touching_border(self):
        """
        Checks if ship is touching the order border
        returns
            (boolean, boolean)          represents touching the wall in the x
                                            value and y value
        """
        # TODO add log
        # check if we touching either a horizontal or vertical wall and if we
        # do, change the accordint parameter (by reversing its direction via
        # multiplication with -1)
        if ((self.position.x + self.mass + self.wall_thickness) >= width) \
            or ((self.position.x - self.mass - self.wall_thickness) <= 0):
            self.velocity.x *= -1
        if ((self.position.y + self.mass + self.wall_thickness) >= height)    \
        or ((self.position.y - self.mass - self.wall_thickness) <= 0):
            self.velocity.y *= -1



    def touch_circle(self, circle): # rename collision of two circles TODO
        """
        Checks whether the spaceship touches some other object with a circle
        shape
        args
            circle      (object)        object who has radius property
        """
        # TODO add log
        # calculate vector from spaceship to circle
        difference_vec = Vector(circle.position.x-self.position.x,
                                circle.position.y-self.position.y)
        # check if the distance is smaller than the sum of both radius
        # (if it is, bounce)
        # add velocity magnitude, so you can prevent the last step before
        # bouncing actually being in the circle

        if (difference_vec.magnitude - self.velocity.magnitude) < (self.radius + circle.radius): #3
            collision_angle = atan2(circle.position.y - self.position.y, circle.position.x - self.position.x)

            self.velocity *= -1 # TODO
            #MM = self.velocity.magnitude

            #self.velocity.x *= cos(self.heading - collision_angle) * MM
            #self.velocity.y *= sin(self.heading - collision_angle) * MM

            """
            self.velocity = (self.velocity * (self.mass - circle.mass)+    \
                                2*self.mass*circle.mass)*                   \
                                (1/(self.mass+circle.mass))
            """

            logging.info("[*] Spaceship bumped into circle of type {}".format(circle.__class__.__name__))





    def is_hit(self, list_of_missiles):
        """
        Given a list of coordinates, the spaceship checks if it got hit.
        args
            list_of_missiles        (list)      List of Missile to check
        returns
            index                   (int)       if a missile hit, it return the
                                                index of the missile in the
                                                list, otherwise None
        """
        for indx, (x,y) in enumerate(list_of_missiles):
            if ((x - self.position.x)**2 +                    \
                (y - self.position.y)**2 < self.mass**2):
                # TODO add log here --> spaceship destroyed
                self.alive = False
                # play explosion sound
                self.sound_explosion.play()
                logging.info("[*] Spaceship got destroyed")
                return indx
        return None



    def addForce(self, boost):
        """
        Apply boost onto acceleration
        args
            boost                   (Vector)    vector describing where a force
                                                is pushing and how strong it is
                                                (depending on its magnitude)
        """
        self.acceleration += boost



    def grav_Force(self, _planets, _grav_const):
        """
        Given the list of planets, calculate the total gravitation Force
        upon the spaceship and add it to the acceleration
        args
            _planets        (list)          list of all current Planet objects
            _grav_const     (float)         gravitational constant of the
        """
        for p in _planets:
            # Vector towards planet
            pull_v = Vector((p.position.x - self.position.x),
                            (p.position.y - self.position.y))
            # length between spaceship and planet
            dist = pull_v.magnitude
            # normalize vector so we can choose its strength
            pull_v.normalize()
            # equation for gravitational force
            pull_v *= (_grav_const*self.mass*p.mass)/(dist**2)

            self.addForce(pull_v)



    def shoot(self):
        """
        Shoots a missile
        returns
            return the created Missile object
        """

        # calculate a vector for the direction of the shot, depending on what
        # way the spaceship is looking right now
        force = Vector(cos(self.direction),sin(self.direction))
        # set its magnitude to one
        force.normalize()
        # since force will represent the spawning location in relation to the
        # spaceship locaiton, a vector of magnitude self.mass would spawn
        # exactly on the forcefield and thus hit the spaceship itself, thus
        # we add 1 to be outide the forcefield
        force *= (self.mass+1)

        # play laser sound
        self.sound_laser.play()

        return Missile(self.position.x + force.x,
            self.position.y + force.y, self.direction, speed=self.max_speed)



    def boost(self, speed=3):
        """
        calculate the vector, representing the force and apply it to the
        acceleration
        """
        # calculate direction of force
        force = Vector(cos(self.direction),sin(self.direction))
        # calculate magnitude of force
        force *= speed
        # add it to the spacheships acceleration
        self.addForce(force)



    def update(self, _planets, _grav_const): # TODO include them via import then remove them here
        """
        update velocity and position and set acceleration to 0
        """
        self.grav_Force(_planets, _grav_const)
        # apply acceleration to velocity
        self.velocity += self.acceleration
        # apply damping, so it the velocity asymptotically reaches 0 if
        # no acceleration is applied
        self.velocity *= self.damping
        # check if our current velocity magnitude (eqv. to speed) is higher
        # than the spaceships speed limit
        if self.velocity.magnitude > self.max_speed:
            self.velocity *= self.max_speed/self.velocity.magnitude
        # check if touching borders (and bounce if yes)
        self.touching_border()
        # apply velocity to position
        self.position += self.velocity
        # if there is no external force applying onto an object, the
        # acceleration is zero by default
        self.acceleration *= 0



    def display(self):
        """
        drawing spaceship (with forcefield, boosters, etc...) on sketch window
        """
        # since we have turbines at the rocket, we dont want the rocket to be
        # in the exact middle of the circle, but to include a small offset
        # so it has equal distance to the circle to both sides
        shift = 5

        # local changes
        push_matrix()
        # set current position as origin
        translate(self.position.x, self.position.y)
        # rotate the matrix by heading, so we will draw in a shifted version
        rotate(self.direction)
        # draw force field
        fill(100)
        circle((0, 0), (self.mass), mode="RADIUS")
        # draw spaceship
        fill(255)
        triangle((self.mass/2+shift, 0),
                (-self.mass/2+shift, self.mass/3),
                (-self.mass/2+shift, -self.mass/3))
        # draw boosters
        fill(255, 0, 0)
        rect((-self.mass/2-5+shift, self.mass/18),
            (-self.mass/2+shift, 2*self.mass/9),
            mode="CORNERS")
        rect((-self.mass/2-5+shift, -self.mass/18),
            (-self.mass/2+shift, -2*self.mass/9),
            mode="CORNERS")
        # reset locally made global matrix changes
        reset_matrix()



        # TODO doesnt work, doesnt get called
        def __str__(self):
            return "{} with current position={} & current_speed={}".format( \
                        self.__class__.__name__, self.position.x,
                        self.position.y, self.velocity.magnitude)



        # TODO doesnt work, doesnt get called
        def __repr__(self):
            return """{}(
                            position=({}, {}),
                            velocity=({}, {}),
                            speed={},
                            direction={},
                            mass={},
                            damping={},
                            max_speed={}
                        )""".format(self.__class__.__name__, self.position.x,
                                    self.position.y, self.velocity.x,
                                    self.velocity.x, self.velocity.magnitude,
                                    self.direction, self.mass, self.damping,
                                    self.max_speed)
