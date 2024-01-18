import tkinter
from PIL import Image, ImageTk
import neat
import math

class Car:
    def __init__(self, root):

        # Setting up the variables
        self.car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
        self.car_coords = list((self.start_coords[0]-20, self.start_coords[1]))
        self.start_coords = list((540, 666))
        self.speed = 0
        self.wheel_rotation = 0
        self.rotation = 0
        self.speed_change = 0.25
        self.rotation_change = 0.0125
        self.max_wheel_rotation = 0.5
        self.distance = 0
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

        # Loading the photo assets
        self.track_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/track.png'))
        self.start_lane_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/startLane.png'))
        self.car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
       
        # Setting up the canvas
        self.root = root
        self.root.title('Autonomous Car Reinforcement Learning AI Demo')
        self.root.wm_iconphoto(True, self.car_img)

        self.canvas = tkinter.Canvas(height=720, width = 1080)
        self.canvas.pack()

        # Loading the images
        self.canvas.create_image((540, 360), image = self.track_img)
        self.canvas.create_image(self.start_coords, image = self.start_lane_img)
        self.Car = self.canvas.create_image(self.car_coords, image = self.car_img)

    def check_collision(self):
        self.keep_alive = True
        radars = self.gather_line_distances(Image.open('examples/reinforcement learning/assets/track.png').convert('RGB'), self.rotation, self.car_coords[0], self.car_coords[1], self.speed, self.wheel_rotation)
        if radars == 'Null':
            self.keep_alive = False

    def gather_line_distances(track_source, car_rotation, car_position_x, car_position_y, car_speed, car_wheel_rotation):

        # Set up the angles of detection lines
        lines = list((0, 45, 90, 135, 180, 225, 270, 315))

        output = list((0, 0, 0, 0, 0, 0, 0, 0))

        # If car is already on the grass, cancel the whole process
        if track_source.getpixel((car_position_x, car_position_y)) == (34, 177, 76):
            output = 'Null'

        # If car is on the road, compute the distances
        if output != 'Null':
            
            for i in range(8):
                pixel_distance = 1

                x = int(car_position_x + (math.cos(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)
                y = int(car_position_y + (math.sin(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)

                while not track_source.getpixel((x, y)) == (34, 177, 76) and pixel_distance <= 100:
                    pixel_distance += 1
                    x = int(car_position_x + (math.cos(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)
                    y = int(car_position_y + (math.sin(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)
                    
                # Feed the distances into the output list
                output[i] = (pixel_distance-1)/100

            # Appending speed and rotation for future ease
            output.append(car_speed)
            output.append(car_wheel_rotation)

        return output
    
    def update(self):

        # Algorithm to identify keystrokes and accordingly change the tire direction and speed of the car

        # Identifying the keystrokes of w and s and changing speed attribute
        if self.forward:
            speed += self.speed_change
        elif self.backward and speed > 0:
            speed -= self.speed_change*1.5
        elif self.backward and speed <= 0:
            speed -= self.speed_change/2
        elif speed > 0:
            speed -= self.speed_change/2
        elif speed < 0:
            speed += self.speed_change/2

        # Rounding the speed to 0 during very slow speeds
        if -self.speed_change/4 < speed < self.speed_change/4:
            speed = 0

        # Identifying the keystrokes of a and d and changinge the wheel_rotation attribute
        if speed != 0:
            if self.left:
                wheel_rotation += self.rotation_change
                speed -= self.speed_change                                                       # Just for making an award system easier
            elif self.right:
                wheel_rotation -= self.rotation_change
                speed -= self.speed_change                                                       # Just for making an award system easier
            elif wheel_rotation > 0:
                wheel_rotation -= self.rotation_change*2
            elif wheel_rotation < 0:
                wheel_rotation += self.rotation_change*2
        
        # Rounding the rotation to 0 during very small rotations
        if -self.rotation_change < wheel_rotation < self.rotation_change:
            wheel_rotation = 0
            
        if wheel_rotation > self.max_wheel_rotation:
            wheel_rotation = self.max_wheel_rotation
        elif wheel_rotation < -self.max_wheel_rotation:
            wheel_rotation = -self.max_wheel_rotation

        # Applying the calculated physics change to the car itself
        if speed != 0:
            rotation += wheel_rotation/2
        self.rotated_car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png').rotate(rotation*57.2958)) # Rotation is multiplied because of it being counted in radians
        self.car_coords[0] += math.cos(-rotation)*speed
        self.car_coords[1] += math.sin(-rotation)*speed
        self.canvas.delete(self.Car)
        self.Car = self.canvas.create_image(self.car_coords, image = self.rotated_car_img)

        self.check_collision(self)

        self.distance += speed

        return None